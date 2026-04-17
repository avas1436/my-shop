<template>
  <div
    v-if="ui.miniCart"
    class="fixed top-0 right-0 w-80 h-full bg-white shadow-xl z-50 p-4 border-l"
  >
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold">سبد خرید</h2>
      <button @click="ui.toggleMiniCart()">✕</button>
    </div>

    <div v-if="cart.items.length === 0" class="text-gray-500 text-sm text-center mt-20">
      سبد خرید خالی است
    </div>

    <div v-else class="space-y-4 overflow-y-auto max-h-[70vh]">

      <div
        v-for="item in cart.items"
        :key="item.id"
        class="flex gap-3 items-start border-b pb-3"
      >
        <img :src="item.image" class="w-16 rounded" />

        <div class="flex-1">
          <h4 class="text-sm font-bold line-clamp-2">{{ item.title }}</h4>

          <p class="text-blue-600 font-bold text-sm mt-1">
            {{ item.price }} تومان
          </p>

          <div class="flex items-center gap-2 mt-2">
            <button @click="cart.decrease(item.id)" class="px-2 py-1 bg-gray-100">−</button>
            <span>{{ item.qty }}</span>
            <button @click="cart.increase(item.id)" class="px-2 py-1 bg-gray-100">+</button>
          </div>
        </div>

        <button
          @click="cart.remove(item.id)"
          class="text-red-500 text-xs"
        >
          حذف
        </button>
      </div>

    </div>

    <!-- Footer -->
    <div class="absolute bottom-4 left-4 right-4">
      <router-link
        to="/cart"
        class="block w-full bg-blue-600 text-white text-center py-3 rounded"
        @click="ui.toggleMiniCart()"
      >
        مشاهده سبد خرید
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cartStore'
import { useUIStore } from '@/stores/uiStore'

const cart = useCartStore()
const ui = useUIStore()
</script>

<style scoped>
/* Prevent background scroll when drawer is open */
body {
  overflow-y: hidden;
}
</style>
