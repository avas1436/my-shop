<!-- src/views/auth/LoginOtpView.vue -->
<template>
  <div
    class="w-full max-w-100 mx-auto p-8 bg-white rounded-md border border-border-light shadow-(--shadow-soft)"
  >
    <h1 class="m-0 text-[1.5rem] font-bold">ورود با رمز یکبار مصرف</h1>

    <!-- مرحله اول: دریافت شماره -->
    <form v-if="!otpSent" class="grid gap-5 mt-6" @submit.prevent="handleRequest">
      <p class="m-0 text-text-muted">شماره موبایل خود را برای دریافت کد وارد کنید.</p>

      <div class="grid gap-1.5">
        <label class="text-sm font-bold">شماره موبایل</label>
        <BaseInput
          v-model="form.phone"
          type="text"
          placeholder="۰۹۱۲۳۴۵۶۷۸۹"
          :error="fieldErrors.phone?.[0]"
        />
      </div>

      <p v-if="errorMessage" class="m-0 text-center text-sm text-danger">{{ errorMessage }}</p>

      <BaseButton type="submit" variant="primary" block :disabled="isLoading">
        {{ isLoading ? 'در حال ارسال...' : 'ارسال کد تایید' }}
      </BaseButton>
    </form>

    <!-- مرحله دوم: تایید کد -->
    <form v-else class="grid gap-5 mt-6" @submit.prevent="handleVerify">
      <p class="m-0 text-text-muted">
        کد ارسال شده به <span class="font-bold text-text-main">{{ form.phone }}</span> را وارد کنید.
      </p>

      <div class="grid gap-1.5">
        <label class="text-sm font-bold">کد تایید</label>
        <BaseInput
          v-model="form.otpCode"
          type="text"
          placeholder="۱۲۳۴۵"
          :error="fieldErrors.otpCode?.[0]"
        />
      </div>

      <p v-if="errorMessage" class="m-0 text-center text-sm text-danger">{{ errorMessage }}</p>

      <BaseButton type="submit" variant="primary" block :disabled="isLoading">
        {{ isLoading ? 'در حال بررسی...' : 'تایید و ورود' }}
      </BaseButton>

      <button
        type="button"
        class="text-sm text-text-muted hover:text-primary transition-colors text-center bg-transparent border-0 cursor-pointer"
        @click="otpSent = false"
      >
        ویرایش شماره موبایل
      </button>
    </form>

    <div class="mt-4 text-center text-sm">
      <router-link :to="{ name: 'login-password' }" class="text-primary font-bold">
        ورود با رمز عبور
      </router-link>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useOtpAuth } from '@/composable/auth/useOtpAuth'
import { useRouter } from 'vue-router'

const router = useRouter()

const { form, isLoading, otpSent, errorMessage, fieldErrors, requestOtp, verifyOtp } = useOtpAuth({
  onRequestError: async (error) => {
    if (error.code === 'REGISTERED') {
      await router.push('/auth/login-password')
    } else if (error.code === 'USER_NOT_FOUND') {
      await router.push('/auth/register')
    }
  },
  onVerifySuccess: async () => {
    await router.push('/profile')
  },
  onVerifyError: async (error) => {
    if (error.code === 'ALREADY_EXIST_USER') {
      otpSent.value = false
      form.otpCode = ''
      await router.push('/auth/login-password')
    } else if (error.code === 'USER_NOT_FOUND') {
      await router.push('/auth/register')
    } else {
      errorMessage.value = error.message || 'خطا در تایید کد.'
    }
  },
})

const handleRequest = () => requestOtp('login')
const handleVerify = () => verifyOtp('login')
</script>
