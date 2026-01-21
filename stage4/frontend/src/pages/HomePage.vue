<template>
  <div class="landing-page-wrapper">
    <HeroSection />
    <FeaturesSection />
    <HowSection />
    <CTASection />
  </div>
</template>

<script setup>
import HeroSection from '@/components/section/HeroSection.vue'
import FeaturesSection from '@/components/section/FeaturesSection.vue'
import HowSection from '@/components/section/HowSection.vue'
import CTASection from '@/components/section/CTASection.vue'
</script>

<style>
.landing-page-wrapper {
  overflow-x: hidden;
  min-height: 100vh;
  /* ONE COLOR GRADIENT: Flows from light teal to a richer teal */
  background: linear-gradient(
    180deg,
    #f0f9fa 0%,
    /* Very Light Teal */ #e0f2f4 35%,
    /* Soft Teal */ #c2e5e9 100% /* Richer Teal */
  );
  background-attachment: fixed; /* Keeps the gradient smooth as you scroll */
}

.section-padding {
  padding-top: 140px;
  padding-bottom: 140px;
  position: relative;
}

/* Updated Glass Cards to look better on a single-color background */
.glass-card {
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.4) !important;
  /* Shadow uses a dark version of your teal for depth */
  box-shadow: 0 30px 60px -12px rgba(4, 128, 159, 0.12) !important;
}
</style>
