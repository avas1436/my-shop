<template>
  <div class="page-shell">
    <section class="page-panel not-found-card">
      <span class="pill">۴۰۴</span>
      <h1 class="page-title">صفحه موردنظر پیدا نشد</h1>
      <p class="page-description">
        ممکن است مسیر تغییر کرده باشد یا صفحه حذف شده باشد. از لینک‌های زیر دوباره مسیر خود را انتخاب کنید.
      </p>
      <div class="not-found-actions">
        <router-link to="/" class="not-found-link not-found-link--primary">بازگشت به خانه</router-link>
        <router-link to="/products" class="not-found-link">مشاهده محصولات</router-link>
      </div>
    </section>
  </div>
</template>

<style scoped>
.not-found-card {
  padding: 2rem;
  text-align: center;
}

.not-found-actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.85rem;
  margin-top: 1.5rem;
}

.not-found-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 1.2rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--surface-strong);
  font-weight: 700;
}

.not-found-link--primary {
  border: 0;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
}
</style>
