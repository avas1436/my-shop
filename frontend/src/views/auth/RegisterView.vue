<!-- src/views/auth/RegisterView.vue -->
<template>
  <div class="auth-card page-panel">
    <h1 class="section-title">ثبت نام در سایت</h1>

    <!-- مرحله اول: دریافت شماره موبایل -->
    <form v-if="step === 1" @submit.prevent="requestOtp" class="auth-form">
      <p class="muted mb-4">شماره موبایل خود را وارد کنید.</p>

      <div class="form-group">
        <label>شماره موبایل</label>
        <input
          type="text"
          v-model="form.phone"
          placeholder="۰۹۱۲۳۴۵۶۷۸۹"
          :class="{ 'has-error': fieldErrors.phone }"
        />
        <span v-if="fieldErrors.phone" class="error-text field-error">
          {{ fieldErrors.phone[0] }}
        </span>
      </div>

      <p v-if="errorMessage" class="error-text global-error">{{ errorMessage }}</p>

      <BaseButton type="submit" :disabled="isLoading" block>
        {{ isLoading ? 'در حال ارسال...' : 'ارسال کد تایید' }}
      </BaseButton>
    </form>

    <!-- مرحله دوم: تایید کد OTP -->
    <form v-else-if="step === 2" @submit.prevent="verifyOtp" class="auth-form">
      <p class="muted mb-4">کد ارسال شده به {{ form.phone }} را وارد کنید.</p>

      <div class="form-group">
        <label>کد تایید</label>
        <input
          type="text"
          v-model="form.otpCode"
          placeholder="۱۲۳۴۵"
          :class="{ 'has-error': fieldErrors.otpCode }"
        />
        <span v-if="fieldErrors.otpCode" class="error-text field-error">
          {{ fieldErrors.otpCode[0] }}
        </span>
      </div>

      <p v-if="errorMessage" class="error-text global-error">{{ errorMessage }}</p>

      <BaseButton type="submit" :disabled="isLoading" block>
        {{ isLoading ? 'در حال بررسی...' : 'تایید کد' }}
      </BaseButton>
    </form>

    <div class="auth-links mt-3" v-if="step === 1">
      <router-link :to="{ name: 'login-password' }">حساب کاربری دارید؟ ورود</router-link>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { authService } from '@/services/authService'
import { useUserStore } from '@/stores/userStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { validateOtp, validatePhoneNumber } from '@/utils/validators'
import { reactive, ref } from 'vue'
// برای تبدیل تاریخ، نصب پکیج پیشنهاد می‌شود: npm install moment-jalaali

const userStore = useUserStore()

const step = ref(1) // 1: Request OTP, 2: Verify OTP, 3: Complete Profile
const isLoading = ref(false)

const errorMessage = ref('')
const fieldErrors = ref({})

const form = reactive({
  phone: '',
  otpCode: '',
  firstName: '',
  lastName: '',
  birthDateJalali: '', // ورودی کاربر به شمسی
  password: '',
  passwordConfirm: '',
})

// === مرحله ۱: درخواست کد ===
const requestOtp = async () => {
  errorMessage.value = ''
  fieldErrors.value = {}

  const phoneError = validatePhoneNumber(form.phone)
  if (phoneError) {
    fieldErrors.value.phone = [phoneError]
    return
  }

  isLoading.value = true
  try {
    await authService.requestOtp(form.phone, 'register') // ارسال نوع register
    step.value = 2
  } catch (error) {
    errorMessage.value = getErrorMessage(error.code) || error.message || 'خطا در درخواست کد.'
  } finally {
    isLoading.value = false
  }
}

// === مرحله ۲: تایید کد ===
const verifyOtp = async () => {
  errorMessage.value = ''
  fieldErrors.value = {}

  const otpError = validateOtp(form.otpCode)
  if (otpError) {
    fieldErrors.value.otpCode = [otpError]
    return
  }

  isLoading.value = true
  try {
    const data = await authService.verifyOtp(form.phone, form.otpCode, 'register')
    // لاگین کاربر در استیت
    userStore.setAuthSuccess(data.tokens)
    await userStore.initializeAuth()

    // رفتن به مرحله تکمیل اطلاعات
    step.value = 3
  } catch (error) {
    errorMessage.value = getErrorMessage(error.code) || error.message || 'کد نامعتبر است.'
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
