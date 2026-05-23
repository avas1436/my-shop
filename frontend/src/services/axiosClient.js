// src/services/axiosClient.js

import { clearStoredTokens, getStoredTokens, persistTokens } from '@/utils/token'
import axios from 'axios'

const axiosClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

// --- متغیرهای مربوط به مدیریت صف رفرش توکن ---

let isRefreshing = false // آیا در حال گرفتن توکن جدید هستیم؟
let failedQueue = [] // اتاق انتظار درخواست های نیازمند احراز هویت

// مسئول خالی کردن اتاق انتظار بعد از دریافت توکن جدید.
const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

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

  async (error) => {
    const originalRequest = error.config

    if (error.response) {
      const backendError = error.response.data || {}
      const status_code = backendError.status_code || error.response.status

      if (status_code === 401 || errorCode === 'MISSING_TOKEN') {
        if (isRefreshing) {
          return new Promise(function (resolve, reject) {
            failedQueue.push({ resolve, reject })
          })
            .then((token) => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              return axiosClient(originalRequest)
            })
            .catch((err) => {
              return Promise.reject(err)
            })
        }

        originalRequest._retry = true
        isRefreshing = true

        const refreshToken = getStoredTokens().refreshToken

        // اگر رفرش توکن اصلا وجود ندارد، کاربر را خارج کن
        if (!refreshToken) {
          clearStoredTokens()
          window.location.href = '/login'
          return Promise.reject(error)
        }

        return new Promise(function (resolve, reject) {
          // ارسال درخواست برای دریافت توکن جدید
          axios
            .post('http://127.0.0.1:8000/api/v1/users/token/refresh', {
              refresh_token: refreshToken,
            })
            .then(({ data }) => {
              // فرض بر این است که بک‌‌اند توکن‌های جدید را داخل data.data برمی‌گرداند
              const newToken = data.data

              // ذخیره توکن‌های جدید
              persistTokens(newToken)

              // بروزرسانی هدر درخواست اصلی
              axiosClient.defaults.headers.common['Authorization'] =
                `Bearer ${newToken.access_token}`
              originalRequest.headers.Authorization = `Bearer ${newToken.access_token}`

              // پردازش سایر درخواست‌های منتظر در صف
              processQueue(null, newToken.access_token)
              resolve(axiosClient(originalRequest))
            })
            .catch((err) => {
              // اگر خود درخواست رفرش توکن هم خطا داد
              processQueue(err, null)
              clearStoredTokens()
              window.location.href = '/login'
              reject(err)
            })
            .finally(() => {
              isRefreshing = false
            })
        })
      }

      // مدیریت سایر خطاها
      const errorType = backendError.error_type
      const errorMessage = backendError.detail?.message
      const errorCode = backendError.detail?.code

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
