<template>
  <section class="page-panel admin-card">
    <div class="section-head">
      <div>
        <h2 class="section-title">مدیریت سفارش‌ها</h2>
        <p class="section-subtitle">وضعیت سفارش‌ها را برای تیم اجرا و مشتری به‌روز نگه دارید</p>
      </div>
    </div>

    <div class="orders-table">
      <article v-for="order in admin.orders" :key="order.id" class="order-row">
        <div>
          <strong>{{ order.id }}</strong>
          <p>{{ order.customerName }} • {{ order.city }}</p>
        </div>
        <span>{{ formatPrice(order.total) }}</span>
        <span>{{ order.date }}</span>
        <label class="order-status">
          <span>وضعیت</span>
          <select :value="order.status" @change="admin.updateOrderStatus(order.id, $event.target.value)">
            <option v-for="status in statuses" :key="status" :value="status">{{ status }}</option>
          </select>
        </label>
      </article>
    </div>
  </section>
</template>

<script setup>
import { useAdminStore } from '@/stores/adminStore'
import { formatPrice } from '@/utils/format'

const admin = useAdminStore()
const statuses = ['ثبت شده', 'در حال آماده‌سازی', 'ارسال شده', 'تحویل شده', 'لغو شده']
</script>

<style scoped>
.admin-card {
  padding: 1.25rem;
}

.orders-table {
  display: grid;
  gap: 0.8rem;
}

.order-row {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr 0.7fr 220px;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  border-radius: 20px;
  background: var(--bg-muted);
}

.order-row p {
  margin: 0.35rem 0 0;
  color: var(--text-muted);
}

.order-status {
  display: grid;
  gap: 0.35rem;
}

.order-status select {
  min-height: 46px;
  border-radius: 14px;
  border: 1px solid var(--border);
  padding: 0 0.9rem;
  background: var(--surface-strong);
}

@media (max-width: 900px) {
  .order-row {
    grid-template-columns: 1fr;
  }
}
</style>
