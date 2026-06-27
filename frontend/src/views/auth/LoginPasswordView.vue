<!-- src/views/auth/LoginPasswordView.vue -->
<template>
  <div
    class="w-full max-w-100 mx-auto p-8 bg-white rounded-md border border-border-light shadow-(--shadow-soft)"
  >
    <h1 class="m-0 text-[1.5rem] font-bold">ورود به حساب کاربری</h1>
    <p class="mt-2 mb-6 text-text-muted">لطفا شماره موبایل و رمز عبور خود را وارد کنید.</p>

    <form class="grid gap-5" @submit.prevent="handleSubmit">
      <div class="grid gap-1.5">
        <label class="text-sm font-bold">شماره موبایل</label>
        <BaseInput
          v-model="form.phone"
          type="text"
          placeholder="۰۹۱۲۳۴۵۶۷۸۹"
          :error="fieldErrors.phone?.[0]"
        />
      </div>

      <div class="grid gap-1.5">
        <label class="text-sm font-bold">رمز عبور</label>
        <BaseInput
          v-model="form.password"
          type="password"
          placeholder="********"
          :error="fieldErrors.password?.[0]"
        />
      </div>

      <p v-if="errorMessage" class="m-0 text-center text-sm text-danger">{{ errorMessage }}</p>

      <BaseButton type="submit" variant="primary" block :disabled="isLoading">
        {{ isLoading ? 'در حال ورود...' : 'ورود' }}
      </BaseButton>
    </form>

    <div class="mt-6 grid gap-2 text-center text-sm">
      <router-link :to="{ name: 'login-otp' }" class="text-primary font-bold">
        ورود با رمز یکبار مصرف (OTP)
      </router-link>
      <router-link
        :to="{ name: 'register' }"
        class="text-text-muted hover:text-primary transition-colors"
      >
        ثبت‌نام نکرده‌اید؟
      </router-link>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { authService } from '@/services/authService'
import { useUserStore } from '@/stores/userStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { validatePassword, validatePhoneNumber } from '@/utils/validators'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const isLoading = ref(false)
const errorMessage = ref('')
const fieldErrors = ref({})

const form = reactive({ phone: '', password: '' })

const validateForm = () => {
  fieldErrors.value = {}

  const errorPhone = validatePhoneNumber(form.phone)
  if (errorPhone) fieldErrors.value.phone = [errorPhone]

  const errorPass = validatePassword(form.password)
  if (errorPass) fieldErrors.value.password = [errorPass]

  return !errorPhone && !errorPass
}

async function handleSubmit() {
  errorMessage.value = ''
  fieldErrors.value = {}

  if (!validateForm()) return

  isLoading.value = true
  try {
    const data = await authService.loginWithPassword(form.phone, form.password)
    userStore.setAuthSuccess(data)
    await userStore.initializeAuth(true)
    router.push('/profile')
  } catch (error) {
    errorMessage.value = getErrorMessage(error.code)
  } finally {
    isLoading.value = false
  }
}
</script>
