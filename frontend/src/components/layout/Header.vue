<template>
  <header class="site-header">
    <div class="header-top">
      <div class="container header-top__inner">
        <span>ارسال رایگان برای سفارش بالای ۳۰ میلیون تومان</span>
        <div class="header-top__meta">
          <span>پشتیبانی {{ admin.settings.supportPhone }}</span>
          <span>ضمانت اصالت کالا</span>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="header-main">
        <router-link to="/" class="brand">
          <img src="@/assets/images/logo.jpg" alt="لوگوی فروشگاه" class="brand__logo" />
          <div>
            <strong class="brand__title">{{ admin.settings.storeName }}</strong>
            <span class="brand__subtitle">{{ admin.settings.heroMessage }}</span>
          </div>
        </router-link>

        <form class="header-search" @submit.prevent="submitSearch">
          <span class="header-search__icon">⌕</span>
          <BaseInput v-model="searchQuery" placeholder="جستجوی کالای مورد نظر ..." />
        </form>

        <div class="header-actions">
          <router-link to="/auth" class="header-action header-action--link">
            {{ profileLabel }}
          </router-link>
          <button class="header-action" type="button" @click="toggleMiniCart">
            <span>سبد خرید</span>
            <strong>{{ cart.count }}</strong>
          </button>
          <button class="header-burger" type="button" @click="toggleMobile">☰</button>
        </div>
      </div>

      <nav class="header-nav">
        <router-link to="/">خانه</router-link>
        <router-link to="/products">محصولات</router-link>
        <router-link to="/category/digital">کالای دیجیتال</router-link>
        <router-link to="/category/audio">صوتی و پوشیدنی</router-link>
        <router-link to="/category/home">خانه و آشپزخانه</router-link>
        <router-link to="/category/fashion">مد و استایل</router-link>
        <router-link to="/support">پشتیبانی</router-link>
        <router-link v-if="user.profile?.role === 'admin'" to="/admin">پنل ادمین</router-link>
        <router-link v-if="user.profile?.role === 'admin'" to="/admin/products/new"
          >ادمین محصول</router-link
        >
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

defineOptions({
  name: 'SiteHeader',
})

const admin = useAdminStore()
const ui = useUIStore()
const cart = useCartStore()
const user = useUserStore()
const router = useRouter()
const route = useRoute()
const searchQuery = ref(route.query.q || ui.searchQuery)
const profileLabel = computed(() => {
  if (!user.isAuthenticated) {
    return 'حساب کاربری'
  }

  return user.profile?.first_name ? `سلام ${user.profile.first_name}` : 'حساب من'
})

const toggleMiniCart = () => ui.toggleMiniCart()
const toggleMobile = () => ui.toggleMobileMenu()

function submitSearch() {
  ui.setSearchQuery(searchQuery.value)
  router.push({
    name: 'search',
    query: searchQuery.value ? { q: searchQuery.value } : {},
  })
}

watch(
  () => route.query.q,
  (value) => {
    searchQuery.value = value || ui.searchQuery
  },
)
</script>

<style scoped>
.site-header {
  top: 0;
  z-index: 50;
  backdrop-filter: blur(18px);
  background: rgba(244, 247, 251, 0.72);
  border-bottom: 1px solid rgba(15, 23, 42, 0.06);
}

.header-top {
  background: linear-gradient(90deg, rgba(91, 61, 245, 0.95), rgba(255, 122, 89, 0.92));
  color: #fff;
  font-size: 0.84rem;
}

.header-top__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  min-height: 42px;
}

.header-top__meta {
  display: flex;
  gap: 1.2rem;
  opacity: 0.92;
}

.header-main {
  display: grid;
  grid-template-columns: 280px 1fr auto;
  gap: 1rem;
  align-items: center;
  padding: 1rem 0;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.9rem;
}

.brand__logo {
  width: 58px;
  height: 58px;
  object-fit: cover;
  border-radius: 18px;
  box-shadow: var(--shadow-soft);
}

.brand__title {
  display: block;
  font-size: 1.15rem;
}

.brand__subtitle {
  display: block;
  font-size: 0.82rem;
  color: var(--text-muted);
  display: -webkit-box;
  overflow: hidden;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.header-search {
  position: relative;
}

.header-search :deep(.base-input__control) {
  min-height: 56px;
  padding-right: 2.7rem;
  background: rgba(255, 255, 255, 0.78);
}

.header-search__icon {
  position: absolute;
  inset: 0 auto 0 0;
  display: grid;
  place-items: center;
  width: 48px;
  color: var(--text-muted);
  z-index: 1;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-action {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  min-height: 48px;
  padding: 0 1rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.8);
  color: var(--text);
  font-weight: 700;
}

.header-action strong {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--bg-muted);
  color: var(--primary);
}

.header-action--link {
  color: var(--primary);
}

.header-burger {
  display: none;
  min-height: 48px;
  min-width: 48px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.8);
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 0 1rem;
  overflow-x: auto;
  white-space: nowrap;
}

.header-nav a {
  color: var(--text-muted);
  font-size: 0.92rem;
  padding: 0.6rem 0.9rem;
  border-radius: 999px;
  transition:
    color 0.2s ease,
    background-color 0.2s ease;
}

.header-nav a.router-link-active {
  color: var(--primary);
  background: rgba(91, 61, 245, 0.1);
}

@media (max-width: 980px) {
  .header-main {
    grid-template-columns: 1fr;
  }

  .header-actions {
    justify-content: space-between;
  }
}

@media (max-width: 768px) {
  .header-top__inner,
  .header-top__meta {
    flex-direction: column;
    justify-content: center;
    gap: 0.15rem;
    padding: 0.45rem 0;
  }

  .header-nav,
  .header-action--link {
    display: none;
  }

  .header-burger {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .header-actions {
    gap: 0.5rem;
  }

  .header-action {
    flex: 1;
    justify-content: center;
  }
}
</style>
