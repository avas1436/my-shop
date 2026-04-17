<template>
  <div>
    <HeroBanner />

    <CategoryCarousel class="mt-8" />

    <ProductCarousel
      title="پیشنهاد ویژه"
      :products="specialProducts"
      class="mt-12"
    />

    <PromotionBanner class="mt-12" />

    <ProductCarousel
      title="پرفروش‌ترین‌ها"
      :products="bestsellers"
      class="mt-12"
    />

    <BrandsSection class="mt-12" />

  </div>
</template>

<script setup>
import HeroBanner from '@/components/home/HeroBanner.vue'
import CategoryCarousel from '@/components/home/CategoryCarousel.vue'
import ProductCarousel from '@/components/home/ProductCarousel.vue'
import PromotionBanner from '@/components/home/PromotionBanner.vue'
import BrandsSection from '@/components/home/BrandsSection.vue'

const specialProducts = [
  { id: 1, title: 'محصول A', price: 120000, image: '/p1.jpg' },
  { id: 2, title: 'محصول B', price: 180000, image: '/p2.jpg' }
]

const bestsellers = specialProducts
</script>
