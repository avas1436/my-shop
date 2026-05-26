<!-- src/views/auth/LoginOtpView.vue -->
<template>
  <div class="auth-card page-panel">
    <h1 class="section-title">ورود با رمز یکبار مصرف</h1>

    <!-- مرحله اول: دریافت شماره -->
    <form v-if="!otpSent" @submit.prevent="requestOtp" class="auth-form">
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
    <form v-else @submit.prevent="verifyOtp" class="auth-form">
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
import { authService } from '@/services/authService'
import { useUserStore } from '@/stores/userStore'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const isLoading = ref(false)
const otpSent = ref(false)

const errorMessage = ref('') // برای خطاهای کلی فرم
const fieldErrors = ref({}) // برای خطاهای اختصاصی هر فیلد

const form = reactive({ phone: '', otpCode: '' })

const validatePhone = () => {
  fieldErrors.value = {}
  let isValid = true

  if (!form.phone) {
    fieldErrors.value.phone = ['شماره موبایل الزامی است']
    isValid = false
  } else if (!/^09\d{9}$/.test(form.phone)) {
    fieldErrors.value.phone = ['شماره موبایل نامعتبر است']
    isValid = false
  }

  return isValid
}

const validateOtpCode = () => {
  fieldErrors.value = {}
  let isValid = true

  if (!form.otpCode) {
    fieldErrors.value.otpCode = ['کد تایید الزامی است']
    isValid = false
  } else if (form.otpCode.length < 5) {
    fieldErrors.value.otpCode = ['کد تایید باید حداقل پنج رقم باشد']
    isValid = false
  }

  return isValid
}

async function requestOtp() {
  errorMessage.value = ''

  if (!validatePhone()) return

  isLoading.value = true

  try {
    await authService.requestOtp(form.phone, 'login')
    otpSent.value = true
  } catch (error) {
    // مدیریت خطاهای بک‌اند (مشابه فایل رمز عبور)
    if (error.error_type === 'RequestValidationError' && error.validation_errors) {
      error.validation_errors.forEach((err) => {
        const fieldName = err.loc[err.loc.length - 1]
        if (!fieldErrors.value[fieldName]) {
          fieldErrors.value[fieldName] = []
        }
        fieldErrors.value[fieldName].push(err.msg)
        return
      })
    }
    if (error.code === 'REGISTERED') {
      errorMessage.value = 'کاربر وجود دارد لطفا با رمز عبور وارد شوید.'
      setTimeout(() => router.push('/auth/login-password'), 2000)
      return
    }
    if (error.code === 'USER_NOT_FOUND') {
      errorMessage.value = 'کاربر یافت نشد لطفا ابتدا ثبت نام کنید.'
      setTimeout(() => router.push('/auth/register'), 2000)
      return
    }
    if (error.status && error.status >= 400 && error.status < 500) {
      errorMessage.value = error.message || 'خطا در درخواست کد.'
      return
    }
  } finally {
    isLoading.value = false
  }
}

async function verifyOtp() {
  errorMessage.value = ''
  fieldErrors.value = {}

  if (!validateOtpCode()) return

  isLoading.value = true

  try {
    const data = await authService.verifyOtp(form.phone, form.otpCode)

    userStore.setAuthSuccess(data.access_token)

    await userStore.initializeAuth()

    setTimeout(() => router.push('/profile'), 500)
  } catch (error) {
    // مدیریت خطاهای بک‌اند
    if (error.error_type === 'RequestValidationError' && error.validation_errors) {
      error.validation_errors.forEach((err) => {
        let fieldName = err.loc[err.loc.length - 1]
        fieldName = fieldName === 'code' ? 'otpCode' : fieldName // مپ کردن فیلد کد

        if (!fieldErrors.value[fieldName]) {
          fieldErrors.value[fieldName] = []
        }
        fieldErrors.value[fieldName].push(err.msg)
        return
      })
    }
    if (error.code === 'INVALID_OTP') {
      errorMessage.value = 'کد وارد شده نامعتبر است.'
      return
    }
    if (error.code === 'ALREADY_EXIST_USER') {
      errorMessage.value = 'کاربر وجود دارد لطفا وارد شوید.'
      setTimeout(() => {
        ;(router.push('/auth/login-password'), (otpSent.value = false))
        form.otpCode = ''
      }, 2000)
      return
    }
    if (error.code === 'USER_NOT_FOUND') {
      errorMessage.value = 'کاربر یافت نشد لطفا ابتدا ثبت نام کنید.'
      setTimeout(() => router.push('/auth/register'), 2000)
      return
    }
    if (error.status && error.status >= 400 && error.status < 500) {
      errorMessage.value = error.message || 'خطا در تایید کد.'
      return
    }
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
