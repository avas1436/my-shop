<template>
  <div>
    <h1 class="text-2xl mb-4">{{ product?.title }}</h1>

    <p>{{ product?.description }}</p>
    <p class="font-bold mt-4">{{ product?.price }} تومان</p>

    <button
      class="bg-blue-500 text-white px-4 py-2 rounded mt-4"
      @click="addToCart"
    >
      افزودن به سبد خرید
    </button>
  </div>
</template>

<script setup>
import { useProductsStore } from '../stores/products'
import { useCartStore } from '../stores/cart'
import { useRoute } from 'vue-router'

const route = useRoute()
const productStore = useProductsStore()
const cartStore = useCartStore()

const product = productStore.getById(route.params.id)
const addToCart = () => cartStore.add(product)
</script>
