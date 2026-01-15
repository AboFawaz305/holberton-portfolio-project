<script>
import authService from '@/services/authService'

export default {
  data() {
    return {
      isLoading: true,
      success: false,
      errorMessage: '',
    }
  },
  async mounted() {
    const token = this.$route.params.token
    if (!token) {
      this.errorMessage = 'رابط غير صالح'
      this.isLoading = false
      return
    }

    try {
      await authService.verifyEmail(token)
      this.success = true
    } catch (error) {
      this.errorMessage = 'رابط التحقق غير صالح أو منتهي'
      console.log(`${error}`)
    } finally {
      this.isLoading = false
    }
  },
  methods: {
    goToLogin() {
      this.$router.push('/login')
    },
  },
}
</script>

<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card class="pa-8 text-center" max-width="400">
      <!-- Loading -->
      <template v-if="isLoading">
        <v-progress-circular indeterminate color="primary" size="64" />
        <p class="mt-4">جاري التحقق...</p>
      </template>

      <!-- Success -->
      <template v-else-if="success">
        <v-icon color="success" size="64">mdi-check-circle</v-icon>
        <h3 class="mt-4 mb-6">تم التحقق بنجاح!</h3>
        <v-btn color="primary" block @click="goToLogin">تسجيل الدخول</v-btn>
      </template>

      <!-- Error -->
      <template v-else>
        <v-icon color="error" size="64">mdi-close-circle</v-icon>
        <h3 class="mt-4 mb-2">فشل التحقق</h3>
        <p class="mb-6">{{ errorMessage }}</p>
        <v-btn color="primary" block @click="goToLogin">العودة</v-btn>
      </template>
    </v-card>
  </v-container>
</template>
