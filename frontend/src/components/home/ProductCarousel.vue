<template>
  <section class="grid gap-4">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
      <div>
        <h2 class="m-0 text-[clamp(1.35rem,2vw,2rem)] font-bold">{{ title }}</h2>
        <p v-if="subtitle" class="mt-2 text-text-muted text-[0.98rem]">{{ subtitle }}</p>
      </div>
      <router-link to="/products" class="text-primary font-bold">مشاهده همه</router-link>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <ProductCard v-for="product in products" :key="product.id" :product="product" />
    </div>
  </section>
</template>

<script setup>
import ProductCard from '@/components/product/ProductCard.vue';

defineProps({
  title: { type: String, default: 'محصولات' },
  subtitle: { type: String, default: '' },
  products: { type: Array, default: () => [] },
})
</script>
