import { createRouter, createWebHistory } from 'vue-router'

import RegisterView from "./RegisterView.vue"
import LoginView from "./LoginView.vue"


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/register", component: RegisterView },
    { path: "/login", component: LoginView }
  ],
})

export default router
