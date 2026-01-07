import { createRouter, createWebHistory } from 'vue-router'

import RegisterView from './RegisterView.vue'
import LoginView from './LoginView.vue'
import OrganizationsView from './OrganizationsView.vue'
import OrgView from './OrganizationChatView.vue'
import UserProfileView from './UserProfileView.vue'
import MainView from './MainView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/register', component: RegisterView },
    { path: '/login', component: LoginView },
    { path: '/organizations', component: OrganizationsView },
    { path: '/organizations/:id', component: OrgView, props: true },
    { path: '/profile', component: UserProfileView },
    { path: '/home', component: MainView },
    { path: '/', redirect: '/home' },
  ],
})

export default router
