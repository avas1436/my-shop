<!-- src/components/base/BaseButton.vue -->
<template>
  <component
    :is="tag"
    :class="[
      'inline-flex duration-200',
      'hover:-translate-y-px',
      'disabled:transform-none disabled:shadow-none',
      sizeClasses[size],
      variantClasses[variant],
      { 'w-full': block },
      'items-center',
      'justify-center',
      'gap-2',
      'rounded-full',
      'border-0',
      'font-bold',
      'transition-all',
      'disabled:cursor-not-allowed',
      'disabled:opacity-55',
    ]"
    v-bind="$attrs"
  >
    <slot />
  </component>
</template>

<script setup>
// فعال کردن پراپ‌ها برای استفاده در تمپلیت
const { tag, variant, size, block } = defineProps({
  tag: { type: String, default: 'button' },
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'md' },
  block: { type: Boolean, default: false },
})

const sizeClasses = {
  sm: 'min-h-[40px] px-4 text-[0.9rem]',
  md: 'min-h-[48px] px-[1.35rem] text-[0.96rem]',
  lg: 'min-h-[56px] px-[1.7rem] text-base',
}

const variantClasses = {
  // هماهنگ شده با متغیرهای --color-primary و --color-primary-dark تم شما
  primary:
    'text-white bg-gradient-to-br from-primary to-primary-dark shadow-[0_16px_32px_rgba(91,61,245,0.22)] hover:shadow-[0_20px_36px_rgba(91,61,245,0.28)]',

  // هماهنگ با --color-text-main و --color-bg-muted
  secondary: 'text-text-main bg-bg-muted border border-border-light',

  // استفاده از آلفا روی رنگ اصلی تم
  ghost: 'text-primary bg-transparent border border-primary/20 hover:bg-primary/5',

  // هماهنگ شده با --color-success تم شما
  success:
    'text-white bg-gradient-to-br from-success to-success/90 shadow-[0_16px_32px_rgba(15,157,129,0.22)] hover:shadow-[0_20px_36px_rgba(15,157,129,0.28)]',

  // هماهنگ شده با --color-warning تم شما
  warning:
    'text-white bg-gradient-to-br from-warning to-warning/90 shadow-[0_16px_32px_rgba(255,176,32,0.22)] hover:shadow-[0_20px_36px_rgba(255,176,32,0.28)]',

  // هماهنگ شده با --color-danger تم شما
  danger:
    'text-white bg-gradient-to-br from-danger to-danger/90 shadow-[0_16px_32px_rgba(239,68,68,0.22)] hover:shadow-[0_20px_36px_rgba(239,68,68,0.28)]',

  'danger-ghost': 'text-danger bg-transparent border border-danger/20 hover:bg-danger/10',
}
</script>

<!-- مثال استفاده -->
<!-- چند ویژگی همزمان -->
<!-- 
  <BaseButton
  variant="success", "primary", "secondary", "ghost", "danger", "warning", "danger-ghost"

  size="lg", "md", "sm"

  block, disabled

  type="submit"

  :disabled="loading"

  @click="saveData"

  tag="button", "a", "router-link"
>
  {{ loading ? 'در حال ذخیره...' : 'ذخیره' }}
</BaseButton> 
-->
