<script>
import authService from '@/services/authService' // Import authService for authentication checks
export default {
  data() {
    return { isLoggedIn: false }
  },
  async mounted() {
    await this.checkLogin()
  },
  methods: {
    async checkLogin() {
      this.isLoggedIn = await authService.isLoggedIn()
    },
    logout() {
      authService.logout()
      this.$router.push('/login')
    },
  },
  watch: {
    async $route() {
      await this.checkLogin()
    },
  },
}
</script>
<template>
  <v-app-bar app>
    <v-container>
      <v-row align="center" justify="space-between">
        <!-- Start Side -->
        <div v-if="isLoggedIn">
          <v-menu location="bottom">
            <template v-slot:activator="{ props }">
              <v-btn icon="mdi-account" variant="text" v-bind="props"></v-btn>
            </template>
            <v-btn text v-bind="props" to="/profile">الملف الشخصي</v-btn>
            <v-btn text v-bind="props" @click="logout">تسجيل الخروج</v-btn>
          </v-menu>
        </div>
        <v-btn v-else text to="/login" class="font-weight-bold"> تسجيل الدخول </v-btn>

        <!-- Center Navigation -->
        <v-btn-group>
          <v-btn text to="/#about">
            <v-icon icon="mdi-information" start></v-icon>
            عن أتراب</v-btn
          >
          <v-btn text to="/organizations">
            <v-icon icon="mdi-school" start></v-icon>
            الجامعات
          </v-btn>
        </v-btn-group>

        <!-- End Side -->
        <div></div>
      </v-row>
    </v-container>
  </v-app-bar>
</template>
