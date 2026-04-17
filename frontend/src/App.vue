<template>
  <div class="app-shell">
    <Header />

    <main class="app-main">
      <router-view />
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Header from './components/layout/Header.vue'
import Footer from './components/layout/Footer.vue'
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.app-main {
  padding: 2rem 0 4rem;
}

@media (max-width: 768px) {
  .app-main {
    padding-top: 1rem;
  }
}
</style>
