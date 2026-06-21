<template>
  <section class="grid gap-4 p-5 rounded-lg bg-bg-muted">
    <div class="flex items-center justify-between gap-4">
      <div>
        <strong class="block text-[2rem]">★ {{ rating }}</strong>
        <span class="m-0 text-text-muted">میانگین امتیاز کاربران</span>
      </div>
      <p class="m-0 text-text-muted">{{ count }} بررسی ثبت شده</p>
    </div>

    <ul class="grid gap-2.5 m-0 p-0 list-none">
      <li v-for="item in highlights" :key="item" class="py-3 px-4 rounded-2xl bg-surface-strong">
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
