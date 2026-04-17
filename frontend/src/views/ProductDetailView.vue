<template>
  <div class="container mx-auto p-4">

    <ProductGallery :images="product.images" />

    <h1 class="mt-4 text-lg font-bold">{{ product.title }}</h1>

    <div class="mt-2 text-blue-600 font-bold text-xl">
      {{ product.price }} تومان
    </div>

    <div class="mt-4">
      <BaseButton @click="addToCart" class="w-full">
        افزودن به سبد خرید
      </BaseButton>
    </div>

    <div class="mt-8">
      <h2 class="text-lg font-bold mb-2">توضیحات</h2>
      <p class="text-sm leading-7 text-gray-700">{{ product.description }}</p>
    </div>

  </div>
</template>

<script setup>
import ProductGallery from '@/components/product/ProductGallery.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '@/stores/productStore'
import { useCartStore } from '@/stores/cartStore'

const route = useRoute()
const productStore = useProductStore()
const cart = useCartStore()

const product = productStore.getProductById(route.params.id)

function addToCart() {
  cart.add(product)
}
</script>
