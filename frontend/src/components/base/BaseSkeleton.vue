<template>
  <div class="base-skeleton" :style="{ height, width }"></div>
</template>

<script setup>
defineProps({
  width: { type: String, default: '100%' },
  height: { type: String, default: '16px' },
})
</script>

<style scoped>
.base-skeleton {
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(226, 232, 240, 0.8), rgba(248, 250, 252, 1), rgba(226, 232, 240, 0.8));
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite linear;
}

@keyframes shimmer {
  from {
    background-position: 200% 0;
  }

  to {
    background-position: -200% 0;
  }
}
</style>
