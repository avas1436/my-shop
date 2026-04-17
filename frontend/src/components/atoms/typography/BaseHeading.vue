<template>
  <component
    :is="tag"
    :class="[
      'base-heading',
      `base-heading-${variant}`,
      `base-heading-${size}`,
      {
        'base-heading-bold': bold,
        'base-heading-center': center
      }
    ]"
  >
    <slot />
  </component>
</template>

<script setup>
defineProps({
  tag: {
    type: String,
    default: 'h2',
    validator: (value) => ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(value)
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'accent'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl', '2xl'].includes(value)
  },
  bold: {
    type: Boolean,
    default: false
  },
  center: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.base-heading {
  line-height: 1.4;
  margin: 0;
  transition: color 0.2s ease;
}

/* Variants */
.base-heading-primary {
  color: var(--color-text-primary, #1a1a1a);
}
.base-heading-secondary {
  color: var(--color-text-secondary, #666666);
}
.base-heading-accent {
  color: var(--color-accent, #e63946);
}

/* Sizes */
.base-heading-xs { font-size: 0.875rem; font-weight: 600; }
.base-heading-sm { font-size: 1rem; font-weight: 600; }
.base-heading-md { font-size: 1.25rem; font-weight: 700; }
.base-heading-lg { font-size: 1.5rem; font-weight: 700; }
.base-heading-xl { font-size: 2rem; font-weight: 800; }
.base-heading-2xl { font-size: 2.5rem; font-weight: 800; }

/* Modifiers */
.base-heading-bold { font-weight: 900 !important; }
.base-heading-center { text-align: center; }

/* Responsive */
@media (max-width: 768px) {
  .base-heading-xl { font-size: 1.75rem; }
  .base-heading-2xl { font-size: 2rem; }
}
</style>


<!--
<BaseHeading
  tag="h3"
  variant= "primary" / "secondary" / "accent"
  size= "lg" / "xl"
  bold / bold center
>
استفاده نمونه
</BaseHeading>
-->
