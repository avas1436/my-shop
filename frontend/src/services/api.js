const defaultBaseURL = import.meta.env.DEV ? 'http://127.0.0.1:8000/api' : '/api'
const baseURL = (import.meta.env.VITE_API_BASE_URL || defaultBaseURL).replace(/\/$/, '')

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

function getAuthHeaders(headers = {}) {
  if (typeof window === 'undefined') {
    return headers
  }

  const token = window.localStorage.getItem('shop_access_token')
  if (!token) {
    return headers
  }

  return {
    Authorization: `Bearer ${token}`,
    ...headers,
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${baseURL}${path}`, {
    headers: getAuthHeaders({
      'Content-Type': 'application/json',
      ...options.headers,
    }),
    ...options,
  })

  const payload = await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(getErrorMessage(payload))
  }

  return payload
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
