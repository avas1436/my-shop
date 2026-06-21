<template>
  <Teleport to="body">
    <div v-if="ui.mobileMenu" class="fixed inset-0 z-65">
      <button
        class="absolute inset-0 w-full h-full border-0 bg-slate-900/40 backdrop-blur-[6px]"
        type="button"
        @click="close"
      ></button>

      <aside
        class="absolute top-0 right-0 w-[min(320px,100%)] h-full p-5 bg-white/96 shadow-custom border-l border-border-light flex flex-col"
      >
        <div class="flex items-start justify-between gap-4 mb-4">
          <div>
            <h2 class="m-0 font-bold">دسترسی سریع</h2>
            <p class="m-0 text-text-muted text-[0.88rem] mt-1.5">
              مسیرهای اصلی فروشگاه و مدیریت را یکجا ببینید.
            </p>
          </div>
          <button
            type="button"
            class="w-10.5 h-10.5 rounded-xl border border-border-light bg-transparent flex items-center justify-center"
            @click="close"
          >
            ✕
          </button>
        </div>

        <nav class="grid gap-2.5 overflow-y-auto pb-6">
          <router-link
            v-for="link in links"
            :key="link.to"
            @click="close"
            :to="link.to"
            class="py-3.5 px-4 rounded-md bg-bg-muted text-text-main font-bold hover:bg-border-light transition-colors [&.router-link-active]:bg-primary/10 [&.router-link-active]:text-primary"
          >
            {{ link.label }}
          </router-link>
        </nav>
      </aside>
    </div>
  </Teleport>
</template>

<script setup>
import { useUIStore } from '@/stores/uiStore';

const ui = useUIStore()
const close = () => ui.closeMobileMenu()

const links = [
  { to: '/', label: 'خانه' },
  { to: '/products', label: 'فروشگاه' },
  { to: '/category/digital', label: 'کالای دیجیتال' },
  { to: '/category/audio', label: 'صوتی و پوشیدنی' },
  { to: '/category/home', label: 'خانه و آشپزخانه' },
  { to: '/category/fashion', label: 'مد و استایل' },
  { to: '/support', label: 'پشتیبانی' },
  { to: '/profile', label: 'پروفایل' },
  { to: '/cart', label: 'سبد خرید' },
  { to: '/admin', label: 'پنل ادمین' },
]
</script>
