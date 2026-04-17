import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
  }),

  getters: {
    count: (state) => state.items.reduce((sum, item) => sum + item.qty, 0),
    subtotal: (state) => state.items.reduce((sum, item) => sum + item.price * item.qty, 0),
    discount: (state) =>
      state.items.reduce((sum, item) => sum + Math.max((item.oldPrice - item.price) * item.qty, 0), 0),
    shipping() {
      if (!this.items.length) {
        return 0
      }

      return this.subtotal >= 30000000 ? 0 : 89000
    },
    total() {
      return this.subtotal + this.shipping
    },
  },

  actions: {
    add(product) {
      if (!product) {
        return
      }

      const item = this.items.find((entry) => entry.id === product.id)

      if (item) {
        item.qty += 1
        return
      }

      this.items.push({
        id: product.id,
        title: product.title,
        price: product.price,
        oldPrice: product.oldPrice || product.price,
        image: product.image,
        badge: product.badge,
        qty: 1,
      })
    },
    increase(id) {
      const item = this.items.find((entry) => entry.id === id)

      if (item) {
        item.qty += 1
      }
    },
    decrease(id) {
      const item = this.items.find((entry) => entry.id === id)

      if (item && item.qty > 1) {
        item.qty -= 1
      }
    },
    remove(id) {
      this.items = this.items.filter((entry) => entry.id !== id)
    },
    clear() {
      this.items = []
    },
  },
})
