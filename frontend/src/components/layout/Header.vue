<template>
  <header class="fixed top-0 right-0 left-0 bg-white border-b shadow-sm z-50">
    <div class="container mx-auto flex items-center justify-between p-4">

      <!-- Right (Logo) -->
      <div class="header-logo">
        <img src='@/assets/images/logo.jpg' class="w-10" alt="logo" />
      </div>

      <!-- Search (Desktop) -->
      <div class="hidden md:block flex-1 px-6">
        <BaseInput placeholder="جستجو محصول…" />
      </div>

      <!-- Left Icons -->
      <div class="flex items-center gap-4">
        <button @click="toggleMiniCart">
          🛒
        </button>

        <!-- Mobile Menu -->
        <button class="md:hidden" @click="toggleMobile">
          ☰
        </button>
      </div>
    </div>

    <MiniCart />
    <MobileNav />
  </header>
</template>

<script setup>
import { useUIStore } from '@/stores/uiStore'
import BaseInput from '../base/BaseInput.vue'
import MiniCart from './MiniCart.vue'
import MobileNav from './MobileNav.vue'

const ui = useUIStore()

const toggleMiniCart = () => ui.toggleMiniCart()
const toggleMobile = () => ui.toggleMobileMenu()
</script>
