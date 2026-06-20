<template>
  <div
    class="rounded-full bg-[linear-gradient(90deg,rgba(226,232,240,0.8),rgba(248,250,252,1),rgba(226,232,240,0.8))] bg-size-[200%_100%] animate-shimmer"
    :style="{ height, width }"
  ></div>
</template>

<script setup>
defineProps({
  width: { type: String, default: '100%' },
  height: { type: String, default: '16px' },
})
</script>
