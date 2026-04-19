<template>
  <div class="page-shell">
    <section class="profile-layout">
      <aside class="page-panel profile-sidebar">
        <div class="profile-sidebar__head">
          <strong>{{ user.profile.name }}</strong>
          <span class="pill">عضویت {{ user.profile.membership }}</span>
        </div>

        <ul class="profile-menu">
          <li>اطلاعات حساب</li>
          <li>سفارش‌ها</li>
          <li>آدرس‌ها</li>
          <li>کیف پول</li>
        </ul>
      </aside>

      <div class="profile-content">
        <section class="page-panel profile-card">
          <div class="section-head">
            <div>
              <h1 class="section-title">حساب کاربری</h1>
              <p class="section-subtitle">نمای کلی اطلاعات، سفارش‌ها و اعتبار شما</p>
            </div>
          </div>

          <div class="profile-summary">
            <article>
              <span class="muted">شماره تماس</span>
              <strong>{{ user.profile.phone }}</strong>
            </article>
            <article>
              <span class="muted">اعتبار کیف پول</span>
              <strong>{{ formatPrice(user.profile.wallet) }}</strong>
            </article>
            <article>
              <span class="muted">امتیاز باشگاه مشتریان</span>
              <strong>{{ formatNumber(user.profile.loyaltyPoints) }}</strong>
            </article>
          </div>
        </section>

        <section class="page-panel profile-card">
          <h2 class="section-title">سفارش‌های اخیر</h2>
          <div class="profile-orders">
            <article v-for="order in userOrders" :key="order.id" class="profile-order">
              <div>
                <strong>{{ order.id }}</strong>
                <p class="muted">{{ order.date }}</p>
              </div>
              <span class="pill">{{ order.status }}</span>
              <strong>{{ formatPrice(order.total) }}</strong>
            </article>
          </div>
        </section>

        <section class="page-panel profile-card">
          <h2 class="section-title">آدرس‌های ذخیره‌شده</h2>
          <div class="profile-addresses">
            <article v-for="address in user.addresses" :key="address.id" class="profile-address">
              <strong>{{ address.title }}</strong>
              <p>{{ address.details }}</p>
            </article>
          </div>
        </section>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useUserStore } from '@/stores/userStore'
import { formatNumber, formatPrice } from '@/utils/format'

const user = useUserStore()
const admin = useAdminStore()
const userOrders = computed(() => admin.ordersByCustomer(user.profile.customerId))
</script>

<style scoped>
.profile-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.25rem;
}

.profile-sidebar,
.profile-card {
  padding: 1.25rem;
}

.profile-sidebar {
  display: grid;
  gap: 1rem;
  align-content: start;
}

.profile-sidebar__head {
  display: grid;
  gap: 0.55rem;
}

.profile-menu {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.6rem;
}

.profile-menu li {
  padding: 0.9rem 1rem;
  border-radius: 18px;
  background: var(--bg-muted);
  font-weight: 700;
}

.profile-content {
  display: grid;
  gap: 1.25rem;
}

.profile-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.profile-summary article,
.profile-order,
.profile-address {
  padding: 1rem;
  border-radius: 20px;
  background: var(--bg-muted);
}

.profile-summary article {
  display: grid;
  gap: 0.35rem;
}

.profile-orders,
.profile-addresses {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.profile-order {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.profile-order p,
.profile-address p {
  margin: 0.35rem 0 0;
}

@media (max-width: 920px) {
  .profile-layout,
  .profile-summary {
    grid-template-columns: 1fr;
  }

  .profile-order {
    flex-direction: column;
    align-items: start;
  }
}
</style>
