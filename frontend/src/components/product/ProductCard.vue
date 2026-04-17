<template>
  <article class="product-card">
    <router-link :to="`/product/${product.id}`" class="product-card__image-wrap">
      <img :src="product.image" :alt="product.title" class="product-card__image" />
      <span v-if="discountPercent" class="product-card__badge">{{ discountPercent }}٪ تخفیف</span>
    </router-link>

    <div class="product-card__content">
      <div class="product-card__meta">
        <span class="pill">{{ product.badge }}</span>
        <span class="muted">{{ product.brand }}</span>
      </div>

      <router-link :to="`/product/${product.id}`" class="product-card__title">
        {{ product.title }}
      </router-link>

      <p class="product-card__description">{{ product.shortDescription }}</p>

      <div class="product-card__rating">
        <span>★ {{ product.rating }}</span>
        <span class="muted">({{ product.reviewCount }} نظر)</span>
      </div>

      <div class="product-card__price">
        <div>
          <strong class="price">{{ formatPrice(product.price) }}</strong>
          <div v-if="product.oldPrice" class="price-old">{{ formatPrice(product.oldPrice) }}</div>
        </div>
        <BaseButton size="sm" @click="addToCart">افزودن</BaseButton>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import BaseButton from '@/components/base/BaseButton.vue'
import { useCartStore } from '@/stores/cartStore'
import { formatPrice } from '@/utils/format'

const props = defineProps({
  product: { type: Object, required: true },
})

const cart = useCartStore()
const discountPercent = computed(() => {
  if (!props.product.oldPrice || props.product.oldPrice <= props.product.price) {
    return 0
  }

  return Math.round(((props.product.oldPrice - props.product.price) / props.product.oldPrice) * 100)
})

function addToCart() {
  cart.add(props.product)
}
</script>

<style scoped>
.product-card {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border-radius: var(--radius-lg);
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-soft);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow);
}

.product-card__image-wrap {
  position: relative;
}

.product-card__image {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 24px;
}

.product-card__badge {
  position: absolute;
  top: 0.85rem;
  right: 0.85rem;
  background: rgba(239, 68, 68, 0.92);
  color: #fff;
  padding: 0.35rem 0.6rem;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 700;
}

.product-card__content {
  display: grid;
  gap: 0.8rem;
}

.product-card__meta,
.product-card__price,
.product-card__rating {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.product-card__title {
  font-weight: 700;
  font-size: 1.05rem;
}

.product-card__description {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.92rem;
}

.product-card__rating {
  justify-content: start;
  font-size: 0.9rem;
}

.product-card__price {
  align-items: end;
}
</style>
