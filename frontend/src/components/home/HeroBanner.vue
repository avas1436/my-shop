<!-- src/components/home/HeroBanner.vue -->
<template>
  <section
    class="grid grid-cols-1 md:grid-cols-[1.15fr_0.85fr] gap-6 p-5 md:p-8 rounded-xl text-white shadow-(--shadow-custom)"
    style="
      background:
        radial-gradient(circle at top left, rgba(255, 255, 255, 0.32), transparent 30%),
        linear-gradient(135deg, var(--color-primary), rgba(255, 122, 89, 0.94));
    "
  >
    <!-- ستون چپ: متن + CTA + آمار -->
    <div class="grid content-center gap-4">
      <div>
        <span
          class="inline-flex items-center gap-1.5 py-1.5 px-3 rounded-full bg-white/20 text-white text-sm backdrop-blur-sm"
          >فروشگاه مدرن با انتخاب‌های خاص</span
        >
      </div>

      <h1 class="m-0 text-[clamp(2rem,4vw,3.5rem)] leading-tight">
        یک فروشگاه زیبا برای خرید هوشمند، سریع و لذت‌بخش
      </h1>

      <p class="m-0 max-w-[56ch] text-white/80">
        از کالای دیجیتال تا محصولات خانه و استایل، همه‌چیز با طراحی چشم‌نواز، تجربه‌ی روان و
        قیمت‌گذاری حرفه‌ای در دسترس شماست.
      </p>

      <div class="flex flex-wrap gap-3.5">
        <router-link
          to="/products"
          class="inline-flex items-center justify-center min-h-13 px-5 rounded-full font-bold text-primary bg-white"
          >مشاهده همه محصولات</router-link
        >
        <router-link
          to="/category/digital"
          class="inline-flex items-center justify-center min-h-13 px-5 rounded-full font-bold text-white border border-white/20 bg-white/10"
          >پیشنهادهای دیجیتال</router-link
        >
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-2">
        <div class="grid gap-1 p-4 rounded-[20px] bg-white/12 backdrop-blur-md">
          <strong class="text-xl">+۸۰۰</strong>
          <span class="text-white/75 text-sm">کالای منتخب</span>
        </div>
        <div class="grid gap-1 p-4 rounded-[20px] bg-white/12 backdrop-blur-md">
          <strong class="text-xl">۴.۸/۵</strong>
          <span class="text-white/75 text-sm">رضایت مشتریان</span>
        </div>
        <div class="grid gap-1 p-4 rounded-[20px] bg-white/12 backdrop-blur-md">
          <strong class="text-xl">۲۴ ساعته</strong>
          <span class="text-white/75 text-sm">پشتیبانی آنلاین</span>
        </div>
      </div>
    </div>

    <!-- ستون راست: محصول featured + محصولات کوچیک -->
    <div class="grid gap-4">
      <div class="grid gap-4 p-4 rounded-lg bg-white/10 border border-white/10 backdrop-blur-lg">
        <img
          :src="highlight.image"
          :alt="highlight.title"
          class="w-full object-cover rounded-[24px] aspect-4/3"
        />
        <div>
          <span
            class="inline-flex items-center gap-1.5 py-1 px-2.5 mb-2 rounded-full bg-white/20 text-white text-xs"
            >{{ highlight.badge }}</span
          >
          <h2 class="m-0 text-[1.35rem]">{{ highlight.title }}</h2>
          <p class="m-0 mt-1 text-white/80">{{ highlight.shortDescription }}</p>
        </div>
      </div>

      <div v-if="sideHighlights.length" class="grid gap-3.5">
        <article
          v-for="item in sideHighlights"
          :key="item.id"
          class="grid grid-cols-[88px_1fr] gap-3 items-center p-3 rounded-lg bg-white/10 border border-white/10 backdrop-blur-lg"
        >
          <img :src="item.image" :alt="item.title" class="w-full h-22 object-cover rounded-md" />
          <div class="grid">
            <strong>{{ item.title }}</strong>
            <span class="text-white/75 text-sm">{{ item.brand }}</span>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  highlight: { type: Object, required: true },
  sideHighlights: { type: Array, default: () => [] },
})
</script>
