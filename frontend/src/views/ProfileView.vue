<template>
  <div class="page-shell">
    <section v-if="!user.isAuthenticated" class="auth-layout">
      <aside class="page-panel auth-panel auth-panel--accent">
        <span class="auth-badge">ورود / ثبت نام</span>
        <h1 class="section-title">حساب کاربری خود را با OTP فعال کنید</h1>
        <p class="section-subtitle">
          شماره موبایل خود را وارد کنید، کد تایید دریافت کنید و با همان کد وارد فروشگاه شوید.
        </p>

        <div class="auth-highlights">
          <article>
            <strong>سریع و بدون رمز</strong>
            <p>ورود و ثبت نام در یک مسیر ساده و یکپارچه انجام می‌شود.</p>
          </article>
          <article>
            <strong>هماهنگ با بک اند</strong>
            <p>ارسال کد و تایید آن مستقیم به API بک اند شما متصل شده است.</p>
          </article>
        </div>
      </aside>

      <section class="page-panel auth-panel auth-panel--form">
        <div class="auth-tabs">
          <button
            type="button"
            class="auth-tab"
            :class="{ 'auth-tab--active': user.otpForm.purpose === 'login' }"
            @click="selectPurpose('login')"
          >
            ورود
          </button>
          <button
            type="button"
            class="auth-tab"
            :class="{ 'auth-tab--active': user.otpForm.purpose === 'register' }"
            @click="selectPurpose('register')"
          >
            ثبت نام
          </button>
        </div>

        <form class="auth-form" @submit.prevent="submitAuth">
          <BaseInput
            v-model="phoneNumber"
            label="شماره موبایل"
            placeholder="مثلا 09121234567"
            inputmode="numeric"
            maxlength="11"
            :error="phoneError"
          />

          <BaseInput
            v-if="user.otpStep === 'code'"
            v-model="otpCode"
            label="کد تایید"
            placeholder="کد پیامک شده را وارد کنید"
            inputmode="numeric"
            maxlength="6"
            :error="codeError"
          />

          <p v-if="user.otpMessage" class="auth-feedback auth-feedback--success">
            {{ user.otpMessage }}
          </p>
          <p v-if="user.otpError" class="auth-feedback auth-feedback--error">
            {{ user.otpError }}
          </p>

          <BaseButton type="submit" size="lg" block :disabled="isSubmitting">
            {{ submitLabel }}
          </BaseButton>

          <BaseButton
            v-if="user.otpStep === 'code'"
            type="button"
            variant="ghost"
            size="md"
            block
            @click="goBackToPhone"
          >
            ویرایش شماره موبایل
          </BaseButton>
        </form>
      </section>
    </section>

    <section v-else class="profile-layout">
      <aside class="page-panel profile-sidebar">
        <div class="profile-sidebar__head">
          <strong>{{ displayName }}</strong>
          <span class="pill">کاربر وارد شده</span>
        </div>

        <ul class="profile-menu">
          <li>اطلاعات حساب</li>
          <li>سفارش ها</li>
          <li>آدرس ها</li>
          <li>وضعیت ورود</li>
        </ul>

        <BaseButton variant="secondary" block @click="user.logout()">خروج از حساب</BaseButton>
      </aside>

      <div class="profile-content">
        <section class="page-panel profile-card">
          <div class="section-head">
            <div>
              <h1 class="section-title">حساب کاربری</h1>
              <p class="section-subtitle">ورود شما با کد یکبار مصرف با موفقیت انجام شده است.</p>
            </div>
          </div>

          <div class="profile-summary">
            <article>
              <span class="muted">شماره تماس</span>
              <strong>{{ userPhone }}</strong>
            </article>
            <article>
              <span class="muted">وضعیت احراز</span>
              <strong>تایید شده</strong>
            </article>
            <article>
              <span class="muted">نوع ورود</span>
              <strong>OTP</strong>
            </article>
          </div>
        </section>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useUserStore } from '@/stores/userStore'

const user = useUserStore()

const phoneNumber = computed({
  get: () => user.otpForm.phone_number,
  set: (value) => user.setOtpField('phone_number', normalizeDigits(value).slice(0, 11)),
})

const otpCode = computed({
  get: () => user.otpForm.code,
  set: (value) => user.setOtpField('code', normalizeDigits(value).slice(0, 6)),
})

const isSubmitting = computed(() => user.otpSending || user.otpVerifying)
const submitLabel = computed(() => {
  if (user.otpSending) {
    return 'در حال ارسال کد...'
  }
  if (user.otpVerifying) {
    return 'در حال تایید کد...'
  }
  return user.otpStep === 'code' ? 'تایید کد و ورود' : 'ارسال کد تایید'
})

const phoneError = computed(() => {
  if (user.otpError && user.otpStep === 'phone') {
    return user.otpError
  }
  return ''
})

const codeError = computed(() => {
  if (user.otpError && user.otpStep === 'code') {
    return user.otpError
  }
  return ''
})

const userPhone = computed(() => formatPhone(user.otpForm.phone_number || getPhoneFromToken(user.token)))
const displayName = computed(() => userPhone.value || 'کاربر فروشگاه')

function normalizeDigits(value) {
  return String(value).replace(/\D/g, '')
}

function formatPhone(value) {
  if (!value) {
    return '-'
  }

  return value.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3')
}

function getPhoneFromToken(token) {
  if (!token) {
    return ''
  }

  try {
    const [, payload] = token.split('.')
    const decoded = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')))
    return decoded.sub || ''
  } catch {
    return ''
  }
}

function selectPurpose(purpose) {
  user.setOtpPurpose(purpose)
  user.clearOtpFeedback()
}

function goBackToPhone() {
  user.setOtpField('code', '')
  user.otpStep = 'phone'
  user.clearOtpFeedback()
}

async function submitAuth() {
  if (user.otpStep === 'phone') {
    await user.requestOtp()
    return
  }

  await user.verifyOtp()
}
</script>

<style scoped>
.auth-layout,
.profile-layout {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 1.25rem;
}

.auth-panel,
.profile-sidebar,
.profile-card {
  padding: 1.5rem;
}

.auth-panel--accent {
  background:
    linear-gradient(135deg, rgba(91, 61, 245, 0.94), rgba(255, 122, 89, 0.92)),
    var(--surface);
  color: #fff;
}

.auth-badge {
  display: inline-flex;
  width: fit-content;
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  margin-bottom: 1rem;
}

.auth-panel--accent :deep(.section-subtitle) {
  color: rgba(255, 255, 255, 0.85);
}

.auth-highlights {
  display: grid;
  gap: 1rem;
  margin-top: 1.5rem;
}

.auth-highlights article {
  padding: 1rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.14);
}

.auth-highlights p {
  margin: 0.4rem 0 0;
  color: rgba(255, 255, 255, 0.82);
}

.auth-panel--form {
  display: grid;
  align-content: start;
  gap: 1.25rem;
}

.auth-tabs {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  padding: 0.35rem;
  border-radius: 999px;
  background: var(--bg-muted);
}

.auth-tab {
  min-height: 48px;
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: var(--text-muted);
  font-weight: 700;
}

.auth-tab--active {
  background: var(--surface-strong);
  color: var(--primary);
  box-shadow: var(--shadow-soft);
}

.auth-form {
  display: grid;
  gap: 1rem;
}

.auth-feedback {
  margin: 0;
  padding: 0.85rem 1rem;
  border-radius: 16px;
  font-size: 0.92rem;
}

.auth-feedback--success {
  background: rgba(15, 157, 129, 0.12);
  color: var(--success);
}

.auth-feedback--error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger);
}

.profile-sidebar {
  display: grid;
  gap: 1rem;
  align-content: start;
}

.profile-sidebar__head {
  display: grid;
  gap: 0.55rem;
}

.profile-menu {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.6rem;
}

.profile-menu li {
  padding: 0.9rem 1rem;
  border-radius: 18px;
  background: var(--bg-muted);
  font-weight: 700;
}

.profile-content {
  display: grid;
  gap: 1.25rem;
}

.profile-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.profile-summary article {
  display: grid;
  gap: 0.35rem;
  padding: 1rem;
  border-radius: 20px;
  background: var(--bg-muted);
}

@media (max-width: 920px) {
  .auth-layout,
  .profile-layout,
  .profile-summary {
    grid-template-columns: 1fr;
  }
}
</style>
