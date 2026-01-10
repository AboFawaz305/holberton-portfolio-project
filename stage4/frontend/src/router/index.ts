import { createRouter, createWebHistory } from 'vue-router'

import RegisterView from './RegisterView.vue'
import LoginView from './LoginView.vue'
import OrganizationView from './OrganizationView.vue'
import ResourcesPanel from '../components/ResourcesPanel.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/organizations/:orgId',
      name: 'organization',
      component: OrganizationView,
    },
    {
      path: '/organizations/:orgId/groups/:groupId/resources',
      name: 'resources',
      component: ResourcesPanel,
    },
    { path: '/register', component: RegisterView },
    { path: '/login', component: LoginView },
  ],
})

export default router
