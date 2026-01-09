<template>
  <v-app-bar app>
    <v-container>
      <v-row align="center" justify="space-between">
        <!-- Start Side -->
        <v-btn text to="/login" class="font-weight-bold"> تسجيل الدخول </v-btn>

        <!-- Center Navigation -->
        <v-btn-group>
          <v-btn text to="/#about">
            <v-icon icon="mdi-information" start></v-icon>
            عن أتراب</v-btn
          >
          <v-btn text to="/organizations">
            <v-icon icon="mdi-school" start></v-icon>
            الجامعات
          </v-btn>
        </v-btn-group>

        <!-- End Side -->
        <div></div>
      </v-row>
    </v-container>
  </v-app-bar>
</template>
