<template>
  <Teleport to="body">
    <div v-if="ui.miniCart" class="mini-cart-shell">
      <button class="mini-cart-overlay" type="button" @click="ui.closeMiniCart()"></button>

      <aside class="mini-cart">
        <div class="mini-cart__header">
          <div>
            <h2>سبد خرید شما</h2>
            <p>{{ cart.count }} کالا انتخاب شده است</p>
          </div>
          <button type="button" @click="ui.closeMiniCart()">✕</button>
        </div>

        <div v-if="cart.items.length === 0" class="empty-state">
          هنوز محصولی به سبد خرید اضافه نشده است.
        </div>

        <div v-else class="mini-cart__items">
          <article v-for="item in cart.items" :key="item.id" class="mini-cart__item">
            <img :src="item.image" :alt="item.title" class="mini-cart__image" />

            <div class="mini-cart__content">
              <strong>{{ item.title }}</strong>
              <span class="muted">{{ item.badge }}</span>
              <div class="mini-cart__meta">
                <span class="price">{{ formatPrice(item.price) }}</span>
                <div class="mini-cart__qty">
                  <button type="button" @click="cart.increase(item.id)">+</button>
                  <span>{{ item.qty }}</span>
                  <button type="button" @click="cart.decrease(item.id)">−</button>
                </div>
              </div>
            </div>

            <button type="button" class="mini-cart__remove" @click="cart.remove(item.id)">حذف</button>
          </article>
        </div>

        <div class="mini-cart__footer">
          <div class="mini-cart__summary">
            <span>مبلغ قابل پرداخت</span>
            <strong>{{ formatPrice(cart.total) }}</strong>
          </div>

          <router-link to="/cart" class="mini-cart__cta" @click="ui.closeMiniCart()">
            مشاهده سبد و ادامه خرید
          </router-link>
        </div>
      </aside>
    </div>
  </Teleport>
</template>

<script setup>
import { useCartStore } from '@/stores/cartStore'
import { useUIStore } from '@/stores/uiStore'
import { formatPrice } from '@/utils/format'

const cart = useCartStore()
const ui = useUIStore()
</script>

<style scoped>
.mini-cart-shell {
  position: fixed;
  inset: 0;
  z-index: 70;
}

.mini-cart-overlay {
  position: absolute;
  inset: 0;
  border: 0;
  background: rgba(15, 23, 42, 0.38);
  backdrop-filter: blur(4px);
}

.mini-cart {
  position: absolute;
  top: 0;
  right: 0;
  width: min(420px, 100%);
  height: 100%;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.94);
  border-left: 1px solid var(--border);
  box-shadow: var(--shadow);
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 1rem;
}

.mini-cart__header,
.mini-cart__meta,
.mini-cart__summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.mini-cart__header h2,
.mini-cart__header p {
  margin: 0;
}

.mini-cart__header p {
  color: var(--text-muted);
  font-size: 0.88rem;
}

.mini-cart__header button {
  border: 1px solid var(--border);
  background: transparent;
  width: 42px;
  height: 42px;
  border-radius: 14px;
}

.mini-cart__items {
  display: grid;
  gap: 1rem;
  overflow-y: auto;
}

.mini-cart__item {
  display: grid;
  grid-template-columns: 84px 1fr auto;
  gap: 0.9rem;
  align-items: center;
  padding: 0.85rem;
  border-radius: 20px;
  background: var(--bg-muted);
}

.mini-cart__image {
  width: 84px;
  height: 84px;
  object-fit: cover;
  border-radius: 18px;
}

.mini-cart__content {
  display: grid;
  gap: 0.4rem;
}

.mini-cart__qty {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface-strong);
  padding: 0.25rem;
}

.mini-cart__qty button {
  width: 28px;
  height: 28px;
  border: 0;
  border-radius: 50%;
  background: var(--bg-muted);
}

.mini-cart__remove {
  border: 0;
  background: transparent;
  color: var(--danger);
}

.mini-cart__footer {
  display: grid;
  gap: 0.9rem;
}

.mini-cart__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  border-radius: 18px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  font-weight: 700;
}
</style>
