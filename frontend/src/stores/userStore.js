import { defineStore } from 'pinia'

const AUTH_MODE_PASSWORD = 'password'
const OTP_STEP_PHONE = 'phone'
const OTP_STEP_CODE = 'code'

let authListenersAttached = false

function getDefaultLoginForm() {
  return {
    phone_number: '',
    password: '',
  }
}

function getDefaultOtpForm() {
  return {
    phone_number: '',
    code: '',
    purpose: 'register',
  }
}

function getDefaultRegisterForm() {
  return {
    first_name: '',
    last_name: '',
    birth_date: '',
    password: '',
    password_confirm: '',
  }
}

function decodeTokenPayload(token) {
  if (!token) {
    return null
  }

  try {
    const [, payload] = token.split('.')
    if (!payload) {
      return null
    }

    const normalized = payload
      .replace(/-/g, '+')
      .replace(/_/g, '/')
      .padEnd(Math.ceil(payload.length / 4) * 4, '=')

    const decodeBase64 = typeof window !== 'undefined' ? window.atob : globalThis.atob
    return JSON.parse(decodeBase64(normalized))
  } catch {
    return null
  }
}

function getCurrentPayload(state) {
  return decodeTokenPayload(state.accessToken) || decodeTokenPayload(state.refreshToken)
}

function getPhoneNumber(state) {
  return (
    state.profile?.phone_number ||
    getCurrentPayload(state)?.sub ||
    state.otpForm.phone_number ||
    state.loginForm.phone_number ||
    ''
  )
}

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: {
      customerId: 1,
      name: 'آوا رضایی',
      email: 'ava@example.com',
      phone: '۰۹۱۲ ۱۲۳ ۴۵۶۷',
      membership: 'طلایی',
      wallet: 1450000,
      loyaltyPoints: 1280,
    },
    addresses: [
      {
        id: 1,
        title: 'خانه',
        city: 'تهران',
        details: 'تهران، سعادت‌آباد، سرو غربی، پلاک ۲۴، واحد ۶',
      },
      {
        id: 2,
        title: 'محل کار',
        city: 'تهران',
        details: 'تهران، ونک، خیابان خدامی، برج آفتاب، طبقه ۵',
      },
    ],
  }),

  getters: {
    primaryAddress: (state) => state.addresses[0] || null,
  },

  actions: {
    addAddress(address) {
      this.addresses.push({
        id: Date.now(),
        city: address.city || 'تهران',
        ...address,
      })
    },
    updateProfile(patch) {
      this.profile = {
        ...this.profile,
        ...patch,
      }
    },
  },
})
