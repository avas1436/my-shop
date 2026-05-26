import { ERROR_MESSAGES, getErrorMessage } from '@/utils/errorMessages'
import { ref } from 'vue'

export function useApiError(fieldMap = {}) {
  const errorMessage = ref('')
  const fieldErrors = ref({})

  const clearErrors = () => {
    errorMessage.value = ''
    fieldErrors.value = {}
  }

  const handleApiError = (error) => {
    clearErrors()

    // ۱. مدیریت خطاهای اعتبارسنجی (Validation Errors)
    if (error.error_type === 'RequestValidationError' && error.validation_errors) {
      error.validation_errors.forEach((err) => {
        let fieldName = err.loc[err.loc.length - 1]
        // مپ کردن فیلدها (مثلا code به otpCode)
        if (fieldMap[fieldName]) {
          fieldName = fieldMap[fieldName]
        }

        if (!fieldErrors.value[fieldName]) {
          fieldErrors.value[fieldName] = []
        }
        fieldErrors.value[fieldName].push(err.msg)
      })
      return error.code // برگرداندن کد خطا برای اکشن‌های خاص
    }

    // ۲. مدیریت خطاهای دارای کد اختصاصی
    if (error.code) {
      errorMessage.value = getErrorMessage(error.code)
      return error.code
    }

    // ۳. مدیریت خطاهای عمومی HTTP
    if (error.status) {
      if (error.status >= 400 && error.status < 500) {
        errorMessage.value = error.message || ERROR_MESSAGES.DEFAULT_4XX
      } else if (error.status >= 500) {
        errorMessage.value = ERROR_MESSAGES.DEFAULT_5XX
      }
    }

    return null
  }

  return {
    errorMessage,
    fieldErrors,
    clearErrors,
    handleApiError,
  }
}
