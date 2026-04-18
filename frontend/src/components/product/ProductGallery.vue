<template>
  <section class="product-gallery">
    <img :src="activeImage" :alt="title" class="product-gallery__main" />

    <div class="product-gallery__thumbs">
      <button
        v-for="image in images"
        :key="image"
        type="button"
        class="product-gallery__thumb"
        :class="{ 'product-gallery__thumb--active': image === activeImage }"
        @click="activeImage = image"
      >
        <img :src="image" :alt="title" />
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  images: { type: Array, default: () => [] },
  title: { type: String, default: 'محصول' },
})

const activeImage = ref(props.images[0] || '')

watch(
  () => props.images,
  (value) => {
    activeImage.value = value[0] || ''
  },
  { immediate: true },
)
</script>

<style scoped>
.product-gallery {
  display: grid;
  gap: 1rem;
}

.product-gallery__main {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 28px;
  background: var(--surface-strong);
}

.product-gallery__thumbs {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
}

.product-gallery__thumb {
  padding: 0.35rem;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--surface-strong);
}

.product-gallery__thumb--active {
  border-color: rgba(91, 61, 245, 0.38);
  box-shadow: 0 0 0 3px rgba(91, 61, 245, 0.12);
}

.product-gallery__thumb img {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 16px;
}
</style>
