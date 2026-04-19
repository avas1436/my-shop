<template>
  <div class="page-shell">
    <section class="page-panel page-hero">
      <span class="pill">پشتیبانی و خدمات</span>
      <h1 class="page-title">همیشه یک مسیر سریع برای پاسخ‌گویی دارید</h1>
      <p class="page-description">
        برای پیگیری سفارش، راهنمای خرید، بازگشت کالا یا ارتباط با تیم فروش، از کانال‌های زیر استفاده کنید.
      </p>
    </section>

    <section class="support-grid">
      <article class="page-panel support-card">
        <h2 class="section-title">راه‌های ارتباطی</h2>
        <ul>
          <li>تلفن پشتیبانی: {{ admin.settings.supportPhone }}</li>
          <li>ایمیل: {{ admin.settings.supportEmail }}</li>
          <li>زمان پاسخ‌گویی: {{ admin.settings.fulfillmentWindow }}</li>
        </ul>
      </article>

      <article class="page-panel support-card">
        <h2 class="section-title">سوالات پرتکرار</h2>
        <ul>
          <li>پیگیری سفارش از بخش حساب کاربری و پنل ادمین قابل مشاهده است.</li>
          <li>برای سفارش‌های بالای ۳۰ میلیون تومان، ارسال اکسپرس رایگان است.</li>
          <li>در صورت ثبت اشتباه، سفارش از پنل ادمین یا پشتیبانی قابل ویرایش است.</li>
        </ul>
      </article>
    </section>
  </div>
</template>

<script setup>
import { useAdminStore } from '@/stores/adminStore'

const admin = useAdminStore()
</script>

<style scoped>
.support-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.support-card {
  padding: 1.5rem;
}

.support-card ul {
  margin: 1rem 0 0;
  padding: 0 1.1rem 0 0;
  display: grid;
  gap: 0.75rem;
  color: var(--text-muted);
}

@media (max-width: 920px) {
  .support-grid {
    grid-template-columns: 1fr;
  }
}
</style>
