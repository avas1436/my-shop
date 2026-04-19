<template>
  <div class="admin-grid">
    <section class="admin-kpis">
      <article class="admin-kpi page-panel">
        <span class="muted">درآمد کل</span>
        <strong>{{ formatPrice(admin.totalRevenue) }}</strong>
      </article>
      <article class="admin-kpi page-panel">
        <span class="muted">سفارش‌های جاری</span>
        <strong>{{ formatNumber(admin.pendingOrders.length) }}</strong>
      </article>
      <article class="admin-kpi page-panel">
        <span class="muted">محصولات فعال</span>
        <strong>{{ formatNumber(activeProducts.length) }}</strong>
      </article>
      <article class="admin-kpi page-panel">
        <span class="muted">موجودی کل</span>
        <strong>{{ formatNumber(products.totalInventory) }}</strong>
      </article>
    </section>

    <section class="admin-panels">
      <article class="page-panel admin-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">سفارش‌های اخیر</h2>
            <p class="section-subtitle">آخرین وضعیت ثبت و پردازش سفارش‌ها</p>
          </div>
        </div>
        <div class="admin-list">
          <article v-for="order in recentOrders" :key="order.id" class="admin-list__item">
            <div>
              <strong>{{ order.id }}</strong>
              <p>{{ order.customerName }} • {{ order.date }}</p>
            </div>
            <span class="pill">{{ order.status }}</span>
            <strong>{{ formatPrice(order.total) }}</strong>
          </article>
        </div>
      </article>

      <article class="page-panel admin-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">کمبود موجودی</h2>
            <p class="section-subtitle">محصولاتی که نیازمند رسیدگی سریع هستند</p>
          </div>
        </div>
        <div class="admin-list">
          <article v-for="product in products.lowStockProducts" :key="product.id" class="admin-list__item">
            <div>
              <strong>{{ product.title }}</strong>
              <p>{{ product.sku }}</p>
            </div>
            <span class="pill">{{ product.stock }} عدد</span>
            <strong>{{ formatPrice(product.price) }}</strong>
          </article>
        </div>
      </article>
    </section>

    <section class="admin-panels admin-panels--split">
      <article class="page-panel admin-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">کمپین‌های فعال</h2>
            <p class="section-subtitle">کمپین‌هایی که اکنون روی فروشگاه اثر می‌گذارند</p>
          </div>
        </div>
        <div class="admin-list">
          <article v-for="campaign in admin.activeCampaigns" :key="campaign.id" class="admin-list__item">
            <div>
              <strong>{{ campaign.title }}</strong>
              <p>{{ campaign.channel }}</p>
            </div>
            <strong>{{ campaign.budget }}</strong>
          </article>
        </div>
      </article>

      <article class="page-panel admin-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">مشتریان شاخص</h2>
            <p class="section-subtitle">مشتریانی با ارزش خرید و تعامل بالاتر</p>
          </div>
        </div>
        <div class="admin-list">
          <article v-for="customer in admin.customers.slice(0, 4)" :key="customer.id" class="admin-list__item">
            <div>
              <strong>{{ customer.name }}</strong>
              <p>{{ customer.city }} • {{ customer.segment }}</p>
            </div>
            <strong>{{ customer.phone }}</strong>
          </article>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useProductsStore } from '@/stores/products'
import { formatNumber, formatPrice } from '@/utils/format'

const admin = useAdminStore()
const products = useProductsStore()
const recentOrders = computed(() => admin.orders.slice(0, 5))
const activeProducts = computed(() => products.products.filter((product) => product.status === 'active'))
</script>

<style scoped>
.admin-grid {
  display: grid;
  gap: 1rem;
}

.admin-kpis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.admin-kpi,
.admin-card {
  padding: 1.25rem;
}

.admin-kpi {
  display: grid;
  gap: 0.45rem;
}

.admin-kpi strong {
  font-size: clamp(1.3rem, 2vw, 1.8rem);
}

.admin-panels {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.admin-panels--split {
  grid-template-columns: 1.1fr 0.9fr;
}

.admin-list {
  display: grid;
  gap: 0.85rem;
}

.admin-list__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  border-radius: 20px;
  background: var(--bg-muted);
}

.admin-list__item p {
  margin: 0.35rem 0 0;
  color: var(--text-muted);
}

@media (max-width: 1080px) {
  .admin-kpis,
  .admin-panels,
  .admin-panels--split {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .admin-kpis,
  .admin-panels,
  .admin-panels--split {
    grid-template-columns: 1fr;
  }

  .admin-list__item {
    flex-direction: column;
    align-items: start;
  }
}
</style>
