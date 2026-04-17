import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
  }),

  getters: {
    total: (state) => state.items.reduce((sum, i) => sum + i.price * i.qty, 0),
  },

  actions: {
    add(product) {
      const item = this.items.find((i) => i.id === product.id)
      if (item) item.qty++
      else this.items.push({ ...product, qty: 1 })
    },
    increase(id) {
      this.items.find((i) => i.id === id).qty++
    },
    decrease(id) {
      const item = this.items.find((i) => i.id === id)
      if (item.qty > 1) item.qty--
    },
    remove(id) {
      this.items = this.items.filter((i) => i.id !== id)
    },
  },
})
