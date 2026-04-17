<template>
  <section class="mt-10">
    <h2 class="text-lg font-bold mb-4">{{ title }}</h2>

    <div class="flex gap-4 overflow-x-auto no-scrollbar pb-2">

      <div
        v-for="p in products"
        :key="p.id"
        class="min-w-[160px] bg-white shadow rounded p-3 cursor-pointer hover:shadow-lg transition"
      >
        <img :src="p.image" class="w-full h-32 object-cover rounded mb-3" />
        <h3 class="text-sm font-medium mb-1 line-clamp-2">{{ p.title }}</h3>
        <p class="text-blue-600 font-bold text-sm">{{ p.price }} تومان</p>
      </div>

    </div>
  </section>
</template>

<script setup>
defineProps({
  title: { type: String, default: "محصولات" },
  products: { type: Array, default: () => [] }
})
</script>

<style>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>
