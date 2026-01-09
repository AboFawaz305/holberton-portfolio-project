<template>
  <v-container class="cta text-center">
    <!-- Title -->
    <h2 class="text-h4 font-weight-bold mb-4">جاهز للبدء؟</h2>

    <!-- Subtitle -->
    <p class="text-subtitle-1 mb-8">انضم إلى آلاف الطلاب الذين يستفيدون من أتراب كل يوم</p>

    <!-- Call-to-Action Button -->
    <v-btn large color="light" class="px-8 text-grey-darken-4 font-weight-bold"> سجّل الآن </v-btn>
  </v-container>
</template>

<script setup></script>

<style scoped>
.cta {
  background: linear-gradient(
    180deg,
    #3b90a0,
    #2f7f90
  ); /* Gradient background for the CTA section */
  color: #ffffff; /* Light text color for accessibility */
  min-width: 100%;
}
</style>
