import { defineStore } from 'pinia'
import {
  api,
  AUTH_CHANGE_EVENT,
  clearStoredTokens,
  getStoredTokens,
  persistTokens,
  refreshAuthSession,
} from '@/services/api'

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
  state: () => {
    const { accessToken, refreshToken } = getStoredTokens()

    return {
      accessToken,
      refreshToken,
      authMode: AUTH_MODE_PASSWORD,
      loginForm: getDefaultLoginForm(),
      otpForm: getDefaultOtpForm(),
      registerForm: getDefaultRegisterForm(),
      otpStep: OTP_STEP_PHONE,
      otpSending: false,
      otpVerifying: false,
      loginLoading: false,
      registerCompleting: false,
      profileLoading: false,
      authMessage: '',
      authError: '',
      profileError: '',
      profile: null,
    }
  },
  getters: {
    isAuthenticated: (state) => Boolean(state.accessToken || state.refreshToken),
    tokenPayload: (state) => getCurrentPayload(state),
    isNewUser() {
      return Boolean(this.tokenPayload?.is_new)
    },
    userPhone(state) {
      return getPhoneNumber(state)
    },
    displayName(state) {
      if (state.profile?.first_name || state.profile?.last_name) {
        return [state.profile.first_name, state.profile.last_name].filter(Boolean).join(' ')
      }

      return getPhoneNumber(state) || 'کاربر فروشگاه'
    },
  },
  actions: {
    syncTokensFromStorage() {
      const { accessToken, refreshToken } = getStoredTokens()
      this.accessToken = accessToken
      this.refreshToken = refreshToken
    },
    setTokens(tokens) {
      persistTokens(tokens)
      this.syncTokensFromStorage()
    },
    attachAuthListeners() {
      if (typeof window === 'undefined' || authListenersAttached) {
        return
      }

      window.addEventListener(AUTH_CHANGE_EVENT, (event) => {
        this.accessToken = event.detail?.accessToken || ''
        this.refreshToken = event.detail?.refreshToken || ''
      })
      window.addEventListener('storage', () => {
        this.syncTokensFromStorage()
      })
      authListenersAttached = true
    },
    async initializeAuth() {
      this.attachAuthListeners()
      this.syncTokensFromStorage()
      await this.restoreSession()
    },
    setAuthMode(mode) {
      this.authMode = mode
      this.clearFeedback()
    },
    setLoginField(field, value) {
      this.loginForm[field] = value
    },
    setOtpField(field, value) {
      this.otpForm[field] = value
    },
    setRegisterField(field, value) {
      this.registerForm[field] = value
    },
    clearFeedback() {
      this.authMessage = ''
      this.authError = ''
    },
    resetLoginForm() {
      this.loginForm = getDefaultLoginForm()
    },
    resetOtpFlow() {
      this.otpForm = getDefaultOtpForm()
      this.otpStep = OTP_STEP_PHONE
      this.otpSending = false
      this.otpVerifying = false
    },
    resetRegisterForm() {
      this.registerForm = getDefaultRegisterForm()
      this.registerCompleting = false
    },
    async restoreSession() {
      this.syncTokensFromStorage()

      if (!this.accessToken && !this.refreshToken) {
        return
      }

      if (!this.accessToken && this.refreshToken) {
        try {
          await this.refreshSession({ silent: true })
        } catch {
          return
        }
      }

      if (this.isNewUser || this.profile || this.profileLoading) {
        return
      }

      try {
        await this.fetchProfile({ silent: true })
      } catch {
        // Errors are already handled in fetchProfile.
      }
    },
    async refreshSession({ silent = false } = {}) {
      if (!silent) {
        this.clearFeedback()
      }

      try {
        const tokens = await refreshAuthSession()
        this.syncTokensFromStorage()
        return tokens
      } catch (error) {
        this.syncTokensFromStorage()
        if (!silent) {
          this.authError = error.message
        }
        throw error
      }
    },
    async requestOtp() {
      this.otpSending = true
      this.clearFeedback()

      try {
        await api.postData(
          '/v1/users/otp/request',
          {
            phone_number: this.otpForm.phone_number,
            purpose: this.otpForm.purpose,
          },
          { skipAuthRefresh: true },
        )

        this.otpStep = OTP_STEP_CODE
        this.authMessage = 'کد تایید با موفقیت ارسال شد.'
      } catch (error) {
        this.authError = error.message
        throw error
      } finally {
        this.otpSending = false
      }
    },
    async verifyOtp() {
      this.otpVerifying = true
      this.clearFeedback()

      try {
        const response = await api.postData(
          '/v1/users/otp/verify',
          {
            phone_number: this.otpForm.phone_number,
            code: this.otpForm.code,
            purpose: this.otpForm.purpose,
          },
          { skipAuthRefresh: true },
        )

        this.setTokens(response)
        this.otpStep = OTP_STEP_PHONE
        this.otpForm = {
          ...getDefaultOtpForm(),
          phone_number: this.otpForm.phone_number,
        }

        if (this.isNewUser) {
          this.authMessage = 'شماره موبایل تایید شد. حالا اطلاعات حساب را کامل کنید.'
        } else {
          await this.fetchProfile({ silent: true })
          this.authMessage = 'ورود شما با موفقیت انجام شد.'
        }
      } catch (error) {
        this.authError = error.message
        throw error
      } finally {
        this.otpVerifying = false
      }
    },
    async loginWithPassword() {
      this.loginLoading = true
      this.clearFeedback()

      try {
        const response = await api.postData(
          '/v1/users/login/password',
          {
            phone_number: this.loginForm.phone_number,
            password: this.loginForm.password,
          },
          { skipAuthRefresh: true },
        )

        this.setTokens(response)
        await this.fetchProfile({ silent: true })
        this.authMessage = 'ورود شما با رمز عبور با موفقیت انجام شد.'
        this.resetLoginForm()
      } catch (error) {
        this.authError = error.message
        throw error
      } finally {
        this.loginLoading = false
      }
    },
    async completeRegister() {
      const phoneNumber = this.userPhone
      const password = this.registerForm.password

      this.registerCompleting = true
      this.clearFeedback()

      try {
        await api.postData('/v1/users/register/complete', {
          first_name: this.registerForm.first_name,
          last_name: this.registerForm.last_name,
          birth_date: this.registerForm.birth_date || null,
          password,
          password_confirm: this.registerForm.password_confirm,
        })
      } catch (error) {
        this.authError = error.message
        throw error
      }

      try {
        const response = await api.postData(
          '/v1/users/login/password',
          {
            phone_number: phoneNumber,
            password,
          },
          { skipAuthRefresh: true },
        )

        this.setTokens(response)
        await this.fetchProfile({ silent: true })
        this.resetRegisterForm()
        this.resetOtpFlow()
        this.authMode = AUTH_MODE_PASSWORD
        this.authMessage = 'حساب کاربری شما تکمیل شد و وارد شدید.'
      } catch (error) {
        clearStoredTokens()
        this.syncTokensFromStorage()
        this.profile = null
        this.resetRegisterForm()
        this.resetOtpFlow()
        this.authMode = AUTH_MODE_PASSWORD
        this.loginForm.phone_number = phoneNumber
        this.authError = 'اطلاعات حساب ذخیره شد. برای ادامه، با رمز عبور وارد شوید.'
        throw error
      } finally {
        this.registerCompleting = false
      }
    },
    async fetchProfile({ silent = false } = {}) {
      this.syncTokensFromStorage()

      if ((!this.accessToken && !this.refreshToken) || this.isNewUser) {
        return null
      }

      this.profileLoading = true
      if (!silent || !this.profile) {
        this.profileError = ''
      }

      try {
        const profile = await api.getData('/v1/users/me')
        this.syncTokensFromStorage()
        this.profile = profile
        return profile
      } catch (error) {
        this.syncTokensFromStorage()
        this.profile = null
        this.profileError = error.message

        if (error.status === 401) {
          await this.logout({ revoke: false })
        }

        throw error
      } finally {
        this.profileLoading = false
      }
    },
    async logout({ revoke = true } = {}) {
      const phoneNumber = this.userPhone
      const refreshToken = this.refreshToken

      if (revoke && refreshToken) {
        try {
          await api.postData(
            '/v1/users/logout',
            { refresh_token: refreshToken },
            {
              skipAuthRefresh: true,
            },
          )
        } catch {
          // Local logout should continue even if revoke fails.
        }
      }

      clearStoredTokens()
      this.syncTokensFromStorage()
      this.profile = null
      this.profileError = ''
      this.profileLoading = false
      this.clearFeedback()
      this.resetRegisterForm()
      this.resetOtpFlow()
      this.resetLoginForm()
      this.loginForm.phone_number = phoneNumber
      this.authMode = AUTH_MODE_PASSWORD
    },
  },
})
