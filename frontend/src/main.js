// src/main.js
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import './assets/font/font.css'
import './assets/styles/admin-product-workflow.css'
import './assets/styles/main.css'

import App from './App.vue'
import router from './router'
import { useUIStore } from './stores/uiStore'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// خطاهای سراسری
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err, info)
}

// مدیریت UI بعد از هر route
const ui = useUIStore(pinia)
router.afterEach(() => {
  ui.closeMiniCart()
  ui.closeMobileMenu()
})

app.mount('#app')
