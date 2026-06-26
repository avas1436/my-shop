<!-- src/components/base/BaseSkeleton.vue -->
<template>
  <div
    class="animate-shimmer rounded-md bg-shimmer-gradient from-slate-200 via-slate-50 to-slate-200 bg-size-[200%_100%]"
    :style="{ height, width }"
  ></div>
</template>

<script setup>
defineProps({
  width: { type: String, default: '100%' },
  height: { type: String, default: '16px' },
})
</script>
