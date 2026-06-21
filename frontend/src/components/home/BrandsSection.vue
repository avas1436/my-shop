<template>
  <section class="grid gap-4">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
      <div>
        <h2 class="m-0 text-[clamp(1.35rem,2vw,2rem)] font-bold">برندهای محبوب</h2>
        <p class="mt-2 text-text-muted text-[0.98rem]">ترکیبی از برندهای نوآور، خوش‌نام و پرفروش</p>
      </div>
    </div>

    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      <article
        v-for="brand in brands"
        :key="brand.id"
        class="grid place-items-center gap-3 p-5 rounded-lg bg-surface border border-border-light shadow-soft"
      >
        <img :src="brand.logo" :alt="brand.name" class="w-30 h-15 object-contain" />
        <strong class="text-text-main">{{ brand.name }}</strong>
      </article>
    </div>
  </section>
</template>

<script setup>
defineProps({
  brands: { type: Array, default: () => [] },
})
</script>
