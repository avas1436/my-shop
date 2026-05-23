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
import { computed, onErrorCaptured, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useUserStore } from './stores/userStore'

onErrorCaptured((err, instance, info) => {
  console.error('خطا در کامپوننت:', err)
  console.log('اطلاعات خطا:', info)
  return false // برای جلوگیری از انتشار خطا به بالا
})

const user = useUserStore()
const isAuthReady = computed(() => user.isAuthReady)

onMounted(() => {
  user.initializeAuth()
})
</script>
