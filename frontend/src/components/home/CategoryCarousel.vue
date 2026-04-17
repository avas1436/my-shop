<template>
  <section class="category-section">
    <div class="section-head">
      <div>
        <h2 class="section-title">خرید بر اساس دسته‌بندی</h2>
        <p class="section-subtitle">مسیر سریع برای رسیدن به انتخاب‌های محبوب و ترند</p>
      </div>
    </div>

    <div class="category-grid">
      <router-link
        v-for="category in categories"
        :key="category.id"
        :to="`/category/${category.id}`"
        class="category-card"
      >
        <img :src="category.icon" :alt="category.title" />
        <strong>{{ category.title }}</strong>
        <p>{{ category.description }}</p>
      </router-link>
    </div>
  </section>
</template>

<script setup>
defineProps({
  categories: { type: Array, default: () => [] },
})
</script>

<style scoped>
.category-section {
  display: grid;
  gap: 1rem;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.category-card {
  display: grid;
  gap: 0.8rem;
  padding: 1.2rem;
  border-radius: var(--radius-lg);
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-soft);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow);
}

.category-card img {
  width: 84px;
  height: 42px;
  object-fit: contain;
}

.category-card strong,
.category-card p {
  margin: 0;
}

.category-card p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

@media (max-width: 980px) {
  .category-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .category-grid {
    grid-template-columns: 1fr;
  }
}
</style>
