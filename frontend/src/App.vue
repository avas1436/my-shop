<template>
  <div class="min-h-screen bg-gray-50 text-gray-800">
    <Header />

    <main class="pt-20 pb-10">
      <router-view />
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Header from './components/layout/Header.vue'
import Footer from './components/layout/Footer.vue'
</script>
