<!-- src/views/auth/LoginOtpView.vue -->
<template>
  <form class="auth-form" @submit.prevent="submitRegisterOtp">
    <BaseInput
      v-model="registerPhone"
      label="شماره موبایل"
      type="tel"
      placeholder="مثلا 09121234567"
      inputmode="numeric"
      maxlength="11"
      required
    />

    <BaseInput
      v-if="user.otpStep === 'code'"
      v-model="otpCode"
      label="کد تایید"
      type="tel"
      placeholder="کد پیامک شده را وارد کنید"
      inputmode="numeric"
      maxlength="6"
      required
    />

    <p class="auth-hint">
      این مرحله فقط برای ساخت حساب جدید است و پس از تایید شماره، فرم تکمیل اطلاعات نمایش داده می
      شود.
    </p>

    <p v-if="user.authMessage" class="auth-feedback auth-feedback--success">
      {{ user.authMessage }}
    </p>
    <p v-if="user.authError" class="auth-feedback auth-feedback--error">
      {{ user.authError }}
    </p>

    <BaseButton type="submit" size="lg" block :disabled="registerOtpDisabled">
      {{ registerOtpSubmitLabel }}
    </BaseButton>

    <BaseButton
      v-if="user.otpStep === 'code'"
      type="button"
      variant="ghost"
      size="md"
      block
      @click="goBackToPhone"
    >
      ویرایش شماره موبایل
    </BaseButton>
  </form>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useUserStore } from '@/stores/userStore'
import { computed } from 'vue'

const user = useUserStore()

function toEnglishDigits(value) {
  return String(value).replace(/[۰-۹]/g, (digit) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(digit)))
}
function normalizeDigits(value) {
  return toEnglishDigits(value).replace(/\D/g, '')
}

const registerPhone = computed({
  get: () => user.otpForm.phone_number,
  set: (value) => user.setOtpField('phone_number', normalizeDigits(value).slice(0, 11)),
})
const otpCode = computed({
  get: () => user.otpForm.code,
  set: (value) => user.setOtpField('code', normalizeDigits(value).slice(0, 6)),
})

const registerOtpDisabled = computed(() => user.otpSending || user.otpVerifying)
const registerOtpSubmitLabel = computed(() => {
  if (user.otpSending) return 'در حال ارسال کد...'
  if (user.otpVerifying) return 'در حال تایید کد...'
  return user.otpStep === 'code' ? 'تایید کد و ادامه' : 'ارسال کد تایید'
})

async function submitRegisterOtp() {
  if (user.otpStep === 'phone') {
    await user.requestOtp()
    return
  }
  await user.verifyOtp()
}

function goBackToPhone() {
  user.setOtpField('code', '')
  user.otpStep = 'phone'
  user.clearFeedback()
}
</script>

<style scoped>
.auth-form {
  display: grid;
  gap: 1rem;
  margin-top: 1.25rem;
}
.auth-hint {
  margin: 0.4rem 0 0;
  color: var(--text-muted);
  line-height: 1.8;
}
.auth-feedback {
  margin: 0;
  padding: 0.9rem 1rem;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.05);
}
.auth-feedback--success {
  color: #0f766e;
  background: rgba(15, 118, 110, 0.1);
}
.auth-feedback--error {
  color: var(--danger);
  background: rgba(239, 68, 68, 0.1);
}
</style>
