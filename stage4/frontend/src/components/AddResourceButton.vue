<script>
import groupsService from '@/services/groupsService'

export default {
  props: {
    groupId: {
      type: String,
      required: true,
    },
  },

  emits: ['uploaded'],

  data() {
    return {
      // Dialog state
      dialog: false,

      // Form fields
      name: '',
      description: '',
      file: null,

      // UI state
      isUploading: false,
      uploadProgress: 0,
      alertMessage: '',
      alertType: 'error', // 'success' or 'error'
      showAlert: false,

      // Validation rules
      nameRules: [
        (v) => !!v || 'اسم المصدر مطلوب',
        (v) => (v && v.length >= 3) || 'اسم المصدر يجب أن يكون 3 أحرف على الأقل',
        (v) => (v && v.length <= 50) || 'اسم المصدر يجب أن يكون 50 حرف أو أقل',
      ],
      descriptionRules: [(v) => !v || v.length <= 150 || 'الوصف يجب أن يكون 150 حرف أو أقل'],
      fileRules: [(v) => !!v || 'الملف مطلوب'],
    }
  },

  computed: {
    // Display selected file info
    fileInfo() {
      if (!this.file) return null
      const size = this.formatFileSize(this.file.size)
      return `${this.file.name} (${size})`
    },

    // Check if form is valid for submission
    isFormValid() {
      return (
        this.name &&
        this.name.length >= 3 &&
        this.name.length <= 50 &&
        (!this.description || this.description.length <= 150) &&
        this.file
      )
    },
  },

  methods: {
    // Format file size for display
    formatFileSize(bytes) {
      if (bytes === 0) return '0 بايت'
      const k = 1024
      const sizes = ['بايت', 'كيلوبايت', 'ميغابايت', 'غيغابايت']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },

    // Handle file selection
    onFileChange(file) {
      this.file = file
      this.hideAlert()
    },

    // Show alert message
    showAlertMessage(message, type = 'error') {
      this.alertMessage = message
      this.alertType = type
      this.showAlert = true
    },

    // Hide alert
    hideAlert() {
      this.showAlert = false
      this.alertMessage = ''
    },

    // Reset form to initial state
    resetForm() {
      this.name = ''
      this.description = ''
      this.file = null
      this.uploadProgress = 0
      this.hideAlert()
    },

    // Close dialog
    closeDialog() {
      this.dialog = false
      this.resetForm()
    },

    // Handle upload progress
    onUploadProgress(progress) {
      this.uploadProgress = progress
    },

    // Submit the form
    async submitForm() {
      if (!this.isFormValid || this.isUploading) return

      this.isUploading = true
      this.uploadProgress = 0
      this.hideAlert()

      try {
        await groupsService.addResource(
          this.groupId,
          {
            name: this.name,
            description: this.description,
            file: this.file,
          },
          this.onUploadProgress,
        )

        this.$emit('uploaded')
        this.closeDialog()
      } catch (error) {
        // Handle specific error cases
        if (error.message === 'GROUP_NOT_FOUND') {
          this.showAlertMessage('المجموعة غير موجودة')
        } else if (error.message === 'USER_NOT_A_MEMBER') {
          this.showAlertMessage('ليس لديك صلاحية الإضافة في هذه المجموعة')
        } else {
          this.showAlertMessage(error.message || 'حدث خطأ ��ثناء رفع المصدر')
        }
      } finally {
        this.isUploading = false
      }
    },
  },
}
</script>

<template>
  <div>
    <!-- Trigger Card -->
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
          إضافة مصدر
        </div>
      </div>
    </v-card>

    <!-- Upload Dialog -->
    <v-dialog v-model="dialog" max-width="500px" persistent>
      <v-card rounded="xl" class="pa-6">
        <v-card-title class="text-h5 font-weight-bold px-0 d-flex align-center">
          <v-icon start color="primary" class="me-2">mdi-file-upload</v-icon>
          إضافة مصدر جديد
        </v-card-title>

        <v-card-text class="px-0 pt-4">
          <!-- Alert Message -->
          <v-expand-transition>
            <v-alert
              v-if="showAlert"
              :type="alertType"
              variant="tonal"
              density="compact"
              class="mb-4 rounded-lg text-caption"
              closable
              @click:close="hideAlert"
            >
              {{ alertMessage }}
            </v-alert>
          </v-expand-transition>

          <!-- Resource Name -->
          <v-text-field
            v-model="name"
            label="اسم المصدر"
            placeholder="أدخل اسم المصدر هنا..."
            :rules="nameRules"
            :disabled="isUploading"
            variant="outlined"
            color="primary"
            rounded="lg"
            required
            counter="50"
            bg-color="grey-lighten-5"
            prepend-inner-icon="mdi-tag-outline"
            class="mb-3"
          />

          <!-- Description -->
          <v-textarea
            v-model="description"
            label="الوصف (اختياري)"
            placeholder="أدخل وصف المصدر..."
            :rules="descriptionRules"
            :disabled="isUploading"
            variant="outlined"
            color="primary"
            rounded="lg"
            rows="3"
            counter="150"
            bg-color="grey-lighten-5"
            prepend-inner-icon="mdi-text"
            class="mb-3"
          />

          <!-- File Input -->
          <v-file-input
            v-model="file"
            label="اختر ملف"
            placeholder="اختر ملف للرفع"
            :rules="fileRules"
            :disabled="isUploading"
            variant="outlined"
            color="primary"
            rounded="lg"
            bg-color="grey-lighten-5"
            prepend-inner-icon="mdi-paperclip"
            show-size
            @update:model-value="onFileChange"
          >
            <template v-slot:selection="{ text }">
              <v-chip small label color="primary">
                {{ text }}
              </v-chip>
            </template>
          </v-file-input>

          <!-- Upload Progress -->
          <v-progress-linear
            v-if="isUploading"
            :model-value="uploadProgress"
            color="primary"
            height="20"
            striped
            rounded
            class="mb-3"
          >
            <template v-slot:default>
              <strong>{{ uploadProgress }}%</strong>
            </template>
          </v-progress-linear>
        </v-card-text>

        <v-card-actions class="px-0 mt-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" color="grey-darken-1" :disabled="isUploading" @click="closeDialog">
            إلغاء
          </v-btn>
          <v-btn
            color="primary"
            variant="elevated"
            class="px-8 font-weight-bold"
            :disabled="!isFormValid || isUploading"
            :loading="isUploading"
            @click="submitForm"
          >
            <v-icon start>mdi-upload</v-icon>
            إضافة
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
