<!-- src/views/auth/RegisterView.vue -->
<template>
  <div
    class="w-full max-w-100 mx-auto p-8 bg-white rounded-md border border-border-light shadow-(--shadow-soft)"
  >
    <h1 class="m-0 text-[1.5rem] font-bold">ثبت‌نام در سایت</h1>

    <!-- مرحله اول: دریافت شماره موبایل -->
    <form v-if="!otpSent" class="grid gap-5 mt-6" @submit.prevent="handleRequest">
      <p class="m-0 text-text-muted">شماره موبایل خود را وارد کنید.</p>

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

      <div class="text-center text-sm">
        <router-link :to="{ name: 'login-password' }" class="text-primary font-bold">
          حساب کاربری دارید؟ ورود
        </router-link>
      </div>
    </form>

    <!-- مرحله دوم: تایید کد OTP -->
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
        {{ isLoading ? 'در حال بررسی...' : 'تایید کد' }}
      </BaseButton>

      <button
        type="button"
        class="text-sm text-text-muted hover:text-primary transition-colors text-center bg-transparent border-0 cursor-pointer"
        @click="otpSent = false"
      >
        ویرایش شماره موبایل
      </button>
    </form>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useOtpAuth } from '@/composable/auth/useOtpAuth'
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const { form, isLoading, otpSent, errorMessage, fieldErrors, requestOtp, verifyOtp } = useOtpAuth({
  onRequestError: async (error) => {
    if (error.code === 'REGISTERED') {
      await router.push('/auth/login-otp')
    }
  },
  onVerifySuccess: async () => {
    if (!userStore.user?.firstName || !userStore.user?.lastName) {
      await router.push('/auth/complete')
    } else {
      await router.push('/profile')
    }
  },
  onVerifyError: async (error) => {
    if (error.code === 'ALREADY_EXIST_USER') {
      otpSent.value = false
      form.otpCode = ''
      await router.push('/auth/login-password')
    } else {
      errorMessage.value = error.message || 'خطا در تایید کد.'
    }
  },
})

const handleRequest = () => requestOtp('register')
const handleVerify = () => verifyOtp('register')
</script>
