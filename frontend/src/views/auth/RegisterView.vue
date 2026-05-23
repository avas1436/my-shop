<!-- src/views/auth/RegisterView.vue -->
<template>
  <div class="page-shell">
    <section class="profile-layout">
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
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useUserStore } from '@/stores/userStore'
import { computed } from 'vue'

const user = useUserStore()

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

const completeRegisterLabel = computed(() =>
  user.registerCompleting ? 'در حال تکمیل حساب...' : 'ذخیره اطلاعات و ورود',
)

function toEnglishDigits(value) {
  return String(value).replace(/[۰-۹]/g, (digit) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(digit)))
}
function normalizeDigits(value) {
  return toEnglishDigits(value).replace(/\D/g, '')
}
function formatPhone(value) {
  if (!value) return '-'
  const digits = normalizeDigits(value)
  return digits.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3')
}

async function submitCompleteRegister() {
  await user.completeRegister()
}
</script>

<style scoped>
.profile-layout {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 1.25rem;
}
.profile-sidebar,
.profile-card {
  padding: 1.5rem;
  background: var(--surface);
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
.section-head {
  margin-bottom: 1.25rem;
}
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
.auth-hint {
  margin: 0.4rem 0 0;
  color: var(--text-muted);
  line-height: 1.8;
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
@media (max-width: 980px) {
  .profile-layout,
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
