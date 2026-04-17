<template>
  <section class="hero-banner">
    <div class="hero-banner__content">
      <span class="pill">فروشگاه مدرن با انتخاب‌های خاص</span>
      <h1>یک فروشگاه زیبا برای خرید هوشمند، سریع و لذت‌بخش</h1>
      <p>
        از کالای دیجیتال تا محصولات خانه و استایل، همه‌چیز با طراحی چشم‌نواز،
        تجربه‌ی روان و قیمت‌گذاری حرفه‌ای در دسترس شماست.
      </p>

      <div class="hero-banner__actions">
        <router-link to="/products" class="hero-banner__primary">مشاهده همه محصولات</router-link>
        <router-link to="/category/digital" class="hero-banner__secondary">پیشنهادهای دیجیتال</router-link>
      </div>

      <div class="hero-banner__stats">
        <div>
          <strong>+۸۰۰</strong>
          <span>کالای منتخب</span>
        </div>
        <div>
          <strong>۴.۸/۵</strong>
          <span>رضایت مشتریان</span>
        </div>
        <div>
          <strong>۲۴ ساعته</strong>
          <span>پشتیبانی آنلاین</span>
        </div>
      </div>
    </div>

    <div class="hero-banner__visual">
      <div class="hero-banner__card hero-banner__card--main">
        <img :src="highlight.image" :alt="highlight.title" />
        <div>
          <span class="pill">{{ highlight.badge }}</span>
          <h2>{{ highlight.title }}</h2>
          <p>{{ highlight.shortDescription }}</p>
        </div>
      </div>

      <div class="hero-banner__stack">
        <article v-for="item in sideHighlights" :key="item.id" class="hero-banner__card hero-banner__card--mini">
          <img :src="item.image" :alt="item.title" />
          <div>
            <strong>{{ item.title }}</strong>
            <span>{{ item.brand }}</span>
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

<style scoped>
.hero-banner {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 1.5rem;
  padding: 2rem;
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.32), transparent 30%),
    linear-gradient(135deg, rgba(91, 61, 245, 1), rgba(255, 122, 89, 0.94));
  color: #fff;
  box-shadow: var(--shadow);
}

.hero-banner__content {
  display: grid;
  align-content: center;
  gap: 1rem;
}

.hero-banner__content h1,
.hero-banner__content p,
.hero-banner__card h2,
.hero-banner__card p {
  margin: 0;
}

.hero-banner__content h1 {
  font-size: clamp(2rem, 4vw, 3.5rem);
  line-height: 1.2;
}

.hero-banner__content p {
  max-width: 56ch;
  color: rgba(255, 255, 255, 0.82);
}

.hero-banner__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.9rem;
}

.hero-banner__primary,
.hero-banner__secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  padding: 0 1.2rem;
  border-radius: 999px;
  font-weight: 700;
}

.hero-banner__primary {
  color: var(--primary);
  background: #fff;
}

.hero-banner__secondary {
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
}

.hero-banner__stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 0.5rem;
}

.hero-banner__stats div {
  display: grid;
  gap: 0.2rem;
  padding: 1rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
}

.hero-banner__stats strong {
  font-size: 1.25rem;
}

.hero-banner__stats span {
  color: rgba(255, 255, 255, 0.78);
  font-size: 0.9rem;
}

.hero-banner__visual {
  display: grid;
  gap: 1rem;
}

.hero-banner__card {
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(16px);
}

.hero-banner__card img {
  width: 100%;
  object-fit: cover;
}

.hero-banner__card--main {
  display: grid;
  gap: 1rem;
  padding: 1rem;
}

.hero-banner__card--main img {
  border-radius: 24px;
  aspect-ratio: 4 / 3;
}

.hero-banner__card--main h2 {
  font-size: 1.35rem;
}

.hero-banner__card--main p {
  color: rgba(255, 255, 255, 0.78);
}

.hero-banner__stack {
  display: grid;
  gap: 0.9rem;
}

.hero-banner__card--mini {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 0.8rem;
  align-items: center;
  padding: 0.8rem;
}

.hero-banner__card--mini img {
  height: 88px;
  border-radius: 18px;
}

.hero-banner__card--mini div {
  display: grid;
}

.hero-banner__card--mini span {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.9rem;
}

@media (max-width: 900px) {
  .hero-banner {
    grid-template-columns: 1fr;
    padding: 1.25rem;
  }
}

@media (max-width: 640px) {
  .hero-banner__stats {
    grid-template-columns: 1fr;
  }
}
</style>
