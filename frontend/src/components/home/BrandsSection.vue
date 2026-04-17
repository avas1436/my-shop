<template>
  <section class="mt-10">
    <h2 class="text-lg font-bold mb-4">برندهای محبوب</h2>

    <div class="flex gap-6 overflow-x-auto no-scrollbar py-2">
      <div
        v-for="b in brands"
        :key="b.id"
        class="min-w-[90px] h-20 flex items-center justify-center bg-white shadow rounded"
      >
        <img :src="b.logo" class="w-14 h-14 object-contain" />
      </div>
    </div>
  </section>
</template>

<script setup>
const brands = [
  { id: 1, logo: "https://via.placeholder.com/60" },
  { id: 2, logo: "https://via.placeholder.com/60" },
  { id: 3, logo: "https://via.placeholder.com/60" },
  { id: 4, logo: "https://via.placeholder.com/60" }
]
</script>

<style>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>
