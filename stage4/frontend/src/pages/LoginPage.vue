<script>
import authService from '@/services/authService' // Import the authService

export default {
  data() {
    return {
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
      const isValid = await this.$refs.loginForm.validate() // Validate the form
      if (!isValid) return

      this.isRequestInProgress = true

      try {
        // Use the login service
        await authService.login({
          username: this.formData.username,
          password: this.formData.password,
        })

        // Success message and redirect
        this.loginErrorMessage = ''
        this.loginSucccessMessage = 'تم تسجيل الدخول بنجاح'
        setTimeout(() => this.$router.push('/organizations'), 1000)
      } catch (error) {
        // Error handling
        this.loginErrorMessage = `خطأ: ${error.message}`
      } finally {
        this.isRequestInProgress = false
      }
    },
  },
}
</script>

<template>
  <v-container class="justify-center">
    <v-card class="pa-8" outlined>
      <v-form ref="loginForm" @submit.prevent="onSubmit">
        <!-- Title -->
        <h1 class="text-center mb-6">تسجيل الدخول</h1>

        <!-- Error and Success Messages -->
        <v-alert v-if="loginErrorMessage" type="error" dismissible class="mb-4">
          {{ loginErrorMessage }}
        </v-alert>

        <v-alert v-if="loginSucccessMessage" type="success" dismissible class="mb-4">
          {{ loginSucccessMessage }}
        </v-alert>

        <!-- Username Field -->
        <v-text-field
          label="اسم المستخدم"
          v-model="formData.username"
          :rules="[rules.required, rules.minLength(3), rules.maxLength(25)]"
          outlined
          required
        />

        <!-- Password Field -->
        <v-text-field
          label="كلمة المرور"
          v-model="formData.password"
          :rules="[rules.required, rules.minLength(8), rules.maxLength(50)]"
          type="password"
          outlined
          required
        />

        <!-- Forgot Password -->
        <div class="my-4 text-right">
          <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"> هل نسيت كلمة المرور؟ </a>
        </div>

        <!-- Submit Button -->
        <v-btn
          :loading="isRequestInProgress"
          :disabled="isRequestInProgress"
          type="submit"
          block
          color="primary"
          class="gradient-bg"
        >
          تسجيل الدخول
        </v-btn>

        <!-- Progress Indicator -->
        <div v-if="isRequestInProgress" class="text-center mt-4">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>

        <!-- Redirect to Register -->
        <div class="text-center mt-4">
          <RouterLink to="/register">ليس لديك حساب ؟ أنشاء حساب</RouterLink>
        </div>
      </v-form>
    </v-card>
  </v-container>
</template>

<style scoped>
/* Add custom styles if needed */
</style>
