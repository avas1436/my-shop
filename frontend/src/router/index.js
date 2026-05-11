import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
    { path: '/products', name: 'products', component: () => import('@/views/ProductsView.vue') },
    { path: '/product/:id', name: 'product', component: () => import('@/views/ProductDetailView.vue') },
    { path: '/category/:id', name: 'category', component: () => import('@/views/CategoryView.vue') },
    { path: '/search', name: 'search', component: () => import('@/views/SearchView.vue') },
    { path: '/cart', name: 'cart', component: () => import('@/views/CartView.vue') },
    { path: '/checkout', name: 'checkout', component: () => import('@/views/CheckoutView.vue') },
    { path: '/profile', name: 'profile', component: () => import('@/views/ProfileView.vue') },
    {
      path: '/admin/products/new',
      name: 'admin-product-composer',
      component: () => import('@/views/AdminProductComposerView.vue'),
      redirect: { name: 'admin-product-draft' },
      children: [
        {
          path: 'draft',
          name: 'admin-product-draft',
          component: () => import('@/views/admin-product-workflow/AdminProductDraftStepView.vue'),
          meta: { workflowStep: 'draft' },
        },
        {
          path: ':productId/basics',
          name: 'admin-product-basics',
          component: () => import('@/views/admin-product-workflow/AdminProductBasicsStepView.vue'),
          meta: { workflowStep: 'basics', requiresDraft: true },
        },
      ],
    },
    { path: '/about', name: 'about', component: () => import('@/views/AboutView.vue') },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
