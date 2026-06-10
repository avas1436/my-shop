// src/utils/errorMessages.js
export const ERROR_MESSAGES = {
  // Auth Codes (401)
  MISSING_TOKEN: 'لطفا وارد حساب کاربری خود شوید.',
  INVALID_TOKEN: 'نشست شما منقضی شده است. لطفا مجددا وارد شوید.',

  // Access Control Codes (403)
  ACCOUNT_INACTIVE: 'حساب کاربری شما غیرفعال شده است.',
  ACCOUNT_DELETED: 'حساب کاربری شما حذف شده است.',
  ACCESS_DENIED: 'شما دسترسی لازم برای انجام این عملیات را ندارید.',
  PHONE_NOT_VERIFIED: 'شماره موبایل شما تایید نشده است.',
  PROFILE_INCOMPLETE: 'لطفا اطلاعات پروفایل خود را تکمیل کنید.',
  SESSION_TOO_OLD: 'به دلایل امنیتی لطفا مجددا وارد شوید.',

  // Rate Limit (429)
  RATE_LIMIT_EXCEEDED:
    'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً کمی صبر کرده و مجدداً تلاش کنید.',
  DEFAULT_429: 'درخواست‌های شما خیلی سریع ارسال شده‌اند. لطفاً چند لحظه دیگر دوباره تلاش کنید.',

  // Business Logic
  USER_NOT_FOUND: 'کاربر یافت نشد.',
  INVALID_OTP: 'کد وارد شده نامعتبر است.',
  ALREADY_EXIST_USER: 'این شماره قبلا ثبت نام کرده است.',

  // Defaults
  DEFAULT_4XX: 'درخواست نامعتبر است.',
  DEFAULT_5XX: 'خطایی در سرور رخ داده است. لطفا بعدا تلاش کنید.',
  NETWORK_ERROR: 'ارتباط با سرور برقرار نشد. اینترنت خود را بررسی کنید.',

  REGISTERED: 'کاربر وجود دارد لطفا با رمز عبور وارد شوید.',
  NOT_ACTIVATE_PASSWORD: 'این حساب فاقد رمز عبور می باشد',
  PROFILE_COMPLETED: 'اطلاعات پروفایل شما کامل شده است',
}

export const getErrorMessage = (code) => {
  return ERROR_MESSAGES[code] || null
}
