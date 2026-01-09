<template>
  <v-container id="universities" class="hero text-center">
    <v-card class="py-16 px-8" flat>
      <!-- Hero Pill -->
      <v-chip color="teal lighten-5" outlined class="mb-4">
        <v-icon start>mdi-star</v-icon>
        منصة التواصل التعليمية الأولى في المنطقة
      </v-chip>

      <!-- Title -->
      <h1 class="text-h2 font-weight-bold mb-4">
        تواصل مع زملائك <br />
        في نفس المادة
      </h1>

      <!-- Subtitle -->
      <p class="text-subtitle-1 text-grey-darken-1 mb-6">
        انضم إلى آلاف الطلاب الذين يبادلون المعرفة والموارد التعليمية في نفس الجامعة والكلية
        والمادة. تعلّم، شارك، وتميّز!
      </p>

      <!-- Call to Action Button -->
      <v-btn color="primary" large class="text-white gradient-bg" to="/register">
        ابدأ رحلتك الآن
      </v-btn>
    </v-card>
  </v-container>
</template>

<style scoped></style>
