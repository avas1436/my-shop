<!-- src/views/auth/LoginPasswordView.vue -->
<template>
  <div class="auth-card page-panel">
    <h1 class="section-title">ورود به حساب کاربری</h1>
    <p class="muted mb-4">لطفا شماره موبایل و رمز عبور خود را وارد کنید.</p>

    <form @submit.prevent="handleSubmit" class="auth-form">
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

      <div class="form-group">
        <label>رمز عبور</label>
        <input
          type="password"
          v-model="form.password"
          placeholder="********"
          :class="{ 'has-error': fieldErrors.password }"
        />

        <!-- نمایش خطای فیلد رمز عبور -->
        <span v-if="fieldErrors.password" class="error-text field-error">
          {{ fieldErrors.password[0] }}
        </span>
      </div>

      <!-- نمایش خطاهای کلی بیزینسی (مثل رمز اشتباه) -->
      <p v-if="errorMessage" class="error-text global-error">{{ errorMessage }}</p>

      <BaseButton type="submit" :disabled="isLoading" block>
        {{ isLoading ? 'در حال ورود...' : 'ورود' }}
      </BaseButton>
    </form>

    <div class="auth-links mt-3">
      <router-link :to="{ name: 'login-otp' }">ورود با رمز یکبار مصرف (OTP)</router-link>
      <router-link :to="{ name: 'register' }">ثبت‌نام نکرده‌اید؟</router-link>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { authService } from '@/services/authService'
import { useUserStore } from '@/stores/userStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { validatePassword, validatePhoneNumber } from '@/utils/validators'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const isLoading = ref(false)
const errorMessage = ref('') // برای خطاهای کلی فرم
const fieldErrors = ref({}) // برای خطاهای اختصاصی هر فیلد

const form = reactive({ phone: '', password: '' })

const validateForm = () => {
  fieldErrors.value = {}

  const errorPhone = validatePhoneNumber(form.phone)
  if (errorPhone) {
    fieldErrors.value.phone = [errorPhone]
  }

  const errorPass = validatePassword(form.password)
  if (errorPass) {
    fieldErrors.value.password = [errorPass]
  }

  if (errorPhone || errorPass) {
    return false
  }

  return true
}

async function handleSubmit() {
  errorMessage.value = ''
  fieldErrors.value = {}

  // ۱. بررسی خطاهای فرانت‌اند قبل از ارسال درخواست
  if (!validateForm()) return

  isLoading.value = true

  try {
    const data = await authService.loginWithPassword(form.phone, form.password)
    userStore.setAuthSuccess(data)
    console.log(data)
    await userStore.initializeAuth(true)
    setTimeout(() => router.push('/profile'), 1000)
  } catch (error) {
    errorMessage.value = getErrorMessage(error.code)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* استایل‌های پایه برای فرم‌های احراز هویت */
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
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: center;
  font-size: 0.875rem;
}
</style>
