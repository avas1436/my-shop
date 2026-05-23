// src/services/axiosClient.js

import { clearStoredTokens, getStoredTokens } from '@/utils/token'
import axios from 'axios'

const axiosClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

// Request Interceptor
// رهگیر درخواست
// این قسمت به صورت خودکار توکن را در درخواست قرار میدهد
axiosClient.interceptors.request.use(
  (config) => {
    // بررسی skipAuth برای ارسال نکردن توکن در صورت نیاز
    if (config.skipAuth) {
      return config
    }

    const token = getStoredTokens().accessToken

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },

  (error) => {
    return Promise.reject(error)
  },
)

// Request Interceptor
// مدیریت پاسخ و خطای بک اند
axiosClient.interceptors.response.use(
  (response) => {
    if (response.data && response.data.success) {
      return response.data.data
    }

    // حتما باید یک خروجی دیفالت وجود داشته باشد
    return response
  },

  (error) => {
    if (error.response) {
      const backendError = error.response.data || {}

      const errorType = backendError.error_type
      const errorMessage = backendError.detail?.message
      const status_code = backendError.status_code || error.response.status
      const errorCode = backendError.detail?.code

      if (status_code === 401 || errorCode === 'MISSING_TOKEN') {
        // ۱. پاک کردن توکن‌های نامعتبر
        clearStoredTokens()

        // ۲. ریدایرکت به صفحه لاگین
        window.location.href = '/login'
      }
      // فرمت کردن ارور برای استفاده راحت‌تر در کامپوننت‌های Vue
      return Promise.reject({
        status: status_code,
        error_type: errorType,
        message: errorMessage || 'خطایی رخ داده است',
        code: errorCode,
      })
    }

    // خطاهای شبکه
    return Promise.reject({
      status: null,
      message: 'خطا در ارتباط با سرور',
      fullError: error,
    })
  },
)

export default axiosClient
