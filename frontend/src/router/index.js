import AdminLayout from '@/layouts/AdminLayout.vue'
import StorefrontLayout from '@/layouts/StorefrontLayout.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: StorefrontLayout,
      children: [
        { path: '', name: 'home', component: () => import('@/views/HomeView.vue') },
        { path: 'products', name: 'products', component: () => import('@/views/ProductsView.vue') },
        {
          path: 'product/:id',
          name: 'product',
          component: () => import('@/views/ProductDetailView.vue'),
        },
        {
          path: 'category/:id',
          name: 'category',
          component: () => import('@/views/CategoryView.vue'),
        },
        { path: 'search', name: 'search', component: () => import('@/views/SearchView.vue') },
        { path: 'cart', name: 'cart', component: () => import('@/views/CartView.vue') },
        { path: 'checkout', name: 'checkout', component: () => import('@/views/CheckoutView.vue') },
        {
          path: 'checkout/success/:id',
          name: 'order-success',
          component: () => import('@/views/OrderSuccessView.vue'),
        },
        { path: 'profile', name: 'profile', component: () => import('@/views/ProfileView.vue') },
        { path: 'support', name: 'support', component: () => import('@/views/SupportView.vue') },
        { path: 'about', name: 'about', component: () => import('@/views/AboutView.vue') },
      ],
    },
    {
      path: '/admin',
      component: AdminLayout,
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/AdminDashboardView.vue'),
        },
        {
          path: 'products',
          name: 'admin-products',
          component: () => import('@/views/admin/AdminProductsView.vue'),
        },
        {
          path: 'orders',
          name: 'admin-orders',
          component: () => import('@/views/admin/AdminOrdersView.vue'),
        },
        {
          path: 'customers',
          name: 'admin-customers',
          component: () => import('@/views/admin/AdminCustomersView.vue'),
        },
        {
          path: 'content',
          name: 'admin-content',
          component: () => import('@/views/admin/AdminContentView.vue'),
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
