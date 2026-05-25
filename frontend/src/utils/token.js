// src/utils/token.js

// نام کلید های در حافظه محلی
export const ACCESS_TOKEN_KEY = 'shop_access_token'

export const AUTH_CHANGE_EVENT = 'shop:auth-changed'

// اگر وضعیت توکن ها تغییر کند این کد دیگر قسمت ها و مرورگر را مطلع خواهد کرد
function dispatchAuthChange(accessToken) {
  if (typeof window === 'undefined') {
    return
  }

  window.dispatchEvent(
    new CustomEvent(AUTH_CHANGE_EVENT, {
      detail: { accessToken },
    }),
  )
}

// دریافت آخرین وضعیت توکن ها از حافظه داخلی
export function getStoredAccessToken() {
  if (typeof window === 'undefined') {
    return null
  }

  return { accessToken: window.localStorage.getItem(ACCESS_TOKEN_KEY) || null }
}

// اگر توکن باشد وارد حافظه میکند و اگر نباشد حافظه را پاک میکند
export function persistAccessToken(token) {
  if (typeof window === 'undefined') {
    return
  }

  const accessToken = token?.access_token || ''

  if (accessToken) {
    window.localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
  } else {
    window.localStorage.removeItem(ACCESS_TOKEN_KEY)
  }

  dispatchAuthChange(accessToken)
}

// پاکسازی کامل حافظه در زمان خروج
export function clearStoredAccessToken() {
  if (typeof window === 'undefined') {
    return
  }

  window.localStorage.removeItem(ACCESS_TOKEN_KEY)
  dispatchAuthChange('')
}
