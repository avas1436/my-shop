<!-- src/views/ProfileView.vue -->
<template>
  <div class="page-shell">
    <!-- نمایش لودینگ تا زمانی که وضعیت لاگین مشخص شود -->
    <div v-if="!user.isAuthReady" class="auth-feedback text-center mt-4">
      در حال بررسی وضعیت کاربری...
    </div>

    <!-- بخش لاگین / ثبت‌نام-->
    <template v-else-if="!user.isAuthenticated">
      <router-view />
    </template>

    <!-- بخش پروفایل کاربری (پس از ورود موفق) -->
    <section v-else class="profile-layout">
      <aside class="page-panel profile-sidebar">
        <div class="profile-sidebar__head">
          <strong>{{ displayName }}</strong>
          <span class="pill">ورود موفق</span>
        </div>

        <ul class="profile-menu">
          <li>{{ formatPhone(userPhone) }}</li>
          <li>سطح دسترسی: {{ userRoleFa }}</li>
        </ul>

        <BaseButton variant="secondary" block @click="handleLogout">خروج از حساب</BaseButton>
      </aside>

      <div class="profile-content">
        <section class="page-panel profile-card">
          <div class="section-head section-head--spread">
            <div>
              <h1 class="section-title">اطلاعات حساب</h1>
              <p class="section-subtitle">اطلاعات دریافتی شما از سرور</p>
            </div>
            <BaseButton
              type="button"
              variant="ghost"
              size="md"
              :disabled="user.authLoading"
              @click="refreshProfile"
            >
              بروزرسانی
            </BaseButton>
          </div>

          <!-- اصلاح زنجیره v-if و v-else-if -->
          <template v-if="user.authError">
            <p class="auth-feedback auth-feedback--error">
              {{ user.authError }}
            </p>
          </template>

          <template v-else-if="user.authLoading && !user.profile">
            <p class="auth-feedback">در حال دریافت اطلاعات حساب...</p>
          </template>

          <template v-else-if="user.profile">
            <div class="profile-summary profile-summary--details">
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
            </div>
          </template>
        </section>

        <!-- آدرس‌های کاربر (استفاده از ?. برای جلوگیری از کرش صفحه) -->
        <section class="page-panel profile-card" v-if="user.addresses?.length">
          <h2 class="section-title">آدرس‌های من</h2>
          <div class="profile-orders">
            <article v-for="address in user.addresses" :key="address.id" class="profile-order">
              <div>
                <strong>{{ address.title }}</strong>
                <p class="muted">{{ address.city }}</p>
              </div>
              <span class="pill">{{ address.details }}</span>
            </article>
          </div>
        </section>
      </div>
    </section>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { useUserStore } from '@/stores/userStore'
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const user = useUserStore()
const router = useRouter()

const displayName = computed(() => {
  if (!user.profile) return 'کاربر مهمان'
  return (
    `${user.profile.first_name || ''} ${user.profile.last_name || ''}`.trim() || 'کاربر بدون نام'
  )
})

const userPhone = computed(() => user.profile?.phone_number || '')

const userRoleFa = computed(() => {
  if (user.userRole === 'admin') return 'مدیر'
  return 'مشتری'
})

onMounted(async () => {
  if (!user.isAuthReady) {
    await user.initializeAuth()
  }
})

async function refreshProfile() {
  await user.initializeAuth()
}

async function handleLogout() {
  await user.logout()
  // در صورت نبود ROUTES.HOME مستقیم به مسیر اصلی هدایت کنید:
  router.push('/')
}

function normalizeDigits(value) {
  if (!value) return ''
  return String(value)
    .replace(/[۰-۹]/g, (d) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(d)))
    .replace(/\D/g, '')
}

function formatPhone(value) {
  if (!value) return '-'
  const digits = normalizeDigits(value)
  return digits.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3')
}

function formatDate(value) {
  if (!value) return '-'
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(value))
}
</script>

<style scoped>
.auth-layout,
.profile-layout {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 1.25rem;
}

.profile-sidebar,
.profile-card {
  padding: 1.5rem;
  background: var(--surface, #ffffff);
  border-radius: 12px;
}

.profile-sidebar {
  display: grid;
  gap: 1.5rem;
  align-content: start;
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
  color: var(--primary, #5b3df5);
  font-size: 0.86rem;
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
  color: var(--text-muted, #64748b);
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
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.profile-summary article {
  display: grid;
  gap: 0.45rem;
  padding: 1rem;
  border-radius: 18px;
  background: var(--bg-muted, #f8fafc);
}

.muted {
  color: var(--text-muted, #64748b);
  font-size: 0.88rem;
}

.auth-feedback {
  margin: 0;
  padding: 0.9rem 1rem;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.05);
}
.auth-feedback--error {
  color: var(--danger, #ef4444);
  background: rgba(239, 68, 68, 0.1);
}

.profile-orders {
  display: grid;
  gap: 1rem;
}
.profile-order {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--bg-muted, #f8fafc);
  border-radius: 12px;
}

@media (max-width: 980px) {
  .profile-layout,
  .profile-summary {
    grid-template-columns: 1fr;
  }
  .section-head--spread {
    flex-direction: column;
    align-items: stretch;
  }
  .profile-order {
    flex-direction: column;
    align-items: start;
    gap: 0.5rem;
  }
}
</style>
