import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    mobileMenu: false,
    miniCart: false,
    searchQuery: '',
  }),

  actions: {
    syncBodyLock() {
      if (typeof document !== 'undefined') {
        document.body.style.overflow = this.mobileMenu || this.miniCart ? 'hidden' : ''
      }
    },
    toggleMobileMenu() {
      this.mobileMenu = !this.mobileMenu
      this.syncBodyLock()
    },
    closeMobileMenu() {
      this.mobileMenu = false
      this.syncBodyLock()
    },
    toggleMiniCart() {
      this.miniCart = !this.miniCart
      this.syncBodyLock()
    },
    closeMiniCart() {
      this.miniCart = false
      this.syncBodyLock()
    },
    setSearchQuery(value) {
      this.searchQuery = value
    },
  },
})
