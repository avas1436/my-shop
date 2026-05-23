<!-- src/views/auth/LoginPasswordView.vue -->
<template>
  <form class="auth-form" @submit.prevent="submitPasswordLogin">
    <BaseInput
      v-model="loginPhone"
      label="شماره موبایل"
      type="tel"
      placeholder="مثلا 09121234567"
      inputmode="numeric"
      maxlength="11"
      required
    />

    <BaseInput
      v-model="loginPassword"
      label="رمز عبور"
      type="password"
      placeholder="رمز عبور خود را وارد کنید"
      required
    />

    <p v-if="user.authMessage" class="auth-feedback auth-feedback--success">
      {{ user.authMessage }}
    </p>
    <p v-if="user.authError" class="auth-feedback auth-feedback--error">
      {{ user.authError }}
    </p>

    <BaseButton type="submit" size="lg" block :disabled="user.loginLoading">
      {{ passwordSubmitLabel }}
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

const loginPhone = computed({
  get: () => user.loginForm.phone_number,
  set: (value) => user.setLoginField('phone_number', normalizeDigits(value).slice(0, 11)),
})
const loginPassword = computed({
  get: () => user.loginForm.password,
  set: (value) => user.setLoginField('password', value),
})
const passwordSubmitLabel = computed(() => (user.loginLoading ? 'در حال ورود...' : 'ورود به حساب'))

async function submitPasswordLogin() {
  await user.loginWithPassword()
}
</script>

<style scoped>
.auth-form {
  display: grid;
  gap: 1rem;
  margin-top: 1.25rem;
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
