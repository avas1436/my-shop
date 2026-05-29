<!-- src/views/auth/LoginOtpView.vue -->
<template>
  <div class="auth-card page-panel">
    <h1 class="section-title">ورود با رمز یکبار مصرف</h1>

    <!-- مرحله اول: دریافت شماره -->
    <form v-if="!otpSent" @submit.prevent="handleRequest" class="auth-form">
      <p class="muted mb-4">شماره موبایل خود را برای دریافت کد وارد کنید.</p>

      <div class="form-group">
        <label>شماره موبایل</label>
        <input
          type="text"
          v-model="form.phone"
          placeholder="۰۹۱۲۳۴۵۶۷۸۹"
          :class="{ 'has-error': fieldErrors.phone }"
        />
        <!-- نمایش خطای فیلد موبایل -->
        <span v-if="fieldErrors.phone" class="error-text field-error">
          {{ fieldErrors.phone[0] }}
        </span>
      </div>

      <!-- نمایش خطاهای کلی بیزینسی -->
      <p v-if="errorMessage" class="error-text global-error">{{ errorMessage }}</p>

      <BaseButton type="submit" :disabled="isLoading" block>
        {{ isLoading ? 'در حال ارسال...' : 'ارسال کد تایید' }}
      </BaseButton>
    </form>

    <!-- مرحله دوم: تایید کد -->
    <form v-else @submit.prevent="handleVerify" class="auth-form">
      <p class="muted mb-4">کد ارسال شده به {{ form.phone }} را وارد کنید.</p>

      <div class="form-group">
        <label>کد تایید</label>
        <input
          type="text"
          v-model="form.otpCode"
          placeholder="۱۲۳۴۵"
          :class="{ 'has-error': fieldErrors.otpCode }"
        />
        <!-- نمایش خطای فیلد کد تایید -->
        <span v-if="fieldErrors.otpCode" class="error-text field-error">
          {{ fieldErrors.otpCode[0] }}
        </span>
      </div>

      <!-- نمایش خطاهای کلی بیزینسی -->
      <p v-if="errorMessage" class="error-text global-error">{{ errorMessage }}</p>

      <BaseButton type="submit" :disabled="isLoading" block>
        {{ isLoading ? 'در حال بررسی...' : 'تایید و ورود' }}
      </BaseButton>
    </form>

    <div class="auth-links mt-3">
      <router-link :to="{ name: 'login-password' }">ورود با رمز عبور</router-link>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { useOtpAuth } from '@/composable/auth/useOtpAuth'
import { useRouter } from 'vue-router'

const router = useRouter()

const { form, isLoading, otpSent, errorMessage, fieldErrors, requestOtp, verifyOtp } = useOtpAuth({
  onRequestError: (error) => {
    if (error.code === 'REGISTERED') {
      setTimeout(() => router.push('/auth/login-password'), 2000)
    } else if (error.code === 'USER_NOT_FOUND') {
      setTimeout(() => router.push('/auth/register'), 2000)
    }
  },
  onVerifySuccess: () => {
    setTimeout(() => router.push('/profile'), 1000)
  },
  onVerifyError: (error) => {
    if (error.code === 'ALREADY_EXIST_USER') {
      otpSent.value = false
      form.otpCode = ''
      setTimeout(() => router.push('/auth/login-password'), 2000)
    } else if (error.code === 'USER_NOT_FOUND') {
      setTimeout(() => router.push('/auth/register'), 2000)
    } else {
      errorMessage.value = error.message || 'خطا در تایید کد.'
    }
  },
})

// استفاده از توابع با پاس دادن هدف مورد نظر
const handleRequest = () => requestOtp('login')
const handleVerify = () => verifyOtp('login')
</script>

<style scoped>
.auth-card {
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  max-width: 400px;
  margin: 0 auto;
}
.form-group {
  margin-bottom: 1rem;
  display: grid;
  gap: 0.5rem;
}
.form-group input {
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}
.error-text {
  color: #ef4444;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}
.auth-links {
  text-align: center;
  font-size: 0.875rem;
  display: block;
  margin-top: 1rem;
}
</style>
