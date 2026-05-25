// src/services/authService.js
import {
  clearStoredAccessToken,
  persistAccessToken
} from '@/utils/token'
import axiosClient from './axiosClient'

export const authService = {
  /**
   * درخواست کد تایید پیامکی (OTP)
   */
  async requestOtp(phoneNumber, purpose) {
    return await axiosClient.post(
      '/v1/users/otp/request',
      { phone_number: phoneNumber, purpose: purpose },
      { skipAuth: true },
    )
  },

  /**
   * تایید کد OTP و دریافت توکن‌ها
   */
  async verifyOtp(phoneNumber, code, purpose) {
    const data = await axiosClient.post(
      '/v1/users/otp/verify',
      { phone_number: phoneNumber, code: code, purpose: purpose },
      { skipAuth: true },
    )
    // ذخیره توکن‌ها در لوکال استورج
    if (data?.access_token) {
      persistAccessToken(data)
    }
    return data
  },

  /**
   * ورود با رمز عبور
   */
  async loginWithPassword(phoneNumber, password) {
    const data = await axiosClient.post(
      '/v1/users/login/password',
      { phone_number: phoneNumber, password },
      { skipAuth: true },
    )
    // ذخیره توکن‌ها
    if (data?.access_token) {
      persistAccessToken(data)
    }
    return data
  },

  /**
   * تکمیل ثبت نام کاربر جدید
   */
  async completeRegister(userData) {
    // userData باید شامل first_name, last_name, birth_date, password باشد
    return await axiosClient.post('/v1/users/register/complete', userData)
  },

  /**
   * دریافت اطلاعات کاربر فعلی
   */
  getMe() {
    return axiosClient.get('/v1/users/me')
  },

  /**
   * خروج از حساب کاربری فعلی
   */
  async logout() {
    try {
      await axiosClient.post('/v1/users/logout', {})
    } finally {
      // پاک کردن توکن‌ها در هر صورت
      clearStoredAccessToken()
    }
  },

  /**
   * خروج از همه دستگاه‌ها
   */
  async logoutAll(phone_number) {
    try {
      await axiosClient.post('/v1/users/logout/all', { phone_number })
    } finally {
      clearStoredAccessToken()
    }
  },
}
