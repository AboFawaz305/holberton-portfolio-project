<script>
import { Form, Field, ErrorMessage } from 'vee-validate'
import { object, string, ref as yupRef } from 'yup'
export default {
  data() {
    return {
      registerationFormSchema: object({
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
        email: string().required('هذا الحقل إلزامي').email('يجب أن يكون الإيميل صالحا'),
        password: string()
          .required('هذا الحقل إلزامي')
          .min(8, 'أدخل على الأقل ٨ أحرف')
          .max(50, 'هذا الحقل يجب ألا يتعدى ٥٠ حرف'),
        repeatPassword: string()
          .required('هذا الحقل إلزامي')
          .min(8, 'أدخل على الأقل ٨ أحرف')
          .max(50, 'هذا الحقل يجب ألا يتعدى ٥٠ حرف')
          .oneOf([yupRef('password')], 'كلمات السر لا تتطابق'),
      }),
      registerationErrorMessage: '',
      registerationSucccessMessage: '',
      isTheUserAgreeToTermsAndConditions: false,
    }
  },
  components: {
    Form,
    Field,
    ErrorMessage,
  },
  methods: {
    async onSubmit(values) {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          first_name: values.firstname,
          last_name: values.lastname,
          username: values.username,
          email: values.email,
          password: values.password,
        }),
      })
      if (!response.ok) {
        const error = await response.json()
        this.registerationSucccessMessage = ''
        this.registerationErrorMessage = error.detail
        return
      }
      this.registerationErrorMessage = ''
      this.registerationSucccessMessage = 'تم إنشاء الحساب بنجاح'
      this.$router.push('/')
    },
  },
}
</script>
<template>
  <div class="container">
    <Form @submit="onSubmit" :validation-schema="registerationFormSchema">
      <h2>إنشاء حساب جديد</h2>
      <p v-if="registerationErrorMessage.length">{{ registerationErrorMessage }}</p>
      <p v-if="registerationSucccessMessage.length">{{ registerationSucccessMessage }}</p>
      <label for="firstname">الإسم الأول</label>
      <ErrorMessage name="firstname" />
      <Field id="firstname" name="firstname" />
      <label for="lastname">الإسم الأخير</label>
      <ErrorMessage name="lastname" />
      <Field id="lastname" name="lastname" />
      <label for="username">إسم المستخدم</label>
      <ErrorMessage name="username" />
      <Field id="username" name="username" />
      <label for="email">الإيميل</label>
      <ErrorMessage name="email" />
      <Field id="email" name="email" />
      <label for="password">كلمة السر</label>
      <ErrorMessage name="password" />
      <Field id="password" name="password" type="password" />
      <label for="repeatPassword">أعد كتابة كلمة السر</label>
      <ErrorMessage name="repeatPassword" />
      <Field id="repeatPassword" name="repeatPassword" type="password" />
      <label for="termsAndConditions">
        <input
          id="termsAndConditions"
          name="termsAndConditions"
          v-model="isTheUserAgreeToTermsAndConditions"
          type="checkbox"
        />
        أنا أوافق على الشروط والأحكام
      </label>
      <button :disabled="!isTheUserAgreeToTermsAndConditions" type="submit">إنشاء حساب</button>
    </Form>
  </div>
</template>
<style scoped lang="scss">
:root {
}
* {
  /* border: 1px red solid; */
}
.container {
  background-color: #5dadbb;
}

h2 {
  text-align: center;
}

form {
  margin: auto;
  display: flex;
  flex-direction: column;
  max-width: 486px;
  padding: 5em;
  gap: 0.5em;
  border-radius: 25px;
  background-color: #e2e2e2;
}

label {
  font-weight: bolder;
}

input {
  margin-bottom: 1em;
  font-size: inherit;
  color: inherit;
  padding: 0.5em;
  border-radius: 5px;
  border-color: linear-gradient(90deg, rgba(24, 137, 165, 1) 0%, rgba(97, 175, 188, 1) 100%);
}

form button {
  font-size: 1.25em;
  margin-top: 2rem;
  margin-inline: 12.5%;
  border-radius: 5px;
  background: #57a8bb;
  background: linear-gradient(90deg, rgba(87, 168, 187, 1) 0%, rgba(40, 76, 85, 1) 100%);
  color: white;
}

span[role='alert'] {
  color: red;
}

@media screen and (max-width: 586px) {
  form {
    padding-inline: 0;
  }
}
</style>
