<template>
  <section class="brands-section">
    <div class="section-head">
      <div>
        <h2 class="section-title">برندهای محبوب</h2>
        <p class="section-subtitle">ترکیبی از برندهای نوآور، خوش‌نام و پرفروش</p>
      </div>
    </div>

    <div class="brands-grid">
      <article v-for="brand in brands" :key="brand.id" class="brand-card">
        <img :src="brand.logo" :alt="brand.name" />
        <strong>{{ brand.name }}</strong>
      </article>
    </div>
  </section>
</template>

<script setup>
defineProps({
  brands: { type: Array, default: () => [] },
})
</script>

<style scoped>
.brands-section {
  display: grid;
  gap: 1rem;
}

.brands-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 1rem;
}

.brand-card {
  display: grid;
  place-items: center;
  gap: 0.8rem;
  padding: 1.2rem;
  border-radius: var(--radius-lg);
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-soft);
}

.brand-card img {
  width: 120px;
  height: 60px;
  object-fit: contain;
}

@media (max-width: 980px) {
  .brands-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .brands-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
