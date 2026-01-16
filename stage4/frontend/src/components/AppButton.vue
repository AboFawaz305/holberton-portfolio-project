<template>
  <v-btn class="app-btn" elevation="0" rounded="xl" v-bind="$attrs">
    <span class="app-btn__content">
      <slot />
    </span>
  </v-btn>
</template>

<style scoped>
.app-btn {
  background-color: #ffffff;
  color: #04809f;

  /* حجم متوسط ومنطقي */
  min-width: 220px;
  height: 60px;
  border-radius: 16px;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  transition: transform 0.15s ease, box-shadow 0.15s ease;

  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.14);
}

.app-btn__content {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  font-weight: 700;
  font-size: 18px;
  line-height: 1;
}

/* Hover */
.app-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.18);
}

/* Press */
.app-btn:active {
  transform: translateY(0);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.14);
}
</style>
