<template>
  <div class="container mx-auto p-4">

    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-lg font-bold">محصولات دسته‌بندی</h1>

      <select v-model="sort" class="border rounded p-2 text-sm">
        <option value="new">جدیدترین</option>
        <option value="cheap">ارزان‌ترین</option>
        <option value="expensive">گران‌ترین</option>
      </select>
    </div>

    <!-- Layout -->
    <div class="flex gap-6">

      <!-- Filters Desktop -->
      <aside class="hidden lg:block w-64 bg-white p-4 rounded shadow">
        <h3 class="font-bold mb-2">فیلتر قیمت</h3>
        <input type="range" class="w-full" />

        <h3 class="font-bold mt-6 mb-2">موجودی</h3>
        <label class="flex items-center gap-2 text-sm">
          <input type="checkbox" /> فقط موجود
        </label>
      </aside>

      <!-- Products -->
      <div class="flex-1">
        <ProductGrid :products="products" />
      </div>
    </div>

  </div>
</template>

<script setup>
import ProductGrid from '@/components/product/ProductGrid.vue'
import { useProductStore } from '@/stores/cartStore'

const productStore = useProductStore()
const products = productStore.products
const sort = ref('new')
</script>
