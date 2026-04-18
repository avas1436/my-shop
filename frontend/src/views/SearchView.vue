<template>
  <div class="page-shell">
    <section class="page-panel page-hero">
      <span class="pill">جستجو</span>
      <h1 class="page-title">نتایج برای "{{ query || 'همه محصولات' }}"</h1>
      <p class="page-description">
        {{ results.length }} نتیجه پیدا شد. می‌توانید از هدر سایت عبارت جدیدی جستجو کنید.
      </p>
    </section>

    <section v-if="results.length" class="page-panel search-panel">
      <ProductGrid :products="results" />
    </section>

    <section v-else class="empty-state">
      نتیجه‌ای برای عبارت جستجو پیدا نشد.
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ProductGrid from '@/components/product/ProductGrid.vue'
import { useProductsStore } from '@/stores/products'
import { useRoute } from 'vue-router'

const route = useRoute()
const productStore = useProductsStore()
const query = computed(() => route.query.q || '')
const results = computed(() => productStore.search(query.value))
</script>

<style scoped>
.search-panel {
  padding: 1.5rem;
}
</style>
