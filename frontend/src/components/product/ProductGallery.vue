<template>
  <section class="grid gap-4">
    <img
      :src="activeImage"
      :alt="title"
      class="w-full aspect-square object-cover rounded-[28px] bg-surface-strong"
    />

    <div class="grid grid-cols-3 gap-3">
      <button
        v-for="image in images"
        :key="image"
        type="button"
        class="p-1.5 rounded-[20px] border bg-surface-strong transition-all"
        :class="[
          image === activeImage
            ? 'border-primary/40 shadow-[0_0_0_3px_rgba(91,61,245,0.12)]'
            : 'border-border-light hover:border-primary/20',
        ]"
        @click="activeImage = image"
      >
        <img :src="image" :alt="title" class="w-full aspect-square object-cover rounded-2xl" />
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
