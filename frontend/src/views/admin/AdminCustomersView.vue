<template>
  <section class="page-panel admin-card">
    <div class="section-head">
      <div>
        <h2 class="section-title">مشتریان</h2>
        <p class="section-subtitle">نمایی از مشتریان، شهرها و سگمنت‌های فروشگاهی</p>
      </div>
    </div>

    <div class="customer-grid">
      <article v-for="customer in customersWithStats" :key="customer.id" class="customer-card">
        <div>
          <strong>{{ customer.name }}</strong>
          <p>{{ customer.city }} • {{ customer.segment }}</p>
        </div>
        <ul>
          <li>تلفن: {{ customer.phone }}</li>
          <li>ایمیل: {{ customer.email }}</li>
          <li>تعداد سفارش: {{ formatNumber(customer.ordersCount) }}</li>
          <li>جمع خرید: {{ formatPrice(customer.totalSpent) }}</li>
        </ul>
      </article>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { formatNumber, formatPrice } from '@/utils/format'

const admin = useAdminStore()
const customersWithStats = computed(() =>
  admin.customers.map((customer) => {
    const customerOrders = admin.ordersByCustomer(customer.id)

    return {
      ...customer,
      ordersCount: customerOrders.length,
      totalSpent: customerOrders.reduce((sum, order) => sum + order.total, 0),
    }
  }),
)
</script>

<style scoped>
.admin-card {
  padding: 1.25rem;
}

.customer-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.customer-card {
  display: grid;
  gap: 0.85rem;
  padding: 1rem;
  border-radius: 20px;
  background: var(--bg-muted);
}

.customer-card p,
.customer-card ul {
  margin: 0;
}

.customer-card p,
.customer-card li {
  color: var(--text-muted);
}

.customer-card ul {
  padding: 0 1rem 0 0;
  display: grid;
  gap: 0.45rem;
}

@media (max-width: 900px) {
  .customer-grid {
    grid-template-columns: 1fr;
  }
}
</style>
