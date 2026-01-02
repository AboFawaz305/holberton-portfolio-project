import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'

import './styles/global.scss'

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

const app = createApp(App)

app.use(i18n)
app.use(router)

app.mount('#app')
