// src/router/index.js
import AdminLayout from '@/layouts/AdminLayout.vue'
import StorefrontLayout from '@/layouts/StorefrontLayout.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { ROUTES } from './routeNames'; // مسیر فایل ثابت‌ها

const routes = [
  // ==========================================
  // Storefront Routes
  // ==========================================
  {
    path: '/',
    component: StorefrontLayout,
    children: [
      {
        path: '',
        name: ROUTES.HOME,
        component: () => import('@/views/HomeView.vue'),
        props: true,
        meta: { requiresAuth: false },
      },
      {
        path: 'products',
        name: ROUTES.PRODUCTS,
        component: () => import('@/views/ProductsView.vue'),
        props: true,
      },
      {
        path: 'product/:id',
        name: ROUTES.PRODUCT_DETAIL,
        component: () => import('@/views/ProductDetailView.vue'),
        props: true,
      },
      {
        path: 'category/:id',
        name: ROUTES.CATEGORY,
        component: () => import('@/views/CategoryView.vue'),
        props: true,
      },
      {
        path: 'search',
        name: ROUTES.SEARCH,
        component: () => import('@/views/SearchView.vue'),
        props: true,
      },
      {
        path: 'cart',
        name: ROUTES.CART,
        component: () => import('@/views/CartView.vue'),
        props: true,
      },
      {
        path: 'checkout',
        name: ROUTES.CHECKOUT,
        component: () => import('@/views/CheckoutView.vue'),
        props: true,
        meta: { requiresAuth: true }, // نیاز به لاگین دارد
      },
      {
        path: 'checkout/success/:id',
        name: ROUTES.ORDER_SUCCESS,
        component: () => import('@/views/OrderSuccessView.vue'),
        props: true,
        meta: { requiresAuth: true },
      },
      {
        path: 'profile',
        name: ROUTES.PROFILE,
        component: () => import('@/views/ProfileView.vue'),
        props: true,
        meta: { requiresAuth: true }, // نیاز به لاگین دارد
      },
      {
        path: 'support',
        name: ROUTES.SUPPORT,
        component: () => import('@/views/SupportView.vue'),
        props: true,
      },
      {
        path: 'about',
        name: ROUTES.ABOUT,
        component: () => import('@/views/AboutView.vue'),
        props: true,
      },
    ],
  },

  // ==========================================
  // Auth Routes
  // ==========================================
  {
    path: '/auth',
    component: StorefrontLayout,
    redirect: { name: ROUTES.LOGIN }, // ریدایرکت پیش‌فرض بخش auth
    meta: { guestOnly: true }, // فقط کاربرانی که لاگین نکرده‌اند
    children: [
      {
        path: '',
        name: 'auth-index',
        component: () => import('@/views/auth/AuthIndexView.vue'),
      },
      {
        path: 'login-password',
        name: ROUTES.LOGIN_PASSWORD,
        component: () => import('@/views/auth/LoginPasswordView.vue'),
      },
      {
        path: 'login-otp',
        name: ROUTES.LOGIN_OTP,
        component: () => import('@/views/auth/LoginOtpView.vue'),
      },
      {
        path: 'register',
        name: ROUTES.REGISTER,
        component: () => import('@/views/auth/RegisterView.vue'),
      },
    ],
  },

  // ==========================================
  // Admin Routes
  // ==========================================
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' }, // فقط ادمین‌ها دسترسی دارند
    children: [
      {
        path: '',
        name: ROUTES.ADMIN_DASHBOARD,
        component: () => import('@/views/admin/AdminDashboardView.vue'),
        props: true,
      },
      {
        path: 'products',
        name: ROUTES.ADMIN_PRODUCTS,
        component: () => import('@/views/admin/AdminProductsView.vue'),
        props: true,
      },
      {
        path: 'orders',
        name: ROUTES.ADMIN_ORDERS,
        component: () => import('@/views/admin/AdminOrdersView.vue'),
        props: true,
      },
      {
        path: 'customers',
        name: ROUTES.ADMIN_CUSTOMERS,
        component: () => import('@/views/admin/AdminCustomersView.vue'),
        props: true,
      },
      {
        path: 'content',
        name: ROUTES.ADMIN_CONTENT,
        component: () => import('@/views/admin/AdminContentView.vue'),
        props: true,
      },
    ],
  },

  // ==========================================
  // Fallback (404)
  // ==========================================
  {
    path: '/:pathMatch(.*)*',
    name: ROUTES.NOT_FOUND,
    component: () => import('@/views/NotFoundView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  },
})

// ==========================================
// Navigation Guards
// ==========================================
import { useUserStore } from '@/stores/userStore'

router.beforeEach((to, from) => {
  const userStore = useUserStore()

  const isAuthenticated = userStore.isAuthenticated
  const userRole = userStore.userRole

  // بررسی روت‌هایی که فقط برای کاربران لاگین نشده هستند
  if (to.meta.requiresAuth && !isAuthenticated) {
    return { name: ROUTES.LOGIN, query: { redirect: to.fullPath } }
  }

  // اگر لاگین بود و خواست بره صفحه ورود
  else if (to.meta.guestOnly && isAuthenticated) {
    return { name: ROUTES.PROFILE, query: { redirect: to.fullPath } }
  }

  // اگر نیاز به نقش ادمین داشت
  else if (to.meta.role && to.meta.role !== userRole) {
    return { name: ROUTES.HOME }
  }

  true
})

export default router
