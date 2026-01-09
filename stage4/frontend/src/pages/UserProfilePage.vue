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
      // Form data
      form: {
        firstname: '',
        lastname: '',
        username: '',
      },
      emailForm: {
        email: '',
      },
      // Validation rules
      rules: {
        required: (value) => !!value || 'هذا الحقل إلزامي',
        minLength: (min) => (value) =>
          (value && value.length >= min) || `أدخل على الأقل ${min} أحرف`,
        maxLength: (max) => (value) =>
          (value && value.length <= max) || `هذا الحقل يجب ألا يتعدى ${max} ��رف`,
        email: (value) => /.+@.+\..+/.test(value) || 'يجب أن يكون الإيميل صالحا',
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

      const valuesToUpdate = {}
      if (this.form.username !== this.user.username) valuesToUpdate.username = this.form.username
      if (this.form.firstname !== this.user.first_name)
        valuesToUpdate.first_name = this.form.firstname
      if (this.form.lastname !== this.user.last_name) valuesToUpdate.last_name = this.form.lastname

      if (Object.keys(valuesToUpdate).length <= 0) return

      try {
        await usersService.updateUser(valuesToUpdate)
        this.userInformationFormSuccessMessage = 'تم تحديث المعلومات بنجاح'
        this.refreshUserData()
      } catch (error) {
        this.userInformationFormErrorMessage = error.message
      }
    },

    async onEmailAdd() {
      if (!this.validateEmailForm()) return

      try {
        await usersService.addEmail(this.emailForm.email)
        this.emailAddError = ''
      } catch (error) {
        this.emailAddError = error.message
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
  },
}
</script>

<template>
  <v-container>
    <div v-if="user">
      <v-row>
        <v-col>
          <v-card>
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

              <v-form @submit.prevent="onUserInformationUpdate">
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
                <v-btn type="submit">تحديث</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card>
            <v-card-title>
              <span>إضافة الإيميل</span>
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="onEmailAdd">
                <v-text-field
                  v-model="emailForm.email"
                  label="الإيميل"
                  :rules="[rules.required, rules.email]"
                />
                <v-btn type="submit">أضف</v-btn>
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
