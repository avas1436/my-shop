<!-- src/views/auth/AuthIndexView.vue -->
<template>
  <div class="page-shell">
    <section class="w-full max-w-120 mx-auto">
      <div class="p-8 bg-white rounded-md border border-border-light shadow-(--shadow-soft)">
        <div class="text-center">
          <h1 class="m-0 text-[clamp(1.5rem,3vw,2rem)] font-bold">ورود یا ثبت‌نام</h1>
          <p class="mt-2 mb-0 text-text-muted">برای ادامه، لطفا روش ورود خود را انتخاب کنید</p>
        </div>

        <div class="grid gap-4 mt-8">
          <BaseButton variant="primary" block @click="goTo('/auth/login-password')">
            ورود با رمز عبور
          </BaseButton>

          <BaseButton variant="secondary" block @click="goTo('/auth/login-otp')">
            ورود با کد یک‌بار مصرف
          </BaseButton>

          <div class="flex items-center gap-4 my-1">
            <span class="flex-1 h-px bg-border-light" />
            <span class="text-text-muted text-sm">یا</span>
            <span class="flex-1 h-px bg-border-light" />
          </div>

          <BaseButton variant="ghost" block @click="goTo('/auth/register')">
            ثبت‌نام کاربر جدید
          </BaseButton>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const goTo = (path) => router.push(path)
</script>
