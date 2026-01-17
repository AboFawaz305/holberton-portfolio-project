<!-- stage4/frontend/src/components/CreateGroupButton.vue -->
<script>
import groupsService from '@/services/groupsService'

export default {
  name: 'CreateGroupButton',
  props: {
    orgId: { type: String, required: true },
    parentGroupId: { type: String, default: null }, // Handled internally
    buttonLabel: { type: String, default: 'إضافة مجموعة' },
  },
  emits: ['created'],
  data() {
    return {
      dialog: false,
      title: '',
      isCreating: false,
      isFormValid: true,
      showAlert: false,
      alertMessage: '',
      snackbar: { show: false, message: '' },
      titleRules: [
        (v) => !!v || 'يرجى إدخال اسم المجموعة',
        (v) => (v && v.length >= 3) || 'الاسم قصير جداً',
      ],
    }
  },
  methods: {
    hideAlert() {
      this.showAlert = false
    },
    closeDialog() {
      this.dialog = false
      this.title = ''
      this.hideAlert()
      if (this.$refs.createForm) this.$refs.createForm.resetValidation()
    },
    async submitForm() {
      const { valid } = await this.$refs.createForm.validate()
      if (!valid || this.isCreating) return

      this.isCreating = true
      try {
        // We handle the logic here: if parentGroupId exists, it's a subgroup
        const payload = { title: this.title.trim() }
        if (this.parentGroupId) {
          payload.parent_group_id = this.parentGroupId
        }

        await groupsService.createGroup(this.orgId, payload)

        this.snackbar.message = 'تم إنشاء المجموعة بنجاح'
        this.snackbar.show = true

        this.$emit('created')
        this.closeDialog()
      } catch (error) {
        // Map backend errors to simple Arabic messages
        const errorMap = {
          GROUP_ALREADY_EXIST: 'اسم المجموعة موجود بالفعل',
          SUBGROUP_ALREADY_EXIST: 'اسم المجموعة موجود بالفعل في هذا القسم',
          NOT_A_MEMBER: 'ليس لديك صلاحية للإنشاء هنا',
        }
        this.alertMessage = errorMap[error.message] || 'حدث خطأ غير متوقع'
        this.showAlert = true
      } finally {
        this.isCreating = false
      }
    },
  },
}
</script>

<template>
  <div>
    <v-card
      variant="flat"
      class="mb-4 create-placeholder-card d-flex align-center justify-center"
      rounded="xl"
      @click="dialog = true"
      min-height="110"
    >
      <div class="text-center">
        <v-avatar color="primary" size="40" class="mb-2 shadow-sm">
          <v-icon color="white" size="24">mdi-plus</v-icon>
        </v-avatar>
        <div class="text-subtitle-2 font-weight-bold text-primary">
          {{ buttonLabel }}
        </div>
      </div>
    </v-card>

    <v-dialog v-model="dialog" max-width="450px" persistent>
      <v-form ref="createForm" v-model="isFormValid" @submit.prevent="submitForm">
        <v-card rounded="xl" class="pa-6">
          <v-card-title class="text-h5 font-weight-bold px-0 d-flex align-center">
            <v-icon start color="primary" class="me-2">mdi-plus-circle-outline</v-icon>
            إنشاء مجموعة
          </v-card-title>

          <v-card-text class="px-0 pt-4">
            <v-text-field
              v-model="title"
              label="اسم المجموعة"
              placeholder="أدخل اسم المجموعة هنا..."
              :rules="titleRules"
              :disabled="isCreating"
              variant="outlined"
              color="primary"
              rounded="lg"
              required
              bg-color="grey-lighten-5"
              prepend-inner-icon="mdi-tag-outline"
              @keyup.enter="submitForm"
            />

            <v-expand-transition>
              <v-alert
                v-if="showAlert"
                type="error"
                variant="tonal"
                density="compact"
                class="mt-4 rounded-lg text-caption"
                closable
                @click:close="hideAlert"
              >
                {{ alertMessage }}
              </v-alert>
            </v-expand-transition>
          </v-card-text>

          <v-card-actions class="px-0 mt-4">
            <v-spacer />
            <v-btn variant="text" color="grey-darken-1" @click="closeDialog" :disabled="isCreating">
              إلغاء
            </v-btn>
            <v-btn
              color="primary"
              variant="elevated"
              class="px-8 font-weight-bold"
              :loading="isCreating"
              :disabled="!isFormValid"
              @click="submitForm"
            >
              إنشاء
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" color="success" location="bottom" rounded="pill">
      <v-icon start>mdi-check-circle</v-icon>
      {{ snackbar.message }}
    </v-snackbar>
  </div>
</template>

<style scoped>
.create-placeholder-card {
  border: 2px dashed #dcdcdc !important;
  background-color: rgba(255, 255, 255, 0.5) !important;
  transition: all 0.3s ease;
  cursor: pointer;
}

.create-placeholder-card:hover {
  border-color: rgb(var(--v-theme-primary)) !important;
  border-style: solid !important;
  background-color: #ffffff !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}

.shadow-sm {
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.3);
}
</style>
