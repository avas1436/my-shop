<template>
  <Teleport to="body">
    <div v-if="open" class="base-modal">
      <div class="base-modal__backdrop" @click="$emit('close')"></div>
      <div class="base-modal__panel">
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

<style scoped>
.base-modal {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
  z-index: 80;
}

.base-modal__backdrop {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(8px);
}

.base-modal__panel {
  position: relative;
  width: min(560px, calc(100% - 24px));
  background: var(--surface-strong);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  padding: 1.5rem;
}
</style>
