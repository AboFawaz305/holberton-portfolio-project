import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import atrabTheme from '@/styles/atrabTheme'
import AOS from 'aos'
import 'aos/dist/aos.css'

const i18n = createI18n({
  locale: 'ar',
  fallbackLocale: 'ar',
  messages: {
    ar: {
      INVALID_USERNAME: 'إسم مستخدم غير صالح',
      INVALID_PASSWORD: 'كلمة السر غير صالحة',
      USER_ALREADY_EXIST: 'إسم المستخدم أو الإيميل موجود مسبقا',
    },
  },
})

AOS.init({
  duration: 800,
  easing: 'ease-in-out-sine',
  once: false,
  mirror: false,
  startEvent: 'DOMContentLoaded',
})

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'atrabTheme',
    themes: {
      atrabTheme,
    },
  },
})

import './styles/global.scss'

const app = createApp(App)

app.use(i18n)
app.use(router)
app.use(vuetify)

app.mount('#app')
