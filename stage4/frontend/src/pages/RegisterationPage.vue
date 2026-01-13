<script>
import authService from '@/services/authService' // Import the authService

export default {
  data() {
    return {
      registerationForm: {
        firstname: '',
        lastname: '',
        username: '',
        email: '',
        password: '',
        repeatPassword: '',
      },
      registerationErrorMessage: '',
      registerationSucccessMessage: '',
      isTheUserAgreeToTermsAndConditions: false,
      isRequestInProgress: false,
      showVerificationDialog: false,
      rules: {
        required: (value) => !!value || 'هذا الحقل إلزامي',
        min: (length) => (value) => value.length >= length || `أدخل على الأقل ${length} أحرف`,
        max: (length) => (value) =>
          value.length <= length || `هذا الحقل يجب ألا يتعدى ${length} حرف`,
        email: (value) => /.+@.+\..+/.test(value) || 'يجب أن يكون الإيميل صالحا',
        passwordsMatch: (confirmPassword) => (value) =>
          confirmPassword === value || 'كلمات السر لا تتطابق',
      },
    }
  },
  methods: {
    async onSubmit() {
      const isValid = this.$refs.registerationForm.validate() // Validate the form
      if (!isValid) return

      this.isRequestInProgress = true

      try {
        // Use the register service
        await authService.register({
          firstname: this.registerationForm.firstname,
          lastname: this.registerationForm.lastname,
          username: this.registerationForm.username,
          email: this.registerationForm.email,
          password: this.registerationForm.password,
        })

        // Success message and redirect
        this.registerationErrorMessage = ''
        this.registerationSucccessMessage = 'تم إنشاء الحساب بنجاح'
        this.showVerificationDialog = true
      } catch (error) {
        // Error handling
        this.registerationErrorMessage = error.message
      } finally {
        this.isRequestInProgress = false
      }
    },
    onDialogClose() {
      this.showVerificationDialog = false
      this.$router.push('/login')
    },
  },
}
</script>

<template>
  <v-container class="justify-center">
    <v-card outlined class="pa-8">
      <v-form ref="registerationForm">
        <!-- Title -->
        <h2 class="text-center mb-6">إنشاء حساب جديد</h2>

        <!-- Error and Success Messages -->
        <v-alert v-if="registerationErrorMessage" type="error" dismissible class="mb-4">
          {{ registerationErrorMessage }}
        </v-alert>

        <v-alert v-if="registerationSucccessMessage" type="success" dismissible class="mb-4">
          {{ registerationSucccessMessage }}
        </v-alert>

        <!-- First Name -->
        <v-text-field
          label="الإسم الأول"
          v-model="registerationForm.firstname"
          :rules="[rules.required, rules.min(3), rules.max(25)]"
          outlined
          required
        />

        <!-- Last Name -->
        <v-text-field
          label="الإسم الأخير"
          v-model="registerationForm.lastname"
          :rules="[rules.required, rules.min(3), rules.max(25)]"
          outlined
          required
        />

        <!-- Username -->
        <v-text-field
          label="إسم المستخدم"
          v-model="registerationForm.username"
          :rules="[rules.required, rules.min(3), rules.max(25)]"
          outlined
          required
        />

        <!-- Email -->
        <v-text-field
          label="الإيميل"
          v-model="registerationForm.email"
          :rules="[rules.required, rules.email]"
          outlined
          required
        />

        <!-- Password -->
        <v-text-field
          label="كلمة السر"
          v-model="registerationForm.password"
          :rules="[rules.required, rules.min(8), rules.max(50)]"
          type="password"
          outlined
          required
        />

        <!-- Repeat Password -->
        <v-text-field
          label="أعد كتابة كلمة السر"
          v-model="registerationForm.repeatPassword"
          :rules="[
            rules.required,
            rules.min(8),
            rules.max(50),
            rules.passwordsMatch(registerationForm.password),
          ]"
          type="password"
          outlined
          required
        />

        <!-- Terms and Conditions -->
        <div class="my-4">
          <v-checkbox
            v-model="isTheUserAgreeToTermsAndConditions"
            :rules="[rules.required]"
            label="أنا أوافق على الشروط والأحكام"
          />
        </div>

        <!-- Submit Button -->
        <v-btn
          color="primary"
          large
          block
          :disabled="!isTheUserAgreeToTermsAndConditions || isRequestInProgress"
          class="gradient-bg"
          @click="onSubmit"
        >
          <template v-if="isRequestInProgress">
            <v-progress-circular indeterminate color="white" size="16" /> جاري الإرسال
          </template>
          <template v-else>إنشاء حساب</template>
        </v-btn>
      </v-form>
    </v-card>

    <v-dialog v-model="showVerificationDialog" max-width="400" persistent>
      <v-card class="pa-6 text-center">
        <v-icon color="success" size="64" class="mb-4">mdi-email-check</v-icon>
        <h3 class="mb-4">تم إرسال رسالة التحقق</h3>
        <p class="mb-6">يرجى التحقق من بريدك الإلكتروني والنقر على رابط التأكيد</p>
        <v-btn color="primary" block @click="onDialogClose">حسناً</v-btn>
      </v-card>
    </v-dialog>
    
  </v-container>
</template>

<style scoped>
/* Add styles if needed */
</style>
