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
    // meta: { guestOnly: true }, // فقط کاربرانی که لاگین نکرده‌اند
    children: [
      {
        path: '',
        name: 'auth-index',
        meta: { guestOnly: true },
        component: () => import('@/views/auth/AuthIndexView.vue'),
      },
      {
        path: 'login-password',
        name: ROUTES.LOGIN_PASSWORD,
        meta: { guestOnly: true },
        component: () => import('@/views/auth/LoginPasswordView.vue'),
      },
      {
        path: 'login-otp',
        name: ROUTES.LOGIN_OTP,
        meta: { guestOnly: true },
        component: () => import('@/views/auth/LoginOtpView.vue'),
      },
      {
        path: 'register',
        name: ROUTES.REGISTER,
        meta: { guestOnly: true },
        component: () => import('@/views/auth/RegisterView.vue'),
      },
      {
        path: 'complete',
        name: ROUTES.COMPLETE,
        meta: { requiresAuth: true, onlyIncompleteProfile: true },
        component: () => import('@/views/auth/CompleteRegister.vue'),
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
      // {
      //   path: 'inventory',
      //   name: ROUTES.ADMIN_INVENTORY,
      //   component: () => import('@/views/admin/AdminInventoryView.vue'),
      //   props: true,
      // },
      // {
      //   path: 'financials',
      //   name: ROUTES.ADMIN_FINANCIALS,
      //   component: () => import('@/views/admin/AdminFinancialsView.vue'),
      //   props: true,
      // },
      // {
      //   path: 'marketing',
      //   name: ROUTES.ADMIN_MARKETING,
      //   component: () => import('@/views/admin/AdminMarketingView.vue'),
      //   props: true,
      // },
      // {
      //   path: 'support',
      //   name: ROUTES.ADMIN_SUPPORT,
      //   component: () => import('@/views/admin/AdminSupportView.vue'),
      //   props: true,
      // },
      // {
      //   path: 'analytics',
      //   name: ROUTES.ADMIN_ANALYTICS,
      //   component: () => import('@/views/admin/AdminAnalyticsView.vue'),
      //   props: true,
      // },
      // {
      //   path: 'staff',
      //   name: ROUTES.ADMIN_STAFF,
      //   component: () => import('@/views/admin/AdminStaffView.vue'),
      //   props: true,
      // },
      {
        path: 'content',
        name: ROUTES.ADMIN_CONTENT,
        component: () => import('@/views/admin/AdminContentView.vue'),
        props: true,
      },
      // {
      //   path: 'settings',
      //   name: ROUTES.ADMIN_SETTINGS,
      //   component: () => import('@/views/admin/AdminSettingsView.vue'),
      //   props: true,
      // },
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

router.beforeEach(async (to, from) => {
  const userStore = useUserStore()

  // اگر استور هنوز آماده نیست منتظر بمان
  if (!userStore.isAuthReady) {
    await userStore.initializeAuth()
  }

  const isAuthenticated = userStore.isAuthenticated
  const userRole = userStore.userRole

  const hasCompleteProfile = !!userStore.profile?.first_name && !!userStore.profile?.last_name

  // بررسی روت‌هایی که فقط برای کاربران لاگین نشده هستند
  if (to.meta.requiresAuth && !isAuthenticated) {
    return { name: ROUTES.LOGIN_PASSWORD, query: { redirect: to.fullPath } }
  }

  // اگر لاگین بود و خواست بره صفحه ورود
  if (to.meta.guestOnly && isAuthenticated) {
    return { name: ROUTES.PROFILE, query: { redirect: to.fullPath } }
  }

  // اگر نیاز به نقش ادمین داشت
  if (to.meta.role && to.meta.role !== userRole) {
    return { name: ROUTES.HOME }
  }

  // اگر صفحه نیاز به پروفایل کامل دارد اما پروفایل ناقص است
  if (to.meta.requireCompleteProfile && !hasCompleteProfile) {
    return { name: ROUTES.COMPLETE, query: { redirect: to.fullPath } }
  }

  // اگر کاربر وارد صفحه "تکمیل حساب" شد، اما از قبل پروفایلش کامل است
  if (to.meta.onlyIncompleteProfile && hasCompleteProfile) {
    return { name: ROUTES.PROFILE }
  }

  return true
})

export default router
