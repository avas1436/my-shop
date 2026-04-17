import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: () => import('@/views/HomeView.vue') },
    { path: '/product/:id', component: () => import('@/views/ProductDetailView.vue') },
    { path: '/category/:id', component: () => import('@/views/CategoryView.vue') },
    { path: '/cart', component: () => import('@/views/CartView.vue') },
    { path: '/checkout', component: () => import('@/views/CheckoutView.vue') },
    { path: '/profile', component: () => import('@/views/ProfileView.vue') },
  ],
})

export default router
