<template>
  <div class="page-shell">
    <section class="page-panel page-hero">
      <span class="pill">فروشگاه ShopVerse</span>
      <h1 class="page-title">همه محصولات</h1>
      <p class="page-description">
        مجموعه‌ای از کالاهای باکیفیت در دسته‌های متنوع با طراحی کارت‌های حرفه‌ای،
        فیلتر سریع و مسیر خرید شفاف.
      </p>
    </section>

    <section class="catalog-layout">
      <aside class="page-panel catalog-sidebar">
        <h2>فیلتر و مرتب‌سازی</h2>

        <label class="catalog-field">
          <span>مرتب‌سازی</span>
          <select v-model="sortBy">
            <option value="featured">پیشنهادی</option>
            <option value="cheap">ارزان‌ترین</option>
            <option value="expensive">گران‌ترین</option>
            <option value="rating">بالاترین امتیاز</option>
          </select>
        </label>

        <label class="catalog-field">
          <span>دسته‌بندی</span>
          <select v-model="selectedCategory">
            <option value="">همه دسته‌ها</option>
            <option v-for="category in store.categories" :key="category.id" :value="category.id">
              {{ category.title }}
            </option>
          </select>
        </label>

        <label class="catalog-check">
          <input v-model="onlyAvailable" type="checkbox" />
          فقط کالاهای موجود
        </label>
      </aside>

      <section class="catalog-main">
        <div class="section-head">
          <div>
            <h2 class="section-title">نتیجه مرور محصولات</h2>
            <p class="section-subtitle">{{ filteredProducts.length }} کالا برای مشاهده آماده است</p>
          </div>
        </div>

        <ProductGrid :products="filteredProducts" />
      </section>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import ProductGrid from '@/components/product/ProductGrid.vue'
import { useProductsStore } from '@/stores/products'

const store = useProductsStore()
const sortBy = ref('featured')
const selectedCategory = ref('')
const onlyAvailable = ref(false)

const filteredProducts = computed(() => {
  let products = [...store.products]

  if (selectedCategory.value) {
    products = products.filter((product) => product.categoryId === selectedCategory.value)
  }

  if (onlyAvailable.value) {
    products = products.filter((product) => product.stock > 0)
  }

  switch (sortBy.value) {
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
      products.sort((left, right) => Number(right.flags.featured) - Number(left.flags.featured))
      break
  }

  return products
})
</script>

<style scoped>
.catalog-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.25rem;
}

.catalog-sidebar {
  padding: 1.25rem;
  display: grid;
  gap: 1rem;
  align-content: start;
  position: sticky;
  top: 132px;
  height: fit-content;
}

.catalog-sidebar h2 {
  margin: 0;
}

.catalog-field {
  display: grid;
  gap: 0.45rem;
}

.catalog-field span {
  font-weight: 700;
}

.catalog-field select {
  min-height: 48px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: var(--surface-strong);
  padding: 0 1rem;
  color: var(--text);
}

.catalog-check {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-weight: 700;
}

.catalog-main {
  display: grid;
  gap: 1rem;
}

@media (max-width: 920px) {
  .catalog-layout {
    grid-template-columns: 1fr;
  }

  .catalog-sidebar {
    position: static;
  }
}
</style>
