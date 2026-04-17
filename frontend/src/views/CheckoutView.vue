<template>
  <div class="container mx-auto p-4 max-w-3xl">

    <h1 class="text-xl font-bold mb-6">تکمیل خرید</h1>

    <!-- Steps -->
    <div class="flex justify-between mb-8 text-sm">
      <span :class="step === 1 && 'font-bold'">آدرس</span>
      <span :class="step === 2 && 'font-bold'">ارسال</span>
      <span :class="step === 3 && 'font-bold'">پرداخت</span>
    </div>

    <!-- Step 1 -->
    <div v-if="step === 1" class="bg-white p-4 rounded shadow">
      <BaseInput placeholder="آدرس کامل" />
      <BaseButton class="mt-4" @click="step++">ادامه</BaseButton>
    </div>

    <!-- Step 2 -->
    <div v-if="step === 2" class="bg-white p-4 rounded shadow">
      <label class="block mb-2">
        <input type="radio" /> پست پیشتاز
      </label>
      <label class="block mb-4">
        <input type="radio" /> پیک
      </label>

      <BaseButton @click="step++">ادامه</BaseButton>
    </div>

    <!-- Step 3 -->
    <div v-if="step === 3" class="bg-white p-4 rounded shadow">
      <p class="mb-4">مبلغ قابل پرداخت:</p>
      <p class="text-xl font-bold mb-6">۱٬۲۵۰٬۰۰۰ تومان</p>

      <BaseButton>پرداخت نهایی</BaseButton>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseButton from '@/components/base/BaseButton.vue'

const step = ref(1)
</script>
