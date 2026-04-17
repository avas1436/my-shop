<template>
  <article class="base-card">
    <slot />
  </article>
</template>

<style scoped>
.base-card {
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-soft);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(18px);
}
</style>
