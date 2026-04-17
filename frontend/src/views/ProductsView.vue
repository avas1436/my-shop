<template>
  <div>
    <h1 class="text-2xl mb-4">محصولات</h1>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div
        v-for="p in products"
        :key="p.id"
        class="border p-3 rounded shadow cursor-pointer"
        @click="$router.push('/products/' + p.id)"
      >
        <div class="font-bold">{{ p.title }}</div>
        <div class="text-sm">{{ p.price }} تومان</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProductsStore } from '../stores/products'
const store = useProductsStore()
const products = store.products
</script>
