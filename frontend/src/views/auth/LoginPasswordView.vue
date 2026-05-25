<!-- src/views/auth/LoginPasswordView.vue -->
<template>
  <div class="auth-card page-panel">
    <h1 class="section-title">ورود به حساب کاربری</h1>
    <p class="muted mb-4">لطفا شماره موبایل و رمز عبور خود را وارد کنید.</p>

    <form @submit.prevent="handleSubmit" class="auth-form">
      <div class="form-group">
        <label>شماره موبایل</label>
        <input type="text" v-model="form.phone" placeholder="۰۹۱۲۳۴۵۶۷۸۹" required />
      </div>
      <div class="form-group">
        <label>رمز عبور</label>
        <input type="password" v-model="form.password" placeholder="********" required />
      </div>

      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

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
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const isLoading = ref(false)
const errorMessage = ref('')
const form = reactive({ phone: '', password: '' })

async function handleSubmit() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const data = await authService.loginWithPassword(form.phone, form.password)
    userStore.setAuthSuccess(data.access_token)
    await userStore.initializeAuth()
    router.push('/profile')
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'خطا در ورود به حساب'
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
