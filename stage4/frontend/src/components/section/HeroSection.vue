<template>
  <v-container id="universities" class="hero text-center">
    <v-card class="py-16 px-8" flat>
      <!-- Hero Pill -->
      <v-chip color="teal lighten-5" outlined class="mb-4 hero-pill">
        <span class="spark-wrapper">
          <v-icon class="spark small">mdi-creation-outline</v-icon>
        </span>
        <span class="pill-text">منصة تعليمية للتواصل الأكاديمي</span>
      </v-chip>

      <!-- Title -->
      <h1 class="text-h2 font-weight-bold mb-4">
        تواصل مع <span class="gradient-text">زملائك</span><br />
        في نفس المادة
      </h1>

      <!-- Subtitle -->
      <p class="text-subtitle-1 text-grey-darken-1 mb-6">
        منصة تجمع طلاب الجامعة في مجموعات حسب المواد، لمشاركة المصادر، تبادل الأسئلة، وبناء بيئة
        تعلّم تعاونية.
      </p>

      <!-- CTA Button (بدون AppButton) -->
      <v-btn to="/register" class="hero-btn" elevation="6" size="large"> انضم لنا الآن </v-btn>
    </v-card>
  </v-container>
</template>

<script setup></script>

<style scoped>
/* ---------- Hero pill ---------- */
.pill-text {
  color: #04809f;
  margin-inline-start: 4px;
}

.hero-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.spark-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.spark {
  color: #04809f;
  font-size: 18px;
}

.spark.small {
  font-size: 14px;
  opacity: 0.9;
}

/* ---------- Gradient word ---------- */
.gradient-text {
  background: linear-gradient(90deg, #04809f 0%, #75b9c4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ---------- Hero CTA Button ---------- */
.hero-btn {
  color: #ffffff !important;
  font-weight: 700;
  border-radius: 18px;
  padding: 14px 36px;
  font-size: 18px;

  background: linear-gradient(135deg, #04809f 0%, #3f9fb2 50%, #75b9c4 100%) !important;

  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
  transition: all 0.2s ease;
}

.hero-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(0, 0, 0, 0.22);
}
</style>
