<!-- src/views/auth/AuthLayout.vue -->
<template>
  <div class="page-shell">
    <section class="auth-layout">
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
          <router-link to="/auth/login-password" class="auth-tab" active-class="auth-tab--active">
            ورود با رمز
          </router-link>
          <router-link to="/auth/login-otp" class="auth-tab" active-class="auth-tab--active">
            ثبت نام
          </router-link>
        </div>

        <!-- فرم‌های Password و OTP اینجا رندر می‌شوند -->
        <router-view />
      </section>
    </section>
  </div>
</template>

<style scoped>
.auth-layout {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 1.25rem;
}
.auth-panel {
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
.auth-highlights p {
  margin: 0.4rem 0 0;
  color: rgba(255, 255, 255, 0.78);
  line-height: 1.8;
}
.auth-panel--form {
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
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
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
@media (max-width: 980px) {
  .auth-layout {
    grid-template-columns: 1fr;
  }
}
</style>
