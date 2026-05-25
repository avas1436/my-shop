<!-- src/views/auth/RegisterView.vue -->
<template>
  <div class="auth-card page-panel">
    <h1 class="section-title">ثبت نام در سایت</h1>
    <p class="muted mb-4">برای ایجاد حساب کاربری اطلاعات زیر را تکمیل کنید.</p>

    <form @submit.prevent="handleRegister" class="auth-form">
      <div class="form-group">
        <label>نام</label>
        <input type="text" v-model="form.firstName" required />
      </div>
      <div class="form-group">
        <label>نام خانوادگی</label>
        <input type="text" v-model="form.lastName" required />
      </div>
      <div class="form-group">
        <label>شماره موبایل</label>
        <input type="text" v-model="form.phone" required />
      </div>
      <div class="form-group">
        <label>رمز عبور</label>
        <input type="password" v-model="form.password" required />
      </div>

      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

      <BaseButton type="submit" :disabled="isLoading" block>
        {{ isLoading ? 'در حال ثبت نام...' : 'ثبت نام' }}
      </BaseButton>
    </form>

    <div class="auth-links mt-3">
      <router-link :to="{ name: 'login-password' }">حساب کاربری دارید؟ ورود</router-link>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { authService } from '@/services/authService'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoading = ref(false)
const errorMessage = ref('')
const form = reactive({ firstName: '', lastName: '', phone: '', password: '' })

async function handleRegister() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    await authService.register(form) // متد ثبت نام در سرویس شما
    // بعد از ثبت‌نام موفق، هدایت به صفحه لاگین یا ورود خودکار
    router.push({ name: 'login-password' })
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'خطا در ثبت نام'
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
