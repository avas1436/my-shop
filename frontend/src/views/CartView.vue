<template>
  <div class="container mx-auto p-4">

    <h1 class="text-xl font-bold mb-6">سبد خرید</h1>

    <div v-if="cart.items.length === 0" class="text-center text-gray-500">
      سبد خرید شما خالی است
    </div>

    <div v-else class="grid lg:grid-cols-3 gap-6">

      <!-- Items -->
      <div class="lg:col-span-2 bg-white p-4 rounded shadow">
        <div
          v-for="item in cart.items"
          :key="item.id"
          class="flex gap-4 border-b py-4"
        >
          <img :src="item.image" class="w-20 rounded" />

          <div class="flex-1">
            <h3 class="text-sm font-bold">{{ item.title }}</h3>
            <div class="text-blue-600 font-bold mt-2">
              {{ item.price }} تومان
            </div>

            <div class="flex items-center gap-2 mt-3">
              <button @click="cart.decrease(item.id)">−</button>
              <span>{{ item.qty }}</span>
              <button @click="cart.increase(item.id)">+</button>
            </div>
          </div>

          <button
            @click="cart.remove(item.id)"
            class="text-red-500 text-sm"
          >
            حذف
          </button>
        </div>
      </div>

      <!-- Summary -->
      <div class="bg-white p-4 rounded shadow">
        <div class="flex justify-between mb-2">
          <span>جمع کل</span>
          <span class="font-bold">{{ cart.total }} تومان</span>
        </div>

        <router-link
          to="/checkout"
          class="block text-center bg-blue-600 text-white py-3 rounded mt-4"
        >
          ادامه خرید
        </router-link>
      </div>

    </div>

  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cartStore'
const cart = useCartStore()
</script>
