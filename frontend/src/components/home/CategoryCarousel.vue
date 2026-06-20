<template>
  <section class="grid gap-4">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
      <div>
        <h2 class="m-0 text-[clamp(1.35rem,2vw,2rem)] font-bold">خرید بر اساس دسته‌بندی</h2>
        <p class="mt-2 text-text-muted text-[0.98rem]">
          مسیر سریع برای رسیدن به انتخاب‌های محبوب و ترند
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <router-link
        v-for="category in categories"
        :key="category.id"
        :to="`/category/${category.id}`"
        class="grid gap-3 p-5 rounded-lg bg-surface border border-border-light shadow-soft transition-all duration-200 hover:-translate-y-1 hover:shadow-custom"
      >
        <img :src="category.icon" :alt="category.title" class="w-21 h-10.5 object-contain" />
        <strong class="m-0 text-text-main">{{ category.title }}</strong>
        <p class="m-0 text-text-muted text-sm">{{ category.description }}</p>
      </router-link>
    </div>
  </section>
</template>

<script setup>
defineProps({
  categories: { type: Array, default: () => [] },
})
</script>
