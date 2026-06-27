<!-- src/components/home/PromotionBanner.vue -->
<template>
  <section
    class="grid grid-cols-1 md:grid-cols-[1fr_auto] gap-4 items-center p-5 md:py-[1.6rem] md:px-[1.8rem] rounded-xl text-white"
    style="
      background:
        radial-gradient(circle at top right, rgba(255, 255, 255, 0.22), transparent 24%),
        linear-gradient(135deg, #172033, rgba(91, 61, 245, 0.96));
    "
  >
    <div>
      <span
        class="inline-flex items-center gap-1.5 py-1.5 px-3 rounded-full bg-white/10 text-white text-sm backdrop-blur-sm border border-white/10"
        >تخفیف هفتگی</span
      >
      <h2 class="mt-3.5 m-0 text-[clamp(1.5rem,3vw,2.2rem)] font-bold">
        تا ۲۵٪ تخفیف روی کالاهای منتخب دیجیتال و خانه
      </h2>
      <p class="mt-3 m-0 max-w-[52ch] text-white/80 leading-relaxed">
        مجموعه‌ای از محصولات پرفروش با موجودی محدود و ارسال سریع؛ زمان خوبی برای نهایی کردن خرید
        است.
      </p>
    </div>

    <div class="flex flex-wrap gap-3 mt-4 md:mt-0 md:flex-col lg:flex-row">
      <router-link
        to="/category/digital"
        class="inline-flex items-center justify-center min-h-12 px-5 rounded-full font-bold bg-white text-primary whitespace-nowrap"
        >خرید دیجیتال</router-link
      >
      <router-link
        to="/category/home"
        class="inline-flex items-center justify-center min-h-12 px-5 rounded-full font-bold border border-white/20 text-white whitespace-nowrap"
        >محصولات خانه</router-link
      >
    </div>
  </section>
</template>
