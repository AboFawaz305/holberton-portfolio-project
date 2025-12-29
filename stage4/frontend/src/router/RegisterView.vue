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
      this.registerationSucccessMessage = 'Registeratoin done sucessfully'
      this.$router.push('/')
    },
  },
}
</script>
<template>
  <Form @submit="onSubmit" :validation-schema="registerationFormSchema">
    <h2>New Account Registeration</h2>
    <p v-if="registerationErrorMessage.length">{{ registerationErrorMessage }}</p>
    <p v-if="registerationSucccessMessage.length">{{ registerationSucccessMessage }}</p>
    <label for="firstname">First Name</label>
    <ErrorMessage name="firstname" />
    <Field id="firstname" name="firstname" />
    <label for="lastname">Last Name</label>
    <ErrorMessage name="lastname" />
    <Field id="lastname" name="lastname" />
    <label for="username"> Username</label>
    <ErrorMessage name="username" />
    <Field id="username" name="username" />
    <label for="email">Email</label>
    <ErrorMessage name="email" />
    <Field id="email" name="email" />
    <label for="password">Password</label>
    <ErrorMessage name="password" />
    <Field id="password" name="password" type="password" />
    <label for="repeatPassword">Repeat Password</label>
    <ErrorMessage name="repeatPassword" />
    <Field id="repeatPassword" name="repeatPassword" type="password" />
    <label for="termsAndConditions">
      <input
        id="termsAndConditions"
        name="termsAndConditions"
        v-model="isTheUserAgreeToTermsAndConditions"
        type="checkbox"
      />
      I agree to the terms and conditions.
    </label>
    <button :disabled="!isTheUserAgreeToTermsAndConditions" type="submit">Register</button>
  </Form>
</template>
<style scoped>
* {
  /* border: 1px red solid; */
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
}

form button {
  font-size: 1.25em;
  margin-top: 2rem;
  margin-inline: 12.5%;
  border-radius: 5px;
}

@media screen and (max-width: 586px) {
  form {
    padding-inline: 0;
  }
}
</style>
