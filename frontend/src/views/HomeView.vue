<!-- src/views/HomeView.vue -->
<template>
  <div class="page-shell">
    <HeroBanner :highlight="featuredProducts[0]" :side-highlights="featuredProducts.slice(1, 3)" />
    <CategoryCarousel :categories="store.categories" />
    <ProductCarousel
      title="پیشنهادهای ویژه"
      subtitle="محصولات منتخب با طراحی جذاب، ارزش خرید بالا و تحویل سریع"
      :products="featuredProducts.slice(0, 4)"
    />
    <PromotionBanner />
    <ProductCarousel
      title="پرفروش‌ترین‌ها"
      subtitle="پرطرفدارترین کالاها بر اساس خرید و رضایت مشتریان"
      :products="bestsellerProducts.slice(0, 4)"
    />
    <BrandsSection :brands="store.brands" />
  </div>
</template>

<script setup>
import BrandsSection from '@/components/home/BrandsSection.vue'
import CategoryCarousel from '@/components/home/CategoryCarousel.vue'
import HeroBanner from '@/components/home/HeroBanner.vue'
import ProductCarousel from '@/components/home/ProductCarousel.vue'
import PromotionBanner from '@/components/home/PromotionBanner.vue'
import { useProductsStore } from '@/stores/products'
import { computed } from 'vue'

const store = useProductsStore()
const featuredProducts = computed(() => store.featuredProducts)
const bestsellerProducts = computed(() => store.bestsellerProducts)
</script>
