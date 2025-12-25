<script>
import { Form, Field, ErrorMessage } from 'vee-validate'
import { object, string, ref as yupRef } from 'yup'
export default {
  data() {
    return {
      registerationFormSchema: object({
        firstname: string().required().min(3).max(25),
        lastname: string().required().min(3).max(25),
        username: string().required().min(3).max(25),
        email: string().required().email(),
        password: string().required().min(8).max(50),
        repeatPassword: string()
          .required()
          .min(8)
          .max(50)
          .oneOf([yupRef('password')], 'Passwords dont match'),
      }),
      registerationErrorMessage: '',
      registerationSucccessMessage: '',
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
      this.registerationSucccessMessage = 'Registeratoin done sucessfully'
      this.$router.push('/')
    },
  },
}
</script>
<template>
  <Form @submit="onSubmit" :validation-schema="registerationFormSchema">
    <p v-if="registerationErrorMessage.length">{{ registerationErrorMessage }}</p>
    <p v-if="registerationSucccessMessage.length">{{ registerationSucccessMessage }}</p>
    <label for="firstname">First Name</label>
    <Field name="firstname" />
    <ErrorMessage name="firstname" />
    <label for="lastname">Last Name</label>
    <Field name="lastname" />
    <ErrorMessage name="lastname" />
    <label for="username"> Username</label>
    <Field name="username" />
    <ErrorMessage name="username" />
    <label for="email">Email</label>
    <Field name="email" />
    <ErrorMessage name="email" />
    <label for="password">Password</label>
    <Field name="password" />
    <ErrorMessage name="password" />
    <label for="repeatPassword">Repeat Password</label>
    <Field name="repeatPassword" />
    <ErrorMessage name="repeatPassword" />
    <button type="submit">Register</button>
  </Form>
</template>
