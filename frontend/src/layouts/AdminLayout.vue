<template>
  <div class="admin-shell">
    <Sidebar />

    <div class="admin-main">
      <header class="admin-topbar">
        <div>
          <span class="pill">پنل مدیریت</span>
          <h1>مدیریت فروشگاه ShopVerse</h1>
          <p>
            دید کلی از فروش، سفارش‌ها، محصولات و تنظیمات محتوایی فروشگاه در یک نمای یکپارچه.
          </p>
        </div>

        <router-link to="/" class="admin-topbar__link">بازگشت به فروشگاه</router-link>
      </header>

      <section class="admin-content">
        <RouterView />
      </section>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Sidebar from '@/components/layout/Sidebar.vue'
</script>

<style scoped>
.admin-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 290px 1fr;
  background:
    radial-gradient(circle at top right, rgba(91, 61, 245, 0.14), transparent 22%),
    radial-gradient(circle at left bottom, rgba(255, 122, 89, 0.12), transparent 24%),
    #eff3fb;
}

.admin-main {
  padding: 1.25rem;
  display: grid;
  gap: 1rem;
}

.admin-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.4rem 1.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.86);
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow-soft);
}

.admin-topbar h1,
.admin-topbar p {
  margin: 0;
}

.admin-topbar h1 {
  margin-top: 0.6rem;
  font-size: clamp(1.5rem, 3vw, 2.2rem);
}

.admin-topbar p {
  margin-top: 0.45rem;
  color: var(--text-muted);
  max-width: 64ch;
}

.admin-topbar__link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 1.1rem;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  font-weight: 700;
  white-space: nowrap;
}

.admin-content {
  display: grid;
}

@media (max-width: 1080px) {
  .admin-shell {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-topbar {
    flex-direction: column;
    align-items: start;
    padding: 1.15rem;
  }
}
</style>
