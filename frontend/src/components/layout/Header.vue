<!-- src/components/layout/Header.vue -->
<template>
  <header class="sticky top-0 z-50 backdrop-blur-[18px] bg-bg/72 border-b border-slate-900/5">
    <div class="bg-linear-to-r from-primary/95 to-accent/92 text-white text-[0.84rem]">
      <div
        class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-1 md:gap-4 min-h-10.5 py-1.5 md:py-0"
      >
        <span>ارسال رایگان برای سفارش بالای ۳۰ میلیون تومان</span>
        <div class="flex flex-col md:flex-row md:gap-5 opacity-90 items-center">
          <span>پشتیبانی {{ admin.settings.supportPhone }}</span>
          <span>ضمانت اصالت کالا</span>
        </div>
      </div>
    </div>

    <div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-[280px_1fr_auto] gap-4 items-center py-4">
        <router-link to="/" class="flex items-center gap-3.5">
          <img
            src="@/assets/images/logo.jpg"
            alt="لوگوی فروشگاه"
            class="w-14.5 h-14.5 object-cover rounded-md shadow-(--shadow-soft)"
          />
          <div>
            <strong class="block text-[1.15rem]">{{ admin.settings.storeName }}</strong>
            <span class="block text-[0.82rem] text-text-muted line-clamp-2">{{
              admin.settings.heroMessage
            }}</span>
          </div>
        </router-link>

        <form
          class="relative [&_input]:min-h-14 [&_input]:pr-12 [&_input]:bg-white/80"
          @submit.prevent="submitSearch"
        >
          <span
            class="absolute inset-y-0 right-0 flex items-center justify-center w-12 text-text-muted z-10"
            >⌕</span
          >
          <BaseInput v-model="searchQuery" placeholder="جستجوی کالای مورد نظر ..." />
        </form>

        <div class="flex justify-between md:justify-start items-center gap-2 md:gap-3">
          <router-link
            to="/auth"
            class="hidden md:inline-flex items-center gap-2.5 min-h-12 px-4 border border-border-light rounded-full bg-white/80 text-primary font-bold"
          >
            {{ profileLabel }}
          </router-link>

          <button
            class="flex-1 md:flex-none inline-flex items-center justify-center gap-2.5 min-h-12 px-4 border border-border-light rounded-full bg-white/80 text-text-main font-bold"
            type="button"
            @click="toggleMiniCart"
          >
            <span>سبد خرید</span>
            <strong class="w-7 h-7 grid place-items-center rounded-full bg-bg-muted text-primary">{{
              cart.count
            }}</strong>
          </button>

          <button
            class="inline-flex md:hidden items-center justify-center min-h-12 min-w-12 rounded-2xl border border-border-light bg-white/80"
            type="button"
            @click="toggleMobile"
          >
            ☰
          </button>
        </div>
      </div>

      <nav class="hidden md:flex items-center gap-4 pb-4 overflow-x-auto whitespace-nowrap">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="text-text-muted text-[0.92rem] py-2 px-3.5 rounded-full transition-colors duration-200 hover:text-text-main [&.router-link-active]:text-primary [&.router-link-active]:bg-primary/10"
        >
          {{ link.label }}
        </router-link>
      </nav>
    </div>

    <MiniCart />
    <MobileNav />
  </header>
</template>

<script setup>
import { useAdminStore } from '@/stores/adminStore'
import { useCartStore } from '@/stores/cartStore'
import { useUIStore } from '@/stores/uiStore'
import { useUserStore } from '@/stores/userStore'
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseInput from '../base/BaseInput.vue'
import MiniCart from './MiniCart.vue'
import MobileNav from './MobileNav.vue'

defineOptions({ name: 'SiteHeader' })

const admin = useAdminStore()
const ui = useUIStore()
const cart = useCartStore()
const user = useUserStore()
const router = useRouter()
const route = useRoute()
const searchQuery = ref(route.query.q || ui.searchQuery)

const profileLabel = computed(() =>
  !user.isAuthenticated
    ? 'حساب کاربری'
    : user.profile?.first_name
      ? `سلام ${user.profile.first_name}`
      : 'حساب من',
)

const toggleMiniCart = () => ui.toggleMiniCart()
const toggleMobile = () => ui.toggleMobileMenu()

function submitSearch() {
  ui.setSearchQuery(searchQuery.value)
  router.push({ name: 'search', query: searchQuery.value ? { q: searchQuery.value } : {} })
}

watch(
  () => route.query.q,
  (value) => {
    searchQuery.value = value || ui.searchQuery
  },
)

const navLinks = computed(() => {
  const links = [
    { to: '/', label: 'خانه' },
    { to: '/products', label: 'محصولات' },
    { to: '/category/digital', label: 'کالای دیجیتال' },
    { to: '/category/audio', label: 'صوتی و پوشیدنی' },
    { to: '/category/home', label: 'خانه و آشپزخانه' },
    { to: '/category/fashion', label: 'مد و استایل' },
    { to: '/support', label: 'پشتیبانی' },
  ]
  if (user.profile?.role === 'admin') {
    links.push({ to: '/admin', label: 'پنل ادمین' })
  }
  return links
})
</script>
