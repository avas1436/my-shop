import { defineStore } from 'pinia'
import { api } from '@/services/api'

const TOKEN_KEY = 'shop_access_token'
const OTP_STEP_PHONE = 'phone'
const OTP_STEP_CODE = 'code'

function getStoredToken() {
  if (typeof window === 'undefined') {
    return ''
  }

  return window.localStorage.getItem(TOKEN_KEY) || ''
}

function getDefaultOtpForm() {
  return {
    phone_number: '',
    code: '',
    purpose: 'login',
  }
}

export const useUserStore = defineStore('user', {
  state: () => ({
    token: getStoredToken(),
    otpForm: getDefaultOtpForm(),
    otpStep: OTP_STEP_PHONE,
    otpSending: false,
    otpVerifying: false,
    otpMessage: '',
    otpError: '',
    profile: null,
    addresses: [],
    orders: [],
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    setOtpField(field, value) {
      this.otpForm[field] = value
    },
    setOtpPurpose(purpose) {
      this.otpForm.purpose = purpose
    },
    clearOtpFeedback() {
      this.otpError = ''
      this.otpMessage = ''
    },
    resetOtpFlow() {
      this.otpForm = getDefaultOtpForm()
      this.otpStep = OTP_STEP_PHONE
      this.clearOtpFeedback()
      this.otpSending = false
      this.otpVerifying = false
    },
    async requestOtp() {
      this.otpSending = true
      this.clearOtpFeedback()

      try {
        await api.post('/v1/users/otp/request', {
          phone_number: this.otpForm.phone_number,
          purpose: this.otpForm.purpose,
        })

        this.otpStep = OTP_STEP_CODE
        this.otpMessage = 'کد تایید با موفقیت ارسال شد.'
      } catch (error) {
        this.otpError = error.message
        throw error
      } finally {
        this.otpSending = false
      }
    },
    async verifyOtp() {
      this.otpVerifying = true
      this.clearOtpFeedback()

      try {
        const response = await api.post('/v1/users/otp/verify', {
          phone_number: this.otpForm.phone_number,
          code: this.otpForm.code,
          purpose: this.otpForm.purpose,
        })

        this.token = response.access_token
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(TOKEN_KEY, response.access_token)
        }
        this.otpMessage = 'ورود شما با موفقیت انجام شد.'
        this.otpStep = OTP_STEP_PHONE
        this.otpForm = getDefaultOtpForm()
      } catch (error) {
        this.otpError = error.message
        throw error
      } finally {
        this.otpVerifying = false
      }
    },
    logout() {
      this.token = ''
      if (typeof window !== 'undefined') {
        window.localStorage.removeItem(TOKEN_KEY)
      }
      this.resetOtpFlow()
    },
  },
})
