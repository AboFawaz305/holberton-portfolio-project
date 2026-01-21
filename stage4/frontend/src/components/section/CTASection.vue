<template>
  <div class="cta-vibrant-bg section-padding text-center text-white">
    <v-container data-aos="zoom-in">
      <h2 class="text-h2 font-weight-black mb-6">جاهز للتفوق مع زملائك؟</h2>
      <p class="text-h6 mb-10 opacity-90">انضم اليوم إلى آلاف الطلاب في مجتمع أتراب الأكاديمي</p>
      <v-btn
        to="/register"
        size="x-large"
        color="white"
        class="px-12 font-weight-black text-primary rounded-xl"
        style="z-index: 20; position: relative"
        height="64"
        elevation="10"
      >
        سجل الآن
      </v-btn>
    </v-container>
  </div>
</template>

<style scoped>
.cta-vibrant-bg {
  background: linear-gradient(135deg, #04809f 0%, #3f9fb2 50%, #75b9c4 100%);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.cta-vibrant-bg::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7z' fill='%23ffffff' fill-opacity='0.05'/%3E%3C/svg%3E");

  pointer-events: none;
  z-index: 0;
}

.v-container {
  position: relative;
  z-index: 2;
}
</style>
