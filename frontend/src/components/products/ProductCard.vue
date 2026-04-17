<template>
  <div class="bg-white rounded-lg shadow p-3 hover:shadow-md transition">

    <!-- Image -->
    <div class="relative">
      <img :src="product.image" class="w-full rounded" />

      <div v-if="product.discount"
           class="absolute top-2 right-2 bg-red-500 text-white text-xs px-2 py-1 rounded">
        {{ product.discount }}٪
      </div>
    </div>

    <!-- Title -->
    <h3 class="mt-3 text-sm font-medium line-clamp-2">
      {{ product.title }}
    </h3>

    <!-- Price -->
    <div class="mt-2 flex items-center gap-2">
      <span class="font-bold text-blue-600">
        {{ product.price }} تومان
      </span>

      <del v-if="product.oldPrice" class="text-gray-400 text-xs">
        {{ product.oldPrice }}
      </del>
    </div>

    <!-- Rating -->
    <div class="mt-1 text-yellow-500 text-xs">
      ⭐⭐⭐⭐☆
    </div>

    <!-- CTA -->
    <button @click="addToCart"
            class="mt-3 w-full bg-blue-600 text-white text-sm py-2 rounded hover:bg-blue-700">
      افزودن به سبد
    </button>

  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cartStore'
const props = defineProps({
  product: Object
})

const cart = useCartStore()

function addToCart() {
  cart.add(props.product)
}
</script>
