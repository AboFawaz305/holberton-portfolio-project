import { createRouter, createWebHistory } from 'vue-router'

import RegisterView from './RegisterView.vue'
import LoginView from './LoginView.vue'
import OrganizationView from './OrganizationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/organizations/:orgId',
      name: 'organization',
      component: OrganizationView,
    },
    { path: '/register', component: RegisterView },
    { path: '/login', component: LoginView },
  ],
})

export default router
