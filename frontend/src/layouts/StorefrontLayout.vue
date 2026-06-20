<!-- src/layouts/StorefrontLayout.vue -->
<template>
  <div class="min-h-screen">
    <Header />

    <main class="pt-4 md:pt-8 pb-16">
      <RouterView />
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Footer from '@/components/layout/Footer.vue';
import Header from '@/components/layout/Header.vue';
import { RouterView } from 'vue-router';
</script>
