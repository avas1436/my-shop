<template>
  <div class="page-shell">
    <!-- از یک گرید تک‌ستونه و وسط‌چین برای فرم‌های لاگین استفاده می‌کنیم -->
    <section class="auth-layout auth-index-layout">
      <div class="page-panel profile-card">
        <div class="section-head text-center">
          <h1 class="section-title">ورود یا ثبت‌نام</h1>
          <p class="section-subtitle mt-2">برای ادامه، لطفا روش ورود خود را انتخاب کنید</p>
        </div>

        <div class="auth-options">
          <BaseButton variant="primary" block @click="goTo('/auth/login-password')">
            ورود با رمز عبور
          </BaseButton>

          <BaseButton variant="secondary" block @click="goTo('/auth/login-otp')">
            ورود با کد یک‌بار مصرف
          </BaseButton>

          <div class="divider">
            <span class="muted text-sm">یا</span>
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
import BaseButton from '@/components/base/BaseButton.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
/* بازنویسی طرح دو ستونه به تک‌ستونه وسط‌چین برای منوی لاگین */
.auth-index-layout {
  grid-template-columns: 1fr;
  max-width: 480px;
  margin: 0 auto;
}

.profile-card {
  padding: 2rem 1.5rem;
  background: var(--surface, #ffffff);
  border-radius: 12px;
}

.text-center {
  text-align: center;
}

.mt-2 {
  margin-top: 0.5rem;
}

.text-sm {
  font-size: 0.85rem;
}

.auth-options {
  display: grid;
  gap: 1rem;
  margin-top: 2rem;
}

/* خط جداکننده بین دکمه‌های ورود و ثبت‌نام */
.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 0.5rem 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid rgba(15, 23, 42, 0.1);
}

.divider span {
  padding: 0 1rem;
}

.muted {
  color: var(--text-muted, #64748b);
}
</style>
