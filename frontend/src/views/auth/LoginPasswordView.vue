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
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const isLoading = ref(false)
const errorMessage = ref('') // برای خطاهای کلی فرم
const fieldErrors = ref({}) // برای خطاهای اختصاصی هر فیلد

const form = reactive({ phone: '', password: '' })

// تابع اعتبارسنجی سمت فرانت‌اند
const validateFrontend = () => {
  fieldErrors.value = {}
  let isValid = true

  if (!form.phone) {
    fieldErrors.value.phone = ['شماره موبایل الزامی است']
    isValid = false
  }
  if (!form.password) {
    fieldErrors.value.password = ['رمز عبور الزامی است']
    isValid = false
  }

  return isValid
}

async function handleSubmit() {
  errorMessage.value = ''

  // ۱. بررسی خطاهای فرانت‌اند قبل از ارسال درخواست
  if (!validateFrontend()) return

  isLoading.value = true

  try {
    const data = await authService.loginWithPassword(form.phone, form.password)
    userStore.setAuthSuccess(data.access_token)
    await userStore.initializeAuth()
    router.push('/profile')
  } catch (error) {
    // ۲. مدیریت خطاهای بک‌اند

    // الف) 422 validation
    if (error.error_type === 'RequestValidationError' && error.validation_errors) {
      error.validation_errors.forEach((err) => {
        // در Pydantic معمولا فیلد در ایندکس آخر loc قرار دارد: ['body', 'phone']
        const fieldName = err.loc[err.loc.length - 1]

        if (!fieldErrors.value[fieldName]) {
          fieldErrors.value[fieldName] = []
        }
        fieldErrors.value[fieldName].push(err.msg)
      })
    }
    // ب) خطاهای بیزینسی بک‌اند (مثل 400, 401, 403, 404)
    else if (error.status && error.status >= 400 && error.status < 500) {
      errorMessage.value = error.message || 'اطلاعات ورود نامعتبر است.'
    }
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
