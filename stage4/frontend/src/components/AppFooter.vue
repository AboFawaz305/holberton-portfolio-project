<template>
  <v-footer class="footer py-6">
    <v-container>
      <v-row class="footer__bottom justify-center align-center">
        <span class="text-body-2 text-grey-darken-1">
          © {{ year }} أتراب. جميع الحقوق محفوظة.
        </span>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>

<style scoped>
.footer__bottom {
  border-top: 1px solid #eef2f7;
  padding-top: 16px;
}
</style>
