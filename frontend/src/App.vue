<!-- src/App.vue  -->
<template>
  <div class="min-h-screen bg-bg text-text-main overflow-x-hidden">
    <div
      v-if="!isAuthReady"
      class="flex-1 flex flex-col items-center justify-center bg-bg-muted gap-4"
    >
      <div
        class="w-12 h-12 border-4 border-border border-t-primary rounded-full animate-spin"
      ></div>
      <p class="text-text-muted font-medium text-lg">در حال آماده‌سازی...</p>
    </div>

    <RouterView v-else v-slot="{ Component }">
      <Transition
        enter-active-class="transition-opacity duration-300 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        mode="out-in"
      >
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
