<template>
  <div class="hero-wrapper section-padding">
    <v-container>
      <v-row align="center">
        <v-col cols="12" md="7" class="text-right" data-aos="fade-left">
          <v-chip color="primary" variant="tonal" class="mb-6 font-weight-bold px-6 py-4">
            ✨ المنصة الأكاديمية لطلاب الجامعات
          </v-chip>

          <h1 class="text-h2 font-weight-black mb-6 lh-tight text-grey-darken-4">
            تواصل مع <span class="vibrant-gradient-text">زملائك</span><br />
            بأسلوب عصري
          </h1>

          <p class="text-h6 text-grey-darken-2 mb-10 lh-base pl-md-16 font-weight-regular">
            بيئة تعليمية متكاملة تجمعك بطلاب تخصصك. شارك الموارد، ناقش المحاضرات، وتفوق في دراستك مع
            أقرانك.
          </p>

          <div class="d-flex gap-4 flex-wrap">
            <v-btn
              to="/register"
              size="x-large"
              class="brand-btn gradient-bg px-10 elevation-8"
              height="64"
            >
              انضم لنا الآن
            </v-btn>
          </div>
        </v-col>

        <v-col cols="12" md="5" class="d-none d-md-flex justify-center" data-aos="zoom-in-right">
          <div class="app-mockup-wrapper">
            <div class="main-mockup glass-card">
              <div class="mockup-header mb-8"></div>
              <div class="mockup-body">
                <div
                  v-for="n in 4"
                  :key="n"
                  class="skeleton-bar"
                  :style="{ width: 100 - n * 12 + '%' }"
                ></div>
              </div>
            </div>
            <div class="floating-icon shadow-lg">
              <v-icon color="primary">mdi-chat-processing</v-icon>
            </div>
            <div class="floating-icon-2 shadow-lg">
              <v-icon color="#04809f">mdi-file-pdf-box</v-icon>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style scoped>
/* Gradient Text Style */
.vibrant-gradient-text {
  background: linear-gradient(135deg, #04809f 0%, #75b9c4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.brand-btn {
  background: linear-gradient(135deg, #04809f 0%, #3f9fb2 100%) !important;
  color: white !important;
  border-radius: 18px;
  font-weight: 800;
  font-size: 20px;
}

.app-mockup-wrapper {
  position: relative;
  width: 340px;
  height: 420px;
}
.main-mockup {
  width: 100%;
  height: 100%;
  border-radius: 40px;
  padding: 30px;
  transform: rotate(-3deg);
  transition: 0.5s ease;
}
.mockup-header {
  height: 15px;
  width: 40%;
  background: #04809f15;
  border-radius: 10px;
}
.skeleton-bar {
  height: 10px;
  background: #e2e8f0;
  border-radius: 5px;
  margin-bottom: 20px;
}

.floating-icon,
.floating-icon-2 {
  position: absolute;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: float 4s ease-in-out infinite;
}
.floating-icon {
  top: 20px;
  left: -30px;
}
.floating-icon-2 {
  bottom: 60px;
  left: -40px;
  animation-delay: 1.5s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}
</style>
