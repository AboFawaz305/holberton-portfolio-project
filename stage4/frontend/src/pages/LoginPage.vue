<script>
import authService from '@/services/authService' // Import the authService

export default {
  data() {
    return {
      showPassword: false,
      successOverlay: false,
      formData: {
        username: '',
        password: '',
      },
      loginErrorMessage: '',
      loginSucccessMessage: '',
      isRequestInProgress: false,
      // Form rules
      rules: {
        required: (value) => !!value || 'هذا الحقل الزامي',
        minLength: (min) => (value) =>
          (value && value.length >= min) || `لا يمكن ان يكون اقل من ${min} احرف`,
        maxLength: (max) => (value) =>
          (value && value.length <= max) || `يجب ان لا يكون اكثر من ${max} حرفا`,
      },
    }
  },
  methods: {
    async onSubmit() {
      this.loginErrorMessage = ''
      this.loginSucccessMessage = ''

      const { valid } = await this.$refs.loginForm.validate()
      if (!valid) return

      this.isRequestInProgress = true

      try {
        // Use the login service
        await authService.login({
          username: this.formData.username,
          password: this.formData.password,
        })

        this.isRequestInProgress = false // Stop button loading
        this.successOverlay = true
        // Success message and redirect
        this.loginErrorMessage = ''
        this.loginSucccessMessage = 'تم تسجيل الدخول بنجاح'
        setTimeout(() => this.$router.push('/organizations'), 1200)
      } catch (error) {
        const errorMap = {
          INVALID_USERNAME: 'اسم المستخدم غير موجود',
          INVALID_PASSWORD: 'كلمة المرور خاطئة',
        }
        this.loginErrorMessage =
          errorMap[error.message] || 'فشل تسجيل الدخول، يرجى المحاولة مرة أخرى'
      } finally {
        this.isRequestInProgress = false
      }
    },
  },
}
</script>

<template>
  <v-container fluid class="fill-height auth-bg py-10">
    <v-overlay
      v-model="successOverlay"
      class="align-center justify-center"
      persistent
      scrim="primary"
    >
      <div class="text-center">
        <v-progress-circular
          indeterminate
          color="white"
          size="64"
          width="6"
          class="mb-4"
        ></v-progress-circular>
        <h2 class="text-h5 text-white font-weight-bold">جاري تحضير المنظمات...</h2>
      </div>
    </v-overlay>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card rounded="xl" elevation="8" class="pa-8 shadow-card">
          <div class="text-center mb-10">
            <v-avatar color="primary-lighten-5" size="80" class="mb-4">
              <v-icon color="primary" size="40">mdi-login</v-icon>
            </v-avatar>
            <h1 class="text-h4 font-weight-bold mb-2">تسجيل الدخول</h1>
            <p class="text-body-1 text-grey-darken-1">مرحباً بك مجدداً في المنصة</p>
          </div>

          <v-form ref="loginForm" @submit.prevent="onSubmit">
            <v-expand-transition>
              <v-alert
                v-if="loginErrorMessage"
                type="error"
                variant="tonal"
                rounded="lg"
                class="mb-6"
                closable
                @click:close="loginErrorMessage = ''"
              >
                {{ loginErrorMessage }}
              </v-alert>
            </v-expand-transition>

            <v-expand-transition>
              <v-alert
                v-if="loginSucccessMessage"
                type="success"
                variant="tonal"
                rounded="lg"
                class="mb-6"
                closable
                @click:close="loginSucccessMessage = ''"
              >
                {{ loginSucccessMessage }}
              </v-alert>
            </v-expand-transition>

            <v-text-field
              v-model="formData.username"
              label="اسم المستخدم"
              :rules="[rules.required, rules.minLength(3), rules.maxLength(25)]"
              variant="outlined"
              rounded="lg"
              color="primary"
              prepend-inner-icon="mdi-account-outline"
              class="mb-4"
              required
            />

            <v-text-field
              v-model="formData.password"
              label="كلمة المرور"
              :rules="[rules.required, rules.minLength(8), rules.maxLength(50)]"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
              rounded="lg"
              color="primary"
              prepend-inner-icon="mdi-lock-outline"
              class="mb-6"
              required
            >
              <template #append-inner>
                <v-btn variant="text" icon tabindex="-1" @click="showPassword = !showPassword">
                  <v-icon color="grey-darken-1">
                    {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
                  </v-icon>
                </v-btn>
              </template>
            </v-text-field>

            <v-btn
              type="submit"
              color="primary"
              size="large"
              block
              rounded="lg"
              elevation="2"
              class="py-7 font-weight-bold text-h6 gradient-bg"
              :loading="isRequestInProgress"
              :disabled="isRequestInProgress"
            >
              تسجيل الدخول
            </v-btn>

            <div class="text-center mt-8 text-body-2 text-grey-darken-1">
              ليس لديك حساب؟
              <v-btn variant="text" color="primary" to="/register" class="px-1 font-weight-bold">
                أنشئ حساباً الآن
              </v-btn>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.auth-bg {
  background-color: #f8fafd;
}

.shadow-card {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05) !important;
}

.mb-4 {
  margin-bottom: 20px !important;
}
.mb-6 {
  margin-bottom: 24px !important;
}
</style>
