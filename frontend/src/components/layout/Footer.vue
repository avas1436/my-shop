<template>
  <footer class="mt-12 py-10 pb-8 bg-[#101828] text-white/88">
    <div class="container grid grid-cols-1 md:grid-cols-[1.6fr_1fr_1fr] gap-6">
      <section>
        <h3 class="m-0 mb-3.5 text-white">{{ admin.settings.storeName }}</h3>
        <p class="m-0 max-w-[42ch] text-white/72">
          تجربه‌ی یک فروشگاه آنلاین زیبا، سریع و مطمئن با تمرکز روی کالاهای باکیفیت، پشتیبانی
          پاسخ‌گو و تحویل سریع.
        </p>
      </section>

      <section>
        <h4 class="m-0 mb-3.5 text-white">دسترسی سریع</h4>
        <nav class="grid gap-3">
          <router-link to="/" class="text-white/72 hover:text-white transition-colors"
            >خانه</router-link
          >
          <router-link to="/products" class="text-white/72 hover:text-white transition-colors"
            >فروشگاه</router-link
          >
          <router-link to="/support" class="text-white/72 hover:text-white transition-colors"
            >پشتیبانی</router-link
          >
          <router-link to="/admin" class="text-white/72 hover:text-white transition-colors"
            >پنل ادمین</router-link
          >
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
      class="container flex flex-col md:flex-row justify-between gap-4 mt-8 pt-4 border-t border-white/10 text-[0.88rem] text-white/60"
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
