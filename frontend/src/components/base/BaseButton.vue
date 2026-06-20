<template>
  <component
    :is="tag"
    :class="[
      'inline-flex items-center justify-center gap-2 border-0 rounded-full font-bold transition-all duration-200 disabled:cursor-not-allowed disabled:opacity-55 disabled:transform-none disabled:shadow-none hover:-translate-y-px',
      sizeClasses[size],
      variantClasses[variant],
      { 'w-full': block },
    ]"
    v-bind="$attrs"
  >
    <slot />
  </component>
</template>

<script setup>
// const props = defineProps({
//   tag: { type: String, default: 'button' },
//   variant: { type: String, default: 'primary' },
//   size: { type: String, default: 'md' },
//   block: { type: Boolean, default: false },
// })

const sizeClasses = {
  sm: 'min-h-[40px] px-4 text-[0.9rem]',
  md: 'min-h-[48px] px-[1.35rem] text-[0.96rem]',
  lg: 'min-h-[56px] px-[1.7rem] text-base',
}

const variantClasses = {
  primary:
    'text-white bg-gradient-to-br from-primary to-primary-dark shadow-[0_16px_32px_rgba(91,61,245,0.22)] hover:shadow-[0_20px_36px_rgba(91,61,245,0.28)]',
  secondary: 'text-text-main bg-bg-muted border border-border-light',
  ghost: 'text-primary bg-transparent border border-primary/20',
  success:
    'text-white bg-gradient-to-br from-emerald-500 to-emerald-600 shadow-[0_16px_32px_rgba(16,185,129,0.22)] hover:shadow-[0_20px_36px_rgba(16,185,129,0.28)]',
  warning:
    'text-white bg-gradient-to-br from-amber-500 to-amber-600 shadow-[0_16px_32px_rgba(245,158,11,0.22)] hover:shadow-[0_20px_36px_rgba(245,158,11,0.28)]',
  danger:
    'text-white bg-gradient-to-br from-danger to-red-600 shadow-[0_16px_32px_rgba(239,68,68,0.22)] hover:shadow-[0_20px_36px_rgba(239,68,68,0.28)]',
  'danger-ghost': 'text-danger bg-transparent border border-danger/20 hover:bg-danger/10',
}
</script>
