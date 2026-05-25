<!-- src/components/layout/ToastContainer.vue -->
<template>
  <Teleport to="body">
    <div class="toast-container" role="region" aria-label="Notifications" aria-live="polite">
      <TransitionGroup name="toast" tag="div">
        <div
          v-for="error in errorStore.errors"
          :key="error.id"
          :class="['toast', `toast--${error.type}`]"
          role="alert"
        >
          <!-- Icon -->
          <span class="toast__icon" aria-hidden="true">
            {{ icons[error.type] ?? icons.error }}
          </span>

          <!-- Content -->
          <div class="toast__body">
            <p class="toast__title">{{ titles[error.type] ?? titles.error }}</p>
            <p class="toast__message">{{ error.message }}</p>
          </div>

          <!-- Close -->
          <button
            class="toast__close"
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

          <!-- Progress bar -->
          <div class="toast__progress" />
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useErrorStore } from '@/stores/errorStore';

const errorStore = useErrorStore()

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

<style scoped>
/* ── Container ─────────────────────────────────────── */
.toast-container {
  position: fixed;
  bottom: 1.25rem;
  right: 1rem;
  left: 1rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  pointer-events: none;

  /* Desktop: pin to right corner */
  @media (min-width: 480px) {
    left: auto;
    width: 22rem;
  }
}

/* ── Toast card ─────────────────────────────────────── */
.toast {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border-radius: 1rem;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow:
    0 4px 6px -1px rgb(0 0 0 / 0.1),
    0 2px 4px -2px rgb(0 0 0 / 0.1),
    inset 0 1px 0 rgb(255 255 255 / 0.15);
  pointer-events: all;
  position: relative;
  overflow: hidden;
  border: 1px solid transparent;
}

/* ── Variants ───────────────────────────────────────── */
.toast--error {
  background: rgb(254 226 226 / 0.92);
  border-color: rgb(252 165 165 / 0.5);
  color: #991b1b;
}
.toast--warning {
  background: rgb(254 243 199 / 0.92);
  border-color: rgb(253 211 77 / 0.5);
  color: #92400e;
}
.toast--success {
  background: rgb(220 252 231 / 0.92);
  border-color: rgb(134 239 172 / 0.5);
  color: #166534;
}
.toast--info {
  background: rgb(219 234 254 / 0.92);
  border-color: rgb(147 197 253 / 0.5);
  color: #1e40af;
}

/* ── Icon ───────────────────────────────────────────── */
.toast__icon {
  font-size: 1.1rem;
  flex-shrink: 0;
  margin-top: 1px;
}

/* ── Body ───────────────────────────────────────────── */
.toast__body {
  flex: 1;
  min-width: 0;
}

.toast__title {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  margin: 0 0 0.15rem;
  opacity: 0.75;
  text-transform: uppercase;
}

.toast__message {
  font-size: 0.9rem;
  line-height: 1.45;
  margin: 0;
  word-break: break-word;
}

/* ── Close button ───────────────────────────────────── */
.toast__close {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  border: none;
  background: rgb(0 0 0 / 0.08);
  color: inherit;
  cursor: pointer;
  transition: background 0.15s;
  margin-top: 1px;
}
.toast__close:hover {
  background: rgb(0 0 0 / 0.16);
}

/* ── Progress bar ───────────────────────────────────── */
.toast__progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  width: 100%;
  background: currentColor;
  opacity: 0.25;
  border-radius: 0 0 1rem 1rem;
  transform-origin: left;
  animation: shrink 4s linear forwards;
}

@keyframes shrink {
  from {
    transform: scaleX(1);
  }
  to {
    transform: scaleX(0);
  }
}

/* ── Transition ─────────────────────────────────────── */
.toast-enter-active {
  animation: slide-in 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toast-leave-active {
  animation: slide-out 0.25s ease-in forwards;
}

@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateY(1rem) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
@keyframes slide-out {
  to {
    opacity: 0;
    transform: translateY(0.5rem) scale(0.95);
  }
}
</style>
