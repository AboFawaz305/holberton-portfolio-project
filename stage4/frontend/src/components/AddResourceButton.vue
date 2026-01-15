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
    <!-- Trigger Button -->
    <v-btn color="primary" @click="dialog = true">
      <v-icon left>mdi-plus</v-icon>
      إضافة مصدر
    </v-btn>

    <!-- Upload Dialog -->
    <v-dialog v-model="dialog" max-width="500px" persistent>
      <v-card>
        <v-card-title>
          <v-icon color="primary" class="ml-2">mdi-file-upload</v-icon>
          إضافة مصدر جديد
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text>
          <!-- Alert Message -->
          <v-alert v-if="showAlert" :type="alertType" dismissible class="mb-4" close="hideAlert">
            {{ alertMessage }}
          </v-alert>

          <!-- Resource Name -->
          <v-text-field
            v-model="name"
            label="اسم المصدر"
            :rules="nameRules"
            :disabled="isUploading"
            outlined
            required
            counter="50"
            class="mb-3"
          />

          <!-- Description -->
          <v-textarea
            v-model="description"
            label="الوصف (اختياري)"
            :rules="descriptionRules"
            :disabled="isUploading"
            outlined
            rows="3"
            counter="150"
            class="mb-3"
          />

          <!-- File Input with Drag and Drop -->
          <v-file-input
            v-model="file"
            label="اختر ملف"
            :rules="fileRules"
            :disabled="isUploading"
            outlined
            prepend-icon="mdi-paperclip"
            show-size
            @update:model-value="onFileChange"
          >
            <template v-slot:selection="{ text }">
              <v-chip small label color="primary">
                {{ text }}
              </v-chip>
            </template>
          </v-file-input>

          <!-- File Info Preview -->
          <v-chip v-if="fileInfo" class="mb-3" color="grey lighten-2">
            <v-icon left small>mdi-file</v-icon>
            {{ fileInfo }}
          </v-chip>

          <!-- Upload Progress -->
          <v-progress-linear
            v-if="isUploading"
            :model-value="uploadProgress"
            color="primary"
            height="20"
            striped
            class="mb-3"
          >
            <template v-slot:default>
              <strong>{{ uploadProgress }}%</strong>
            </template>
          </v-progress-linear>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text :disabled="isUploading" @click="closeDialog"> إلغاء </v-btn>
          <v-btn
            color="primary"
            :disabled="!isFormValid || isUploading"
            :loading="isUploading"
            @click="submitForm"
          >
            <v-icon left>mdi-upload</v-icon>
            إضافة
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
/* RTL support for icons */
.v-icon.ml-2 {
  margin-left: 8px;
}
</style>
