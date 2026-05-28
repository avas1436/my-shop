// src/stores/userStore.js
import { authService } from '@/services/authService'
import { getStoredAccessToken } from '@/utils/token'
import { defineStore } from 'pinia'

// متغیر برای جلوگیری از درخواست‌های همزمان
let authPromise = null // for prevent race condition

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: null,
    addresses: [
      {
        id: 1,
        title: 'خانه',
        city: 'تهران',
        details: 'تهران، سعادت‌آباد، سرو غربی، پلاک ۲۴، واحد ۶',
      },
      {
        id: 2,
        title: 'محل کار',
        city: 'تهران',
        details: 'تهران، ونک، خیابان خدامی، برج آفتاب، طبقه ۵',
      },
    ],

    // وضعیت احراز هویت
    // accessToken: getStoredAccessToken().accessToken || null,
    accessToken: null,

    isAuthenticated: false,
    isAuthReady: false,
    authLoading: false,
    authError: '',
  }),

  getters: {
    primaryAddress: (state) => state.addresses[0] || null,

    userRole: (state) => state.profile?.role || 'guest',
  },

  actions: {
    // فراخوانی در زمان لود اولیه اپلیکیشن
    async initializeAuth(forceRefresh = false) {
      // اگر اطلاعات از قبل گرفته شده و نیاز به آپدیت اجباری نیست، کاری نکن
      if (this.isAuthReady && this.profile && !forceRefresh) return

      // اگر درخواستی از قبل در حال انجام است، همان را برگردان تا درخواست جدید نرود
      if (authPromise) return authPromise

      // ایجاد درخواست جدید و ذخیره در متغیر
      authPromise = (async () => {
        this.authLoading = true
        this.authError = ''

        // دریافت توکن به صورت زنده برای جلوگیری از خطای خالی بودن
        const tokenData = getStoredAccessToken()
        this.accessToken = tokenData?.accessToken || this.accessToken

        try {
          if (this.accessToken) {
            const userProfile = await authService.getMe()
            this.profile = userProfile
            this.isAuthenticated = true
          } else {
            this.isAuthenticated = false
            this.profile = null
          }
        } catch (err) {
          console.error('Auth init failed:', err)
          this.isAuthenticated = false
          this.profile = null
          this.authError = 'خطا در احراز هویت'
        } finally {
          this.authLoading = false
          this.isAuthReady = true
          authPromise = null // پاک کردن متغیر پس از اتمام
        }
      })()

      return authPromise
    },

    // اکشن برای لاگ‌اوت
    async logout() {
      try {
        // فراخوانی API برای باطل کردن رفرش توکن در سمت سرور
        await authService.logout({ refresh_token: this.refreshToken })
      } catch (err) {
        console.error('Logout API failed:', err)
      } finally {
        // پاک کردن استیت استور
        this.isAuthenticated = false
        this.profile = null
        this.addresses = []
        this.accessToken = null
      }
    },

    // یک اکشن کمکی برای به‌روزرسانی استیت بعد از لاگین/ثبت‌نام موفق
    setAuthSuccess(token) {
      this.isAuthenticated = true
      if (token) {
        this.accessToken = token.accessToken
      }
    },

    // اضافه کردن این اکشن برای ذخیره اطلاعات پروفایل
    setProfile(userData) {
      this.profile = userData
    },
  },
})
