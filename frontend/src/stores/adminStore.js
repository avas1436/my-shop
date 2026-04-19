import { defineStore } from 'pinia'

function formatPersianDate(date = new Date()) {
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(date)
}

function createItems(items) {
  return items.map((item) => ({
    id: item.id,
    title: item.title,
    qty: item.qty,
    price: item.price,
  }))
}

const initialCustomers = [
  {
    id: 1,
    name: 'آوا رضایی',
    phone: '۰۹۱۲ ۱۲۳ ۴۵۶۷',
    email: 'ava@example.com',
    city: 'تهران',
    segment: 'VIP',
    joinedAt: '۱۴۰۳/۰۶/۱۲',
  },
  {
    id: 2,
    name: 'مانی طاهری',
    phone: '۰۹۳۵ ۴۴۴ ۸۸۹۹',
    email: 'مانی@example.com',
    city: 'اصفهان',
    segment: 'وفادار',
    joinedAt: '۱۴۰۳/۰۹/۰۲',
  },
  {
    id: 3,
    name: 'الهام کریمی',
    phone: '۰۹۱۹ ۷۰۰ ۱۲۰۰',
    email: 'elham@example.com',
    city: 'شیراز',
    segment: 'جدید',
    joinedAt: '۱۴۰۴/۰۱/۱۸',
  },
  {
    id: 4,
    name: 'رضا شریفی',
    phone: '۰۹۳۸ ۲۱۰ ۴۳۰۰',
    email: 'reza@example.com',
    city: 'تبریز',
    segment: 'عمده',
    joinedAt: '۱۴۰۳/۱۱/۰۸',
  },
]

const initialOrders = [
  {
    id: 'A-2048',
    customerId: 1,
    customerName: 'آوا رضایی',
    status: 'در حال آماده‌سازی',
    date: '۱۴۰۵/۰۱/۲۰',
    total: 13289000,
    subtotal: 13200000,
    shippingCost: 89000,
    shippingMethod: 'post',
    paymentMethod: 'online',
    items: createItems([{ id: 105, title: 'اسپرسوساز Soma Barista Mini', qty: 1, price: 13200000 }]),
    city: 'تهران',
  },
  {
    id: 'A-1982',
    customerId: 1,
    customerName: 'آوا رضایی',
    status: 'تحویل شده',
    date: '۱۴۰۴/۱۲/۲۲',
    total: 6379000,
    subtotal: 6290000,
    shippingCost: 89000,
    shippingMethod: 'post',
    paymentMethod: 'wallet',
    items: createItems([{ id: 103, title: 'هدفون Orio Wave ANC', qty: 1, price: 6290000 }]),
    city: 'تهران',
  },
  {
    id: 'A-2110',
    customerId: 2,
    customerName: 'مانی طاهری',
    status: 'ارسال شده',
    date: '۱۴۰۵/۰۱/۲۴',
    total: 57900000,
    subtotal: 57900000,
    shippingCost: 0,
    shippingMethod: 'express',
    paymentMethod: 'online',
    items: createItems([{ id: 102, title: 'لپ‌تاپ Luma Air 14', qty: 1, price: 57900000 }]),
    city: 'اصفهان',
  },
  {
    id: 'A-2114',
    customerId: 3,
    customerName: 'الهام کریمی',
    status: 'ثبت شده',
    date: '۱۴۰۵/۰۱/۲۵',
    total: 5669000,
    subtotal: 5580000,
    shippingCost: 89000,
    shippingMethod: 'post',
    paymentMethod: 'online',
    items: createItems([{ id: 106, title: 'چراغ مطالعه Luma Beam', qty: 2, price: 2790000 }]),
    city: 'شیراز',
  },
]

const initialCampaigns = [
  {
    id: 1,
    title: 'کمپین بهار دیجیتال',
    channel: 'صفحه اصلی',
    budget: '۴۵ میلیون تومان',
    active: true,
  },
  {
    id: 2,
    title: 'ارسال رایگان مشتریان VIP',
    channel: 'باشگاه مشتریان',
    budget: '۱۲ میلیون تومان',
    active: true,
  },
  {
    id: 3,
    title: 'بازگشت مشتریان غیرفعال',
    channel: 'پیامک',
    budget: '۸ میلیون تومان',
    active: false,
  },
]

export const useAdminStore = defineStore('admin', {
  state: () => ({
    settings: {
      storeName: 'ShopVerse',
      supportPhone: '۰۲۱-۸۸۸۸۰۰۰۱',
      supportEmail: 'support@shopverse.local',
      freeShippingThreshold: '۳۰,۰۰۰,۰۰۰ تومان',
      heroMessage: 'خرید هوشمند، سریع و مطمئن برای خانه و سبک زندگی مدرن',
      fulfillmentWindow: 'تحویل ۲۴ تا ۴۸ ساعته در شهرهای اصلی',
    },
    customers: initialCustomers,
    orders: initialOrders,
    campaigns: initialCampaigns,
  }),

  getters: {
    ordersByCustomer: (state) => (customerId) =>
      state.orders.filter((order) => order.customerId === Number(customerId)),
    getOrderById: (state) => (orderId) => state.orders.find((order) => order.id === orderId),
    getCustomerById: (state) => (customerId) => state.customers.find((customer) => customer.id === Number(customerId)),
    totalRevenue: (state) =>
      state.orders
        .filter((order) => order.status !== 'لغو شده')
        .reduce((sum, order) => sum + order.total, 0),
    pendingOrders: (state) =>
      state.orders.filter((order) => ['ثبت شده', 'در حال آماده‌سازی'].includes(order.status)),
    activeCampaigns: (state) => state.campaigns.filter((campaign) => campaign.active),
  },

  actions: {
    createOrder(payload) {
      const nextOrderId = `A-${Math.floor(1000 + Math.random() * 9000)}`
      const order = {
        id: nextOrderId,
        customerId: Number(payload.customerId),
        customerName: payload.customerName,
        status: 'ثبت شده',
        date: formatPersianDate(),
        total: payload.total,
        subtotal: payload.subtotal,
        shippingCost: payload.shippingCost,
        shippingMethod: payload.shippingMethod,
        paymentMethod: payload.paymentMethod,
        items: createItems(payload.items || []),
        city: payload.city || 'تهران',
        recipient: {
          name: payload.recipient?.name,
          phone: payload.recipient?.phone,
          address: payload.recipient?.address,
        },
      }

      this.orders.unshift(order)
      this.syncCustomer(payload)

      return order
    },
    syncCustomer(payload) {
      const customerId = Number(payload.customerId)
      const currentCustomer = this.getCustomerById(customerId)

      if (currentCustomer) {
        Object.assign(currentCustomer, {
          name: payload.customerName,
          phone: payload.recipient?.phone || currentCustomer.phone,
          city: payload.city || currentCustomer.city,
          email: payload.email || currentCustomer.email,
        })

        return
      }

      this.customers.unshift({
        id: customerId,
        name: payload.customerName,
        phone: payload.recipient?.phone || 'ثبت نشده',
        email: payload.email || 'unknown@example.com',
        city: payload.city || 'تهران',
        segment: 'جدید',
        joinedAt: formatPersianDate(),
      })
    },
    updateOrderStatus(orderId, status) {
      const order = this.getOrderById(orderId)

      if (order) {
        order.status = status
      }
    },
    toggleCampaign(campaignId) {
      const campaign = this.campaigns.find((item) => item.id === campaignId)

      if (campaign) {
        campaign.active = !campaign.active
      }
    },
    updateSettings(patch) {
      this.settings = {
        ...this.settings,
        ...patch,
      }
    },
  },
})
