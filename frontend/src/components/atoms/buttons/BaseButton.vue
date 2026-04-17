<template>
  <component
    :is="tag"
    :type="nativeType"
    :disabled="disabled || loading"
    :class="[
      'base-button',
      `base-button--${variant}`,
      `base-button--${size}`,
      {
        'base-button--block': block,
        'base-button--rounded': rounded,
        'base-button--loading': loading,
        'base-button--icon-only': iconOnly
      }
    ]"
    @click="handleClick"
  >
    <!-- Loading Spinner -->
    <span v-if="loading" class="base-button__spinner"></span>

    <!-- Icon Left -->
    <span
      v-if="$slots.iconLeft && !loading"
      class="base-button__icon base-button__icon--left"
    >
      <slot name="iconLeft" />
    </span>

    <!-- Content -->
    <span v-if="!iconOnly" class="base-button__content">
      <slot />
    </span>

    <!-- Icon Only -->
    <span v-if="iconOnly && !loading" class="base-button__icon">
      <slot />
    </span>

    <!-- Icon Right -->
    <span
      v-if="$slots.iconRight && !loading"
      class="base-button__icon base-button__icon--right"
    >
      <slot name="iconRight" />
    </span>
  </component>
</template>

<script setup>
const props = defineProps({
  tag: {
    type: String,
    default: 'button'
  },

  nativeType: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },

  variant: {
    type: String,
    default: 'primary',
    validator: (value) =>
      ['primary', 'secondary', 'ghost', 'danger', 'success', 'warning', 'outline'].includes(value)
  },

  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },

  disabled: {
    type: Boolean,
    default: false
  },

  loading: {
    type: Boolean,
    default: false
  },

  block: {
    type: Boolean,
    default: false
  },

  rounded: {
    type: Boolean,
    default: false
  },

  iconOnly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: 'Vazirmatn', sans-serif;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  white-space: nowrap;
  user-select: none;
  position: relative;
  overflow: hidden;
}

.base-button:focus-visible {
  outline: 2px solid var(--color-primary, #3b82f6);
  outline-offset: 2px;
}

/* Sizes */
.base-button--xs {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  min-height: 1.75rem;
}

.base-button--sm {
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  min-height: 2.25rem;
}

.base-button--md {
  font-size: 1rem;
  padding: 0.625rem 1.5rem;
  border-radius: 0.5rem;
  min-height: 2.75rem;
}

.base-button--lg {
  font-size: 1.125rem;
  padding: 0.75rem 2rem;
  border-radius: 0.625rem;
  min-height: 3.25rem;
}

.base-button--xl {
  font-size: 1.25rem;
  padding: 1rem 2.5rem;
  border-radius: 0.75rem;
  min-height: 3.75rem;
}

/* Icon-Only Sizes */
.base-button--icon-only.base-button--xs {
  padding: 0.375rem;
  width: 1.75rem;
}
.base-button--icon-only.base-button--sm {
  padding: 0.5rem;
  width: 2.25rem;
}
.base-button--icon-only.base-button--md {
  padding: 0.625rem;
  width: 2.75rem;
}
.base-button--icon-only.base-button--lg {
  padding: 0.75rem;
  width: 3.25rem;
}
.base-button--icon-only.base-button--xl {
  padding: 1rem;
  width: 3.75rem;
}

/* Variants */
.base-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.base-button--primary:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transform: translateY(-1px);
}

.base-button--secondary {
  background-color: var(--color-secondary, #6b7280);
  color: white;
}

.base-button--ghost {
  background-color: transparent;
  color: var(--color-text-primary, #1a1a1a);
  border: 1.5px solid #e5e7eb;
}

.base-button--outline {
  background-color: transparent;
  color: var(--color-primary, #3b82f6);
  border: 2px solid currentColor;
}

.base-button--danger {
  background-color: var(--color-error, #ef4444);
  color: white;
}

.base-button--success {
  background-color: var(--color-success, #10b981);
  color: white;
}

.base-button--warning {
  background-color: var(--color-warning, #f59e0b);
  color: white;
}

/* States */
.base-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.base-button--loading {
  pointer-events: none;
}

/* Modifiers */
.base-button--block {
  width: 100%;
}

.base-button--rounded {
  border-radius: 9999px;
}

/* Icons */
.base-button__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.base-button__icon--left {
  margin-left: -0.25rem;
}

.base-button__icon--right {
  margin-right: -0.25rem;
}

/* Content */
.base-button__content {
  display: inline-flex;
  align-items: center;
}

/* Loading Spinner */
.base-button__spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Ripple */
.base-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.base-button:active:not(:disabled)::before {
  width: 300px;
  height: 300px;
}
</style>
`
