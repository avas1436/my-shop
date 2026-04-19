<template>
  <div class="page-shell">
    <section class="page-panel page-hero">
      <span class="pill">درباره ما</span>
      <h1 class="page-title">{{ admin.settings.storeName }} چگونه شکل گرفت؟</h1>
      <p class="page-description">
        این ویترین فروشگاهی با تمرکز روی تجربه کاربری، سرعت، زیبایی و شفافیت در خرید
        طراحی شده تا به‌سادگی قابل توسعه، اتصال به بک‌اند واقعی و مقیاس‌پذیری برای تیم فروش باشد.
      </p>
    </section>

    <section class="about-grid">
      <article class="page-panel about-card">
        <h2 class="section-title">چشم‌انداز</h2>
        <p>
          ما تجربه‌ای می‌سازیم که از کشف محصول تا ثبت سفارش و پیگیری پس از خرید، برای کاربر
          سریع، شفاف و قابل اعتماد باشد.
        </p>
      </article>

      <article class="page-panel about-card">
        <h2 class="section-title">زیرساخت توسعه</h2>
        <p>
          معماری فعلی پروژه بر پایه Vue 3، Vite، Vue Router و Pinia است و برای افزودن API واقعی،
          احراز هویت و گزارش‌گیری آماده شده است.
        </p>
      </article>

      <article class="page-panel about-card">
        <h2 class="section-title">تجربه مشتری</h2>
        <p>
          جست‌وجوی سریع، دسته‌بندی قابل توسعه، سبد خرید، صفحه سفارش، پروفایل و پنل مدیریت
          در این نسخه برای یک دمو فروشگاهی کامل‌تر کنار هم قرار گرفته‌اند.
        </p>
      </article>
    </section>
  </div>
</template>

<script setup>
import { useAdminStore } from '@/stores/adminStore'

const admin = useAdminStore()
</script>

<style scoped>
.about-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.about-card {
  padding: 1.5rem;
}

.about-card p {
  margin: 0.9rem 0 0;
  color: var(--text-muted);
}

@media (max-width: 920px) {
  .about-grid {
    grid-template-columns: 1fr;
  }
}
</style>
