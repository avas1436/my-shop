<template>
  <div class="container mx-auto p-4 grid lg:grid-cols-4 gap-6">

    <!-- Sidebar -->
    <aside class="bg-white p-4 rounded shadow">
      <ul class="space-y-3 text-sm">
        <li>اطلاعات حساب</li>
        <li>سفارش‌ها</li>
        <li>آدرس‌ها</li>
        <li class="text-red-500">خروج</li>
      </ul>
    </aside>

    <!-- Content -->
    <div class="lg:col-span-3 bg-white p-6 rounded shadow">
      <h2 class="text-lg font-bold mb-4">سفارش‌های من</h2>

      <div class="text-sm text-gray-500">
        سفارشی ثبت نشده است
      </div>
    </div>

  </div>
</template>

<script setup>
</script>
