<template>
  <div
    v-if="ui.mobileMenu"
    class="fixed top-0 right-0 w-72 h-full bg-white z-40 shadow-xl p-4 border-l"
  >
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-lg font-bold">منو</h2>
      <button @click="close">✕</button>
    </div>

    <nav class="flex flex-col gap-4 text-sm">
      <router-link @click="close" to="/" class="border-b pb-2">خانه</router-link>
      <router-link @click="close" to="/category/1" class="border-b pb-2">دسته‌ها</router-link>
      <router-link @click="close" to="/search?q=all" class="border-b pb-2">جستجو</router-link>
      <router-link @click="close" to="/profile" class="border-b pb-2">پروفایل</router-link>
      <router-link @click="close" to="/cart" class="border-b pb-2">سبد خرید</router-link>
    </nav>

  </div>
</template>

<script setup>
import { useUIStore } from '@/stores/uiStore'

const ui = useUIStore()
const close = () => ui.toggleMobileMenu()
</script>
