<script setup>
import {
  BaseHeading,
  BaseText,
  BaseLabel,
  BaseBadge,
  BasePriceTag
} from '@/components/atoms/typography'
</script>

<template>
  <BaseHeading bold variant="accent">
  سلام علیکم
  </BaseHeading>


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

<BaseLabel htmlFor="email" required>
  ایمیل
</BaseLabel>

<base-badge variant=sale size=lg dot rounded outline>
سلام و کیر خر
</base-badge>


<BasePriceTag
  price="230000"
  originalPrice="320000"
  size="lg"
  currency="toman"
/>

  <RouterView />
</template>
