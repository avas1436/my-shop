// src/main.js
import { createPinia } from 'pinia'
import { createApp } from 'vue'

// وارد کردن فایل‌های استایل
import './assets/font/font.css'
import './assets/styles/main.css'

import App from './App.vue'
import router from './router'
import { useErrorStore } from './stores/errorStore'
import { useUIStore } from './stores/uiStore'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

const errorStore = useErrorStore(pinia)

// مدیریت خطاهای داخلی سیستم (Vue)
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue System Error:', err, info)
  errorStore.addError({
    type: 'system',
    message: 'خطای سیستمی رخ داده است. لطفا صفحه را رفرش کنید.',
  })
}

// مدیریت خطاهای جاوا اسکریپت خارج از Vue
window.addEventListener('error', (event) => {
  console.error('Global JS Error:', event.error)
  errorStore.addError({ type: 'system', message: 'خطای غیرمنتظره‌ای رخ داد.' })
})

// مدیریت Promise های هندل نشده (مثل خطاهای axios که catch نشوند)
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled Promise Rejection:', event.reason)
  // در صورتی که ساختار استاندارد داشت (از axios آمد)، آن را نادیده بگیر چون قبلا ثبت شده
  if (!event.reason || !event.reason.error_type) {
    errorStore.addError({ type: 'system', message: 'خطای پردازش داده رخ داد.' })
  }
})

// مدیریت UI بعد از هر route
const ui = useUIStore(pinia)
router.afterEach(() => {
  ui.closeMiniCart()
  ui.closeMobileMenu()
})

app.mount('#app')
