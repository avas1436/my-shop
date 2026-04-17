<template>
  <component
    :is="tag"
    :class="[
      'base-text',
      `base-text-${variant}`,
      `base-text-${size}`,
      `base-text-${weight}`,
      {
        'base-text-truncate': truncate,
        'base-text-center': center,
        'base-text-justify': justify,
        'base-text-italic': italic,
        'base-text-underline': underline,
        'base-text-strikethrough': strikethrough
      }
    ]"
    :style="lineClampStyle"
  >
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tag: {
    type: String,
    default: 'p'
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) =>
      ['primary', 'secondary', 'muted', 'success', 'error', 'warning'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  weight: {
    type: String,
    default: 'normal',
    validator: (value) =>
      ['light', 'normal', 'medium', 'semibold', 'bold'].includes(value)
  },
  truncate: {
    type: Boolean,
    default: false
  },
  lineClamp: {
    type: Number,
    default: null
  },
  center: {
    type: Boolean,
    default: false
  },
  justify: {
    type: Boolean,
    default: false
  },
  italic: {
    type: Boolean,
    default: false
  },
  underline: {
    type: Boolean,
    default: false
  },
  strikethrough: {
    type: Boolean,
    default: false
  }
})

const lineClampStyle = computed(() => {
  if (props.lineClamp) {
    return {
      display: '-webkit-box',
      '-webkit-line-clamp': props.lineClamp,
      '-webkit-box-orient': 'vertical',
      overflow: 'hidden'
    }
  }
  return {}
})
</script>

<style scoped>
.base-text {
  font-family: 'Vazirmatn', sans-serif;
  line-height: 1.7;
  margin: 0;
  transition: color 0.2s ease;
}

/* Variants */
.base-text-primary {
  color: var(--color-text-primary, #1a1a1a);
}

.base-text-secondary {
  color: var(--color-text-secondary, #4a4a4a);
}

.base-text-muted {
  color: var(--color-text-muted, #9ca3af);
}

.base-text-success {
  color: var(--color-success, #10b981);
}

.base-text-error {
  color: var(--color-error, #ef4444);
}

.base-text-warning {
  color: var(--color-warning, #f59e0b);
}

/* Sizes */
.base-text-xs {
  font-size: 0.75rem;
}

.base-text-sm {
  font-size: 0.875rem;
}

.base-text-md {
  font-size: 1rem;
}

.base-text-lg {
  font-size: 1.125rem;
}

.base-text-xl {
  font-size: 1.25rem;
}

/* Weights */
.base-text-light {
  font-weight: 300;
}

.base-text-normal {
  font-weight: 400;
}

.base-text-medium {
  font-weight: 500;
}

.base-text-semibold {
  font-weight: 600;
}

.base-text-bold {
  font-weight: 700;
}

/* Modifiers */
.base-text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.base-text-center {
  text-align: center;
}

.base-text-justify {
  text-align: justify;
}

.base-text-italic {
  font-style: italic;
}

.base-text-underline {
  text-decoration: underline;
}

.base-text-strikethrough {
  text-decoration: line-through;
}
</style>

<!--
<BaseText
  tag="p"
  variant="secondary"
  size="lg"
  weight="medium"
  :lineClamp="2"
  italic
  center
>
یک متن نمونه
</BaseText>
-->
