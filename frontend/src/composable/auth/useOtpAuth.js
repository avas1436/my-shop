// composables/auth/useOtpAuth.js
import { authService } from '@/services/authService'
import { useUserStore } from '@/stores/userStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { validateOtp, validatePhoneNumber } from '@/utils/validators'
import { reactive, ref } from 'vue'

export function useOtpAuth(options = {}) {
  const userStore = useUserStore()

  const isLoading = ref(false)
  const otpSent = ref(false)

  const errorMessage = ref('')
  const fieldErrors = ref({})

  const form = reactive({ phone: '', otpCode: '' })

  const validatePhone = () => {
    fieldErrors.value = {}
    const errorMsg = validatePhoneNumber(form.phone)
    if (errorMsg) {
      fieldErrors.value.phone = [errorMsg]
      return false
    }
    return true
  }

  const validateOtpCode = () => {
    fieldErrors.value = {}
    const errorMsg = validateOtp(form.otpCode)
    if (errorMsg) {
      fieldErrors.value.otpCode = [errorMsg]
      return false
    }
    return true
  }

  // گرفتن پارامتر هدف (login, register, reset)
  const requestOtp = async (purpose = 'login') => {
    errorMessage.value = ''
    fieldErrors.value = {}

    if (!validatePhone()) return false

    isLoading.value = true
    try {
      await authService.requestOtp(form.phone, purpose)
      otpSent.value = true

      // فراخوانی در صورت نیاز به انجام کار خاص بعد از ارسال موفق
      if (options.onRequestSuccess) options.onRequestSuccess()

      return true
    } catch (error) {
      errorMessage.value = getErrorMessage(error.code) || error.message || 'خطا در درخواست کد.'

      // سپردن مدیریت خطاهای خاص به کامپوننت
      if (options.onRequestError) options.onRequestError(error)

      return false
    } finally {
      isLoading.value = false
    }
  }

  // در verify معمولا به purpose نیاز نیست مگر اینکه API شما بخواهد
  const verifyOtp = async (purpose = 'login') => {
    errorMessage.value = ''
    fieldErrors.value = {}

    if (!validateOtpCode()) return false

    isLoading.value = true
    try {
      const data = await authService.verifyOtp(form.phone, form.otpCode, purpose)
      userStore.setAuthSuccess(data.access_token)
      await userStore.initializeAuth(true)

      if (options.onVerifySuccess) options.onVerifySuccess(data)

      return true
    } catch (error) {
      errorMessage.value = getErrorMessage(error.code) || error.message || 'خطا در تایید کد.'

      if (options.onVerifyError) options.onVerifyError(error)

      return false
    } finally {
      isLoading.value = false
    }
  }

  return {
    form,
    isLoading,
    otpSent,
    errorMessage,
    fieldErrors,
    requestOtp,
    verifyOtp,
  }
}
