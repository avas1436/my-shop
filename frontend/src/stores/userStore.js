import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: {
      customerId: 1,
      name: 'آوا رضایی',
      email: 'ava@example.com',
      phone: '۰۹۱۲ ۱۲۳ ۴۵۶۷',
      membership: 'طلایی',
      wallet: 1450000,
      loyaltyPoints: 1280,
    },
    addresses: [
      {
        id: 1,
        title: 'خانه',
        city: 'تهران',
        details: 'تهران، سعادت‌آباد، سرو غربی، پلاک ۲۴، واحد ۶',
      },
      {
        id: 2,
        title: 'محل کار',
        city: 'تهران',
        details: 'تهران، ونک، خیابان خدامی، برج آفتاب، طبقه ۵',
      },
    ],
  }),

  getters: {
    primaryAddress: (state) => state.addresses[0] || null,
  },

  actions: {
    addAddress(address) {
      this.addresses.push({
        id: Date.now(),
        city: address.city || 'تهران',
        ...address,
      })
    },
    updateProfile(patch) {
      this.profile = {
        ...this.profile,
        ...patch,
      }
    },
  },
})
