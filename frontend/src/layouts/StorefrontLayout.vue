<!-- src/layouts/StorefrontLayout.vue -->
<template>
  <div class="min-h-screen flex flex-col">
    <Header />

    <main class="grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 md:pt-8 pb-16">
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
