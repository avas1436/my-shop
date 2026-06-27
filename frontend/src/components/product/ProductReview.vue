<!-- src/components/product/ProductReview.vue -->
<!-- باکس مخصوص نمایش نظرات کاربران -->
<template>
  <section v-if="count > 0" class="grid gap-4 p-5 rounded-lg bg-bg-muted">
    <div class="flex items-center justify-between gap-4">
      <div>
        <strong class="block text-[2rem] text-amber-500">★ {{ rating.toFixed(1) }}</strong>
        <span class="text-text-muted text-sm">میانگین امتیاز کاربران</span>
      </div>
      <p class="m-0 text-text-muted text-sm">{{ count }} بررسی ثبت شده</p>
    </div>

    <ul v-if="highlights.length" class="grid gap-2.5 m-0 p-0 list-none">
      <li
        v-for="item in highlights"
        :key="item"
        class="py-3 px-4 rounded-2xl bg-surface-strong text-[0.95rem]"
      >
        {{ item }}
      </li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  rating: { type: Number, default: 0 },
  count: { type: Number, default: 0 },
  highlights: { type: Array, default: () => [] },
})
</script>
