<!-- src/views/ProfileView.vue -->
<template>
  <div class="page-shell">
    <section v-if="!user.isAuthenticated" class="auth-layout">
      <aside class="page-panel auth-panel auth-panel--accent">
        <span class="auth-badge">حساب کاربری</span>
        <h1 class="section-title">ورود با رمز عبور و ثبت نام مرحله ای</h1>
        <p class="section-subtitle">
          برای کاربران جدید ابتدا شماره موبایل تایید می شود، سپس اطلاعات حساب شامل نام، تاریخ تولد و
          رمز عبور ثبت خواهد شد.
        </p>

        <div class="auth-highlights">
          <article>
            <strong>ورود سریع با رمز</strong>
            <p>کاربران قبلی می توانند مستقیم با شماره موبایل و رمز عبور وارد شوند.</p>
          </article>
          <article>
            <strong>هماهنگ با API جدید</strong>
            <p>دریافت پروفایل، تکمیل ثبت نام و ذخیره JWT همگی با روت های جدید متصل شده اند.</p>
          </article>
        </div>
      </aside>

      <section class="page-panel auth-panel auth-panel--form">
        <div class="auth-tabs">
          <button
            type="button"
            class="auth-tab"
            :class="{ 'auth-tab--active': user.authMode === 'password' }"
            @click="user.setAuthMode('password')"
          >
            ورود با رمز
          </button>
          <button
            type="button"
            class="auth-tab"
            :class="{ 'auth-tab--active': user.authMode === 'register' }"
            @click="user.setAuthMode('register')"
          >
            ثبت نام
          </button>
        </div>

        <form
          v-if="user.authMode === 'password'"
          class="auth-form"
          @submit.prevent="submitPasswordLogin"
        >
          <BaseInput
            v-model="loginPhone"
            label="شماره موبایل"
            type="tel"
            placeholder="مثلا 09121234567"
            inputmode="numeric"
            maxlength="11"
            required
          />

          <BaseInput
            v-model="loginPassword"
            label="رمز عبور"
            type="password"
            placeholder="رمز عبور خود را وارد کنید"
            required
          />

          <p v-if="user.authMessage" class="auth-feedback auth-feedback--success">
            {{ user.authMessage }}
          </p>
          <p v-if="user.authError" class="auth-feedback auth-feedback--error">
            {{ user.authError }}
          </p>

          <BaseButton type="submit" size="lg" block :disabled="user.loginLoading">
            {{ passwordSubmitLabel }}
          </BaseButton>
        </form>

        <form v-else class="auth-form" @submit.prevent="submitRegisterOtp">
          <BaseInput
            v-model="registerPhone"
            label="شماره موبایل"
            type="tel"
            placeholder="مثلا 09121234567"
            inputmode="numeric"
            maxlength="11"
            required
          />

          <BaseInput
            v-if="user.otpStep === 'code'"
            v-model="otpCode"
            label="کد تایید"
            type="tel"
            placeholder="کد پیامک شده را وارد کنید"
            inputmode="numeric"
            maxlength="6"
            required
          />

          <p class="auth-hint">
            این مرحله فقط برای ساخت حساب جدید است و پس از تایید شماره، فرم تکمیل اطلاعات نمایش داده
            می شود.
          </p>

          <p v-if="user.authMessage" class="auth-feedback auth-feedback--success">
            {{ user.authMessage }}
          </p>
          <p v-if="user.authError" class="auth-feedback auth-feedback--error">
            {{ user.authError }}
          </p>

          <BaseButton type="submit" size="lg" block :disabled="registerOtpDisabled">
            {{ registerOtpSubmitLabel }}
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

    <section v-else-if="user.isNewUser" class="profile-layout">
      <aside class="page-panel profile-sidebar profile-sidebar--pending">
        <div class="profile-sidebar__head">
          <strong>{{ formatPhone(user.userPhone) }}</strong>
          <span class="pill pill--warning">ثبت نام نیمه تمام</span>
        </div>

        <ul class="profile-menu">
          <li>شماره موبایل تایید شده است</li>
          <li>نام و نام خانوادگی را وارد کنید</li>
          <li>تاریخ تولد و رمز عبور را ثبت کنید</li>
        </ul>

        <BaseButton variant="secondary" block @click="user.logout()">انصراف و خروج</BaseButton>
      </aside>

      <section class="page-panel profile-card">
        <div class="section-head">
          <div>
            <h1 class="section-title">تکمیل اطلاعات حساب</h1>
            <p class="section-subtitle">
              برای نهایی شدن ثبت نام، اطلاعات کاربری و رمز عبور را ثبت کنید.
            </p>
          </div>
        </div>

        <form class="complete-form" @submit.prevent="submitCompleteRegister">
          <div class="form-grid">
            <BaseInput v-model="firstName" label="نام" placeholder="نام" required />
            <BaseInput
              v-model="lastName"
              label="نام خانوادگی"
              placeholder="نام خانوادگی"
              required
            />
            <BaseInput v-model="birthDate" label="تاریخ تولد" type="date" required />
            <BaseInput
              v-model="registerPassword"
              label="رمز عبور"
              type="password"
              placeholder="رمز عبور جدید"
              required
            />
            <BaseInput
              v-model="registerPasswordConfirm"
              label="تکرار رمز عبور"
              type="password"
              placeholder="تکرار رمز عبور"
              required
            />
          </div>

          <p class="auth-hint">
            رمز عبور باید حداقل 8 کاراکتر بوده و شامل حروف کوچک و بزرگ، عدد و کاراکتر ویژه باشد.
          </p>

          <p v-if="user.authMessage" class="auth-feedback auth-feedback--success">
            {{ user.authMessage }}
          </p>
          <p v-if="user.authError" class="auth-feedback auth-feedback--error">
            {{ user.authError }}
          </p>

          <BaseButton type="submit" size="lg" block :disabled="user.registerCompleting">
            {{ completeRegisterLabel }}
          </BaseButton>
        </form>
      </section>
    </section>

    <section v-else class="profile-layout">
      <aside class="page-panel profile-sidebar">
        <div class="profile-sidebar__head">
          <strong>{{ user.displayName }}</strong>
          <span class="pill">ورود موفق</span>
        </div>

        <ul class="profile-menu">
          <li>{{ formatPhone(user.userPhone) }}</li>
          <li>JWT ذخیره شده و آماده استفاده است</li>
          <li>اطلاعات حساب از بک اند دریافت می شود</li>
        </ul>

        <BaseButton variant="secondary" block @click="user.logout()">خروج از حساب</BaseButton>
      </aside>

      <div class="profile-content">
        <section class="page-panel profile-card">
          <div class="section-head section-head--spread">
            <div>
              <h1 class="section-title">اطلاعات حساب</h1>
              <p class="section-subtitle">نمایش اطلاعات کاربر از مسیر `GET /v1/users/me`.</p>
            </div>
            <BaseButton
              type="button"
              variant="ghost"
              size="md"
              :disabled="user.profileLoading"
              @click="refreshProfile"
            >
              بروزرسانی
            </BaseButton>
          </div>

          <p v-if="user.profileError" class="auth-feedback auth-feedback--error">
            {{ user.profileError }}
          </p>
          <p v-if="user.profileLoading && !user.profile" class="auth-feedback">
            در حال دریافت اطلاعات حساب...
          </p>

          <div v-else-if="user.profile" class="profile-summary profile-summary--details">
            <article>
              <span class="muted">نام</span>
              <strong>{{ user.profile.first_name || '-' }}</strong>
            </article>
            <article>
              <span class="muted">نام خانوادگی</span>
              <strong>{{ user.profile.last_name || '-' }}</strong>
            </article>
            <article>
              <span class="muted">شماره تماس</span>
              <strong>{{ formatPhone(user.profile.phone_number) }}</strong>
            </article>
            <article>
              <span class="muted">تاریخ تولد</span>
              <strong>{{ formatDate(user.profile.birth_date) }}</strong>
            </article>
            <article>
              <span class="muted">امتیاز باشگاه مشتریان</span>
              <strong>{{ formatNumber(user.profile.loyaltyPoints) }}</strong>
              <span class="muted">سن</span>
              <strong>{{ user.profile.age ?? '-' }}</strong>
            </article>
          </div>
        </section>

        <section class="page-panel profile-card">
          <h2 class="section-title">سفارش‌های اخیر</h2>
          <div class="profile-orders">
            <article v-for="order in userOrders" :key="order.id" class="profile-order">
              <div>
                <strong>{{ order.id }}</strong>
                <p class="muted">{{ order.date }}</p>
              </div>
              <span class="pill">{{ order.status }}</span>
              <strong>{{ formatPrice(order.total) }}</strong>
            </article>
            <article>
              <span class="muted">وضعیت حساب</span>
              <strong>{{ user.profile.is_active ? 'فعال' : 'غیرفعال' }}</strong>
            </article>
            <article>
              <span class="muted">تایید شماره موبایل</span>
              <strong>{{ user.profile.is_phone_verified ? 'تایید شده' : 'در انتظار' }}</strong>
            </article>
            <article>
              <span class="muted">تاریخ عضویت</span>
              <strong>{{ formatDateTime(user.profile.created_at) }}</strong>
            </article>
          </div>
        </section>
      </div>
    </section>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useAdminStore } from '@/stores/adminStore'
import { useUserStore } from '@/stores/userStore'
import { formatNumber, formatPrice } from '@/utils/format'
import { computed, onMounted } from 'vue'

const user = useUserStore()
const admin = useAdminStore()
const userOrders = computed(() => admin.ordersByCustomer(user.profile.customerId))

onMounted(() => {
  user.restoreSession()
})

const loginPhone = computed({
  get: () => user.loginForm.phone_number,
  set: (value) => user.setLoginField('phone_number', normalizeDigits(value).slice(0, 11)),
})

const loginPassword = computed({
  get: () => user.loginForm.password,
  set: (value) => user.setLoginField('password', value),
})

const registerPhone = computed({
  get: () => user.otpForm.phone_number,
  set: (value) => user.setOtpField('phone_number', normalizeDigits(value).slice(0, 11)),
})

const otpCode = computed({
  get: () => user.otpForm.code,
  set: (value) => user.setOtpField('code', normalizeDigits(value).slice(0, 6)),
})

const firstName = computed({
  get: () => user.registerForm.first_name,
  set: (value) => user.setRegisterField('first_name', value),
})

const lastName = computed({
  get: () => user.registerForm.last_name,
  set: (value) => user.setRegisterField('last_name', value),
})

const birthDate = computed({
  get: () => user.registerForm.birth_date,
  set: (value) => user.setRegisterField('birth_date', value),
})

const registerPassword = computed({
  get: () => user.registerForm.password,
  set: (value) => user.setRegisterField('password', value),
})

const registerPasswordConfirm = computed({
  get: () => user.registerForm.password_confirm,
  set: (value) => user.setRegisterField('password_confirm', value),
})

const passwordSubmitLabel = computed(() => (user.loginLoading ? 'در حال ورود...' : 'ورود به حساب'))

const registerOtpSubmitLabel = computed(() => {
  if (user.otpSending) {
    return 'در حال ارسال کد...'
  }
  if (user.otpVerifying) {
    return 'در حال تایید کد...'
  }

  return user.otpStep === 'code' ? 'تایید کد و ادامه' : 'ارسال کد تایید'
})

const completeRegisterLabel = computed(() =>
  user.registerCompleting ? 'در حال تکمیل حساب...' : 'ذخیره اطلاعات و ورود',
)

const registerOtpDisabled = computed(() => user.otpSending || user.otpVerifying)

function toEnglishDigits(value) {
  return String(value).replace(/[۰-۹]/g, (digit) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(digit)))
}

function normalizeDigits(value) {
  return toEnglishDigits(value).replace(/\D/g, '')
}

function formatPhone(value) {
  if (!value) {
    return '-'
  }

  const digits = normalizeDigits(value)
  return digits.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3')
}

function formatDate(value) {
  if (!value) {
    return '-'
  }

  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(value))
}

function formatDateTime(value) {
  if (!value) {
    return '-'
  }

  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

function formatRole(value) {
  if (!value) {
    return '-'
  }

  const roles = {
    customer: 'مشتری',
    admin: 'مدیر',
    CUSTOMER: 'مشتری',
    ADMIN: 'مدیر',
  }

  return roles[value] || value
}

async function submitPasswordLogin() {
  await user.loginWithPassword()
}

async function submitRegisterOtp() {
  if (user.otpStep === 'phone') {
    await user.requestOtp()
    return
  }

  await user.verifyOtp()
}

async function submitCompleteRegister() {
  await user.completeRegister()
}

function goBackToPhone() {
  user.setOtpField('code', '')
  user.otpStep = 'phone'
  user.clearFeedback()
}

async function refreshProfile() {
  await user.fetchProfile()
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
    linear-gradient(135deg, rgba(91, 61, 245, 0.94), rgba(255, 122, 89, 0.92)), var(--surface);
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
  margin-top: 2rem;
}

.auth-highlights article {
  padding: 1rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.14);
}

.auth-highlights p,
.auth-hint {
  margin: 0.4rem 0 0;
  color: var(--text-muted);
  line-height: 1.8;
}

.auth-panel--accent .auth-highlights p {
  color: rgba(255, 255, 255, 0.78);
}

.auth-panel--form,
.profile-card,
.profile-sidebar {
  background: var(--surface);
}

.auth-tabs {
  display: inline-grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  width: 100%;
  gap: 0.5rem;
  padding: 0.35rem;
  background: var(--bg-muted);
  border-radius: 18px;
}

.auth-tab {
  min-height: 48px;
  border: 0;
  border-radius: 14px;
  background: transparent;
  color: var(--text-muted);
  font-weight: 700;
}

.auth-tab--active {
  background: #fff;
  color: var(--primary);
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
}

.auth-form,
.complete-form {
  display: grid;
  gap: 1rem;
  margin-top: 1.25rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.form-grid :deep(.base-input:first-child),
.form-grid :deep(.base-input:nth-child(4)),
.form-grid :deep(.base-input:nth-child(5)) {
  grid-column: span 1;
}

.auth-feedback {
  margin: 0;
  padding: 0.9rem 1rem;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.05);
}

.auth-feedback--success {
  color: #0f766e;
  background: rgba(15, 118, 110, 0.1);
}

.auth-feedback--error {
  color: var(--danger);
  background: rgba(239, 68, 68, 0.1);
}

.profile-sidebar {
  display: grid;
  gap: 1.5rem;
  align-content: start;
}

.profile-sidebar--pending {
  background: linear-gradient(180deg, rgba(255, 122, 89, 0.12), rgba(255, 255, 255, 0.96));
}

.profile-sidebar__head {
  display: grid;
  gap: 0.5rem;
}

.pill {
  display: inline-flex;
  width: fit-content;
  padding: 0.38rem 0.7rem;
  border-radius: 999px;
  background: rgba(91, 61, 245, 0.12);
  color: var(--primary);
  font-size: 0.86rem;
}

.pill--warning {
  background: rgba(255, 122, 89, 0.14);
  color: #c2410c;
}

.profile-menu {
  display: grid;
  gap: 0.75rem;
  padding: 0;
  margin: 0;
  list-style: none;
}

.profile-menu li {
  padding: 0.9rem 1rem;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.04);
  color: var(--text-muted);
}

.profile-content {
  display: grid;
  gap: 1rem;
}

.section-head {
  margin-bottom: 1.25rem;
}

.section-head--spread {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 1rem;
}

.profile-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.profile-summary article {
  display: grid;
  gap: 0.45rem;
  padding: 1rem;
  border-radius: 18px;
  background: var(--bg-muted);
}

.muted {
  color: var(--text-muted);
  font-size: 0.88rem;
}

@media (max-width: 980px) {
  .auth-layout,
  .profile-layout,
  .profile-summary,
  .form-grid {
    grid-template-columns: 1fr;
  }

  .profile-order {
    flex-direction: column;
    align-items: start;
  }

  .section-head--spread {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
