<template>
  <div class="page-shell">
    <section class="page-panel page-hero">
      <span class="pill">سبد خرید</span>
      <h1 class="page-title">مرور سفارش شما</h1>
      <p class="page-description">
        کالاهای انتخاب‌شده را بررسی کنید، تعداد را تغییر دهید و با خیال راحت به مرحله
        نهایی خرید بروید.
      </p>
    </section>

    <section v-if="cart.items.length" class="cart-layout">
      <div class="page-panel cart-items">
        <article v-for="item in cart.items" :key="item.id" class="cart-item">
          <img :src="item.image" :alt="item.title" class="cart-item__image" />

          <div class="cart-item__content">
            <strong>{{ item.title }}</strong>
            <span class="muted">{{ item.badge }}</span>
            <div class="cart-item__controls">
              <div class="cart-item__qty">
                <button type="button" @click="cart.increase(item.id)">+</button>
                <span>{{ item.qty }}</span>
                <button type="button" @click="cart.decrease(item.id)">−</button>
              </div>
              <strong class="price">{{ formatPrice(item.price * item.qty) }}</strong>
            </div>
          </div>

          <button type="button" class="cart-item__remove" @click="cart.remove(item.id)">حذف</button>
        </article>
      </div>

      <aside class="page-panel cart-summary">
        <h2>خلاصه پرداخت</h2>
        <div class="cart-summary__row">
          <span>جمع سبد خرید</span>
          <strong>{{ formatPrice(cart.subtotal) }}</strong>
        </div>
        <div class="cart-summary__row">
          <span>هزینه ارسال</span>
          <strong>{{ cart.shipping ? formatPrice(cart.shipping) : 'رایگان' }}</strong>
        </div>
        <div class="cart-summary__row">
          <span>سود شما از تخفیف</span>
          <strong>{{ formatPrice(cart.discount) }}</strong>
        </div>
        <div class="cart-summary__row cart-summary__row--total">
          <span>مبلغ نهایی</span>
          <strong>{{ formatPrice(cart.total) }}</strong>
        </div>

        <router-link to="/checkout" class="cart-summary__cta">ادامه فرایند خرید</router-link>
      </aside>
    </section>

    <section v-else class="empty-state">
      سبد خرید شما خالی است؛ از صفحه محصولات خریدتان را شروع کنید.
    </section>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cartStore'
import { formatPrice } from '@/utils/format'

const cart = useCartStore()
</script>

<style scoped>
.cart-layout {
  display: grid;
  grid-template-columns: 1.4fr 0.8fr;
  gap: 1.25rem;
}

.cart-items {
  padding: 1.25rem;
  display: grid;
  gap: 1rem;
}

.cart-item {
  display: grid;
  grid-template-columns: 120px 1fr auto;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  border-radius: 22px;
  background: var(--bg-muted);
}

.cart-item__image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 22px;
}

.cart-item__content {
  display: grid;
  gap: 0.55rem;
}

.cart-item__controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.cart-item__qty {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.25rem;
  border-radius: 999px;
  background: var(--surface-strong);
  border: 1px solid var(--border);
}

.cart-item__qty button {
  width: 30px;
  height: 30px;
  border: 0;
  border-radius: 50%;
  background: var(--bg-muted);
}

.cart-item__remove {
  border: 0;
  background: transparent;
  color: var(--danger);
}

.cart-summary {
  padding: 1.25rem;
  display: grid;
  gap: 1rem;
  align-content: start;
  position: sticky;
  top: 132px;
  height: fit-content;
}

.cart-summary h2 {
  margin: 0;
}

.cart-summary__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  color: var(--text-muted);
}

.cart-summary__row--total {
  color: var(--text);
  font-size: 1.05rem;
  padding-top: 0.8rem;
  border-top: 1px solid var(--border);
}

.cart-summary__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  border-radius: 18px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  font-weight: 700;
}

@media (max-width: 920px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }

  .cart-summary {
    position: static;
  }
}

@media (max-width: 640px) {
  .cart-item {
    grid-template-columns: 1fr;
  }
}
</style>
