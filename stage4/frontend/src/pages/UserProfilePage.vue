<script>
import authService from '@/services/authService'
import usersService from '@/services/usersService'

export default {
  data() {
    return {
      user: null,
      loading: true,

      // Visibility states for closable alerts
      showInfoError: false,
      showInfoSuccess: false,
      showEmailError: false,
      showEmailSuccess: false,
      showPasswordError: false,
      showPasswordSuccess: false,
      showGlobalError: false,

      // Message strings
      error: '',
      userInformationFormErrorMessage: '',
      userInformationFormSuccessMessage: '',
      emailAddError: '',
      emailAddSuccess: '',
      passwordResetFormError: '',
      passwordResetFormSuccess: '',

      // Form data
      form: {
        firstname: '',
        lastname: '',
        username: '',
      },
      emailForm: {
        email: '',
      },
      passwordResetForm: {
        password: '',
        repeatPassword: '',
      },

      // Validation rules
      rules: {
        required: (value) => !!value || 'هذا الحقل إلزامي',
        minLength: (min) => (value) =>
          (value && value.length >= min) || `أدخل على الأقل ${min} أحرف`,
        maxLength: (max) => (value) =>
          (value && value.length <= max) || `هذا الحقل يجب ألا يتعدى ${max} حرف`,
        email: (value) => /.+@.+\..+/.test(value) || 'يجب أن يكون الإيميل صالحاً',
        passwordsMatch: (confirmPassword) => (value) =>
          confirmPassword === value || 'كلمات السر لا تتطابق',
      },
    }
  },
  async mounted() {
    await this.refreshUserData()
  },
  methods: {
    translateError(err) {
      const code = err.response?.data?.detail || err.message || err

      const messages = {
        USERNAME_ALREADY_EXIST: 'اسم المستخدم هذا مستخدم بالفعل، يرجى اختيار اسم آخر.',
        EMAIL_ALREADY_EXIST: 'هذا البريد الإلكتروني مسجل بالفعل في حساب آخر.',
        EMAIL_DONT_EXIST: 'هذا البريد الإلكتروني غير موجود.',
        DELETE_ALL_EMAILS_NOT_ALLOWED:
          'لا يمكن حذف البريد الأخير، يجب أن تمتلك بريداً واحداً على الأقل.',
        ORGANIZATION_NOT_FOUND: 'المنظمة غير موجودة.',
        GROUP_NOT_FOUND: 'المجموعة غير موجودة.',
        USER_ALREADY_JOINED: 'أنت مشترك بالفعل في هذه المجموعة.',
      }

      return messages[code] || 'حدث خطأ غير متوقع، يرجى المحاولة لاحقاً'
    },

    handleBack() {
      this.$router.back()
    },

    async onUserInformationUpdate() {
      if (!this.validateUserInformationForm()) return

      const valuestoupdate = {}
      if (this.form.username !== this.user.username) valuestoupdate.username = this.form.username
      if (this.form.firstname !== this.user.first_name)
        valuestoupdate.first_name = this.form.firstname
      if (this.form.lastname !== this.user.last_name) valuestoupdate.last_name = this.form.lastname

      if (Object.keys(valuestoupdate).length <= 0) return

      try {
        await usersService.updateUser(valuestoupdate)
        this.userInformationFormSuccessMessage = 'تم تحديث المعلومات بنجاح'
        this.showInfoSuccess = true
        this.showInfoError = false
        this.$refs.userInfoForm.resetValidation()
        await this.refreshUserData()
      } catch (error) {
        this.userInformationFormErrorMessage = this.translateError(error)
        this.showInfoError = true
        this.showInfoSuccess = false
      }
    },

    async onEmailAdd() {
      if (!this.validateEmailForm()) return

      try {
        await usersService.addEmail(this.emailForm.email)
        this.emailAddSuccess = 'تمت إضافة الإيميل بنجاح: ' + this.emailForm.email
        this.showEmailSuccess = true
        this.showEmailError = false
        this.emailForm.email = ''
        this.$refs.emailAddForm.reset()
        await this.refreshUserData()
      } catch (error) {
        this.emailAddError = this.translateError(error)
        this.showEmailError = true
        this.showEmailSuccess = false
      }
    },

    async deleteEmail(email_id) {
      try {
        if (this.user.email.length <= 1) {
          this.emailAddError = 'لا تستطيع حذف آخر إيميل لديك'
          this.showEmailError = true
          return
        }
        const emailStr = this.user.email[email_id].value
        await usersService.deleteEmail(email_id)
        this.emailAddSuccess = 'تم حذف البريد ' + emailStr + ' بنجاح'
        this.showEmailSuccess = true
        this.showEmailError = false
        await this.refreshUserData()
      } catch (error) {
        this.emailAddError = this.translateError(error)
        this.showEmailError = true
        this.showEmailSuccess = false
      }
    },

    async onPasswordReset() {
      if (!this.validatePasswordResetForm()) return

      try {
        await usersService.updateUser({ password: this.passwordResetForm.password })
        this.passwordResetFormSuccess = 'تم تحديث كلمة السر بنجاح'
        this.showPasswordSuccess = true
        this.showPasswordError = false
        this.$refs.passwordResetForm.reset()
      } catch (error) {
        this.passwordResetFormError = this.translateError(error)
        this.showPasswordError = true
        this.showPasswordSuccess = false
      }
    },

    async refreshUserData() {
      this.loading = true
      try {
        this.user = await authService.getCurrentUser()
        this.form.firstname = this.user.first_name
        this.form.lastname = this.user.last_name
        this.form.username = this.user.username
      } catch (error) {
        this.error = this.translateError(error)
        this.showGlobalError = true
      } finally {
        this.loading = false
      }
    },

    validateUserInformationForm() {
      return (
        this.rules.required(this.form.firstname) === true &&
        this.rules.required(this.form.lastname) === true &&
        this.rules.required(this.form.username) === true
      )
    },

    validateEmailForm() {
      return this.rules.email(this.emailForm.email) === true
    },

    validatePasswordResetForm() {
      return (
        this.rules.required(this.passwordResetForm.password) === true &&
        this.rules.minLength(8)(this.passwordResetForm.password) === true &&
        this.passwordResetForm.password === this.passwordResetForm.repeatPassword
      )
    },
  },
}
</script>

<template>
  <div class="main-dashboard-wrapper page-background">
    <v-card flat height="280" class="gradient-bg d-flex align-center header-section" rounded="0">
      <v-container class="max-width-container">
        <div class="d-flex align-center">
          <v-avatar size="120" color="white" class="elevation-4 ms-6">
            <v-icon size="80" color="primary">mdi-account-circle-outline</v-icon>
          </v-avatar>

          <div class="d-flex flex-column align-start">
            <template v-if="loading">
              <v-skeleton-loader
                type="button"
                width="80"
                bg-color="transparent"
                class="mb-2 opacity-30"
              ></v-skeleton-loader>
              <v-skeleton-loader
                type="text"
                width="200"
                bg-color="transparent"
                class="mb-2"
              ></v-skeleton-loader>
              <v-skeleton-loader type="text" width="150" bg-color="transparent"></v-skeleton-loader>
            </template>
            <template v-else>
              <v-btn
                variant="text"
                color="white"
                prepend-icon="mdi-arrow-right"
                class="pa-0 mb-1 back-btn-header"
                density="compact"
                @click="handleBack"
              >
                رجوع
              </v-btn>
              <h1 class="text-h3 font-weight-bold text-white mb-1">
                {{ form.firstname }} {{ form.lastname }}
              </h1>
              <span class="text-h6 text-white opacity-70">إعدادات الحساب الشخصي</span>
            </template>
          </div>
        </div>
      </v-container>
    </v-card>

    <v-container class="mt-n12 pb-12 max-width-container">
      <v-row v-if="user">
        <v-col cols="12" md="8">
          <v-card class="rounded-xl layered-shadow mb-6 overflow-hidden">
            <v-toolbar color="white" flat class="px-4 border-b">
              <v-icon color="primary" class="me-3">mdi-badge-account-outline</v-icon>
              <v-toolbar-title class="font-weight-bold">المعلومات الشخصية</v-toolbar-title>
            </v-toolbar>

            <v-card-text class="pa-6">
              <v-alert
                v-model="showInfoError"
                closable
                density="compact"
                type="error"
                variant="tonal"
                class="mb-4 rounded-lg"
              >
                {{ userInformationFormErrorMessage }}
              </v-alert>
              <v-alert
                v-model="showInfoSuccess"
                closable
                density="compact"
                type="success"
                variant="tonal"
                class="mb-4 rounded-lg"
              >
                {{ userInformationFormSuccessMessage }}
              </v-alert>

              <v-form @submit.prevent="onUserInformationUpdate" ref="userInfoForm">
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="form.firstname"
                      label="الإسم الأول"
                      variant="outlined"
                      rounded="lg"
                      density="comfortable"
                      :rules="[rules.required]"
                    />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="form.lastname"
                      label="الإسم الأخير"
                      variant="outlined"
                      rounded="lg"
                      density="comfortable"
                      :rules="[rules.required]"
                    />
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      v-model="form.username"
                      label="إسم المستخدم"
                      variant="outlined"
                      rounded="lg"
                      density="comfortable"
                      prepend-inner-icon="mdi-at"
                      :rules="[rules.required]"
                    />
                  </v-col>
                </v-row>
                <v-btn color="primary" type="submit" rounded="lg" size="large" class="px-8 mt-2"
                  >تحديث المعلومات</v-btn
                >
              </v-form>
            </v-card-text>
          </v-card>

          <v-card class="rounded-xl layered-shadow overflow-hidden">
            <v-toolbar color="white" flat class="px-4 border-b">
              <v-icon color="primary" class="me-3">mdi-lock-reset</v-icon>
              <v-toolbar-title class="font-weight-bold">تغيير كلمة السر</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="pa-6">
              <v-alert
                v-model="showPasswordError"
                closable
                density="compact"
                type="error"
                variant="tonal"
                class="mb-4 rounded-lg"
              >
                {{ passwordResetFormError }}
              </v-alert>
              <v-alert
                v-model="showPasswordSuccess"
                closable
                density="compact"
                type="success"
                variant="tonal"
                class="mb-4 rounded-lg"
              >
                {{ passwordResetFormSuccess }}
              </v-alert>
              <v-form @submit.prevent="onPasswordReset" ref="passwordResetForm">
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="passwordResetForm.password"
                      type="password"
                      label="كلمة السر الجديدة"
                      variant="outlined"
                      rounded="lg"
                      density="comfortable"
                      :rules="[rules.required, rules.minLength(8)]"
                    />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="passwordResetForm.repeatPassword"
                      type="password"
                      label="تأكيد كلمة السر"
                      variant="outlined"
                      rounded="lg"
                      density="comfortable"
                      :rules="[rules.required, rules.passwordsMatch(passwordResetForm.password)]"
                    />
                  </v-col>
                </v-row>
                <v-btn
                  color="primary"
                  variant="tonal"
                  type="submit"
                  rounded="lg"
                  size="large"
                  class="px-8 mt-2"
                  >تحديث كلمة السر</v-btn
                >
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card class="rounded-xl layered-shadow overflow-hidden h-100">
            <v-toolbar color="white" flat class="px-4 border-b">
              <v-icon color="primary" class="me-3">mdi-email-multiple-outline</v-icon>
              <v-toolbar-title class="font-weight-bold">البريد الإلكتروني</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="pa-6">
              <v-alert
                v-model="showEmailError"
                closable
                density="compact"
                type="error"
                variant="tonal"
                class="mb-4 rounded-lg"
              >
                {{ emailAddError }}
              </v-alert>
              <v-alert
                v-model="showEmailSuccess"
                closable
                density="compact"
                type="success"
                variant="tonal"
                class="mb-4 rounded-lg"
              >
                {{ emailAddSuccess }}
              </v-alert>
              <v-list class="pa-0 mb-6 bg-transparent">
                <v-list-item
                  v-for="(emailObj, i) in user.email"
                  :key="i"
                  class="email-item rounded-lg mb-2 border shadow-sm"
                >
                  <v-list-item-title class="text-body-2 ms-2">{{
                    emailObj.value
                  }}</v-list-item-title>
                  <template v-slot:append>
                    <v-chip
                      size="x-small"
                      :color="emailObj.is_verified ? 'success' : 'warning'"
                      class="me-2"
                      variant="tonal"
                    >
                      {{ emailObj.is_verified ? 'موثق' : 'غير موثق' }}
                    </v-chip>
                    <v-btn
                      icon="mdi-delete-outline"
                      @click="deleteEmail(i)"
                      color="error"
                      variant="text"
                      size="small"
                    ></v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <v-divider class="mb-6"></v-divider>
              <v-form @submit.prevent="onEmailAdd" ref="emailAddForm">
                <v-text-field
                  v-model="emailForm.email"
                  label="إضافة بريد جديد"
                  variant="outlined"
                  rounded="lg"
                  density="comfortable"
                  :rules="[rules.required, rules.email]"
                  class="mb-2"
                />
                <v-btn block color="primary" type="submit" rounded="lg" class="font-weight-bold"
                  >أضف بريد</v-btn
                >
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-snackbar v-model="showGlobalError" color="error" timeout="5000" rounded="pill">
      <v-icon start>mdi-alert-circle-outline</v-icon>
      {{ error }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showGlobalError = false">إغلاق</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<style scoped>
.page-background {
  background-color: #f4f7fa;
  min-height: 100vh;
}

/* Centering constraint for wide screens */
.max-width-container {
  max-width: 1400px !important;
  margin: 0 auto !important;
}

.header-section {
  flex: 0 0 280px;
  z-index: 1;
}

.layered-shadow {
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
}

.email-item {
  border: 1px solid #edf2f7 !important;
  background-color: #ffffff;
}

.opacity-70 {
  opacity: 0.7;
}
.back-btn-header {
  font-weight: bold;
  opacity: 0.9;
}
:deep(.v-skeleton-loader) {
  background: transparent !important;
}
</style>
