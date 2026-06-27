<!-- src/views/ProfileView.vue -->
<template>
  <div class="page-shell">
    <!-- لودینگ وضعیت احراز هویت -->
    <div
      v-if="!userStore.isAuthReady"
      class="text-center py-3.5 px-4 rounded-2xl bg-slate-900/5 text-text-muted"
    >
      در حال بررسی وضعیت کاربری...
    </div>

    <!-- کاربر لاگین نکرده -->
    <template v-else-if="!userStore.isAuthenticated">
      <router-view />
    </template>

    <!-- پروفایل کاربر لاگین‌شده -->
    <section v-else class="grid grid-cols-1 lg:grid-cols-[1.05fr_1fr] gap-5">
      <!-- ستون چپ: اطلاعات خلاصه + دکمه‌ها -->
      <aside
        class="grid content-start gap-6 p-6 bg-surface rounded-xl border border-border-light shadow-(--shadow-soft)"
      >
        <div class="grid gap-2">
          <strong class="text-[1.1rem]">{{ displayName }}</strong>
          <span
            class="inline-flex w-fit py-1.5 px-3 rounded-full bg-primary/10 text-primary text-[0.86rem]"
          >
            ورود موفق
          </span>
        </div>

        <ul class="grid gap-3 p-0 m-0 list-none">
          <li class="py-3.5 px-4 rounded-2xl bg-slate-900/5 text-text-muted">{{ userPhone }}</li>
          <li class="py-3.5 px-4 rounded-2xl bg-slate-900/5 text-text-muted">{{ userRoleFa }}</li>
        </ul>

        <div class="grid gap-3">
          <BaseButton variant="success" block @click="handleAddAddress">
            افزودن آدرس جدید
          </BaseButton>

          <BaseButton
            v-if="!userStore.profile?.first_name"
            variant="warning"
            block
            @click="handleCompleteProfile"
          >
            تکمیل حساب کاربری
          </BaseButton>

          <BaseButton variant="secondary" block @click="handleLogout"> خروج از حساب </BaseButton>
        </div>
      </aside>

      <!-- ستون راست: جزئیات + آدرس‌ها -->
      <div class="grid gap-4 content-start">
        <section
          class="p-6 bg-surface rounded-xl border border-border-light shadow-(--shadow-soft)"
        >
          <div
            class="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4 mb-5"
          >
            <h1 class="m-0 text-2xl font-bold">اطلاعات حساب</h1>
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

          <p
            v-if="userStore.authError"
            class="m-0 py-3.5 px-4 rounded-2xl text-danger bg-danger/10"
          >
            {{ userStore.authError }}
          </p>

          <p
            v-else-if="userStore.authLoading && !userStore.profile"
            class="m-0 py-3.5 px-4 rounded-2xl bg-slate-900/5 text-text-muted"
          >
            در حال دریافت اطلاعات حساب...
          </p>

          <div v-else-if="userStore.profile" class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <article class="grid gap-2 p-4 rounded-md bg-bg-muted">
              <span class="text-text-muted text-[0.88rem]">نام</span>
              <strong>{{ userStore.profile.first_name || '—' }}</strong>
            </article>
            <article class="grid gap-2 p-4 rounded-md bg-bg-muted">
              <span class="text-text-muted text-[0.88rem]">نام خانوادگی</span>
              <strong>{{ userStore.profile.last_name || '—' }}</strong>
            </article>
            <article class="grid gap-2 p-4 rounded-md bg-bg-muted">
              <span class="text-text-muted text-[0.88rem]">شماره تماس</span>
              <strong>{{ userPhone }}</strong>
            </article>
            <article class="grid gap-2 p-4 rounded-md bg-bg-muted">
              <span class="text-text-muted text-[0.88rem]">نقش</span>
              <strong>{{ userRoleFa }}</strong>
            </article>
          </div>
        </section>

        <!-- آدرس‌های کاربر -->
        <section
          v-if="userStore.addresses?.length"
          class="p-6 bg-surface rounded-xl border border-border-light shadow-(--shadow-soft)"
        >
          <h2 class="m-0 text-xl font-bold mb-5">آدرس‌های من</h2>
          <div class="grid gap-4">
            <article
              v-for="address in userStore.addresses"
              :key="address.id"
              class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-3 p-4 bg-bg-muted rounded-xl"
            >
              <div>
                <strong>{{ address.title }}</strong>
                <p class="text-text-muted text-[0.88rem] m-0 mt-1">{{ address.city }}</p>
              </div>
              <span
                class="inline-flex w-fit py-1.5 px-3 rounded-full bg-primary/10 text-primary text-[0.86rem]"
              >
                {{ address.details }}
              </span>
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

const userRoleFa = computed(() => (userStore.profile?.role === 'admin' ? 'مدیر' : 'مشتری'))

onMounted(async () => {
  await userStore.initializeAuth(!userStore.profile)
})

async function refreshProfile() {
  await userStore.initializeAuth(true)
}

async function handleLogout() {
  await userStore.logout()
  router.push('/')
}

function handleCompleteProfile() {
  router.push('/auth/complete')
}

function handleAddAddress() {
  // TODO: باز کردن مودال یا هدایت به صفحه افزودن آدرس
}
</script>
