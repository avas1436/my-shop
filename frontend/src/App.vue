<!-- src/App.vue  -->
<template>
  <div v-if="!isAuthReady" class="app-loading">
    <div class="loader"></div>
    <p>در حال آماده‌سازی...</p>
  </div>

  <RouterView v-else v-slot="{ Component }">
    <Transition name="fade" mode="out-in">
      <component :is="Component" />
    </Transition>
  </RouterView>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useUserStore } from './stores/userStore'

const user = useUserStore()
const isAuthReady = computed(() => user.isAuthReady)

onMounted(() => {
  user.initializeAuth()
})
</script>
