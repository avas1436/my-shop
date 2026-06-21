<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 grid place-items-center z-80">
      <div class="absolute inset-0 bg-slate-900/45 backdrop-blur-sm" @click="$emit('close')"></div>

      <div
        class="relative w-[min(560px,calc(100%-24px))] bg-surface-strong rounded-lg shadow-custom border border-border-light p-6"
      >
        <slot />
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  open: { type: Boolean, default: false },
})

defineEmits(['close'])
</script>
