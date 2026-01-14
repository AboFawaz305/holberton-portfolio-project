import { createRouter, createWebHistory } from 'vue-router'
import authService from '@/services/authService'

import RegisterationPage from '@/pages/RegisterationPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import OrganizationsPage from '@/pages/OrganizationsPage.vue'
import OrganizationHomePage from '@/pages/OrganizationHomePage.vue'
import UserProfilePage from '@/pages/UserProfilePage.vue'
import HomePage from '@/pages/HomePage.vue'
import GroupsHomePage from '@/pages/GroupsHomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/register', component: RegisterationPage },
    { path: '/login', component: LoginPage },
    { path: '/organizations', component: OrganizationsPage },
    {
      path: '/organizations/:id',
      component: OrganizationHomePage,
      props: true,
      meta: { requiresAuth: true },
    },
    {
      path: '/groups/:id',
      name: 'group',
      component: GroupsHomePage,
      props: true,
    },
    { path: '/profile', component: UserProfilePage, meta: { requiresAuth: true } },
    { path: '/home', component: HomePage },
    { path: '/', redirect: '/home' },
  ],
})

export default router
router.beforeEach(async (to, _, next) => {
  if (to.meta.requiresAuth && !(await authService.isLoggedIn())) {
    next('/login') // Redirect to login if user is not authenticated
  } else {
    next() // Proceed as normal if authenticated
  }
})
