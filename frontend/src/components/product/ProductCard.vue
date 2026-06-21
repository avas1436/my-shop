<template>
  <article
    class="grid gap-4 p-4 rounded-(--radius-lg) bg-white border border-border-light shadow-soft transition-all duration-200 hover:-translate-y-1 hover:shadow-custom"
  >
    <router-link :to="`/product/${product.id}`" class="relative">
      <img
        :src="product.image"
        :alt="product.title"
        class="w-full aspect-square object-cover rounded-3xl"
      />
      <span
        v-if="discountPercent"
        class="absolute top-3.5 right-3.5 bg-red-500/92 text-white py-1.5 px-2.5 rounded-full text-[0.82rem] font-bold"
      >
        {{ discountPercent }}٪ تخفیف
      </span>
      <span
        v-if="product.stock === 0"
        class="absolute bottom-3.5 right-3.5 bg-slate-900/78 text-white py-1.5 px-2.5 rounded-full text-[0.82rem] font-bold"
      >
        ناموجود
      </span>
    </router-link>

    <div class="grid gap-3.5">
      <div class="flex items-center justify-between gap-3">
        <span class="pill">{{ product.badge }}</span>
        <span class="muted">{{ product.brand }}</span>
      </div>

      <router-link :to="`/product/${product.id}`" class="font-bold text-[1.05rem]">
        {{ product.title }}
      </router-link>

      <p class="m-0 text-text-muted text-[0.92rem]">{{ product.shortDescription }}</p>

      <div class="flex items-center justify-start gap-3 text-[0.9rem]">
        <span>★ {{ product.rating }}</span>
        <span class="muted">({{ product.reviewCount }} نظر)</span>
      </div>

      <div class="flex items-end justify-between gap-3">
        <div>
          <strong class="price">{{ formatPrice(product.price) }}</strong>
          <div v-if="product.oldPrice" class="price-old">{{ formatPrice(product.oldPrice) }}</div>
        </div>
        <BaseButton size="sm" :disabled="product.stock === 0" @click="addToCart">
          {{ product.stock === 0 ? 'ناموجود' : 'افزودن' }}
        </BaseButton>
      </div>
    </div>
  </article>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { useCartStore } from '@/stores/cartStore'
import { formatPrice } from '@/utils/format'
import { computed } from 'vue'

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
