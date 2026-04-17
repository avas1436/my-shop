<template>
  <section class="carousel-section">
    <div class="section-head">
      <div>
        <h2 class="section-title">{{ title }}</h2>
        <p class="section-subtitle">{{ subtitle }}</p>
      </div>
      <router-link to="/products" class="carousel-section__link">مشاهده همه</router-link>
    </div>

    <div class="carousel-grid">
      <ProductCard v-for="product in products" :key="product.id" :product="product" />
    </div>
  </section>
</template>

<script setup>
import ProductCard from '@/components/product/ProductCard.vue'

defineProps({
  title: { type: String, default: 'محصولات' },
  subtitle: { type: String, default: '' },
  products: { type: Array, default: () => [] },
})
</script>

<style scoped>
.carousel-section {
  display: grid;
  gap: 1rem;
}

.carousel-section__link {
  color: var(--primary);
  font-weight: 700;
}

.carousel-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

@media (max-width: 1100px) {
  .carousel-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 780px) {
  .carousel-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 540px) {
  .carousel-grid {
    grid-template-columns: 1fr;
  }
}
</style>
