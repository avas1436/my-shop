<template>
  <div class="admin-shell" :class="{ 'sidebar-open': isSidebarOpen }">
    <div class="sidebar-backdrop" @click="isSidebarOpen = false"></div>

    <div class="admin-sidebar-wrapper">
      <Sidebar />
    </div>

    <div class="admin-main">
      <header class="admin-topbar">
        <div class="topbar-right-zone">
          <button
            class="menu-toggle-btn"
            @click="isSidebarOpen = !isSidebarOpen"
            aria-label="Toggle Menu"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </button>

          <div>
            <span class="pill">پنل مدیریت</span>
            <h1>مدیریت فروشگاه {{ admin.settings.storeName }}</h1>
          </div>
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
import Sidebar from '@/components/layout/Sidebar.vue'
import { useAdminStore } from '@/stores/adminStore'
import { ref } from 'vue'
import { RouterView } from 'vue-router'

const admin = useAdminStore()
const isSidebarOpen = ref(false)
</script>

<style scoped>
.admin-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 290px 1fr;
  background:
    radial-gradient(circle at top right, rgba(91, 61, 245, 0.14), transparent 22%),
    radial-gradient(circle at left bottom, rgba(255, 122, 89, 0.12), transparent 24%), #eff3fb;
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
.topbar-right-zone {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* دکمه منو در دسکتاپ مخفی است */
.menu-toggle-btn {
  display: none;
  background: none;
  border: 1px solid var(--border);
  padding: 0.5rem;
  border-radius: var(--radius-md, 8px);
  cursor: pointer;
  color: var(--text-main, #333);
  align-items: center;
  justify-content: center;
}

.sidebar-backdrop {
  display: none;
}

/* ===================================================
   Media Queries (بهینه‌سازی برای تبلت و موبایل)
   =================================================== */

@media (max-width: 1080px) {
  .admin-shell {
    grid-template-columns: 1fr;
  }

  .menu-toggle-btn {
    display: flex;
  }

  .admin-sidebar-wrapper {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: 290px;
    z-index: 999;
    background: #fff;
    box-shadow: -4px 0 24px rgba(0, 0, 0, 0.15);
    transform: translateX(100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .sidebar-open .admin-sidebar-wrapper {
    transform: translateX(0);
  }

  /* اصلاح این بخش: display: block فقط اینجا فعال میشه */
  .sidebar-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.4);
    backdrop-filter: blur(4px);
    z-index: 998;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
  }

  .sidebar-open .sidebar-backdrop {
    opacity: 1;
    pointer-events: auto;
  }

  .admin-main {
    padding: 0.75rem;
  }
}

@media (max-width: 768px) {
  .admin-topbar {
    flex-direction: column;
    align-items: stretch; /* دکمه بازگشت به فروشگاه عریض‌تر و خوش‌دست‌تر شود */
    padding: 1rem;
    gap: 1.25rem;
  }

  .admin-topbar__link {
    width: 100%; /* دکمه در موبایل تمام‌عرض می‌شود تا تاچ‌تارگت بهتری داشته باشد */
  }

  .topbar-right-zone {
    align-items: flex-start;
  }
}
</style>
