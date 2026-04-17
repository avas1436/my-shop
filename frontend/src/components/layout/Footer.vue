<template>
  <footer class="site-footer">
    <div class="container footer-grid">
      <section>
        <h3>ShopVerse</h3>
        <p>
          تجربه‌ی یک فروشگاه آنلاین زیبا، سریع و مطمئن با تمرکز روی کالاهای باکیفیت و
          ارسال سریع.
        </p>
      </section>

      <section>
        <h4>دسترسی سریع</h4>
        <nav class="footer-links">
          <router-link to="/">خانه</router-link>
          <router-link to="/products">فروشگاه</router-link>
          <router-link to="/cart">سبد خرید</router-link>
          <router-link to="/profile">حساب کاربری</router-link>
        </nav>
      </section>

      <section>
        <h4>اعتماد و پشتیبانی</h4>
        <ul class="footer-points">
          <li>هفت روز ضمانت بازگشت</li>
          <li>پشتیبانی تلفنی و آنلاین</li>
          <li>پرداخت امن و سریع</li>
        </ul>
      </section>
    </div>

    <div class="container footer-bottom">
      <span>© ۱۴۰۵ ShopVerse — تمامی حقوق محفوظ است.</span>
      <span>طراحی شده برای یک تجربه‌ی خرید لوکس و ساده</span>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  margin-top: 3rem;
  padding: 2.5rem 0 2rem;
  background: #101828;
  color: rgba(255, 255, 255, 0.88);
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr;
  gap: 1.5rem;
}

.site-footer h3,
.site-footer h4 {
  margin: 0 0 0.9rem;
  color: #fff;
}

.site-footer p {
  margin: 0;
  max-width: 42ch;
  color: rgba(255, 255, 255, 0.72);
}

.footer-links,
.footer-points {
  display: grid;
  gap: 0.75rem;
}

.footer-links a,
.footer-points li {
  color: rgba(255, 255, 255, 0.72);
}

.footer-points {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 0.88rem;
  color: rgba(255, 255, 255, 0.62);
}

@media (max-width: 768px) {
  .footer-grid,
  .footer-bottom {
    grid-template-columns: 1fr;
    display: grid;
  }
}
</style>
