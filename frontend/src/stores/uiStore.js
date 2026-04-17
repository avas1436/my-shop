import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    mobileMenu: false,
    miniCart: false,
  }),

  actions: {
    toggleMobileMenu() {
      this.mobileMenu = !this.mobileMenu
    },
    toggleMiniCart() {
      this.miniCart = !this.miniCart
    },
  },
})
