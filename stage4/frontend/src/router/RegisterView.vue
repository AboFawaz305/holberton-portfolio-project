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
    'V-Form': Form,
    'V-Field': Field,
    'V-ErrorMessage': ErrorMessage,
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
        this.registerationErrorMessage = this.$t(error.detail)
        return
      }
      this.registerationErrorMessage = ''
      this.registerationSucccessMessage = 'تم إنشاء الحساب بنجاح'
      setTimeout(() => this.$router.push('/login'), 1000)
    },
  },
}
</script>
<template>
  <div class="container">
    <V-Form @submit="onSubmit" :validation-schema="registerationFormSchema">
      <h2>إنشاء حساب جديد</h2>
      <p v-if="registerationErrorMessage.length">{{ registerationErrorMessage }}</p>
      <p v-if="registerationSucccessMessage.length">{{ registerationSucccessMessage }}</p>
      <label for="firstname">الإسم الأول</label>
      <V-ErrorMessage name="firstname" />
      <V-Field id="firstname" name="firstname" />
      <label for="lastname">الإسم الأخير</label>
      <V-ErrorMessage name="lastname" />
      <V-Field id="lastname" name="lastname" />
      <label for="username">إسم المستخدم</label>
      <V-ErrorMessage name="username" />
      <V-Field id="username" name="username" />
      <label for="email">الإيميل</label>
      <V-ErrorMessage name="email" />
      <V-Field id="email" name="email" />
      <label for="password">كلمة السر</label>
      <V-ErrorMessage name="password" />
      <V-Field id="password" name="password" type="password" />
      <label for="repeatPassword">أعد كتابة كلمة السر</label>
      <V-ErrorMessage name="repeatPassword" />
      <V-Field id="repeatPassword" name="repeatPassword" type="password" />
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
    </V-Form>
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
  background: hsla(188, 40%, 61%, 1);
  background: linear-gradient(90deg, hsla(188, 40%, 61%, 1) 0%, hsla(192, 95%, 32%, 1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

h2 {
  text-align: center;
}

form {
  margin: auto;
  display: flex;
  flex-direction: column;
  box-shadow: 0px 4px 6px black;
  max-width: 486px;
  padding: 5em;
  gap: 0.5em;
  border-radius: 25px;
  flex: 1;
  background-color: #e2e2e2;
}

button[disabled] {
  opacity: 60%;
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
  border: none;
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

<i18n>
{
  ar: {
    USER_ALREADY_EXIST: "المستخدم موجود مسبقا"
  }
}
</i18n>
