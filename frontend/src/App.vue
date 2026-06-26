<!-- src/App.vue  -->
<template>
  <div class="min-h-screen overflow-x-hidden bg-bg text-text-main">
    <div
      v-if="!isAuthReady"
      class="flex min-h-screen flex-col items-center justify-center gap-4 bg-bg-muted"
    >
      <div
        class="h-12 w-12 animate-spin rounded-full border-4 border-border-light border-t-primary"
      ></div>
      <p class="text-lg font-medium text-text-muted">در حال آماده‌سازی...</p>
    </div>

    <RouterView v-else v-slot="{ Component }">
      <Transition name="fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>

    <ToastContainer />
  </div>
</template>

<script setup>
import ToastContainer from '@/components/layout/ToastContainer.vue'
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
  user.initializeAuth(true)
})
</script>
