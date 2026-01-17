<script>
import authService from '@/services/authService' // Import the authService

export default {
  data() {
    return {
      showPassword: false,
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
      this.registerationErrorMessage = ''
      this.registerationSucccessMessage = ''

      const { valid } = await this.$refs.registerationForm.validate()
      if (!valid) return

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
        const errorMap = {
          USER_ALREADY_EXIST: 'اسم المستخدم أو البريد الإلكتروني مسجل مسبقاً',
          'Registration failed': 'فشل الاتصال بالخادم، يرجى المحاولة لاحقاً',
        }

        this.registerationErrorMessage =
          errorMap[error.message] || 'الرجاء التحقق من المعلومات المدخلة'
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
  <v-container fluid class="fill-height auth-bg py-10">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="5">
        <v-card rounded="xl" elevation="8" class="pa-8">
          <div class="text-center mb-10">
            <v-avatar color="primary-lighten-5" size="80" class="mb-4">
              <v-icon color="primary" size="40">mdi-account-plus-outline</v-icon>
            </v-avatar>
            <h1 class="text-h4 font-weight-bold mb-2">إنشاء حساب جديد</h1>
            <p class="text-body-1 text-grey-darken-1">أدخل بياناتك للانضمام إلينا</p>
          </div>

          <v-form ref="registerationForm">
            <v-expand-transition>
              <v-alert
                v-if="registerationErrorMessage"
                type="error"
                variant="tonal"
                rounded="lg"
                class="mb-6"
                closable
                @click:close="registerationErrorMessage = ''"
              >
                {{ registerationErrorMessage }}
              </v-alert>
            </v-expand-transition>

            <v-expand-transition>
              <v-alert
                v-if="registerationSucccessMessage"
                type="success"
                variant="tonal"
                rounded="lg"
                class="mb-6"
                @click:close="registerationSucccessMessage = ''"
              >
                {{ registerationSucccessMessage }}
              </v-alert>
            </v-expand-transition>

            <v-row dense class="mb-2">
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="registerationForm.firstname"
                  :rules="[rules.required, rules.min(3), rules.max(25)]"
                  label="الإسم الأول"
                  variant="outlined"
                  rounded="lg"
                  color="primary"
                  prepend-inner-icon="mdi-account-outline"
                  required
                  class="mb-2"
                />
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="registerationForm.lastname"
                  :rules="[rules.required, rules.min(3), rules.max(25)]"
                  label="الإسم الأخير"
                  variant="outlined"
                  rounded="lg"
                  color="primary"
                  required
                  class="mb-2"
                />
              </v-col>
            </v-row>

            <v-text-field
              v-model="registerationForm.username"
              :rules="[rules.required, rules.min(3), rules.max(25)]"
              label="إسم المستخدم"
              variant="outlined"
              rounded="lg"
              color="primary"
              prepend-inner-icon="mdi-at"
              required
              class="mb-4"
            />

            <v-text-field
              v-model="registerationForm.email"
              :rules="[rules.required, rules.email]"
              label="البريد الإلكتروني"
              variant="outlined"
              rounded="lg"
              color="primary"
              prepend-inner-icon="mdi-email-outline"
              required
              class="mb-4"
            />

            <v-text-field
              v-model="registerationForm.password"
              :rules="[rules.required, rules.min(8), rules.max(50)]"
              label="كلمة السر"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
              rounded="lg"
              color="primary"
              prepend-inner-icon="mdi-lock-outline"
              class="mb-4"
            >
              <template #append-inner>
                <v-btn variant="text" icon tabindex="-1" @click="showPassword = !showPassword">
                  <v-icon color="grey-darken-1">
                    {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
                  </v-icon>
                </v-btn>
              </template>
            </v-text-field>

            <v-text-field
              v-model="registerationForm.repeatPassword"
              :rules="[
                rules.required,
                rules.min(8),
                rules.max(50),
                rules.passwordsMatch(registerationForm.password),
              ]"
              label="تأكيد كلمة السر"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
              rounded="lg"
              color="primary"
              prepend-inner-icon="mdi-lock-check-outline"
              class="mb-2"
            >
              <template #append-inner>
                <v-btn variant="text" icon tabindex="-1" @click="showPassword = !showPassword">
                  <v-icon color="grey-darken-1">
                    {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
                  </v-icon>
                </v-btn>
              </template>
            </v-text-field>

            <div class="mb-2">
              <v-checkbox
                v-model="isTheUserAgreeToTermsAndConditions"
                :rules="[rules.required]"
                color="primary"
                hide-details
              >
                <template v-slot:label>
                  <div class="text-body-2">أوافق على الشروط والأحكام</div>
                </template>
              </v-checkbox>
            </div>

            <v-btn
              color="primary"
              size="large"
              block
              rounded="lg"
              elevation="2"
              class="mt-4 font-weight-bold py-7 text-h6 gradient-bg"
              :disabled="!isTheUserAgreeToTermsAndConditions || isRequestInProgress"
              @click="onSubmit"
            >
              <template v-if="isRequestInProgress">
                <v-progress-circular indeterminate color="white" size="20" class="me-2" />
                جاري الإرسال...
              </template>
              <template v-else>إنشاء حساب</template>
            </v-btn>

            <div class="text-center mt-8 text-body-2 text-grey-darken-1">
              لديك حساب بالفعل؟
              <v-btn variant="text" color="primary" to="/login" class="px-1 font-weight-bold">
                تسجيل الدخول
              </v-btn>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showVerificationDialog" max-width="450" persistent>
      <v-card class="pa-8 text-center" rounded="xl">
        <v-avatar color="success-lighten-5" size="90" class="mb-6">
          <v-icon color="success" size="50">mdi-email-check-outline</v-icon>
        </v-avatar>
        <h3 class="text-h5 font-weight-bold mb-4">تم إرسال رسالة التحقق</h3>
        <p class="text-body-1 text-grey-darken-1 mb-8">
          يرجى التحقق من بريدك الإلكتروني والنقر على رابط التأكيد لتنشيط حسابك.
        </p>
        <v-btn color="primary" block size="large" rounded="lg" @click="onDialogClose">
          حسناً
        </v-btn>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.auth-bg {
  background-color: #f8fafd;
}

.v-card {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05) !important;
}
</style>
