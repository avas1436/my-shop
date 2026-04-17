<template>
  <section class="review-panel">
    <div class="review-panel__summary">
      <div>
        <strong>★ {{ rating }}</strong>
        <span>میانگین امتیاز کاربران</span>
      </div>
      <p>{{ count }} بررسی ثبت شده</p>
    </div>

    <ul class="review-panel__list">
      <li v-for="item in highlights" :key="item">{{ item }}</li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  rating: { type: Number, default: 0 },
  count: { type: Number, default: 0 },
  highlights: { type: Array, default: () => [] },
})
</script>

<style scoped>
.review-panel {
  display: grid;
  gap: 1rem;
  padding: 1.25rem;
  border-radius: var(--radius-lg);
  background: var(--bg-muted);
}

.review-panel__summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.review-panel__summary strong {
  font-size: 2rem;
  display: block;
}

.review-panel__summary span,
.review-panel__summary p {
  color: var(--text-muted);
  margin: 0;
}

.review-panel__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 0.6rem;
}

.review-panel__list li {
  padding: 0.8rem 1rem;
  border-radius: 16px;
  background: var(--surface-strong);
}
</style>
