<template>
  <v-container class="section d-flex justify-center">
    <v-row class="d-flex justify-center">
      <v-col v-for="(feature, i) in features" :key="i" cols="3" sm="6" md="4">
        <!-- class="d-flex justify-center" -->
        <v-card outlined class="card pa-4 d-flex flex-column align-center">
          <!-- Card Icon -->
          <v-avatar
            size="56"
            class="mb-4"
            :style="{ backgroundColor: feature.bg }"
            aria-hidden="true"
          >
            <span class="text-h5">{{ feature.icon }}</span>
          </v-avatar>

          <!-- Card Title -->
          <h3 class="text-h6 font-weight-bold text-center mt-0 mb-2">
            {{ feature.title }}
          </h3>

          <!-- Card Description -->
          <p class="text-body-2 text-center mt-0">
            {{ feature.desc }}
          </p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
const features = [
  {
    icon: '💬',
    bg: '#FFE7C6',
    title: 'نقاشات حيّة',
    desc: 'شارك في نقاشات المواد، اسأل واستفد، واحصل على إجابات من زملائك والمساعدين.',
  },
  {
    icon: '📄',
    bg: '#DDF5D9',
    title: 'موارد تعليمية',
    desc: 'احصل على ملخصات، ملفات PDF، وملاحظات من مشاركة الطلاب المتفوقين.',
  },
  {
    icon: '👥',
    bg: '#DCEEFF',
    title: 'تواصل مباشر',
    desc: 'تواصل مع زملائك في نفس الجامعة والكلية والمادة، وابدأ محادثات خاصة أو جماعية.',
  },
  {
    icon: '❤️',
    bg: '#FFE2EA',
    title: 'مجتمع داعم',
    desc: 'انضم لمجتمع من الطلاب المتحمسين الذين يدعمون بعضهم لتحقيق أفضل النتائج.',
  },
  {
    icon: '🛡️',
    bg: '#E6F4F6',
    title: 'آمن وخاص',
    desc: 'بياناتك محمية. نحترم الخصوصية والأمان بمعايير عالية.',
  },
  {
    icon: '🔎',
    bg: '#F0E7FF',
    title: 'بحث ذكي',
    desc: 'ابحث عن المواد والموارد والنقاشات بسهولة، ورتّب وقتك بذكاء.',
  },
]
</script>

<style scoped>
.section {
  padding: 46px 0; /* Optional: To maintain similar spacing as the original */
}

.card {
  /* width: 270px; /* Ensures all cards have the same width */
  height: 100%;
  box-shadow: 0 6px 22px rgba(15, 23, 42, 0.06); /* Optional for shadow effect */
  border-radius: 16px; /* Optional for rounded corners */
}

.text-h5 {
  font-size: 24px; /* Icon font size (adjust as needed) */
}
</style>
