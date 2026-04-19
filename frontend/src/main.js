import './assets/styles/main.css'
import './assets/font/font.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useUIStore } from './stores/uiStore'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

const ui = useUIStore(pinia)
router.afterEach(() => {
  ui.closeMiniCart()
  ui.closeMobileMenu()
})

app.mount('#app')
