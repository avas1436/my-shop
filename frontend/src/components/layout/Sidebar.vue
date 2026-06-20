<template>
  <aside
    class="lg:sticky lg:top-0 lg:h-screen p-5 grid content-start gap-5 border-l border-slate-900/10 bg-[#101828]/96 text-white/90 overflow-y-auto [&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-thumb]:bg-white/10 [&::-webkit-scrollbar-thumb]:rounded-full"
  >
    <router-link
      to="/admin"
      class="flex items-center gap-3.5 p-4 rounded-3xl bg-white/10 hover:bg-white/15 transition-colors"
    >
      <img
        src="@/assets/images/logo.jpg"
        alt="لوگوی فروشگاه"
        class="w-13 h-13 object-cover rounded-md shadow-soft"
      />
      <div>
        <span class="block font-bold">مرکز کنترل فروشگاه</span>
        <span class="block mt-1 text-[0.88rem] text-white/64">سیستم مدیریت</span>
      </div>
    </router-link>

    <nav class="grid gap-1.5">
      <router-link
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 py-3.5 px-4 rounded-md text-white/75 transition-all duration-200 hover:text-white hover:bg-white/10 hover:-translate-x-1 [&.router-link-exact-active]:text-white [&.router-link-exact-active]:bg-white/12 [&.router-link-exact-active]:-translate-x-1"
      >
        <component :is="item.icon" class="w-5 h-5 stroke-2 shrink-0" />
        {{ item.label }}
      </router-link>
    </nav>

    <div
      class="p-4 rounded-[24px] bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.14),transparent_35%),linear-gradient(135deg,rgba(91,61,245,0.44),rgba(255,122,89,0.32))] mt-2"
    >
      <span
        class="inline-flex items-center gap-1.5 py-1 px-2.5 rounded-full bg-white/20 text-white text-xs backdrop-blur-sm"
        >یادآوری امروز</span
      >
      <strong class="block mt-3.5 text-[0.95rem]"
        >کمبود موجودی و سفارش‌های جدید را بررسی کنید.</strong
      >
      <p class="block m-0 mt-2 text-white/75 text-[0.9rem] leading-relaxed">
        این بخش برای عملیات روزانه و پاسخ سریع به تیم فروش طراحی شده است.
      </p>
    </div>
  </aside>
</template>

<script setup>
import {
  CircleDollarSign,
  FileText,
  LayoutDashboard,
  Mail,
  Settings,
  ShieldCheck,
  ShoppingBag,
  ShoppingBasket,
  Tag,
  TrendingUp,
  Users,
  Warehouse,
} from '@lucide/vue';

defineOptions({ name: 'AdminSidebar' })

const items = [
  { to: '/admin', label: 'داشبورد', icon: LayoutDashboard },
  { to: '/admin/products', label: 'محصولات', icon: ShoppingBag },
  { to: '/admin/orders', label: 'سفارش‌ها', icon: ShoppingBasket },
  { to: '/admin/customers', label: 'مشتریان', icon: Users },
  { to: '/admin/inventory', label: 'انبارداری و تامین', icon: Warehouse },
  { to: '/admin/financials', label: 'مدیریت مالی و تراکنش‌ها', icon: CircleDollarSign },
  { to: '/admin/marketing', label: 'تخفیف‌ها و کمپین‌ها', icon: Tag },
  { to: '/admin/support', label: 'تیکت‌ها و پشتیبانی', icon: Mail },
  { to: '/admin/analytics', label: 'گزارش‌ها و آمار', icon: TrendingUp },
  { to: '/admin/staff', label: 'دسترسی کارکنان', icon: ShieldCheck },
  { to: '/admin/content', label: 'مدیریت محتوا', icon: FileText },
  { to: '/admin/settings', label: 'تنظیمات پیشرفته سیستم', icon: Settings },
]
</script>
