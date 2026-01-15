<script>
import authService from '@/services/authService'
import usersService from '@/services/usersService'

export default {
  data() {
    return {
      user: null,
      error: '',
      userInformationFormErrorMessage: '',
      userInformationFormSuccessMessage: '',
      emailAddError: '',
      emailAddSuccess: '',
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
      passwordResetFormError: '',
      passwordResetFormSuccess: '',
      // Validation rules
      rules: {
        required: (value) => !!value || 'هذا الحقل إلزامي',
        minLength: (min) => (value) =>
          (value && value.length >= min) || `أدخل على الأقل ${min} أحرف`,
        maxLength: (max) => (value) =>
          (value && value.length <= max) || `هذا الحقل يجب ألا يتعدى ${max} ��رف`,
        email: (value) => /.+@.+\..+/.test(value) || 'يجب أن يكون الإيميل صالحا',
        passwordsMatch: (confirmPassword) => (value) =>
          confirmPassword === value || 'كلمات السر لا تتطابق',
      },
    }
  },
  async mounted() {
    try {
      this.user = await authService.getCurrentUser()
      this.form.firstname = this.user.first_name
      this.form.lastname = this.user.last_name
      this.form.username = this.user.username
    } catch (error) {
      this.error = error.message
    }
  },
  methods: {
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
        this.userInformationFormErrorMessage = ''
        this.userInformationFormSuccessMessage = 'تم تحديث المعلومات بنجاح'
        this.$refs.userInfoForm.reset()
        this.refreshUserData()
      } catch (error) {
        this.userInformationFormSuccessMessage = ''
        this.userInformationFormErrorMessage = error.message
      }
    },

    async onEmailAdd() {
      if (!this.validateEmailForm()) return

      try {
        await usersService.addEmail(this.emailForm.email)
        this.emailAddError = ''
        this.emailAddSuccess = 'تمت إضافة الإيميل بنجاح' + ` ${this.emailForm.email}`
        this.emailForm.email = ''
        this.$refs.emailAddForm.reset()
        this.refreshUserData()
      } catch (error) {
        this.emailAddSuccess = ''
        this.emailAddError = error.message
      }
    },

    async deleteEmail(email_id) {
      try {
        if (this.user.email.length <= 1) {
          this.emailAddError = 'لا تستطيع حذف أخر إيميل لديك'
          return
        }
        const emailStr = this.user.email[email_id].value
        await usersService.deleteEmail(email_id)
        this.emailAddError = ''
        this.emailAddSuccess = 'تم حذف تاإيميل ' + emailStr + ' بنجاح'
        this.refreshUserData()
      } catch (error) {
        this.emailAddSuccess = ''
        this.emailAddError = error.message
      }
    },
    async onPasswordReset() {
      if (!this.validatePasswordResetForm()) return

      const valuestoupdate = {}
      if (this.passwordResetForm.password !== '')
        valuestoupdate.password = this.passwordResetForm.password

      try {
        await usersService.updateUser(valuestoupdate)
        this.passwordResetFormSuccess = 'تم تحديث كلمة السر بنجاح'
        this.$refs.passwordResetForm.reset()
      } catch (error) {
        this.passwordResetFormError = error.message
      }
    },

    async refreshUserData() {
      try {
        this.user = await authService.getCurrentUser()
        this.form.firstname = this.user.first_name
        this.form.lastname = this.user.last_name
        this.form.username = this.user.username
      } catch (error) {
        this.error = error.message
      }
    },

    // Form validation using Vuetify's rules
    validateUserInformationForm() {
      const rules = this.rules
      if (
        !rules.required(this.form.firstname) ||
        !rules.minLength(3)(this.form.firstname) ||
        !rules.maxLength(25)(this.form.firstname) ||
        !rules.required(this.form.lastname) ||
        !rules.minLength(3)(this.form.lastname) ||
        !rules.maxLength(25)(this.form.lastname) ||
        !rules.required(this.form.username) ||
        !rules.minLength(3)(this.form.username) ||
        !rules.maxLength(25)(this.form.username)
      ) {
        this.userInformationFormErrorMessage = 'يرجى التأكد من إدخال جميع الحقول بشكل صحيح'
        return false
      }
      return true
    },

    validateEmailForm() {
      const rules = this.rules
      if (!rules.required(this.emailForm.email) || !rules.email(this.emailForm.email)) {
        this.emailAddError = 'يرجى إدخال بريد إلكتروني صالح'
        return false
      }
      return true
    },
    validatePasswordResetForm() {
      const rules = this.rules
      if (
        !rules.required(this.passwordResetForm.password) ||
        !rules.minLength(8)(this.passwordResetForm.password) ||
        !rules.maxLength(50)(this.passwordResetForm.pasword) ||
        this.passwordResetForm.password !== this.passwordResetForm.repeatPassword
      ) {
        this.passwordResetFormError = 'كلمة السر غير صالحة'
        return false
      }
      return true
    },
  },
}
</script>

<template>
  <v-container>
    <div v-if="user">
      <v-row>
        <v-col>
          <v-card outline>
            <v-card-title>
              <span>المعلومات الشخصية</span>
            </v-card-title>
            <v-card-text>
              <v-alert type="error" v-if="userInformationFormErrorMessage.length">
                {{ userInformationFormErrorMessage }}
              </v-alert>
              <v-alert type="success" v-if="userInformationFormSuccessMessage.length">
                {{ userInformationFormSuccessMessage }}
              </v-alert>

              <v-form @submit.prevent="onUserInformationUpdate" ref="userInfoForm">
                <v-text-field
                  v-model="form.firstname"
                  label="الإسم الأول"
                  :rules="[rules.required, rules.minLength(3), rules.maxLength(25)]"
                />
                <v-text-field
                  v-model="form.lastname"
                  label="الإسم الأخير"
                  :rules="[rules.required, rules.minLength(3), rules.maxLength(25)]"
                />
                <v-text-field
                  v-model="form.username"
                  label="إسم المستخدم"
                  :rules="[rules.required, rules.minLength(3), rules.maxLength(25)]"
                />
                <v-btn color="primary" type="submit">تحديث</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card outline>
            <v-card-title>
              <span>الإيميلات</span>
            </v-card-title>
            <v-card-text>
              <v-alert type="error" v-if="emailAddError.length">{{ emailAddError }}</v-alert>
              <v-alert type="success" v-if="emailAddSuccess.length">{{ emailAddSuccess }}</v-alert>
              <v-list>
                <v-list-item v-for="(emailObj, i) in user.email" :key="i">
                  <v-btn
                    icon="mdi-delete"
                    @click="deleteEmail(i)"
                    color="error"
                    size="small"
                    class="me-2"
                  ></v-btn>

                  {{ emailObj.value }}

                  <v-chip
                    size="x-small"
                    :color="emailObj.is_verified ? 'success' : 'warning'"
                    class="ms-2"
                  >
                    {{ emailObj.is_verified ? 'موثق' : 'غير موثق' }}
                  </v-chip>
                </v-list-item>
              </v-list>
              <v-form @submit.prevent="onEmailAdd" ref="emailAddForm">
                <v-text-field
                  v-model="emailForm.email"
                  label="الإيميل"
                  :rules="[rules.required, rules.email]"
                />
                <v-btn color="primary" type="submit">أضف</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card outline>
            <v-card-title>تغيير كلمة السر</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="onPasswordReset" ref="passwordResetForm">
                <v-alert type="error" v-if="passwordResetFormError.length">{{
                  passwordResetFormError
                }}</v-alert>
                <v-alert type="success" v-if="passwordResetFormSuccess.length">{{
                  passwordResetFormSuccess
                }}</v-alert>
                <v-text-field
                  v-model="passwordResetForm.password"
                  type="password"
                  label="كلمة السر"
                  :rules="[rules.required, rules.minLength(8), rules.maxLength(50)]"
                />
                <v-text-field
                  v-model="passwordResetForm.repeatPassword"
                  type="password"
                  label="أعد كلمة السر"
                  :rules="[
                    rules.required,
                    rules.minLength(8),
                    rules.maxLength(50),
                    rules.passwordsMatch(passwordResetForm.password),
                  ]"
                />
                <v-btn color="primary" type="submit">حدث كلمة السر</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div v-else>
      <span>يتم تحميل الصفحة</span>
    </div>
  </v-container>
</template>
