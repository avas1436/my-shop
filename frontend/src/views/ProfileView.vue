<!-- src/views/ProfileView.vue -->
<template>
  <div class="page-shell">
    <!-- نمایش لودینگ تا زمانی که وضعیت لاگین مشخص شود -->
    <div
      v-if="!userStore.isAuthReady"
      class="text-center mt-4 py-3.5 px-4 rounded-2xl bg-slate-900/5"
    >
      در حال بررسی وضعیت کاربری...
    </div>

    <!-- بخش لاگین / ثبت‌نام-->
    <template v-else-if="!userStore.isAuthenticated">
      <router-view />
    </template>

    <!-- بخش پروفایل کاربری (پس از ورود موفق) -->
    <section v-else class="grid grid-cols-1 lg:grid-cols-[1.05fr_1fr] gap-5">
      <aside class="grid content-start gap-6 p-6 bg-surface rounded-xl">
        <div class="grid gap-2">
          <strong>{{ displayName }}</strong>
          <span
            class="inline-flex w-fit py-1.5 px-3 rounded-full bg-primary/12 text-primary text-[0.86rem]"
            >ورود موفق</span
          >
        </div>

        <ul class="grid gap-3 p-0 m-0 list-none">
          <li class="py-3.5 px-4 rounded-2xl bg-slate-900/5 text-text-muted">{{ userPhone }}</li>
          <li class="py-3.5 px-4 rounded-2xl bg-slate-900/5 text-text-muted">{{ userRoleFa }}</li>
        </ul>

        <BaseButton variant="success" block @click="handleAddAddress">
          افزودن آدرس جدید
        </BaseButton>

        <BaseButton
          v-if="!!userStore.first_name"
          variant="warning"
          block
          @click="handleCompleteProfile"
        >
          تکمیل حساب کاربری
        </BaseButton>

        <BaseButton variant="secondary" block @click="handleLogout"> خروج از حساب </BaseButton>
      </aside>

      <div class="grid gap-4">
        <section class="p-6 bg-surface rounded-xl">
          <div
            class="flex flex-col lg:flex-row items-stretch lg:items-start justify-between gap-4 mb-5"
          >
            <div>
              <h1 class="text-2xl font-bold">اطلاعات حساب</h1>
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
            <p class="m-0 py-3.5 px-4 rounded-2xl text-red-500 bg-red-500/10">
              {{ userStore.authError }}
            </p>
          </template>

          <template v-else-if="userStore.authLoading && !userStore.profile">
            <p class="m-0 py-3.5 px-4 rounded-2xl bg-slate-900/5">در حال دریافت اطلاعات حساب...</p>
          </template>

          <template v-else-if="userStore.profile">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <article class="grid gap-2 p-4 rounded-md bg-bg-muted">
                <span class="text-text-muted text-[0.88rem]">نام</span>
                <strong>{{ userStore.profile.first_name || '-' }}</strong>
              </article>
              <article class="grid gap-2 p-4 rounded-md bg-bg-muted">
                <span class="text-text-muted text-[0.88rem]">نام خانوادگی</span>
                <strong>{{ userStore.profile.last_name || '-' }}</strong>
              </article>
              <article class="grid gap-2 p-4 rounded-md bg-bg-muted">
                <span class="text-text-muted text-[0.88rem]">شماره تماس</span>
                <strong>{{ userPhone }}</strong>
              </article>
            </div>
          </template>
        </section>

        <!-- آدرس‌های کاربر (استفاده از ?. برای جلوگیری از کرش صفحه) -->
        <section class="p-6 bg-surface rounded-xl" v-if="userStore.addresses?.length">
          <h2 class="text-xl font-bold mb-5">آدرس‌های من</h2>
          <div class="grid gap-4">
            <article
              v-for="address in userStore.addresses"
              :key="address.id"
              class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-2 lg:gap-0 p-4 bg-bg-muted rounded-xl"
            >
              <div>
                <strong>{{ address.title }}</strong>
                <p class="text-text-muted text-[0.88rem] m-0 mt-1">{{ address.city }}</p>
              </div>
              <span
                class="inline-flex w-fit py-1.5 px-3 rounded-full bg-primary/12 text-primary text-[0.86rem]"
                >{{ address.details }}</span
              >
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
  if (!userStore.profile) {
    await userStore.initializeAuth(true)
  } else {
    await userStore.initializeAuth()
  }
})

async function refreshProfile() {
  // ارسال true برای نادیده گرفتن کش و دریافت مجدد اطلاعات
  await userStore.initializeAuth(true)
}

async function handleLogout() {
  await userStore.logout()
  router.push('/')
}

async function handleCompleteProfile() {
  router.push('/auth/complete')
}
</script>
