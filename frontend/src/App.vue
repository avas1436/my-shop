<script setup>
import {
  BaseHeading,
  BaseText,
  BaseLabel,
  BaseBadge,
  BasePriceTag
} from '@/components/atoms/typography'

import {
  BaseButton,
  BaseFloatingButton,
  BaseIconButton,
  BaseLoadingButton
} from '@/components/atoms/buttons'

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

<BaseButton loading variant=warning size=xl block rounded iconOnly>
در حال ارسال…
</BaseButton>

<BaseIconButton active ariaLabel="خانه">
  <Icon name="home" />
</BaseIconButton>

<BaseFloatingButton extended ariaLabel="افزودن آیتم">
  <template #icon><Icon name="add" /></template>
  افزودن
</BaseFloatingButton>

  <RouterView />
</template>
