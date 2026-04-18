<template>
  <section class="promo-banner">
    <div>
      <span class="pill">تخفیف هفتگی</span>
      <h2>تا ۲۵٪ تخفیف روی کالاهای منتخب دیجیتال و خانه</h2>
      <p>
        مجموعه‌ای از محصولات پرفروش با موجودی محدود و ارسال سریع؛ زمان خوبی برای
        نهایی کردن خرید است.
      </p>
    </div>

    <div class="promo-banner__actions">
      <router-link to="/category/digital" class="promo-banner__primary">خرید دیجیتال</router-link>
      <router-link to="/category/home" class="promo-banner__secondary">محصولات خانه</router-link>
    </div>
  </section>
</template>

<style scoped>
.promo-banner {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1rem;
  align-items: center;
  padding: 1.6rem 1.8rem;
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.22), transparent 24%),
    linear-gradient(135deg, rgba(23, 32, 51, 1), rgba(91, 61, 245, 0.96));
  color: #fff;
}

.promo-banner h2,
.promo-banner p {
  margin: 0;
}

.promo-banner h2 {
  margin-top: 0.85rem;
  font-size: clamp(1.5rem, 3vw, 2.2rem);
}

.promo-banner p {
  margin-top: 0.75rem;
  max-width: 52ch;
  color: rgba(255, 255, 255, 0.8);
}

.promo-banner__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
}

.promo-banner__primary,
.promo-banner__secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 1.15rem;
  border-radius: 999px;
  font-weight: 700;
}

.promo-banner__primary {
  background: #fff;
  color: var(--primary);
}

.promo-banner__secondary {
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: #fff;
}

@media (max-width: 768px) {
  .promo-banner {
    grid-template-columns: 1fr;
    padding: 1.25rem;
  }
}
</style>
