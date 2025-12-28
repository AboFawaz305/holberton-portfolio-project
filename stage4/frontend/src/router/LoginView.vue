<script>
import { Form, Field, ErrorMessage } from 'vee-validate'
import { object, string } from 'yup'
export default {
  data() {
    return {
      loginFormSchema: object({
        username: string().required().min(3).max(25),
        password: string().required().min(8).max(50),
      }),
      loginErrorMessage: '',
      loginSucccessMessage: '',
    }
  },
  components: {
    Form,
    Field,
    ErrorMessage,
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

      if (!response.ok) {
        const error = await response.json()
        this.loginSucccessMessage = ''
        this.loginErrorMessage = error.detail
        return
      }

      const token = await response.json()

      localStorage.setItem('token', token.access_token)
      this.loginErrorMessage = ''
      this.loginSucccessMessage = 'Login done sucessfully'
      this.$router.push('/')
    },
  },
}
</script>
<template>
  <Form @submit="onSubmit" :validation-schema="loginFormSchema">
    <p v-if="loginErrorMessage.length">{{ loginErrorMessage }}</p>
    <p v-if="loginSucccessMessage.length">{{ loginSucccessMessage }}</p>

    <label for="username"> Username</label>
    <Field name="username" />
    <ErrorMessage name="username" />

    <label for="password">Password</label>
    <Field name="password" type="password" />
    <ErrorMessage name="password" />
    <button type="submit">Login</button>
  </Form>
</template>
