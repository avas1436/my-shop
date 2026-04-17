<template>
  <button
    :type="nativeType"
    :disabled="disabled"
    :aria-label="ariaLabel"
    :class="[
      'base-icon-button',
      `base-icon-button--${variant}`,
      `base-icon-button--${size}`,
      {
        'base-icon-button--rounded': rounded,
        'base-icon-button--active': active
      }
    ]"
    @click="handleClick"
  >
    <span class="base-icon-button__icon">
      <slot />
    </span>

    <!-- Badge -->
    <span v-if="badge" class="base-icon-button__badge">
      {{ badge }}
    </span>
  </button>
</template>

<script setup>
const props = defineProps({
  nativeType: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },

  variant: {
    type: String,
    default: 'default',
    validator: (value) =>
      ['default', 'primary', 'ghost', 'danger', 'success'].includes(value)
  },

  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },

  disabled: { type: Boolean, default: false },
  rounded: { type: Boolean, default: false },
  active: { type: Boolean, default: false },

  ariaLabel: {
    type: String,
    required: true
  },

  badge: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>

<style scoped>
.base-icon-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Vazirmatn', sans-serif;
  user-select: none;
  flex-shrink: 0;
}

.base-icon-button:focus-visible {
  outline: 2px solid var(--color-primary, #3b82f6);
  outline-offset: 2px;
}

/* Sizes */
.base-icon-button--xs {
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 0.375rem;
}

.base-icon-button--xs .base-icon-button__icon {
  font-size: 0.875rem;
}

.base-icon-button--sm {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.5rem;
}

.base-icon-button--sm .base-icon-button__icon {
  font-size: 1rem;
}

.base-icon-button--md {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 0.5rem;
}

.base-icon-button--md .base-icon-button__icon {
  font-size: 1.25rem;
}

.base-icon-button--lg {
  width: 3.25rem;
  height: 3.25rem;
  border-radius: 0.625rem;
}

.base-icon-button--lg .base-icon-button__icon {
  font-size: 1.5rem;
}

.base-icon-button--xl {
  width: 3.75rem;
  height: 3.75rem;
  border-radius: 0.75rem;
}

.base-icon-button--xl .base-icon-button__icon {
  font-size: 1.75rem;
}

/* Variants */
.base-icon-button--default {
  background-color: #f3f4f6;
  color: var(--color-text-primary, #1a1a1a);
}

.base-icon-button--default:hover:not(:disabled) {
  background-color: #e5e7eb;
  transform: scale(1.05);
}

.base-icon-button--primary {
  background-color: var(--color-primary, #3b82f6);
  color: white;
}

.base-icon-button--primary:hover:not(:disabled) {
  background-color: #2563eb;
  transform: scale(1.05);
}

.base-icon-button--ghost {
  background-color: transparent;
  color: var(--color-text-secondary, #6b7280);
}

.base-icon-button--ghost:hover:not(:disabled) {
  background-color: #f3f4f6;
  color: var(--color-text-primary, #1a1a1a);
}

.base-icon-button--danger {
  background-color: #fee2e2;
  color: var(--color-error, #ef4444);
}

.base-icon-button--danger:hover:not(:disabled) {
  background-color: #fecaca;
  transform: scale(1.05);
}

.base-icon-button--success {
  background-color: #d1fae5;
  color: var(--color-success, #10b981);
}

.base-icon-button--success:hover:not(:disabled) {
  background-color: #a7f3d0;
  transform: scale(1.05);
}

/* States */
.base-icon-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none !important;
}

.base-icon-button--active {
  background-color: var(--color-primary, #3b82f6);
  color: white;
}

.base-icon-button--active.base-icon-button--ghost {
  background-color: #eff6ff;
  color: var(--color-primary, #3b82f6);
}

/* Rounded */
.base-icon-button--rounded {
  border-radius: 9999px;
}

/* Icon */
.base-icon-button__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

/* Badge */
.base-icon-button__badge {
  position: absolute;
  top: -0.25rem;
  left: -0.25rem;
  min-width: 1.25rem;
  height: 1.25rem;
  padding: 0 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-error, #ef4444);
  color: white;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Press Animation */
.base-icon-button:active:not(:disabled) {
  transform: scale(0.95);
}
</style>
`
