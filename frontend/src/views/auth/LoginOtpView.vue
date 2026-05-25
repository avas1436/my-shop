<!-- src/views/auth/LoginOtpView.vue -->
<template>
  <div class="auth-card page-panel">
    <h1 class="section-title">ورود با رمز یکبار مصرف</h1>

    <!-- مرحله اول: دریافت شماره -->
    <form v-if="!otpSent" @submit.prevent="requestOtp" class="auth-form">
      <p class="muted mb-4">شماره موبایل خود را برای دریافت کد وارد کنید.</p>
      <div class="form-group">
        <label>شماره موبایل</label>
        <input type="text" v-model="phone" placeholder="۰۹۱۲۳۴۵۶۷۸۹" required />
      </div>
      <BaseButton type="submit" :disabled="isLoading" block>ارسال کد تایید</BaseButton>
    </form>

    <!-- مرحله دوم: تایید کد -->
    <form v-else @submit.prevent="verifyOtp" class="auth-form">
      <p class="muted mb-4">کد ارسال شده به {{ phone }} را وارد کنید.</p>
      <div class="form-group">
        <label>کد تایید</label>
        <input type="text" v-model="otpCode" placeholder="۱۲۳۴۵" required />
      </div>
      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      <BaseButton type="submit" :disabled="isLoading" block>تایید و ورود</BaseButton>
    </form>

    <div class="auth-links mt-3">
      <router-link :to="{ name: 'login-password' }">ورود با رمز عبور</router-link>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { authService } from '@/services/authService'
import { useUserStore } from '@/stores/userStore'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const isLoading = ref(false)
const otpSent = ref(false)
const errorMessage = ref('')
const phone = ref('')
const otpCode = ref('')

async function requestOtp() {
  isLoading.value = true
  try {
    await authService.requestOtp(phone.value) // متد فرضی ارسال OTP در سرویس شما
    otpSent.value = true
  } catch {
    errorMessage.value = 'خطا در ارسال کد'
  } finally {
    isLoading.value = false
  }
}

async function verifyOtp() {
  isLoading.value = true
  try {
    const data = await authService.verifyOtp(phone.value, otpCode.value)
    userStore.setAuthSuccess(data.access_token)
    await userStore.initializeAuth()
    router.push('/')
  } catch {
    errorMessage.value = 'کد نامعتبر است'
  } finally {
    isLoading.value = false
  }
}
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
