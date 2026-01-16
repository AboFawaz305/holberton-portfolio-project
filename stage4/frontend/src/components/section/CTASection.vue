<template>
  <v-container fluid class="cta text-center">
    <!-- Title -->
    <h2 class="text-h4 font-weight-bold mb-4">جاهز للبدء؟</h2>

    <!-- Subtitle -->
    <p class="text-subtitle-1 mb-8">انضم إلى آلاف الطلاب الذين يستفيدون من أتراب كل يوم</p>

    <!-- Call-to-Action Button -->
    <v-btn size="large" class="px-8 font-weight-bold cta-btn" elevation="4" to="/register">
      سجّل الآن
    </v-btn>
  </v-container>
</template>

<script setup></script>

<style scoped>
.cta {
  width: 100%;
  padding: 80px 24px;

  /* التدرج من فوق لتحت */
  background: linear-gradient(to bottom, #04809f 0%, #3f9fb2 50%, #75b9c4 100%);

  color: #ffffff;
}

/* زر أبيض مثل الصورة */
.cta-btn {
  background-color: #ffffff;
  color: #04809f;
  border-radius: 12px;
}
</style>
