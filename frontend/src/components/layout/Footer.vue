<!-- src/components/layout/Footer.vue -->
<template>
  <footer class="mt-12 py-10 pb-8 bg-text-main text-bg-soft/90">
    <div
      class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-[1.6fr_1fr_1fr] gap-6"
    >
      <section>
        <h3 class="m-0 mb-3.5 text-bg-soft font-bold text-lg">
          {{ admin.settings.storeName }}
        </h3>
        <p class="m-0 max-w-[42ch] text-bg-soft/70 leading-relaxed">
          {{ admin.settings.heroMessage }}
        </p>
      </section>

      <section>
        <h4 class="m-0 mb-3.5 text-bg-soft font-semibold">دسترسی سریع</h4>
        <nav class="grid gap-3">
          <router-link
            to="/"
            class="text-bg-soft/70 hover:text-accent transition-colors duration-200"
            >خانه
          </router-link>

          <router-link
            to="/products"
            class="text-bg-soft/70 hover:text-accent transition-colors duration-200"
            >فروشگاه
          </router-link>

          <router-link
            to="/support"
            class="text-bg-soft/70 hover:text-accent transition-colors duration-200"
            >پشتیبانی
          </router-link>

          <router-link
            to="/admin"
            class="text-bg-soft/70 hover:text-accent transition-colors duration-200"
            >پنل ادمین
          </router-link>
        </nav>
      </section>

      <section>
        <h4 class="m-0 mb-3.5 text-white">اعتماد و پشتیبانی</h4>
        <ul class="grid gap-3 list-none p-0 m-0">
          <li class="text-white/72">هفت روز ضمانت بازگشت</li>
          <li class="text-white/72">{{ admin.settings.supportPhone }}</li>
          <li class="text-white/72">{{ admin.settings.supportEmail }}</li>
        </ul>
      </section>
    </div>

    <div
      class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between gap-4 mt-8 pt-4 border-t border-white/10 text-[0.88rem] text-white/60"
    >
      <span>© ۱۴۰۵ {{ admin.settings.storeName }} — تمامی حقوق محفوظ است.</span>
      <span>{{ admin.settings.fulfillmentWindow }}</span>
    </div>
  </footer>
</template>

<script setup>
import { useAdminStore } from '@/stores/adminStore';

defineOptions({ name: 'SiteFooter' })
const admin = useAdminStore()
</script>
