<script>
import { Form, Field, ErrorMessage } from 'vee-validate'
import { object, string } from 'yup'
export default {
  data() {
    return {
      loginFormSchema: object({
        username: string()
          .required('هذا الحقل الزامي')
          .min(3, 'لا يمكن  ان يكون اقل من 3 احرف')
          .max(25, 'يجب ان لا يكون اكثر من 25 حرفا'),
        password: string()
          .required('هذا الحقل الزامي')
          .min(8, ' لا يمكن ان يكون اقل من 8 احرف')
          .max(50, 'يجب ان لا يكون اكثر من 50 حرفا'),
      }),
      loginErrorMessage: '',
      loginSucccessMessage: '',
    }
  },
  components: {
    'V-Form': Form,
    'V-Field': Field,
    'V-ErrorMessage': ErrorMessage,
  },
  methods: {
    async onSubmit(values) {
      const formData = new FormData()
      formData.append('username', values.username)
      formData.append('password', values.password)

      const response = await fetch('/api/login', {
        method: 'POST',
        body: formData,
      })

      const error = await response.json()
      if (!response.ok) {
        console.log(error.detail)
        this.loginSucccessMessage = ''
        this.loginErrorMessage = 'خطا ' + this.$t(error.detail)
        return
      }

      const token = await response.json()

      localStorage.setItem('token', token.access_token)
      this.loginErrorMessage = ''
      this.loginSucccessMessage = 'تم تسجيل الدخل بنجاح'
      setTimeout(() => this.$router.push('/'), 1000)
    },
  },
  i18n: {
    messages: {
      ar: {
        INVALID_USERNAME: 'إسم المستخدم غير صالح',
        INVALID_PASSWORD: 'كلمة السر غير صالحة',
      },
    },
  },
}
</script>
<template>
  <div class="contanor">
    <V-Form @submit="onSubmit" :validation-schema="loginFormSchema">
      <h1>تسجيل الدخول</h1>
      <p v-if="loginErrorMessage.length" class="error">{{ loginErrorMessage }}</p>
      <p v-if="loginSucccessMessage.length">{{ loginSucccessMessage }}</p>

      <label for="username"> اسم المستخدم </label>
      <V-ErrorMessage class="error" name="username" />
      <V-Field name="username" />

      <label for="password">كلمة المرور</label>
      <V-ErrorMessage class="error" name="password" />
      <V-Field name="password" type="password" />
      <div class="forgot">
        <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"> هل نسيت كلمة المرور؟ </a>
      </div>

      <button type="submit">تسيجل الدخول</button>

      <div class="noAccount">
        <RouterLink to="/register">ليس لديك حساب ؟ أنشاء حساب</RouterLink>
      </div>
    </V-Form>
  </div>
</template>
<style scoped>
.contanor {
  min-height: 100%;
  background: hsla(188, 40%, 61%, 1);
  background: linear-gradient(90deg, hsla(188, 40%, 61%, 1) 0%, hsla(192, 95%, 32%, 1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.forgot {
  display: flex;
  justify-content: flex-end;
}
.noAccount {
  font-weight: bolder;
  display: flex;
  justify-content: center;
}
h1 {
  text-align: center;
}
.error {
  color: red;
}
form {
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
  gap: 10px;
  border-radius: 15px;
  border: 1px solid #5dadbb;
  padding: 2.5em;
  box-shadow: 0px 4px 6px black;
  background-color: #e2e2e2;
  flex: 1;
  max-width: 400px;
}
label {
  font-size: 1.5em;
  font-weight: bolder;
}
input {
  margin-bottom: 2em;
  padding: 0.5em;
  border-radius: 5px;
  border: 2px solid #5dadbb;
}

form button {
  color: white;
  font-size: 1.25em;
  margin-top: 2rem;
  margin-inline: 12.5%;
  border-radius: 5px;
  border: 2px solid #5dadbb;
  background-image: linear-gradient(to right, #5dadbb, #294f58);
}
</style>

<i18n>
{
  "ar": {
    "INVALID_USERNAME": "إسم المستخدم غير صالح",
    "INVALID_PASSWORD": "كلمة السر غير صالحة"
  }
}
</i18n>
