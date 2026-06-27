<!-- src/components/product/ProductGrid.vue -->
<!-- یک نمایش سه ستونه از محصولات برای جستجو یا دسته بندی ها -->
<template>
  <div v-if="products.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    <ProductCard v-for="product in products" :key="product.id" :product="product" />
  </div>

  <div v-else class="py-16 text-center text-text-muted">
    <p class="text-[1.1rem]">محصولی یافت نشد.</p>
  </div>
</template>

<script setup>
import ProductCard from './ProductCard.vue';

defineProps({
  products: { type: Array, default: () => [] },
})
</script>
