import { createRouter, createWebHistory } from 'vue-router'
import OrganizationView from '../views/OrganizationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/organizations/:orgId',
      name: 'organization',
      component: OrganizationView,
    },
  ],
})

export default router
