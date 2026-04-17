<template>
  <div v-if="product" class="page-shell">
    <section class="detail-layout page-panel">
      <ProductGallery :images="product.gallery" :title="product.title" />

      <div class="detail-content">
        <div class="detail-meta">
          <span class="pill">{{ product.badge }}</span>
          <span class="muted">{{ product.brand }}</span>
        </div>

        <h1 class="page-title detail-title">{{ product.title }}</h1>
        <p class="page-description">{{ product.description }}</p>

        <div class="detail-rating">
          <strong>★ {{ product.rating }}</strong>
          <span class="muted">{{ product.reviewCount }} نظر ثبت شده</span>
        </div>

        <div class="detail-pricing">
          <div>
            <strong class="price detail-price">{{ formatPrice(product.price) }}</strong>
            <div v-if="product.oldPrice" class="price-old">{{ formatPrice(product.oldPrice) }}</div>
          </div>
          <span class="pill">موجودی: {{ product.stock }} عدد</span>
        </div>

        <div class="detail-actions">
          <BaseButton size="lg" block @click="addToCart">افزودن به سبد خرید</BaseButton>
          <router-link to="/cart" class="detail-link">مشاهده سبد خرید</router-link>
        </div>

        <ul class="detail-specs">
          <li v-for="spec in product.specs" :key="spec.label">
            <span>{{ spec.label }}</span>
            <strong>{{ spec.value }}</strong>
          </li>
        </ul>
      </div>
    </section>

    <section class="detail-extra">
      <ProductReview
        class="page-panel"
        :rating="product.rating"
        :count="product.reviewCount"
        :highlights="product.reviewHighlights"
      />

      <div class="page-panel detail-related">
        <div class="section-head">
          <div>
            <h2 class="section-title">محصولات مرتبط</h2>
            <p class="section-subtitle">انتخاب‌هایی از همین دسته برای تکمیل خرید</p>
          </div>
        </div>
        <ProductGrid :products="relatedProducts" />
      </div>
    </section>
  </div>

  <div v-else class="page-shell">
    <section class="empty-state">
      محصول موردنظر پیدا نشد.
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import BaseButton from '@/components/base/BaseButton.vue'
import ProductGallery from '@/components/product/ProductGallery.vue'
import ProductGrid from '@/components/product/ProductGrid.vue'
import ProductReview from '@/components/product/ProductReview.vue'
import { useCartStore } from '@/stores/cartStore'
import { useProductsStore } from '@/stores/products'
import { formatPrice } from '@/utils/format'
import { useRoute } from 'vue-router'

const route = useRoute()
const productStore = useProductsStore()
const cart = useCartStore()

const product = computed(() => productStore.getById(route.params.id))
const relatedProducts = computed(() => productStore.getRelatedProducts(route.params.id))

function addToCart() {
  cart.add(product.value)
}
</script>

<style scoped>
.detail-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  padding: 1.5rem;
}

.detail-content {
  display: grid;
  gap: 1rem;
  align-content: start;
}

.detail-meta,
.detail-rating,
.detail-pricing {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.detail-title {
  font-size: clamp(1.8rem, 3vw, 2.8rem);
}

.detail-price {
  font-size: 1.8rem;
}

.detail-actions {
  display: grid;
  gap: 0.8rem;
}

.detail-link {
  text-align: center;
  padding: 0.85rem 1rem;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: var(--bg-muted);
  color: var(--text);
  font-weight: 700;
}

.detail-specs {
  display: grid;
  gap: 0.75rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.detail-specs li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.9rem 1rem;
  border-radius: 18px;
  background: var(--bg-muted);
}

.detail-extra {
  display: grid;
  gap: 1.25rem;
}

.detail-related {
  padding: 1.5rem;
}

@media (max-width: 920px) {
  .detail-layout {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
}
</style>
