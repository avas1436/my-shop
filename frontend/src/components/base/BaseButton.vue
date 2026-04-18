<template>
  <component
    :is="tag"
    class="base-button"
    :class="[`base-button--${variant}`, `base-button--${size}`, { 'base-button--block': block }]"
    v-bind="$attrs"
  >
    <slot />
  </component>
</template>

<script setup>
defineProps({
  tag: { type: String, default: 'button' },
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'md' },
  block: { type: Boolean, default: false },
})
</script>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: 0;
  border-radius: 999px;
  font-weight: 700;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background-color 0.2s ease;
}

.base-button:hover {
  transform: translateY(-1px);
}

.base-button--block {
  width: 100%;
}

.base-button--sm {
  min-height: 40px;
  padding: 0 1rem;
  font-size: 0.9rem;
}

.base-button--md {
  min-height: 48px;
  padding: 0 1.35rem;
  font-size: 0.96rem;
}

.base-button--lg {
  min-height: 56px;
  padding: 0 1.7rem;
  font-size: 1rem;
}

.base-button--primary {
  color: #fff;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  box-shadow: 0 16px 32px rgba(91, 61, 245, 0.22);
}

.base-button--primary:hover {
  box-shadow: 0 20px 36px rgba(91, 61, 245, 0.28);
}

.base-button--secondary {
  color: var(--text);
  background: var(--bg-muted);
  border: 1px solid var(--border);
}

.base-button--ghost {
  color: var(--primary);
  background: transparent;
  border: 1px solid rgba(91, 61, 245, 0.18);
}
</style>
