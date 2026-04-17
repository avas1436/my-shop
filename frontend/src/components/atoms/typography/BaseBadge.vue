<template>
  <span
    :class="[
      'base-badge',
      `base-badge-${variant}`,
      `base-badge-${size}`,
      {
        'base-badge-rounded': rounded,
        'base-badge-outlined': outlined,
        'base-badge-dot': dot
      }
    ]"
  >
    <span v-if="dot" class="base-badge__dot"></span>
    <slot />
  </span>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) =>
      [
        'primary',
        'secondary',
        'success',
        'error',
        'warning',
        'info',
        'new',
        'sale',
        'unavailable'
      ].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  rounded: {
    type: Boolean,
    default: false
  },
  outlined: {
    type: Boolean,
    default: false
  },
  dot: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.base-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-family: 'Vazirmatn', sans-serif;
  font-weight: 600;
  white-space: nowrap;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
}

/* Sizes */
.base-badge-sm {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
}

.base-badge-md {
  font-size: 0.875rem;
  padding: 0.25rem 0.75rem;
}

.base-badge-lg {
  font-size: 1rem;
  padding: 0.375rem 1rem;
}

/* Variants - Filled */
.base-badge-primary {
  background-color: var(--color-primary, #3b82f6);
  color: white;
}

.base-badge-secondary {
  background-color: var(--color-secondary, #6b7280);
  color: white;
}

.base-badge-success {
  background-color: var(--color-success, #10b981);
  color: white;
}

.base-badge-error {
  background-color: var(--color-error, #ef4444);
  color: white;
}

.base-badge-warning {
  background-color: var(--color-warning, #f59e0b);
  color: white;
}

.base-badge-info {
  background-color: var(--color-info, #06b6d4);
  color: white;
}

.base-badge-new {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.base-badge-sale {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.base-badge-unavailable {
  background-color: #e5e7eb;
  color: #6b7280;
}

/* Outlined */
.base-badge-outlined {
  background-color: transparent;
  border: 1.5px solid currentColor;
}

.base-badge-outlined.base-badge-primary {
  color: var(--color-primary, #3b82f6);
}

.base-badge-outlined.base-badge-secondary {
  color: var(--color-secondary, #6b7280);
}

.base-badge-outlined.base-badge-success {
  color: var(--color-success, #10b981);
}

.base-badge-outlined.base-badge-error {
  color: var(--color-error, #ef4444);
}

.base-badge-outlined.base-badge-warning {
  color: var(--color-warning, #f59e0b);
}

.base-badge-outlined.base-badge-info {
  color: var(--color-info, #06b6d4);
}

/* Rounded */
.base-badge-rounded {
  border-radius: 9999px;
}

/* Dot */
.base-badge__dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: currentColor;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
