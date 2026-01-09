<script setup lang="ts">
import AppNavbar from '@/components/AppNavbar.vue'
import AppFooter from '@/components/AppFooter.vue'
import { useLocale } from 'vuetify'
const { current } = useLocale()
current.value = 'ar'
</script>

<template>
  <v-app>
    <AppNavbar />
    <v-main class="our-colors">
      <RouterView />
    </v-main>
    <AppFooter />
  </v-app>
</template>

<style></style>
