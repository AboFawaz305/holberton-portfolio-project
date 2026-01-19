<template>
  <v-footer class="footer">
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
.footer {
  background: #ffffff;
}

.footer__bottom {
  padding-top: 16px;
  padding-bottom: 16px;
}
</style>
