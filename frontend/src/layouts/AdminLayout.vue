<!-- src/layouts/AdminLayout.vue -->
<template>
  <div
    class="min-h-screen bg-[#eff3fb]"
    style="
      background-image:
        radial-gradient(circle at top right, rgba(91, 61, 245, 0.14), transparent 22%),
        radial-gradient(circle at left bottom, rgba(255, 122, 89, 0.12), transparent 24%);
    "
  >
    <!-- موبایل: overlay پشت sidebar -->
    <div
      class="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs transition-opacity duration-300 lg:hidden"
      :class="isSidebarOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'"
      @click="isSidebarOpen = false"
    />

    <!-- Wrapper: Sidebar + Content -->
    <div class="flex h-screen">
      <!-- Sidebar - موبایل: fixed، دسکتاپ: static -->
      <div
        class="w-72.5 shrink-0 fixed inset-y-0 right-0 z-50 transition-transform duration-300 lg:static lg:z-auto lg:translate-x-0"
        :class="isSidebarOpen ? 'translate-x-0' : 'translate-x-full'"
      >
        <Sidebar />
      </div>

      <!-- محتوای اصلی - فقط این اسکرول می‌کند -->
      <div class="flex-1 overflow-y-auto">
        <!-- Header - ثابت در بالا -->
        <header
          class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-5 p-3 lg:p-5 lg:py-[1.4rem] lg:px-6 rounded-lg border border-border-light bg-white/85 backdrop-blur-md shadow-(--shadow-soft) m-3 lg:m-5"
        >
          <div class="flex items-start md:items-center gap-4">
            <button
              class="flex lg:hidden items-center justify-center p-2 border border-border-light rounded-md text-text-main bg-transparent cursor-pointer"
              aria-label="باز و بسته کردن منو"
              @click="isSidebarOpen = !isSidebarOpen"
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
                aria-hidden="true"
              >
                <line x1="3" y1="12" x2="21" y2="12" />
                <line x1="3" y1="6" x2="21" y2="6" />
                <line x1="3" y1="18" x2="21" y2="18" />
              </svg>
            </button>
            <div>
              <span class="pill">پنل مدیریت</span>
              <h1 class="m-0 mt-2.5 text-[clamp(1.5rem,3vw,2.2rem)] font-bold">
                مدیریت فروشگاه {{ admin.settings.storeName }}
              </h1>
            </div>
          </div>
          <router-link
            to="/"
            class="inline-flex items-center justify-center min-h-12 px-4 rounded-full bg-linear-to-br from-primary to-primary-dark text-white font-bold whitespace-nowrap w-full md:w-auto"
          >
            بازگشت به فروشگاه
          </router-link>
        </header>

        <!-- محتوای اصلی - اسکرول می‌شود -->
        <section class="flex-1 p-3 lg:p-5 grid gap-4 min-w-0 overflow-y-auto">
          <RouterView />
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/layout/Sidebar.vue'
import { useAdminStore } from '@/stores/adminStore'
import { ref, watch } from 'vue'
import { RouterView, useRoute } from 'vue-router'

const admin = useAdminStore()
const isSidebarOpen = ref(false)
const route = useRoute()

watch(
  () => route.path,
  () => {
    isSidebarOpen.value = false
  },
)
</script>
