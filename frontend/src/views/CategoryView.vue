<template>
  <div class="page-shell">
    <section class="page-panel page-hero">
      <span class="pill">دسته‌بندی</span>
      <h1 class="page-title">{{ category?.title || 'دسته‌بندی نامشخص' }}</h1>
      <p class="page-description">{{ category?.description || 'محصولات مرتبط با این دسته را ببینید.' }}</p>
    </section>

    <section v-if="category" class="page-panel category-panel">
      <div class="section-head">
        <div>
          <h2 class="section-title">مرور محصولات</h2>
          <p class="section-subtitle">{{ filteredProducts.length }} محصول در این دسته موجود است</p>
        </div>

        <select v-model="sort" class="category-select">
          <option value="new">جدیدترین</option>
          <option value="cheap">ارزان‌ترین</option>
          <option value="expensive">گران‌ترین</option>
          <option value="rating">بالاترین امتیاز</option>
        </select>
      </div>

      <ProductGrid :products="filteredProducts" />
    </section>

    <section v-else class="empty-state">
      دسته‌بندی موردنظر پیدا نشد.
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import ProductGrid from '@/components/product/ProductGrid.vue'
import { useProductsStore } from '@/stores/products'
import { useRoute } from 'vue-router'

const sort = ref('new')
const route = useRoute()
const productStore = useProductsStore()

const category = computed(() => productStore.getCategoryById(route.params.id))
const filteredProducts = computed(() => {
  const products = [...productStore.getByCategory(route.params.id)]

  switch (sort.value) {
    case 'cheap':
      products.sort((left, right) => left.price - right.price)
      break
    case 'expensive':
      products.sort((left, right) => right.price - left.price)
      break
    case 'rating':
      products.sort((left, right) => right.rating - left.rating)
      break
    default:
      products.sort((left, right) => Number(right.flags.newest) - Number(left.flags.newest))
      break
  }

  return products
})
</script>

<style scoped>
.category-panel {
  padding: 1.5rem;
}

.category-select {
  min-height: 48px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: var(--surface-strong);
  padding: 0 1rem;
  color: var(--text);
}
</style>
