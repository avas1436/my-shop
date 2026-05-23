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
    component: () => import('@/views/ProfileView.vue'), // لی‌آوت مخصوص لاگین/ثبت نام
    // redirect: { name: ROUTES.LOGIN }, // ریدایرکت پیش‌فرض بخش auth
    meta: { guestOnly: true }, // فقط کاربرانی که لاگین نکرده‌اند
    children: [
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
router.beforeEach((to, from) => {
  // TODO: وضعیت لاگین کاربر و نقش او را از Store بگیرید
  const isAuthenticated = false
  const userRole = 'customer' // 'admin' یا

  // ۱. بررسی روت‌هایی که فقط برای کاربران لاگین نشده هستند
  if (to.meta.guestOnly && isAuthenticated) {
    return { name: ROUTES.HOME }
  }

  // ۲. بررسی روت‌هایی که نیاز به لاگین دارند
  if (to.meta.requiresAuth && !isAuthenticated) {
    return { name: ROUTES.LOGIN, query: { redirect: to.fullPath } }
  }

  // ۳. بررسی نقش‌ها
  if (to.meta.role && to.meta.role !== userRole) {
    return { name: ROUTES.HOME } // یا ریدایرکت به صفحه 403 Access Denied
  }

  // در غیر این صورت اجازه عبور داده می‌شود
  true
})

export default router
