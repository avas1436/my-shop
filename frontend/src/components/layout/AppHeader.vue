<template>
  <header class="shadow bg-white p-4 sticky top-0 z-50">
    <div class="container mx-auto flex justify-between items-center">
      <div class="text-xl font-bold">فروشگاه من</div>

      <nav class="hidden md:flex gap-6">
        <RouterLink to="/">خانه</RouterLink>
        <RouterLink to="/products">محصولات</RouterLink>
        <RouterLink to="/cart">سبد خرید</RouterLink>
      </nav>

      <button class="md:hidden" @click="toggleMenu">☰</button>
    </div>

    <div v-if="menuOpen" class="md:hidden mt-2 p-4 bg-gray-100">
      <RouterLink class="block mb-2" to="/">خانه</RouterLink>
      <RouterLink class="block mb-2" to="/products">محصولات</RouterLink>
      <RouterLink class="block mb-2" to="/cart">سبد خرید</RouterLink>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
const menuOpen = ref(false)
const toggleMenu = () => (menuOpen.value = !menuOpen.value)
</script>
