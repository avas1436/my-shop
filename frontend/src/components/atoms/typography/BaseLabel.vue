<template>
  <label
    :for="htmlFor"
    :class="[
      'base-label',
      `base-label-${size}`,
      {
        'base-label-required': required,
        'base-label-disabled': disabled,
        'base-label-error': error
      }
    ]"
  >
    <slot />

    <span
      v-if="required"
      class="base-label__asterisk"
      aria-label="ضروری"
    >*</span>

    <span
      v-if="optional"
      class="base-label__optional"
    >(اختیاری)</span>
  </label>
</template>

<script setup>
defineProps({
  htmlFor: {
    type: String,
    default: null
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  required: {
    type: Boolean,
    default: false
  },
  optional: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.base-label {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-family: 'Vazirmatn', sans-serif;
  font-weight: 500;
  color: var(--color-text-primary, #1a1a1a);
  cursor: pointer;
  transition: color 0.2s ease;
  user-select: none;
}

/* Sizes */
.base-label-sm {
  font-size: 0.875rem;
}

.base-label-md {
  font-size: 1rem;
}

.base-label-lg {
  font-size: 1.125rem;
}

/* States */
.base-label-disabled {
  color: var(--color-text-muted, #9ca3af);
  cursor: not-allowed;
}

.base-label-error {
  color: var(--color-error, #ef4444);
}

/* Required Asterisk */
.base-label__asterisk {
  color: var(--color-error, #ef4444);
  font-weight: 700;
  margin-right: 0.125rem;
}

/* Optional text */
.base-label__optional {
  font-size: 0.875em;
  font-weight: 400;
  color: var(--color-text-muted, #9ca3af);
  margin-right: 0.25rem;
}

/* Hover */
.base-label:hover:not(.base-label-disabled) {
  color: var(--color-accent, #e63946);
}
</style>
