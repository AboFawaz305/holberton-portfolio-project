<template>
  <v-footer class="footer-wrapper pa-0">
    <div class="footer-top-line"></div>

    <v-container class="py-16">
      <v-row justify="center" class="text-center">
        <v-col cols="12" md="10" lg="8">
          <div class="footer-logo mb-6" data-aos="fade-up">
            <span class="logo-text vibrant-gradient-text">أتراب</span>
          </div>

          <p
            class="text-h8 text-grey-darken-2 font-weight-regular lh-relaxed mb-10 px-md-16"
            data-aos="fade-up"
          >
            منصة أكاديمية تجمع طلاب الجامعات السعودية في مكان واحد لمشاركة المعرفة والتفوق معاً.
          </p>

          <div
            class="footer-nav d-flex flex-wrap justify-center align-center gap-8 mb-8"
            data-aos="fade-up"
          >
            <a href="/organizations" class="nav-link">الجامعات</a>
            <a href="/terms" class="nav-link">الشروط و الاحكام</a>
            <a href="#" class="nav-link">اتصل بنا</a>
          </div>

          <v-divider class="mb-8 opacity-10"></v-divider>

          <p class="text-caption text-grey-darken-1 font-weight-bold">
            © {{ year }} أتراب. جميع الحقوق محفوظة.
          </p>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup>
const year = new Date().getFullYear()
const socialIcons = ['mdi-twitter', 'mdi-instagram', 'mdi-linkedin', 'mdi-github']
</script>

<style scoped>
/* 1. The Simple Background - A soft, solid teal tint */
.footer-wrapper {
  background-color: #f5fbfc !important;
  position: relative;
  display: block !important;
}

/* A subtle define-line instead of a complex transition */
.footer-top-line {
  height: 1px;
  width: 100%;
  background-color: rgba(4, 128, 159, 0.08);
}

/* 2. Logo Branding */
.logo-text {
  font-size: 2.8rem;
  font-weight: 900;
  letter-spacing: -1px;
}

.vibrant-gradient-text {
  background: linear-gradient(135deg, #04809f 0%, #75b9c4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.lh-relaxed {
  line-height: 1.8 !important;
}

/* 3. Navigation Styling */
.nav-link {
  text-decoration: none;
  color: #546e7a;
  font-weight: 800;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: #04809f;
}

/* 4. Social Buttons */
.social-btn {
  background: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 1) !important;
  box-shadow: 0 4px 12px rgba(4, 128, 159, 0.05) !important;
}

.social-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(4, 128, 159, 0.1) !important;
}

.gap-4 {
  gap: 16px;
}
.gap-8 {
  gap: 40px;
}
</style>
