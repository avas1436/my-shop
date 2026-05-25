// src/stores/userStore.js
import { authService } from '@/services/authService'
import { getStoredAccessToken } from '@/utils/token'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    // ---- داده‌های فعلی شما ----
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

    // ---- وضعیت احراز هویت ----
    accessToken: getStoredAccessToken().accessToken || null,

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
    // فراخوانی در زمان لود اولیه اپلیکیشن (مثلاً در App.vue یا روتر)
    async initializeAuth() {
      this.authLoading = true
      this.authError = ''

      const accessToken = getStoredAccessToken()

      try {
        if (this.accessToken) {
          // دریافت اطلاعات واقعی کاربر از API
          const userProfile = await authService.getMe()
          this.profile = userProfile.data
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
        // اگر توکن‌ها منقضی شده باشند و رفرش هم ناموفق باشد، توکن‌ها باید پاک شوند
      } finally {
        this.authLoading = false
        this.isAuthReady = true
      }
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
    setAuthSuccess(profileData, token) {
      this.profile = profileData
      this.isAuthenticated = true
      if (token) {
        this.accessToken = token.accessToken
      }
    },
  },
})
