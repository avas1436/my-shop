<template>
  <div class="container mx-auto p-4">

    <h1 class="text-lg font-bold mb-4">
      نتایج جستجو برای "{{ route.query.q }}"
    </h1>

    <ProductGrid :products="results" />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import ProductGrid from '@/components/product/ProductGrid.vue'
import { useProductStore } from '@/stores/productStore'

const route = useRoute()
const productStore = useProductStore()
const results = productStore.search(route.query.q)
</script>
