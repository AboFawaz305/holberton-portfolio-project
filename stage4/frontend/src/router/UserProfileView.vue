<script>
import { Form, Field, ErrorMessage } from 'vee-validate'
import { object, string } from 'yup'
import { nextTick } from 'vue'

export default {
  data() {
    return {
      user: null,
      error: '',
      userInformationFormErrorMessage: '',
      userInformationFormSucccessMessage: '',
      userInformationFormSchema: object({
        firstname: string()
          .required('هذا الحقل إلزامي')
          .min(3, 'أدخل على الأقل ٣ أحرف')
          .max(25, 'هذا الحقل يجب ألا يتعدى ٢٥ حرف'),
        lastname: string()
          .required('هذا الحقل إلزامي')
          .min(3, 'أدخل على الأقل ٣ أحرف')
          .max(25, 'هذا الحقل يجب ألا يتعدى ٢٥ حرف'),
        username: string()
          .required('هذا الحقل إلزامي')
          .min(3, 'أدخل على الأقل ٣ أحرف')
          .max(25, 'هذا الحقل يجب ألا يتعدى ٢٥ حرف'),
        // email: string().required('هذا الحقل إلزامي').email('يجب أن يكون الإيميل صالحا'),
        // password: string()
        //   .required('هذا الحقل إلزامي')
        //   .min(8, 'أدخل على الأقل ٨ أحرف')
        //   .max(50, 'هذا الحقل يجب ألا يتعدى ٥٠ حرف'),
        // repeatPassword: string()
        //   .required('هذا الحقل إلزامي')
        //   .min(8, 'أدخل على الأقل ٨ أحرف')
        //   .max(50, 'هذا الحقل يجب ألا يتعدى ٥٠ حرف')
        //   .oneOf([yupRef('password')], 'كلمات السر لا تتطابق'),
      }),
      addEmailFormSchema: object({
        email: string().required('هذا الحقل إلزامي').email('يجب أن يكون الإيميل صالحا'),
      }),
      emailAddError: '',
    }
  },
  components: {
    'V-Form': Form,
    'V-Field': Field,
    'V-ErrorMessage': ErrorMessage,
  },
  async mounted() {
    const me = await fetch('/api/me', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })
    if (!me.ok) {
      this.error = 'حدث خطأ أثناء جلب بيانات المستخدم'
      return
    }
    this.user = await me.json()
    await nextTick()
    console.log(this.$refs)
    this.$refs.userInformationForm.setValues({
      firstname: this.user.first_name,
      lastname: this.user.last_name,
      username: this.user.username,
    })
  },
  methods: {
    async onUserInformationUpdate(values) {
      const values_to_update = {}
      if (values.username !== this.user.username) values_to_update.username = values.username
      if (values.firstname !== this.user.first_name) values_to_update.first_name = values.firstname
      if (values.lastname !== this.user.last_name) values_to_update.last_name = values.lastname
      console.log(values_to_update)
      if (Object.keys(values_to_update).length <= 0) return
      const response = await fetch('/api/users', {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values_to_update),
      })
      if (!response.ok) {
        const error = await response.json()
        console.log(error)
        this.userInformationFormErrorMessage = error.detail
        this.$refs.userInformationForm.setValues({
          firstname: this.user.first_name,
          lastname: this.user.last_name,
          username: this.user.username,
        })
        return
      }
      this.userInformationFormSucccessMessage = 'تم تحديث المعلومات بنجاح'
      const me = await fetch('/api/me', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      if (!me.ok) {
        this.error = 'حدث خطأ أثناء جلب بيانات المستخدم'
        return
      }
      this.user = await me.json()
      this.$refs.userInformationForm.setValues({
        firstname: this.user.first_name,
        lastname: this.user.last_name,
        username: this.user.username,
      })
    },

    async onEmailAdd({ email }) {
      this.emailAddError = ''
      const response = await fetch('/api/users/emails', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
      })
      if (!response.ok) {
        const error = await response.json()
        this.emailAddError = error.detail
        return
      }
    },
  },
}
</script>
<template>
  <div v-if="user">
    <div id="banner">
      <router-link to="/">الصفحة الرئيسية</router-link>
      <h1>{{ user.first_name + ' ' + user.last_name }}</h1>
    </div>
    <span v-if="error.length">{{ error }}</span>
    <div id="user-information-card">
      <V-Form
        @submit="onUserInformationUpdate"
        :validation-schema="userInformationFormSchema"
        ref="userInformationForm"
      >
        <h2>المعلومات الشخصية</h2>
        <p v-if="userInformationFormErrorMessage.length">{{ userInformationFormErrorMessage }}</p>
        <p v-if="userInformationFormSucccessMessage.length">
          {{ userInformationFormSucccessMessage }}
        </p>
        <label for="firstname">الإسم الأول</label>
        <V-ErrorMessage name="firstname" />
        <V-Field id="firstname" name="firstname" />
        <label for="lastname">الإسم الأخير</label>
        <V-ErrorMessage name="lastname" />
        <V-Field id="lastname" name="lastname" />
        <label for="username">إسم المستخدم</label>
        <V-ErrorMessage name="username" />
        <V-Field id="username" name="username" />
        <button type="submit">تحديث</button>
      </V-Form>
      <div id="emails-card">
        <div class="email-field" v-for="(email, index) in user.email" :key="index">
          <span>X</span>
          <span>{{ email }}</span>
          <span>Resest</span>
        </div>
        <V-Form @submit="onEmailAdd" :validation-schema="addEmailFormSchema">
          <span v-if="emailAddError.length">{{ emailAddError }}</span>
          <label for="email">الإيميل</label>
          <V-ErrorMessage name="email" />
          <V-Field id="email" name="email" />
          <button type="submit">أضف</button>
        </V-Form>
      </div>
    </div>
  </div>
  <div v-else>
    <span>يتم تحميل الصفحة</span>
  </div>
</template>
