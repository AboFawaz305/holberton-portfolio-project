<template>
  <v-dialog v-model="internalOpen" max-width="500px" persistent>
    <v-form ref="domainForm" v-model="isFormValid" @submit.prevent="save">
      <v-card rounded="xl" class="pa-4">
        <v-card-title class="text-h5 font-weight-bold d-flex align-center">
          <v-icon start color="primary">mdi-shield-lock</v-icon>
          إدارة النطاقات المسموحة
        </v-card-title>

        <v-card-text>
          <p class="text-body-2 text-grey-darken-1 mb-4">
            أضف أو احذف نطاقات البريد. سيتمكن مستخدمو هذه النطاقات فقط من الانضمام.
          </p>

          <v-combobox
            v-model="internalDomains"
            :rules="domainRules"
            label="النطاقات النشطة"
            multiple
            chips
            closable-chips
            hint="مثال: seu.edu.sa أو gmail.com"
            persistent-hint
            variant="outlined"
            color="primary"
            prepend-inner-icon="mdi-at"
            @update:model-value="normalizeDomains"
          ></v-combobox>
        </v-card-text>

        <v-card-actions class="mt-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" color="grey" @click="close" :disabled="loading">إلغاء</v-btn>
          <v-btn
            color="primary"
            variant="elevated"
            :loading="loading"
            :disabled="!isFormValid"
            @click="save"
            class="px-6"
          >
            حفظ التغييرات
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
  <v-snackbar
    v-model="snackbar.show"
    :color="snackbar.color"
    timeout="3000"
    location="bottom"
  >
    {{ snackbar.message }}

    <template v-slot:actions>
      <v-btn variant="text" @click="snackbar.show = false"> إغلاق </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import groupsService from '@/services/groupsService'

export default {
  props: {
    modelValue: Boolean,
    groupId: String,
    orgId: String,
    initialDomains: Array,
  },
  emits: ['update:modelValue', 'saved'],
  data() {
    return {
      loading: false,
      isFormValid: true,
      internalDomains: [],
      snackbar: {
        show: false,
        message: '',
        color: 'success',
      },
      // Validation Logic
      domainRules: [
        (v) => {
          if (!v || v.length === 0) return true
          
          const domainRegex = /^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$/i
          const invalidDomains = v.filter((domain) => !domainRegex.test(domain))

          return (
            invalidDomains.length === 0 ||
            'بعض النطاقات غير صالحة (مثال: seu.edu.sa)'
          )
        },
      ],
    }
  },
  computed: {
    internalOpen: {
      get() {
        return this.modelValue
      },
      set(val) {
        this.$emit('update:modelValue', val)
      },
    },
  },
  watch: {
    modelValue(isOpen) {
      if (isOpen) {
        this.internalDomains = this.initialDomains ? [...this.initialDomains] : []
        // Reset validation when opening
        this.$nextTick(() => {
          if (this.$refs.domainForm) this.$refs.domainForm.resetValidation()
        })
      }
    },
  },
  methods: {
    normalizeDomains(val) {
      if (!val) return
      this.internalDomains = val.map(d => d.toLowerCase().trim())
    },
    async save() {
      const { valid } = await this.$refs.domainForm.validate()
      if (!valid || !this.groupId || !this.orgId) return

      this.loading = true
      try {
        await groupsService.updateAllowedDomains(this.orgId, this.groupId, this.internalDomains)

        // Trigger the success message
        this.snackbar.message = 'تم تحديث النطاقات بنجاح'
        this.snackbar.color = 'success'
        this.snackbar.show = true

        this.$emit('saved', this.internalDomains)

        this.close()
      } catch (err) {
        this.snackbar.message = 'حدث خطأ أثناء الحفظ'
        this.snackbar.color = 'error'
        this.snackbar.show = true
        console.error('Failed to save domains:', err)
      } finally {
        this.loading = false
      }
    },
    close() {
      this.internalOpen = false
    },
  },
}
</script>
