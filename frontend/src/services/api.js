export const ACCESS_TOKEN_KEY = 'shop_access_token'
export const REFRESH_TOKEN_KEY = 'shop_refresh_token'
export const AUTH_CHANGE_EVENT = 'shop:auth-changed'

const defaultBaseURL = import.meta.env.DEV ? 'http://127.0.0.1:8000/api' : '/api'
const baseURL = (import.meta.env.VITE_API_BASE_URL || defaultBaseURL).replace(/\/$/, '')

let refreshRequestPromise = null

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

export function clearStoredTokens() {
  if (typeof window === 'undefined') {
    return
  }

  window.localStorage.removeItem(ACCESS_TOKEN_KEY)
  window.localStorage.removeItem(REFRESH_TOKEN_KEY)
  dispatchAuthChange('', '')
}

function getErrorMessage(payload) {
  if (!payload) {
    return 'در ارتباط با سرور مشکلی پیش آمد.'
  }

  if (typeof payload.detail === 'string') {
    return payload.detail
  }

  if (Array.isArray(payload.detail)) {
    return payload.detail.map((item) => item.msg).filter(Boolean).join(' - ')
  }

  return payload.message || 'در ارتباط با سرور مشکلی پیش آمد.'
}

function getAuthHeaders(headers = {}, { skipAuth = false } = {}) {
  if (skipAuth || typeof window === 'undefined') {
    return headers
  }

  const { accessToken } = getStoredTokens()
  if (!accessToken) {
    return headers
  }

  return {
    Authorization: `Bearer ${accessToken}`,
    ...headers,
  }
}

async function request(path, options = {}) {
  const { skipAuth = false, skipAuthRefresh = false, ...fetchOptions } = options
  const headers = getAuthHeaders(
    {
      'Content-Type': 'application/json',
      ...fetchOptions.headers,
    },
    { skipAuth },
  )

  const response = await fetch(`${baseURL}${path}`, {
    ...fetchOptions,
    headers,
  })

  const payload = await response.json().catch(() => null)

  if (
    response.status === 401 &&
    !skipAuth &&
    !skipAuthRefresh &&
    path !== '/v1/users/token/refresh' &&
    getStoredTokens().refreshToken
  ) {
    await refreshAuthSession()
    return request(path, {
      ...options,
      skipAuthRefresh: true,
    })
  }

  if (!response.ok) {
    const error = new Error(getErrorMessage(payload))
    error.status = response.status
    error.payload = payload
    throw error
  }

  return payload
}

export async function refreshAuthSession() {
  const { refreshToken } = getStoredTokens()

  if (!refreshToken) {
    const error = new Error('نشست کاربری شما منقضی شده است.')
    error.status = 401
    throw error
  }

  if (!refreshRequestPromise) {
    refreshRequestPromise = request('/v1/users/token/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token: refreshToken }),
      skipAuth: true,
      skipAuthRefresh: true,
    })
      .then((payload) => {
        persistTokens(payload)
        return payload
      })
      .catch((error) => {
        clearStoredTokens()
        throw error
      })
      .finally(() => {
        refreshRequestPromise = null
      })
  }

  return refreshRequestPromise
}

export const api = {
  get(path, options) {
    return request(path, { method: 'GET', ...options })
  },
  post(path, body, options) {
    return request(path, {
      method: 'POST',
      body: JSON.stringify(body),
      ...options,
    })
  },
  put(path, body, options) {
    return request(path, {
      method: 'PUT',
      body: JSON.stringify(body),
      ...options,
    })
  },
  delete(path, options) {
    return request(path, { method: 'DELETE', ...options })
  },
}
