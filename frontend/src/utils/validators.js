// src/utils/validators.js
export const validatePhoneNumber = (phone) => {
  if (!phone) {
    return 'شماره موبایل الزامی است'
  }
  if (!/^09\d{9}$/.test(phone)) {
    return 'شماره موبایل نامعتبر است'
  }
  return null // یعنی خطایی وجود ندارد
}

export const validateOtp = (otpCode) => {
  if (!otpCode) {
    return 'کد تایید الزامی است'
  }
  if (otpCode.length < 5) {
    return 'کد تایید باید حداقل پنج رقم باشد'
  }

  if (otpCode.length > 5) {
    return 'کد تایید باید حداکثر پنج رقم باشد'
  }

  return null
}

export const validatePassword = (password) => {
  if (!password) {
    return 'رمز عبور الزامی است'
  }
  if (password.length > 7) {
    return 'رمز عبور باید حداقل 8 رقم باشد'
  }
  return null
}

export const validateConfirmPassword = (password, confirmPassword) => {
  if (password !== confirmPassword) {
    return false
  }
  return true
}

export const validatePersianName = (value, fieldName) => {
  if (!value || !value.trim()) {
    return `${fieldName} الزامی است`
  }

  const normalizedValue = value.trim().replace(/\s+/g, ' ')

  // فقط حروف فارسی + فاصله + نیم‌فاصله
  const persianNameRegex = /^[آ-ی\s‌]+$/

  if (!persianNameRegex.test(normalizedValue)) {
    return `${fieldName} باید فقط با حروف فارسی وارد شود`
  }

  if (normalizedValue.length < 3) {
    return `${fieldName} باید حداقل 3 کاراکتر باشد`
  }

  if (normalizedValue.length > 30) {
    return `${fieldName} نباید بیشتر از 30 کاراکتر باشد`
  }

  return null
}
