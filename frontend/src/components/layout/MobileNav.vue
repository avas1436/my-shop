<template>
  <Teleport to="body">
    <div v-if="ui.mobileMenu" class="mobile-nav-shell">
      <button class="mobile-nav__overlay" type="button" @click="close"></button>

      <aside class="mobile-nav">
        <div class="mobile-nav__header">
          <div>
            <h2>دسترسی سریع</h2>
            <p>مسیرهای اصلی فروشگاه و مدیریت را یکجا ببینید.</p>
          </div>
          <button type="button" @click="close">✕</button>
        </div>

        <nav class="mobile-nav__links">
          <router-link @click="close" to="/">خانه</router-link>
          <router-link @click="close" to="/products">فروشگاه</router-link>
          <router-link @click="close" to="/category/digital">کالای دیجیتال</router-link>
          <router-link @click="close" to="/category/audio">صوتی و پوشیدنی</router-link>
          <router-link @click="close" to="/category/home">خانه و آشپزخانه</router-link>
          <router-link @click="close" to="/category/fashion">مد و استایل</router-link>
          <router-link @click="close" to="/support">پشتیبانی</router-link>
          <router-link @click="close" to="/profile">پروفایل</router-link>
          <router-link @click="close" to="/cart">سبد خرید</router-link>
          <router-link @click="close" to="/admin">پنل ادمین</router-link>
        </nav>
      </aside>
    </div>
  </Teleport>
</template>

<script setup>
import { useUIStore } from '@/stores/uiStore'

const ui = useUIStore()
const close = () => ui.closeMobileMenu()
</script>

<style scoped>
.mobile-nav-shell {
  position: fixed;
  inset: 0;
  z-index: 65;
}

.mobile-nav__overlay {
  position: absolute;
  inset: 0;
  border: 0;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(6px);
}

.mobile-nav {
  position: absolute;
  top: 0;
  right: 0;
  width: min(320px, 100%);
  height: 100%;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: var(--shadow);
  border-left: 1px solid var(--border);
}

.mobile-nav__header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.mobile-nav__header h2,
.mobile-nav__header p {
  margin: 0;
}

.mobile-nav__header p {
  color: var(--text-muted);
  font-size: 0.88rem;
  margin-top: 0.3rem;
}

.mobile-nav__header button {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: transparent;
}

.mobile-nav__links {
  display: grid;
  gap: 0.65rem;
}

.mobile-nav__links a {
  padding: 0.95rem 1rem;
  border-radius: 18px;
  background: var(--bg-muted);
  color: var(--text);
  font-weight: 700;
}
</style>
