<template>
  <div
    class="min-h-screen grid grid-cols-1 lg:grid-cols-[290px_1fr] bg-[#eff3fb] relative overflow-hidden"
    style="
      background-image:
        radial-gradient(circle at top right, rgba(91, 61, 245, 0.14), transparent 22%),
        radial-gradient(circle at left bottom, rgba(255, 122, 89, 0.12), transparent 24%);
    "
  >
    <div
      class="fixed inset-0 z-998 bg-slate-900/40 backdrop-blur-xs transition-opacity duration-300 lg:hidden"
      :class="isSidebarOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'"
      @click="isSidebarOpen = false"
    ></div>

    <div
      class="fixed inset-y-0 right-0 z-999 w-72.5 bg-white shadow-[-4px_0_24px_rgba(0,0,0,0.15)] transition-transform duration-300 ease-in-out lg:static lg:translate-x-0 lg:shadow-none"
      :class="isSidebarOpen ? 'translate-x-0' : 'translate-x-full'"
    >
      <Sidebar />
    </div>

    <div class="p-3 lg:p-5 grid gap-4">
      <header
        class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-5 p-4 lg:py-[1.4rem] lg:px-6 rounded-lg border border-border bg-white/86 backdrop-blur-md shadow-soft"
      >
        <div class="flex items-start md:items-center gap-4">
          <button
            class="flex lg:hidden items-center justify-center p-2 border border-border rounded-md text-text-main bg-transparent cursor-pointer"
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

      <section class="grid">
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
