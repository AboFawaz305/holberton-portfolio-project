<template>
  <v-app-bar flat height="72" color="white" class="app-navbar">
    <v-container class="nav-container">
      <!-- يسار: بروفايل + تنبيه (فقط للمسجل دخول) -->
      <div class="nav-left" v-if="isAuthed">
        <!-- ملفك الشخصي -->
        <v-btn icon class="icon-btn" to="/UserProfilePage">
          <v-icon>mdi-account</v-icon>
        </v-btn>

        <!-- الإشعارات -->
        <v-btn icon class="icon-btn">
          <v-badge dot color="primary" offset-x="6" offset-y="6">
            <v-icon>mdi-bell-outline</v-icon>
          </v-badge>
        </v-btn>
      </div>

      <!-- اليمين: شعار أتراب (يظهر دائمًا) -->
      <router-link to="/" class="logo-link">
        <img src="/logo.svg" alt="أتراب" class="logo" />
      </router-link>

      <!-- الوسط: روابط التنقل (فقط للمسجل دخول) -->
      <div class="nav-center" v-if="isAuthed">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          :class="{ active: isActive(item.to) }"
        >
          <v-icon v-if="item.icon" size="18">
            {{ item.icon }}
          </v-icon>
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <!-- إذا مو مسجل دخول: فراغ (بس اللوغو ظاهر) -->
      <div v-else class="nav-center-empty"></div>
    </v-container>
  </v-app-bar>
</template>

<script setup>
import { useRoute } from 'vue-router'
import authService from '@/services/authService'

const route = useRoute()

/* هل المستخدم مسجل دخول؟ */
const isAuthed = !!authService.getToken()

/* عناصر الناف بار */
const navItems = [
  { label: 'عن أتراب', to: '/about' },
  { label: 'الجامعات', to: '/organizations', icon: 'mdi-domain' },
  { label: 'الكليات', to: '/groups', icon: 'mdi-school-outline' },
  { label: 'الموارد', to: '/resources', icon: 'mdi-file-document-outline' },
]

/* تحديد الصفحة النشطة */
const isActive = (to) => route.path.startsWith(to)
</script>

<style scoped>
.app-navbar {
  border-bottom: 1px solid #eef2f7;
}

/* الحاوية */
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

/* يسار */
.nav-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.icon-btn {
  border-radius: 999px;
}

/* الوسط */
.nav-center {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: center;
}
.nav-center-empty {
  flex: 1;
}

/* عناصر التنقل */
.nav-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 999px;
  text-decoration: none;
  color: #1f2937;
  font-weight: 500;
  transition: 0.15s ease;
}

/* Active (زر أزرق وحدود مثل الصورة) */
.nav-item.active {
  color: #04809f;
  border: 1.5px solid rgba(4, 128, 159, 0.35);
  background: rgba(4, 128, 159, 0.08);
  box-shadow: 0 6px 14px rgba(15, 23, 42, 0.08);
}
</style>
