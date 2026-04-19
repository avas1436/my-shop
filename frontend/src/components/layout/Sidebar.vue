<template>
  <aside class="admin-sidebar">
    <router-link to="/admin" class="admin-sidebar__brand">
      <span class="admin-sidebar__logo">SV</span>
      <div>
        <strong>ShopVerse Admin</strong>
        <span>مرکز کنترل فروشگاه</span>
      </div>
    </router-link>

    <nav class="admin-sidebar__nav">
      <router-link v-for="item in items" :key="item.to" :to="item.to">
        <span>{{ item.icon }}</span>
        {{ item.label }}
      </router-link>
    </nav>

    <div class="admin-sidebar__card">
      <span class="pill">یادآوری امروز</span>
      <strong>کمبود موجودی و سفارش‌های جدید را قبل از ظهر بررسی کنید.</strong>
      <p>این بخش برای عملیات روزانه، مدیریت کمپین‌ها و پاسخ سریع به تیم فروش طراحی شده است.</p>
    </div>
  </aside>
</template>

<script setup>
defineOptions({
  name: 'AdminSidebar',
})

const items = [
  { to: '/admin', label: 'داشبورد', icon: '◫' },
  { to: '/admin/products', label: 'محصولات', icon: '◧' },
  { to: '/admin/orders', label: 'سفارش‌ها', icon: '◩' },
  { to: '/admin/customers', label: 'مشتریان', icon: '◎' },
  { to: '/admin/content', label: 'محتوا و تنظیمات', icon: '✦' },
]
</script>

<style scoped>
.admin-sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  padding: 1.25rem;
  display: grid;
  align-content: start;
  gap: 1.2rem;
  border-left: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(16, 24, 40, 0.96);
  color: rgba(255, 255, 255, 0.88);
}

.admin-sidebar__brand {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 1rem;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.08);
}

.admin-sidebar__brand strong,
.admin-sidebar__brand span {
  display: block;
}

.admin-sidebar__brand span:last-child {
  margin-top: 0.2rem;
  font-size: 0.88rem;
  color: rgba(255, 255, 255, 0.64);
}

.admin-sidebar__logo {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border-radius: 18px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: #fff;
  font-weight: 700;
}

.admin-sidebar__nav {
  display: grid;
  gap: 0.45rem;
}

.admin-sidebar__nav a {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.95rem 1rem;
  border-radius: 18px;
  color: rgba(255, 255, 255, 0.74);
  transition:
    background-color 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.admin-sidebar__nav a:hover,
.admin-sidebar__nav a.router-link-exact-active {
  color: #fff;
  background: rgba(255, 255, 255, 0.12);
  transform: translateX(-2px);
}

.admin-sidebar__card {
  padding: 1rem;
  border-radius: 24px;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.14), transparent 35%),
    linear-gradient(135deg, rgba(91, 61, 245, 0.44), rgba(255, 122, 89, 0.32));
}

.admin-sidebar__card strong,
.admin-sidebar__card p {
  display: block;
}

.admin-sidebar__card strong {
  margin-top: 0.85rem;
}

.admin-sidebar__card p {
  margin: 0.55rem 0 0;
  color: rgba(255, 255, 255, 0.76);
  font-size: 0.9rem;
}

@media (max-width: 1080px) {
  .admin-sidebar {
    position: static;
    height: auto;
  }
}
</style>
