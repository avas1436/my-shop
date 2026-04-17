import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
  }),

  actions: {
    add(product) {
      const existing = this.items.find((i) => i.id === product.id)
      if (existing) existing.qty++
      else this.items.push({ ...product, qty: 1 })
    },

    remove(id) {
      this.items = this.items.filter((i) => i.id !== id)
    },
  },
})
