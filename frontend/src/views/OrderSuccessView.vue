<template>
  <div class="page-shell">
    <section class="page-panel success-card" v-if="order">
      <span class="pill">سفارش با موفقیت ثبت شد</span>
      <h1 class="page-title">کد سفارش {{ order.id }}</h1>
      <p class="page-description">
        سفارش شما ثبت شد و اکنون در وضعیت «{{ order.status }}» قرار دارد. جزئیات آن در حساب کاربری و پنل ادمین قابل مشاهده است.
      </p>

      <div class="success-summary">
        <article>
          <span class="muted">تاریخ ثبت</span>
          <strong>{{ order.date }}</strong>
        </article>
        <article>
          <span class="muted">روش ارسال</span>
          <strong>{{ shippingLabel }}</strong>
        </article>
        <article>
          <span class="muted">مبلغ نهایی</span>
          <strong>{{ formatPrice(order.total) }}</strong>
        </article>
      </div>

      <div class="success-actions">
        <router-link to="/profile" class="success-link success-link--primary">مشاهده حساب کاربری</router-link>
        <router-link to="/products" class="success-link">ادامه خرید</router-link>
      </div>
    </section>

    <section v-else class="empty-state">سفارش موردنظر پیدا نشد.</section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAdminStore } from '@/stores/adminStore'
import { formatPrice } from '@/utils/format'

const route = useRoute()
const admin = useAdminStore()
const order = computed(() => admin.getOrderById(route.params.id))
const shippingLabel = computed(() => (order.value?.shippingMethod === 'express' ? 'ارسال اکسپرس' : 'پست پیشتاز'))
</script>

<style scoped>
.success-card {
  padding: 2rem;
}

.success-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.success-summary article {
  display: grid;
  gap: 0.35rem;
  padding: 1rem;
  border-radius: 20px;
  background: var(--bg-muted);
}

.success-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  margin-top: 1.5rem;
}

.success-link {
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

.success-link--primary {
  border: 0;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
}

@media (max-width: 920px) {
  .success-summary {
    grid-template-columns: 1fr;
  }
}
</style>
