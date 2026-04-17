<template>
  <section class="mt-8">
    <h2 class="text-lg font-bold mb-4">دسته‌ها</h2>

    <div class="flex gap-4 overflow-x-auto no-scrollbar py-2">
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="min-w-[90px] h-24 bg-white shadow rounded flex flex-col items-center justify-center text-sm cursor-pointer hover:bg-gray-50"
      >
        <img :src="cat.image" class="w-10 h-10 rounded mb-2" />
        <span>{{ cat.title }}</span>
      </div>
    </div>
  </section>
</template>

<script setup>
const categories = [
  { id: 1, title: "موبایل", image: "https://via.placeholder.com/50" },
  { id: 2, title: "لپ‌تاپ", image: "https://via.placeholder.com/50" },
  { id: 3, title: "کفش", image: "https://via.placeholder.com/50" },
  { id: 4, title: "لباس", image: "https://via.placeholder.com/50" }
]
</script>

<style>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>
