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
  <v-container fluid class="justify-center">
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
/* يغطي الصفحة بالكامل */
.v-container {
  min-height: 100vh;
  width: 100%;

  display: flex;
  align-items: center;
  justify-content: center;

  /* تدرج ناعم ومريح */
  background: linear-gradient(180deg, #5fb0be 0%, #6fbac6 45%, #84c7d0 100%);
}

/* الكارد الرئيسي */
.v-card {
  background: #f1f1f1;
  border-radius: 36px;

  /* حجم مناسب للابتوب */
  width: 640px;
  max-width: 92%;

  padding: 56px 48px;

  box-shadow: 0 32px 70px rgba(0, 0, 0, 0.2);
}

/* العنوان */
h2 {
  font-weight: 700;
  margin-bottom: 40px;
}

/* الحقول */
.v-text-field {
  margin-bottom: 22px;
}

.v-text-field .v-field {
  border-radius: 14px;
  background: #eaeaea;
}

/* Checkbox */
.v-checkbox {
  margin-top: 18px;
  margin-bottom: 32px;
}

/* زر إنشاء حساب */
.gradient-bg {
  height: 72px;
  border-radius: 22px;

  font-size: 20px;
  font-weight: 700;

  background: linear-gradient(90deg, #6fb6c4 0%, #2f6f7c 100%);

  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.25);
  transition: all 0.2s ease;
}

.gradient-bg:hover {
  transform: translateY(-2px);
  box-shadow: 0 22px 44px rgba(0, 0, 0, 0.3);
}

.gradient-bg:active {
  transform: translateY(0);
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.22);
}
</style>
