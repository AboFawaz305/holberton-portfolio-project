<!-- stage4/frontend/src/components/CreateGroupButton.vue -->
<script>
import groupsService from '@/services/groupsService'

export default {
  name: 'CreateGroupButton',

  props: {
    orgId: {
      type: String,
      required: true,
    },
    // إذا موجود => ينشئ SubGroup
    parentGroupId: {
      type: String,
      default: null,
    },
    // نص الزر (اختياري)
    buttonLabel: {
      type: String,
      default: 'إضافة مجموعة',
    },
  },

  emits: ['created'],

  data() {
    return {
      dialog: false,
      title: '',
      isCreating: false,

      showAlert: false,
      alertMessage: '',
      alertType: 'error',

      titleRules: [
        (v) => !!v || 'اسم المجموعة مطلوب',
        (v) => (v && v.length >= 3) || 'اسم المجموعة يجب أن يكون 3 أحرف على الأقل',
        (v) => (v && v.length <= 100) || 'اسم المجموعة يجب أن يكون 100 حرف أو أقل',
      ],
    }
  },

  computed: {
    isFormValid() {
      const t = (this.title || '').trim()
      return t.length >= 3 && t.length <= 100
    },
  },

  methods: {
    showAlertMessage(message, type = 'error') {
      this.alertMessage = message
      this.alertType = type
      this.showAlert = true
    },
    hideAlert() {
      this.showAlert = false
      this.alertMessage = ''
    },
    resetForm() {
      this.title = ''
      this.hideAlert()
    },
    closeDialog() {
      this.dialog = false
      this.resetForm()
    },

    async submitForm() {
      if (!this.isFormValid || this.isCreating) return

      this.isCreating = true
      this.hideAlert()

      try {
        const token = localStorage.getItem('token')

        const payload = { title: this.title.trim() }
        if (this.parentGroupId) payload.parent_group_id = this.parentGroupId

        await groupsService.createGroup(this.orgId, payload, token)

        this.$emit('created') // عشان الأب يسوي refresh للقائمة
        this.closeDialog()
      } catch (error) {
        if (error.message === 'GROUP_ALREADY_EXIST') {
          this.showAlertMessage('اسم المجموعة مستخدم مسبقًا')
        } else if (error.message === 'SUBGROUP_ALREADY_EXIST') {
          this.showAlertMessage('اسم المجموعة الفرعية مستخدم مسبقًا')
        } else if (error.message === 'ORGANIZATION_NOT_FOUND') {
          this.showAlertMessage('الكلية غير موجودة')
        } else if (error.message === 'NOT_A_MEMBER') {
          this.showAlertMessage('لا تملكين صلاحية إنشاء مجموعة فرعية هنا')
        } else {
          this.showAlertMessage(error.message || 'حدث خطأ أثناء إنشاء المجموعة')
        }
      } finally {
        this.isCreating = false
      }
    },
  },
}
</script>

<template>
  <div>
    <!-- Trigger Button -->
    <v-btn color="primary" rounded="xl" block @click="dialog = true">
      <v-icon left>mdi-plus</v-icon>
      {{ buttonLabel }}
    </v-btn>

    <!-- Dialog -->
    <v-dialog v-model="dialog" max-width="500px" persistent>
      <v-card rounded="xl">
        <v-card-title class="text-right font-weight-bold">
          <v-icon color="primary" class="ml-2">mdi-account-group</v-icon>
          {{ parentGroupId ? 'إنشاء مجموعة فرعية' : 'إنشاء مجموعة جديدة' }}
        </v-card-title>

        <v-divider />

        <v-card-text>
          <v-alert
            v-if="showAlert"
            :type="alertType"
            dismissible
            class="mb-4"
            @click:close="hideAlert"
          >
            {{ alertMessage }}
          </v-alert>

          <v-text-field
            v-model="title"
            label="اسم المجموعة"
            placeholder="مثال: علوم الحاسب"
            :rules="titleRules"
            :disabled="isCreating"
            outlined
            required
            counter="100"
          />
        </v-card-text>

        <v-divider />

        <v-card-actions>
          <v-spacer />
          <v-btn text :disabled="isCreating" @click="closeDialog">إلغاء</v-btn>
          <v-btn
            color="primary"
            :disabled="!isFormValid || isCreating"
            :loading="isCreating"
            @click="submitForm"
          >
            <v-icon left>mdi-check</v-icon>
            إنشاء
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.v-icon.ml-2 {
  margin-left: 8px;
}
</style>
