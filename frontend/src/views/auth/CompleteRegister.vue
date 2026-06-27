<!-- src/views/auth/CompleteRegister.vue -->
<template>
  <div
    class="w-full max-w-100 mx-auto p-8 bg-white rounded-md border border-border-light shadow-(--shadow-soft)"
  >
    <h1 class="m-0 text-[1.5rem] font-bold">تکمیل اطلاعات حساب</h1>
    <p class="mt-2 mb-6 text-text-muted">
      لطفا برای استفاده از امکانات سایت، اطلاعات زیر را تکمیل کنید.
    </p>

    <form class="grid gap-5" @submit.prevent="submitProfile">
      <div class="grid gap-1.5">
        <label class="text-sm font-bold">نام</label>
        <BaseInput
          v-model="form.first_name"
          placeholder="مثلا: علی"
          :error="fieldErrors.first_name?.[0]"
        />
      </div>

      <div class="grid gap-1.5">
        <label class="text-sm font-bold">نام خانوادگی</label>
        <BaseInput
          v-model="form.last_name"
          placeholder="مثلا: محمدی"
          :error="fieldErrors.last_name?.[0]"
        />
      </div>

      <div class="grid gap-1.5">
        <label class="text-sm font-bold">رمز عبور</label>
        <BaseInput
          v-model="form.password"
          type="password"
          placeholder="یک رمز عبور امن وارد کنید"
          :error="fieldErrors.password?.[0]"
        />
      </div>

      <div class="grid gap-1.5">
        <label class="text-sm font-bold">تکرار رمز عبور</label>
        <BaseInput
          v-model="form.password_confirm"
          type="password"
          placeholder="رمز عبور خود را مجددا وارد کنید"
          :error="fieldErrors.password_confirm?.[0]"
        />
      </div>

      <p v-if="errorMessage" class="m-0 text-center text-sm text-danger">
        {{ errorMessage }}
      </p>

      <BaseButton type="submit" variant="primary" block :disabled="isLoading">
        {{ isLoading ? 'در حال ثبت...' : 'ثبت اطلاعات و ورود' }}
      </BaseButton>
    </form>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
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
    fieldErrors.value.first_name = [firstNameError]
    isLoading.value = false
    return
  }

  const lastNameError = validatePersianName(form.last_name, 'نام خانوادگی')
  if (lastNameError) {
    fieldErrors.value.last_name = [lastNameError]
    isLoading.value = false
    return
  }

  const passwordError = validatePassword(form.password)
  if (passwordError) {
    fieldErrors.value.password = [passwordError]
    isLoading.value = false
    return
  }

  if (!validateConfirmPassword(form.password, form.password_confirm)) {
    fieldErrors.value.password_confirm = ['رمز عبور و تکرار آن مطابقت ندارند']
    isLoading.value = false
    return
  }

  try {
    const data = await authService.completeRegister(form)
    userStore.setProfile(data.data)
    await router.push('/profile')
  } catch (error) {
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
