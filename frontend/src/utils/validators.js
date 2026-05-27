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
  return null
}

export const validatePassword = (otpCode) => {
  if (!otpCode) {
    return 'رمز عبور الزامی است'
  }
  if (otpCode.length < 4) {
    return 'رمز عبور باید حداقل چهار رقم باشد'
  }
  return null
}
