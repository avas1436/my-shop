<!-- src/views/auth/CompleteRegister.vue -->
<template>
  <div class="auth-card page-panel">
    <h1 class="section-title">تکمیل اطلاعات حساب</h1>
    <p class="muted mb-4">لطفا برای استفاده از امکانات سایت، اطلاعات زیر را تکمیل کنید.</p>

    <form @submit.prevent="submitProfile" class="auth-form">
      <!-- نام -->
      <div class="form-group">
        <label>نام</label>
        <input
          type="text"
          v-model="form.first_name"
          placeholder="مثلا: علی"
          :class="{ 'has-error': fieldErrors.firstName }"
        />
        <span v-if="fieldErrors.firstName" class="error-text field-error">
          {{ fieldErrors.firstName[0] }}
        </span>
      </div>

      <!-- نام خانوادگی -->
      <div class="form-group">
        <label>نام خانوادگی</label>
        <input
          type="text"
          v-model="form.last_name"
          placeholder="مثلا: محمدی"
          :class="{ 'has-error': fieldErrors.lastName }"
        />
        <span v-if="fieldErrors.lastName" class="error-text field-error">
          {{ fieldErrors.lastName[0] }}
        </span>
      </div>

      <!-- رمز عبور -->
      <div class="form-group">
        <label>رمز عبور</label>
        <input
          type="password"
          v-model="form.password"
          placeholder="یک رمز عبور امن وارد کنید"
          :class="{ 'has-error': fieldErrors.password }"
        />
        <span v-if="fieldErrors.password" class="error-text field-error">
          {{ fieldErrors.password[0] }}
        </span>
      </div>

      <!-- تکرار رمز عبور -->
      <div class="form-group">
        <label>تکرار رمز عبور</label>
        <input
          type="password"
          v-model="form.password_confirm"
          placeholder="رمز عبور خود را مجددا وارد کنید"
          :class="{ 'has-error': fieldErrors.password }"
        />
        <span v-if="fieldErrors.password" class="error-text field-error">
          {{ fieldErrors.password[0] }}
        </span>
      </div>

      <p v-if="errorMessage" class="error-text global-error">{{ errorMessage }}</p>

      <BaseButton type="submit" :disabled="isLoading" block>
        {{ isLoading ? 'در حال ثبت...' : 'ثبت اطلاعات و ورود' }}
      </BaseButton>
    </form>
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

const form = ref({
  first_name: '',
  last_name: '',
  password: '',
  password_confirm: '',
})

const isLoading = ref(false)
const errorMessage = ref('')
const fieldErrors = ref({})

const submitProfile = async () => {
  isLoading.value = true
  errorMessage.value = ''
  fieldErrors.value = {}

  try {
    const data = await authService.completeRegister(form.value)

    userStore.setProfile(data.data)

    // انتقال به صفحه اصلی یا داشبورد
    setTimeout(() => router.push('/profile'), 500)
  } catch (error) {
    if (error.response?.status === 422) {
      fieldErrors.value = error.response.data.errors || {}
    } else {
      errorMessage.value = error.response?.data?.message || 'خطایی در ثبت اطلاعات رخ داد.'
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
  margin-bottom: 1.25rem;
  display: grid;
  gap: 0.5rem;
}
.form-group input {
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  transition: border-color 0.2s;
}
.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
}
.form-group input.has-error {
  border-color: #ef4444;
}
.error-text {
  color: #ef4444;
  font-size: 0.875rem;
}
.global-error {
  margin-bottom: 1rem;
  text-align: center;
}
</style>
