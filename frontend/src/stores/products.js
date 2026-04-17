import { defineStore } from 'pinia'

export const useProductsStore = defineStore('products', {
  state: () => ({
    products: [
      { id: 1, title: 'محصول ۱', price: 120000, description: 'توضیح محصول ۱' },
      { id: 2, title: 'محصول ۲', price: 220000, description: 'توضیح محصول ۲' },
    ],
  }),
  actions: {
    getById(id) {
      return this.products.find((p) => p.id == id)
    },
  },
})
