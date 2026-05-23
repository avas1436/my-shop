// src/utils/token.js

// نام کلید های در حافظه محلی
export const ACCESS_TOKEN_KEY = 'shop_access_token'
export const REFRESH_TOKEN_KEY = 'shop_refresh_token'
export const AUTH_CHANGE_EVENT = 'shop:auth-changed'

// اگر وضعیت توکن ها تغییر کند این کد دیگر قسمت ها و مرورگر را مطلع خواهد کرد
function dispatchAuthChange(accessToken, refreshToken) {
  if (typeof window === 'undefined') {
    return
  }

  window.dispatchEvent(
    new CustomEvent(AUTH_CHANGE_EVENT, {
      detail: {
        accessToken,
        refreshToken,
      },
    }),
  )
}

// دریافت آخرین وضعیت توکن ها از حافظه داخلی
export function getStoredTokens() {
  if (typeof window === 'undefined') {
    return {
      accessToken: '',
      refreshToken: '',
    }
  }

  return {
    accessToken: window.localStorage.getItem(ACCESS_TOKEN_KEY) || '',
    refreshToken: window.localStorage.getItem(REFRESH_TOKEN_KEY) || '',
  }
}

// اگر توکن باشد وارد حافظه میکند و اگر نباشد حافظه را پاک میکند
export function persistTokens(tokens) {
  if (typeof window === 'undefined') {
    return
  }

  const accessToken = tokens?.access_token || ''
  const refreshToken = tokens?.refresh_token || ''

  if (accessToken) {
    window.localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
  } else {
    window.localStorage.removeItem(ACCESS_TOKEN_KEY)
  }

  if (refreshToken) {
    window.localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
  } else {
    window.localStorage.removeItem(REFRESH_TOKEN_KEY)
  }

  dispatchAuthChange(accessToken, refreshToken)
}

// پاکسازی کامل حافظه در زمان خروج
export function clearStoredTokens() {
  if (typeof window === 'undefined') {
    return
  }

  window.localStorage.removeItem(ACCESS_TOKEN_KEY)
  window.localStorage.removeItem(REFRESH_TOKEN_KEY)
  dispatchAuthChange('', '')
}
