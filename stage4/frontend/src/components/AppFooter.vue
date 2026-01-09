<template>
  <v-footer id="about" class="footer py-10">
    <v-container>
      <!-- Footer Grid -->
      <v-row class="mb-8">
        <!-- Brand Section -->
        <v-col cols="12" sm="6" md="4">
          <div class="footerBrand d-flex">
            <v-avatar size="56" color="teal lighten-5" class="footerLogo">
              <span class="text-primary text-h6 font-weight-bold">تخرج</span>
            </v-avatar>
            <div>
              <div class="footerName text-h6 font-weight-bold">أتراب</div>
              <p class="footerDesc text-body-2 text-grey-darken-1 mt-2">
                منصة تواصل تعليمية تجمع الطلاب لنفس الجامعة والكلية والمادة لمشاركة المعرفة والموارد
                التعليمية.
              </p>
            </div>
          </div>
        </v-col>

        <!-- Links: About Section -->
        <v-col cols="12" sm="6" md="2">
          <p class="footerTitle font-weight-bold mb-4">عن أتراب</p>
          <v-list nav dense>
            <v-list-item link href="#about">
              <v-list-item-title>عن المنصة</v-list-item-title>
            </v-list-item>
            <v-list-item link href="#courses">
              <v-list-item-title>كيف يعمل</v-list-item-title>
            </v-list-item>
            <v-list-item link href="#resources">
              <v-list-item-title>المزايا</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-col>

        <!-- Links: Support Section -->
        <v-col cols="12" sm="6" md="2">
          <p class="footerTitle font-weight-bold mb-4">الدعم</p>
          <v-list nav dense>
            <v-list-item link href="#">
              <v-list-item-title>سياسة الاستخدام</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-col>

        <!-- Links: Contact Section -->
        <v-col cols="12" sm="6" md="2">
          <p class="footerTitle font-weight-bold mb-4">تواصل</p>
          <v-list nav dense>
            <v-list-item link href="mailto:hello@atrab.com">
              <v-list-item-title>البريد الإلكتروني</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>

      <!-- Footer Bottom -->
      <v-row class="footer__bottom justify-space-between align-center">
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
  background: #ffffff; /* Footer background color */
}
.footerLogo {
  margin-right: 12px;
  border-radius: 50%;
}

.footer__bottom {
  padding-top: 16px;
  border-top: 1px solid #eef2f7;
}

.floating {
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.16);
}
</style>
