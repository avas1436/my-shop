// src/stores/errorStore.js
import { defineStore } from 'pinia'

export const useErrorStore = defineStore('error', {
  state: () => ({
    errors: [],
  }),
  actions: {
    addError(error) {
      const id = Date.now()
      this.errors.push({ id, ...error })
      // حذف خودکار خطا بعد از 5 ثانیه
      setTimeout(() => {
        this.removeError(id)
      }, 5000)
    },
    removeError(id) {
      this.errors = this.errors.filter((e) => e.id !== id)
    },
  },
})
