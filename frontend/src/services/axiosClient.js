// src/services/axiosClient.js

import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { clearStoredAccessToken, getStoredAccessToken, persistAccessToken } from '@/utils/token'
import axios from 'axios'

const axiosClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
  // با فعال کردن این گزینه کوکی ها هم به بک اند ارسال میشوند
  withCredentials: true,
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

    const token = getStoredAccessToken().accessToken

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
    const errorStore = useErrorStore()

    // console.log('AXIOS ERROR:', error)
    // console.log('STATUS:', error.response?.status)
    // console.log('DATA:', error.response?.data)

    if (error.response) {
      const backendError = error.response.data || {}
      const status_code = backendError.status_code || error.response.status
      const errorType = backendError.error_type || 'خطای ناشناخته'
      const detail = backendError.detail
      const errorCode = detail?.code || null // دریافت کد خطا برای بررسی در شرط

      // استخراج پیام خطا بر اساس ساختار بک‌اند
      let errorMessage = 'خطایی رخ داده است'
      let validationErrors = null

      if (errorType === 'RequestValidationError') {
        // خطاهای ولیدیشن 422
        errorMessage = 'اطلاعات وارد شده نامعتبر است'
        validationErrors = detail // آرایه خطاهای pydantic
      } else if (detail && detail.message) {
        // خطاهای ServiceError و HttpError
        errorMessage = detail.message
      } else if (typeof detail === 'string') {
        errorMessage = detail
      }

      // ارور مربوط به تعداد درخواست بیش از حد مجاز
      if (status_code === 429 || errorCode === 'RATE_LIMIT_EXCEEDED') {
        const msg = getErrorMessage(errorCode) || getErrorMessage('DEFAULT_429')

        errorStore.addError({
          type: 'warning',
          message: msg,
        })

        return Promise.reject({
          status: 429,
          error_type: errorType,
          message: msg,
          code: errorCode,
          path: backendError.path || null,
        })
      }

      // مدیریت ۴۰۱ و رفرش توکن
      if ((status_code === 401 || errorCode === 'MISSING_TOKEN') && !originalRequest._retry) {
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

        return new Promise(function (resolve, reject) {
          // ارسال درخواست برای دریافت توکن جدید
          axios
            .post('http://127.0.0.1:8000/api/v1/users/token/refresh', {}, { withCredentials: true })
            .then(({ data }) => {
              // سرور اکسس توکن جدید را در پاسخ برمیگرداند و کوکی رفرش جدید را ست میکند
              const newToken = { access_token: data.data.access_token }
              persistAccessToken(newToken) // ذخیره اکسس توکن جدید

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
              clearStoredAccessToken()
              window.location.href = '/login'
              reject(err)
            })
            .finally(() => {
              isRefreshing = false
            })
        })
      }

      // ایجاد خطای استاندارد برای خطاهای غیر ۴۰۱
      const standardError = {
        status: status_code,
        error_type: errorType,
        message: errorMessage,
        code: errorCode,
        validation_errors: validationErrors,
        path: backendError.path || null,
      }

      // الان تنها ارور هایی وارد استور میشن که کد اختصاصی ندارن
      // هدف این کار اینه که تنها ارور های غیر منتطره پاپ آپ بشن
      const isValidationError = errorType === 'RequestValidationError'
      const isBusinessError = !!detail?.code

      if (status_code !== 401 && !isValidationError && !isBusinessError) {
        errorStore.addError({
          type: status_code >= 500 ? 'server' : 'client',
          message: standardError.message,
        })
      }

      return Promise.reject(standardError)
    }

    // خطاهای شبکه (مثل قطعی اینترنت یا CORS)
    const networkError = {
      status: null,
      error_type: 'NetworkError',
      message: 'خطا در ارتباط با سرور. لطفا اتصال اینترنت خود را بررسی کنید.',
      fullError: error,
    }

    errorStore.addError({
      type: 'network',
      message: networkError.message,
    })

    return Promise.reject(networkError)
  },
)

export default axiosClient
