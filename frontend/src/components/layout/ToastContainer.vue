<template>
  <Teleport to="body">
    <div
      class="fixed bottom-5 right-4 left-4 z-9999 flex flex-col gap-2.5 pointer-events-none sm:left-auto sm:w-88"
      role="region"
      aria-label="Notifications"
      aria-live="polite"
    >
      <TransitionGroup
        name="toast"
        tag="div"
        enter-active-class="transition-all duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]"
        enter-from-class="opacity-0 translate-y-4 scale-95"
        enter-to-class="opacity-100 translate-y-0 scale-100"
        leave-active-class="transition-all duration-250 ease-in"
        leave-from-class="opacity-100 translate-y-0 scale-100"
        leave-to-class="opacity-0 translate-y-2 scale-95"
        class="flex flex-col gap-2.5"
      >
        <div
          v-for="error in errorStore.errors"
          :key="error.id"
          :class="[
            'flex items-start gap-3 py-3.5 px-4 rounded-2xl backdrop-blur-md shadow-[0_4px_6px_-1px_rgb(0_0_0/0.1),0_2px_4px_-2px_rgb(0_0_0/0.1),inset_0_1px_0_rgb(255_255_255/0.15)] pointer-events-auto relative overflow-hidden border',
            variantClasses[error.type] || variantClasses.error,
          ]"
          role="alert"
        >
          <span class="text-[1.1rem] shrink-0 mt-px" aria-hidden="true">
            {{ icons[error.type] ?? icons.error }}
          </span>

          <div class="flex-1 min-w-0">
            <p class="text-[0.8rem] font-bold tracking-wide m-0 mb-0.5 opacity-75 uppercase">
              {{ titles[error.type] ?? titles.error }}
            </p>
            <p class="text-[0.9rem] leading-snug m-0 wrap-break-word">{{ error.message }}</p>
          </div>

          <button
            class="shrink-0 flex items-center justify-center w-6 h-6 mt-px rounded-full border-none bg-black/5 text-inherit cursor-pointer transition-colors duration-150 hover:bg-black/15"
            @click="errorStore.removeError(error.id)"
            :aria-label="`Close notification: ${error.message}`"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
              <path
                d="M1 1l12 12M13 1L1 13"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
          </button>

          <div
            class="absolute bottom-0 left-0 h-0.75 w-full bg-current opacity-25 rounded-b-2xl origin-left animate-shrink"
          />
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useErrorStore } from '@/stores/errorStore'

const errorStore = useErrorStore()

const variantClasses = {
  error: 'bg-red-100/92 border-red-300/50 text-red-800',
  warning: 'bg-amber-100/92 border-amber-300/50 text-amber-900',
  success: 'bg-green-100/92 border-green-300/50 text-green-800',
  info: 'bg-blue-100/92 border-blue-300/50 text-blue-900',
}

const icons = {
  error: '🔴',
  warning: '🟡',
  success: '🟢',
  info: '🔵',
}

const titles = {
  error: 'خطا',
  warning: 'هشدار',
  success: 'موفق',
  info: 'اطلاعات',
}
</script>
