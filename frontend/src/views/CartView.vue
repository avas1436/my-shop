<template>
  <div>
    <h1 class="text-2xl mb-4">سبد خرید</h1>

    <div v-for="item in cart" :key="item.id" class="border p-3 mb-2 rounded">
      {{ item.title }} - {{ item.price }} تومان
    </div>

    <RouterLink
      class="bg-green-600 text-white px-4 py-2 rounded inline-block mt-4"
      to="/checkout"
    >
      ادامه خرید
    </RouterLink>
  </div>
</template>

<script setup>
import { useCartStore } from '../stores/cart'
const store = useCartStore()
const cart = store.items
</script>
