<template>
  <v-container id="courses" class="section">
    <!-- Title and Subtitle -->
    <v-card class="py-8 text-center" flat>
      <h2 class="text-h4 font-weight-bold mb-4">كيف يعمل أتراب؟</h2>
      <p class="text-subtitle-1 text-grey-darken-1">ثلاث خطوات بسيطة للبدء</p>
    </v-card>

    <!-- Steps Section -->
    <v-row class="mt-8">
      <v-col
        v-for="(step, i) in steps"
        :key="i"
        cols="12"
        sm="6"
        md="4"
        class="d-flex justify-center"
      >
        <!-- Each Step as a Card -->
        <v-card outlined class="howStep pa-6 text-center d-flex flex-column align-center">
          <v-avatar size="64" class="mb-4" color="primary">
            <span class="text-h5 text-white">{{ step.icon }}</span>
          </v-avatar>

          <!-- Step Title -->
          <h3 class="text-h6 font-weight-bold mt-0 mb-2">{{ step.title }}</h3>

          <!-- Step Description -->
          <p class="text-body-2 text-grey-darken-1 mt-0">{{ step.desc }}</p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
const steps = [
  { icon: '🎓', title: 'اختر جامعتك', desc: 'ابدأ باختيار جامعتك من قائمة الجامعات المدعومة.' },
  { icon: '📘', title: 'اختر موادك', desc: 'حدد الكلية والمواد التي تدرسها لهذا الفصل.' },
  { icon: '🤝', title: 'تواصل وشارك', desc: 'ابدأ التواصل مع زملائك وشارك المعرفة والموارد.' },
]
</script>

<style scoped>
.section {
  padding: 46px 0; /* Optional: Maintain visual spacing */
}
.howStep {
  width: 270px; /* To maintain uniform card width */
  height: auto; /* Dynamic height based on content */
  border-radius: 16px; /* Rounded corners */
  box-shadow: 0 6px 22px rgba(15, 23, 42, 0.06); /* Optional for card shadow effect */
}
.text-h5 {
  font-size: 24px; /* Icon or number size */
}
</style>
