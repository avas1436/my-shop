<template>
  <section class="w-full rounded-xl overflow-hidden bg-gray-200 relative">

    <img
      src="https://via.placeholder.com/1200x400"
      class="w-full h-48 md:h-72 object-cover"
    />

    <div class="absolute top-0 right-0 w-full h-full flex flex-col items-center justify-center text-center bg-black/30 text-white">
      <h1 class="text-xl md:text-3xl font-bold mb-3">جدیدترین محصولات</h1>
      <p class="text-sm md:text-lg mb-4">بهترین قیمت، مطمئن‌ترین خرید</p>

      <router-link
        to="/category/1"
        class="bg-blue-600 px-5 py-3 rounded-lg text-sm md:text-base"
      >
        مشاهده محصولات
      </router-link>
    </div>

  </section>
</template>

<script setup>
</script>
