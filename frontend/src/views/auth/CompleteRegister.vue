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
          :class="{ 'has-error': fieldErrors.first_name }"
        />
        <span v-if="fieldErrors.first_name" class="error-text field-error">
          {{ fieldErrors.first_name[0] }}
        </span>
      </div>

      <!-- نام خانوادگی -->
      <div class="form-group">
        <label>نام خانوادگی</label>
        <input
          type="text"
          v-model="form.last_name"
          placeholder="مثلا: محمدی"
          :class="{ 'has-error': fieldErrors.last_name }"
        />
        <span v-if="fieldErrors.last_name" class="error-text field-error">
          {{ fieldErrors.last_name[0] }}
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
          :class="{ 'has-error': fieldErrors.password_confirm }"
        />
        <span v-if="fieldErrors.password_confirm" class="error-text field-error">
          {{ fieldErrors.password_confirm[0] }}
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
import { validateConfirmPassword, validatePassword, validatePersianName } from '@/utils/validators'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
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

  const firstNameError = validatePersianName(form.first_name, 'نام')
  if (firstNameError) {
    isLoading.value = false
    fieldErrors.value.first_name = [firstNameError]
    return
  }

  const lastNameError = validatePersianName(form.last_name, 'نام خانوادگی')
  if (lastNameError) {
    isLoading.value = false
    fieldErrors.value.last_name = [lastNameError]
    return
  }

  const passwordError = validatePassword(form.password)
  if (passwordError) {
    isLoading.value = false
    fieldErrors.value.password = [passwordError]
    return
  }

  if (!validateConfirmPassword(form.password, form.password_confirm)) {
    isLoading.value = false
    fieldErrors.value.password_confirm = ['رمز عبور و تکرار آن مطابقت ندارند']
    return
  }

  try {
    const data = await authService.completeRegister(form)

    userStore.setProfile(data.data)

    // انتقال به صفحه اصلی یا داشبورد
    await router.push('/profile')
  } catch (error) {
    // if (error.response?.status === 422) {
    //   fieldErrors.value = error.response.data.errors || {}
    // }
    if (error.validation_errors) {
      fieldErrors.value = error.validation_errors.reduce((acc, curr) => {
        const field = curr.loc[curr.loc.length - 1]
        acc[field] = [curr.msg]
        return acc
      }, {})
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
