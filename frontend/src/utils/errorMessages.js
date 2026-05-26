// src/utils/errorMessages.js
export const ERROR_MESSAGES = {
  REGISTERED: 'کاربر وجود دارد لطفا با رمز عبور وارد شوید.',
  USER_NOT_FOUND: 'کاربر یافت نشد لطفا ابتدا ثبت نام کنید.',
  INVALID_OTP: 'کد وارد شده نامعتبر است.',
  ALREADY_EXIST_USER: 'کاربر وجود دارد لطفا وارد شوید.',
  DEFAULT_4XX: 'خطا در انجام درخواست.',
  DEFAULT_5XX: 'خطای سرور. لطفا بعدا تلاش کنید.',
}

export const getErrorMessage = (code) => {
  return ERROR_MESSAGES[code] || 'خطای نامشخصی رخ داده است.'
}
