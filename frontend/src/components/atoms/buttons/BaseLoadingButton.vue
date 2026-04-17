<template>
  <button
    :type="nativeType"
    :disabled="disabled || loading"
    :class="[
      'base-loading-button',
      `base-loading-button--${variant}`,
      `base-loading-button--${size}`,
      {
        'base-loading-button--loading': loading,
        'base-loading-button--success': showSuccess,
        'base-loading-button--error': showError,
        'base-loading-button--block': block
      }
    ]"
    @click="handleClick"
    :aria-busy="loading"
  >
    <!-- Loading -->
    <span v-if="loading" class="base-loading-button__state">
      <span class="base-loading-button__spinner"></span>
      <span v-if="loadingText" class="base-loading-button__text">
        {{ loadingText }}
      </span>
    </span>

    <!-- Success -->
    <span v-else-if="showSuccess" class="base-loading-button__state">
      <svg class="base-loading-button__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <polyline points="20 6 9 17 4 12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <span v-if="successText" class="base-loading-button__text">
        {{ successText }}
      </span>
    </span>

    <!-- Error -->
    <span v-else-if="showError" class="base-loading-button__state">
      <svg class="base-loading-button__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <line x1="18" y1="6" x2="6" y2="18" stroke-width="2" stroke-linecap="round"/>
        <line x1="6" y1="6" x2="18" y2="18" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <span v-if="errorText" class="base-loading-button__text">
        {{ errorText }}
      </span>
    </span>

    <!-- Default -->
    <span v-else class="base-loading-button__content">
      <slot />
    </span>
  </button>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  nativeType: { type: String, default: 'button' },
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'danger'].includes(v)
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v)
  },
  loading: Boolean,
  success: Boolean,
  error: Boolean,
  disabled: Boolean,
  block: Boolean,
  loadingText: { type: String, default: 'در حال پردازش…' },
  successText: { type: String, default: 'موفق' },
  errorText: { type: String, default: 'خطا' },
  successDuration: { type: Number, default: 2000 },
  errorDuration: { type: Number, default: 2000 }
})

const emit = defineEmits(['click'])

const showSuccess = ref(false)
const showError = ref(false)

watch(() => props.success, (val) => {
  if (val) {
    showSuccess.value = true
    setTimeout(() => (showSuccess.value = false), props.successDuration)
  }
})

watch(() => props.error, (val) => {
  if (val) {
    showError.value = true
    setTimeout(() => (showError.value = false), props.errorDuration)
  }
})

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.base-loading-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: "Vazirmatn", sans-serif;
  font-weight: 600;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  padding: 0 1.25rem;
  height: 3rem;
  transition: all 0.2s ease;
  position: relative;
  user-select: none;
}

/* Block mode */
.base-loading-button--block {
  width: 100%;
}

/* Variants */
.base-loading-button--primary {
  background: var(--color-primary, #6366f1);
  color: white;
}
.base-loading-button--primary:hover:not(:disabled):not(.base-loading-button--loading) {
  background: #4f46e5;
}

.base-loading-button--secondary {
  background: #e5e7eb;
  color: #111;
}
.base-loading-button--secondary:hover:not(:disabled):not(.base-loading-button--loading) {
  background: #d1d5db;
}

.base-loading-button--danger {
  background: #e63946;
  color: white;
}
.base-loading-button--danger:hover:not(:disabled):not(.base-loading-button--loading) {
  background: #d62828;
}

/* Sizes */
.base-loading-button--sm {
  height: 2.5rem;
  padding: 0 1rem;
  font-size: 0.85rem;
}

.base-loading-button--md {
  height: 3rem;
  font-size: 1rem;
}

.base-loading-button--lg {
  height: 3.5rem;
  padding: 0 1.75rem;
  font-size: 1.1rem;
}

/* Loading state */
.base-loading-button--loading {
  cursor: wait;
  opacity: 0.85;
}

.base-loading-button__spinner {
  width: 1.2rem;
  height: 1.2rem;
  border: 3px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.base-loading-button__state {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

/* Success & Error Icons */
.base-loading-button__icon {
  width: 1.3rem;
  height: 1.3rem;
}

/* Disabled */
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
`
