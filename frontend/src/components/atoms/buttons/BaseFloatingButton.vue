<template>
  <button
    :type="nativeType"
    :disabled="disabled"
    :aria-label="ariaLabel"
    :class="[
      'base-floating-button',
      `base-floating-button--${variant}`,
      `base-floating-button--${size}`,
      `base-floating-button--${position}`,
      {
        'base-floating-button--extended': extended,
        'base-floating-button--hidden': hidden
      }
    ]"
    @click="handleClick"
  >
    <span class="base-floating-button__icon">
      <slot name="icon" />
    </span>

    <span v-if="extended" class="base-floating-button__label">
      <slot />
    </span>
  </button>
</template>

<script setup>
const props = defineProps({
  nativeType: {
    type: String,
    default: "button"
  },

  variant: {
    type: String,
    default: "primary",
    validator: (value) =>
      ["primary", "secondary", "accent"].includes(value)
  },

  size: {
    type: String,
    default: "md",
    validator: (value) => ["sm", "md", "lg"].includes(value)
  },

  position: {
    type: String,
    default: "bottom-right",
    validator: (value) =>
      [
        "bottom-right",
        "bottom-left",
        "top-right",
        "top-left",
        "bottom-center"
      ].includes(value)
  },

  extended: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  hidden: { type: Boolean, default: false },

  ariaLabel: {
    type: String,
    required: true
  }
})

const emit = defineEmits(["click"])

const handleClick = (event) => {
  if (!props.disabled) {
    emit("click", event)
  }
}
</script>

<style scoped>
.base-floating-button {
  position: fixed;
  z-index: 1000;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  border: none;
  cursor: pointer;
  font-family: "Vazirmatn", sans-serif;
  font-weight: 600;
  border-radius: 9999px;
  user-select: none;
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.15),
    0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.base-floating-button:focus-visible {
  outline: 2px solid var(--color-primary, #3b82f6);
  outline-offset: 2px;
}

/* ---------------- SIZES ---------------- */
.base-floating-button--sm {
  width: 3rem;
  height: 3rem;
  font-size: 0.875rem;
}
.base-floating-button--sm.base-floating-button--extended {
  width: auto;
  padding: 0 1.25rem;
}
.base-floating-button--sm .base-floating-button__icon {
  font-size: 1.25rem;
}

.base-floating-button--md {
  width: 3.5rem;
  height: 3.5rem;
  font-size: 1rem;
}
.base-floating-button--md.base-floating-button--extended {
  width: auto;
  padding: 0 1.5rem;
}
.base-floating-button--md .base-floating-button__icon {
  font-size: 1.5rem;
}

.base-floating-button--lg {
  width: 4rem;
  height: 4rem;
  font-size: 1.125rem;
}
.base-floating-button--lg.base-floating-button--extended {
  width: auto;
  padding: 0 2rem;
}
.base-floating-button--lg .base-floating-button__icon {
  font-size: 1.75rem;
}

/* ---------------- VARIANTS ---------------- */
.base-floating-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
.base-floating-button--primary:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.05);
  box-shadow:
    0 6px 16px rgba(102, 126, 234, 0.4),
    0 4px 8px rgba(0, 0, 0, 0.15);
}

.base-floating-button--secondary {
  background: white;
  color: var(--color-text-primary, #1a1a1a);
  border: 1px solid #e5e7eb;
}
.base-floating-button--secondary:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.05);
  box-shadow:
    0 6px 16px rgba(0, 0, 0, 0.2),
    0 4px 8px rgba(0, 0, 0, 0.15);
}

.base-floating-button--accent {
  background: var(--color-accent, #e63946);
  color: white;
}
.base-floating-button--accent:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.05);
  box-shadow:
    0 6px 16px rgba(230, 57, 70, 0.4),
    0 4px 8px rgba(0, 0, 0, 0.15);
}

/* ---------------- POSITIONS ---------------- */
.base-floating-button--bottom-right {
  bottom: 1.5rem;
  right: 1.5rem;
}

.base-floating-button--bottom-left {
  bottom: 1.5rem;
  left: 1.5rem;
}

.base-floating-button--top-right {
  top: 1.5rem;
  right: 1.5rem;
}

.base-floating-button--top-left {
  top: 1.5rem;
  left: 1.5rem;
}

.base-floating-button--bottom-center {
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
}
.base-floating-button--bottom-center:hover:not(:disabled) {
  transform: translateX(-50%) translateY(-2px) scale(1.05) !important;
}

/* ---------------- STATES ---------------- */
.base-floating-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.base-floating-button--hidden {
  opacity: 0;
  transform: scale(0);
  pointer-events: none;
}

.base-floating-button:active:not(:disabled) {
  transform: scale(0.95);
}

/* ---------------- ICON ---------------- */
.base-floating-button__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* ---------------- LABEL ---------------- */
.base-floating-button__label {
  white-space: nowrap;
}

/* ---------------- RESPONSIVE ---------------- */
@media (max-width: 768px) {
  .base-floating-button--bottom-right,
  .base-floating-button--bottom-left {
    bottom: 1rem;
  }
  .base-floating-button--bottom-right {
    right: 1rem;
  }
  .base-floating-button--bottom-left {
    left: 1rem;
  }
}
</style>
`
