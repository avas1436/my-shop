import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: {
      name: 'آوا رضایی',
      phone: '۰۹۱۲ ۱۲۳ ۴۵۶۷',
      membership: 'طلایی',
      wallet: 1450000,
    },
    addresses: [
      {
        id: 1,
        title: 'خانه',
        details: 'تهران، سعادت‌آباد، سرو غربی، پلاک ۲۴، واحد ۶',
      },
    ],
    orders: [
      {
        id: 'A-2048',
        status: 'در حال آماده‌سازی',
        date: '۱۴۰۵/۰۱/۲۰',
        total: 13200000,
      },
      {
        id: 'A-1982',
        status: 'تحویل شده',
        date: '۱۴۰۴/۱۲/۲۲',
        total: 6290000,
      },
    ],
  }),
})
