<template>
  <v-container class="section-padding overflow-visible">
    <v-row align="center">
      <v-col cols="12" md="6" class="d-none d-md-flex justify-center" data-aos="fade-right">
        <div class="steps-container">
          <div class="step-visual-card glass-card top-card">
            <v-icon color="primary" class="mb-3">mdi-school-outline</v-icon>
            <div class="skeleton-bar w-75"></div>
          </div>
          <div class="step-visual-card glass-card bottom-card shadow-xl">
            <v-icon color="secondary" class="mb-3">mdi-book-multiple</v-icon>
            <div class="skeleton-line w-50"></div>
          </div>
        </div>
      </v-col>

      <v-col cols="12" md="6" class="text-right" data-aos="fade-left">
        <h2 class="text-h3 font-weight-black mb-12 text-grey-darken-4">كيف يعمل أتراب؟</h2>

        <div v-for="(step, i) in steps" :key="i" class="step-item d-flex align-start mb-12">
          <v-avatar
            color="primary"
            size="56"
            class="text-white font-weight-black elevation-4 flex-shrink-0"
          >
            {{ i + 1 }}
          </v-avatar>

          <div class="flex-grow-1 ms-10 ps-2">
            <h3 class="text-h5 font-weight-bold mb-2">{{ step.title }}</h3>
            <p class="text-body-1 text-grey-darken-2 lh-relaxed">{{ step.desc }}</p>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
const steps = [
  { title: 'اختر جامعتك وكليتك', desc: 'ابدأ بتحديد مؤسستك التعليمية لتصل إلى مجتمعك الخاص.' },
  { title: 'حدد المواد الدراسية', desc: 'اختر المواد التي تدرسها لتنضم تلقائياً لمجموعات النقاش.' },
  { title: 'ابدأ التواصل والتعاون', desc: 'شارك الموارد، اطرح الأسئلة، وتفاعل مع زملائك فوراً.' },
]
</script>

<style scoped>
.lh-relaxed {
  line-height: 1.7 !important;
}
.steps-container {
  position: relative;
  width: 320px;
  height: 350px;
}
.step-visual-card {
  position: absolute;
  width: 200px;
  padding: 25px;
  border-radius: 28px;
}
.top-card {
  top: 0;
  right: 0;
  transform: rotate(5deg);
}
.bottom-card {
  bottom: 0;
  left: -40px;
  transform: rotate(-5deg);
  z-index: 10;
}
.skeleton-bar,
.skeleton-line {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
}

/* Smooth scaling effect on hover */
.step-item:hover .v-avatar {
  transform: scale(1.15) rotate(5deg);
  transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
</style>
