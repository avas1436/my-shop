<!-- src/views/ProfileView.vue -->
<template>
  <div class="page-shell">
    <!-- نمایش لودینگ تا زمانی که وضعیت لاگین مشخص شود -->
    <div v-if="!userStore.isAuthReady" class="auth-feedback text-center mt-4">
      در حال بررسی وضعیت کاربری...
    </div>

    <!-- بخش لاگین / ثبت‌نام-->
    <template v-else-if="!userStore.isAuthenticated">
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
          <li>{{ userPhone }}</li>
          <li>{{ userRoleFa }}</li>
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
              :disabled="userStore.authLoading"
              @click="refreshProfile"
            >
              بروزرسانی
            </BaseButton>
          </div>

          <!-- اصلاح زنجیره v-if و v-else-if -->
          <template v-if="userStore.authError">
            <p class="auth-feedback auth-feedback--error">
              {{ userStore.authError }}
            </p>
          </template>

          <template v-else-if="userStore.authLoading && !userStore.profile">
            <p class="auth-feedback">در حال دریافت اطلاعات حساب...</p>
          </template>

          <template v-else-if="userStore.profile">
            <div class="profile-summary profile-summary--details">
              <article>
                <span class="muted">نام</span>
                <strong>{{ userStore.profile.first_name || '-' }}</strong>
              </article>
              <article>
                <span class="muted">نام خانوادگی</span>
                <strong>{{ userStore.profile.last_name || '-' }}</strong>
              </article>
              <article>
                <span class="muted">شماره تماس</span>
                <strong>{{ userPhone }}</strong>
              </article>
              <article>
                <span class="muted">سن</span>
                <strong>{{ userStore.profile.age }}</strong>
              </article>
            </div>
          </template>
        </section>

        <!-- آدرس‌های کاربر (استفاده از ?. برای جلوگیری از کرش صفحه) -->
        <section class="page-panel profile-card" v-if="userStore.addresses?.length">
          <h2 class="section-title">آدرس‌های من</h2>
          <div class="profile-orders">
            <article v-for="address in userStore.addresses" :key="address.id" class="profile-order">
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
import { formatPhone } from '@/utils/format'
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const displayName = computed(() => {
  const profile = userStore.profile
  if (!profile) return 'کاربر مهمان'
  return `${profile.first_name || ''} ${profile.last_name || ''}`.trim() || 'کاربر بدون نام'
})

const userPhone = computed(() => formatPhone(userStore.profile?.phone_number))

const userRoleFa = computed(() => {
  return userStore.profile?.role === 'admin' ? 'مدیر' : 'مشتری'
})

onMounted(async () => {
  // فراخوانی ایمن، استور خودش تشخیص می‌دهد که درخواست بفرستد یا نه
  await userStore.initializeAuth()
})

async function refreshProfile() {
  // ارسال true برای نادیده گرفتن کش و دریافت مجدد اطلاعات
  await userStore.initializeAuth(true)
}

async function handleLogout() {
  await userStore.logout()
  router.push('/')
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
