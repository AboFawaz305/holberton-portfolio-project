<template>
  <v-app-bar flat height="72" color="white" class="app-navbar">
    <v-container class="nav-container">
      <!-- الشعار -->
      <div class="logo-link">
        <img src="/logo.svg" alt="أتراب" class="logo" />
      </div>

      <!-- روابط التنقل -->
      <div class="nav-center">
        <router-link
          v-for="item in navItems"
          :key="item.key"
          :to="item.to"
          class="nav-item"
          :class="{ active: isActive(item) }"
        >
          <!-- أيقونة حقيقية أو وهمية للمحاذاة -->
          <v-icon size="18" class="nav-icon" :class="{ invisible: !item.icon }">
            {{ item.icon || 'mdi-circle-small' }}
          </v-icon>

          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <!-- منيو الحساب -->
      <div class="nav-right">
        <v-menu location="bottom end" offset="10">
          <template #activator="{ props }">
            <v-btn icon class="icon-btn" v-bind="props" aria-label="Account menu">
              <v-icon>mdi-account</v-icon>
            </v-btn>
          </template>

          <v-list class="account-card" density="comfortable">
            <v-list-item class="account-item" to="/login">
              <template #prepend>
                <v-icon class="account-icon">mdi-login-variant</v-icon>
              </template>
              <v-list-item-title class="account-title">تسجيل الدخول</v-list-item-title>
            </v-list-item>

            <v-list-item class="account-item" to="/register">
              <template #prepend>
                <v-icon class="account-icon">mdi-account-plus-outline</v-icon>
              </template>
              <v-list-item-title class="account-title">إنشاء حساب</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </v-container>
  </v-app-bar>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { key: 'about', label: 'الرئيسية', to: '/' }, // بدون أيقونة
  { key: 'orgs', label: 'الجامعات', to: '/organizations', icon: 'mdi-domain' },
]

const isActive = (item) => {
  // عن أتراب: نشغّله إذا إحنا بالهوم + الهاش #about
  if (item.key === 'about') {
    return route.path === '/' && route.hash === '#about'
  }

  // باقي الروابط
  return route.path === item.to || route.path.startsWith(item.to)
}
</script>

<style scoped>
.app-navbar {
  border-bottom: 1px solid #eef2f7;
}

.nav-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

/* الشعار */
.logo-link {
  display: flex;
  align-items: center;
}
.logo {
  height: 30px;
}

/* الوسط */
.nav-center {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: center;
}

/* زر الحساب */
.nav-right {
  display: flex;
  align-items: center;
}
.icon-btn {
  border-radius: 999px;
}

/* أزرار التنقل */
.nav-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border-radius: 999px;
  text-decoration: none;
  color: #1f2937;
  font-weight: 600;
  transition: 0.15s ease;
}

/* الأيقونة */
.nav-icon {
  color: #04809f;
}

/* أيقونة وهمية */
.invisible {
  opacity: 0;
}

/* Active */
.nav-item.active {
  color: #04809f;
  border: 1.5px solid rgba(4, 128, 159, 0.35);
  background: rgba(4, 128, 159, 0.08);
  box-shadow: 0 6px 14px rgba(15, 23, 42, 0.08);
}

/* ================= Account menu ================= */

.account-card {
  min-width: 260px;
  padding: 0 !important;
  border-radius: 22px;
  border: 2px solid rgba(4, 128, 159, 0.35);
  background: #ffffff;
  overflow: hidden;
  box-shadow:
    0 18px 36px rgba(15, 23, 42, 0.14),
    0 2px 6px rgba(4, 128, 159, 0.12);
}

.account-item {
  width: 100%;
  padding: 16px 18px !important;
  border-bottom: 1px solid rgba(4, 128, 159, 0.14);
  transition: background 0.18s ease;
}
.account-item:last-child {
  border-bottom: none;
}
.account-item:hover {
  background: rgba(4, 128, 159, 0.12);
}

.account-icon {
  color: #04809f;
}

.account-title {
  font-weight: 700;
  color: #0f172a;
}
</style>
