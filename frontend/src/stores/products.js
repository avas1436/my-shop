import { defineStore } from 'pinia'

function createArtwork(label, colors, accent = 'rgba(255,255,255,0.28)') {
  const [start, end] = colors

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
    <svg xmlns="http://www.w3.org/2000/svg" width="900" height="900" viewBox="0 0 900 900">
      <defs>
        <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="${start}" />
          <stop offset="100%" stop-color="${end}" />
        </linearGradient>
      </defs>
      <rect width="900" height="900" rx="72" fill="url(#g)" />
      <circle cx="700" cy="180" r="110" fill="${accent}" />
      <circle cx="180" cy="760" r="160" fill="rgba(255,255,255,0.12)" />
      <rect x="80" y="96" width="220" height="18" rx="9" fill="rgba(255,255,255,0.24)" />
      <rect x="80" y="134" width="160" height="18" rx="9" fill="rgba(255,255,255,0.18)" />
      <text x="80" y="690" fill="white" font-family="Arial, sans-serif" font-size="76" font-weight="700">${label}</text>
      <text x="80" y="770" fill="rgba(255,255,255,0.85)" font-family="Arial, sans-serif" font-size="36">Premium Collection</text>
    </svg>
  `)}`
}

function createLogo(text, colors) {
  const [start, end] = colors

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
    <svg xmlns="http://www.w3.org/2000/svg" width="240" height="120" viewBox="0 0 240 120">
      <defs>
        <linearGradient id="brand" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="${start}" />
          <stop offset="100%" stop-color="${end}" />
        </linearGradient>
      </defs>
      <rect width="240" height="120" rx="28" fill="url(#brand)" />
      <text x="120" y="70" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="38" font-weight="700">${text}</text>
    </svg>
  `)}`
}

const categories = [
  {
    id: 'digital',
    title: 'کالای دیجیتال',
    description: 'موبایل، لپ‌تاپ و ابزارهای هوشمند برای سبک زندگی مدرن',
    icon: createLogo('Tech', ['#5b3df5', '#8b5cf6']),
  },
  {
    id: 'audio',
    title: 'صوتی و پوشیدنی',
    description: 'هدفون، ساعت و گجت‌هایی که روز شما را هوشمندتر می‌کنند',
    icon: createLogo('Audio', ['#ff7a59', '#ff4d6d']),
  },
  {
    id: 'home',
    title: 'خانه و آشپزخانه',
    description: 'محصولات کاربردی و خوش‌طراحی برای خانه‌ای مرتب‌تر',
    icon: createLogo('Home', ['#0f9d81', '#14b8a6']),
  },
  {
    id: 'fashion',
    title: 'مد و استایل',
    description: 'انتخاب‌های مینیمال برای استایل روزمره و حرفه‌ای',
    icon: createLogo('Mode', ['#f59e0b', '#f97316']),
  },
]

const brands = [
  { id: 1, name: 'Nova', logo: createLogo('Nova', ['#5b3df5', '#6d28d9']) },
  { id: 2, name: 'Luma', logo: createLogo('Luma', ['#0f9d81', '#10b981']) },
  { id: 3, name: 'Orio', logo: createLogo('Orio', ['#ff7a59', '#f43f5e']) },
  { id: 4, name: 'Mira', logo: createLogo('Mira', ['#2563eb', '#06b6d4']) },
  { id: 5, name: 'Soma', logo: createLogo('Soma', ['#f59e0b', '#fb7185']) },
]

const products = [
  {
    id: 101,
    title: 'گوشی Nova X Pro',
    categoryId: 'digital',
    brand: 'Nova',
    badge: 'ارسال فوری',
    price: 38900000,
    oldPrice: 42800000,
    rating: 4.8,
    reviewCount: 126,
    image: createArtwork('NOVA X', ['#5b3df5', '#8b5cf6']),
    gallery: [
      createArtwork('NOVA X', ['#5b3df5', '#8b5cf6']),
      createArtwork('CAMERA', ['#1d4ed8', '#7c3aed']),
      createArtwork('DISPLAY', ['#0f172a', '#334155']),
    ],
    stock: 7,
    shortDescription: 'پرچمدار سبک با نمایشگر ۱۲۰ هرتز و دوربین ۵۰ مگاپیکسلی.',
    description:
      'Nova X Pro برای کاربرانی طراحی شده که تجربه‌ی روان، دوربین حرفه‌ای و شارژ سریع را در یک بدنه‌ی خوش‌ساخت می‌خواهند.',
    specs: [
      { label: 'نمایشگر', value: '6.7 اینچ AMOLED' },
      { label: 'حافظه', value: '256 گیگابایت' },
      { label: 'باتری', value: '5000 میلی‌آمپرساعت' },
    ],
    reviewHighlights: ['کیفیت عالی نمایشگر', 'شارژدهی یک‌روزه', 'دوربین شب قدرتمند'],
    flags: { featured: true, bestseller: true, newest: true },
  },
  {
    id: 102,
    title: 'لپ‌تاپ Luma Air 14',
    categoryId: 'digital',
    brand: 'Luma',
    badge: 'پیشنهاد ویژه',
    price: 57900000,
    oldPrice: 62400000,
    rating: 4.7,
    reviewCount: 84,
    image: createArtwork('LUMA AIR', ['#0f9d81', '#06b6d4']),
    gallery: [
      createArtwork('LUMA AIR', ['#0f9d81', '#06b6d4']),
      createArtwork('KEYBOARD', ['#14b8a6', '#0891b2']),
      createArtwork('LIGHT', ['#134e4a', '#164e63']),
    ],
    stock: 4,
    shortDescription: 'لپ‌تاپی فوق‌سبک برای کار، جلسه و مطالعه.',
    description:
      'بدنه‌ی آلومینیومی، عمر باتری طولانی و نمایشگر دقیق باعث شده Luma Air 14 انتخابی محبوب برای حرفه‌ای‌ها باشد.',
    specs: [
      { label: 'پردازنده', value: 'Core Ultra 7' },
      { label: 'رم', value: '16 گیگابایت' },
      { label: 'وزن', value: '1.25 کیلوگرم' },
    ],
    reviewHighlights: ['کیبورد نرم و دقیق', 'بدنه‌ی سبک', 'مناسب کار روزانه و طراحی'],
    flags: { featured: true, bestseller: false, newest: true },
  },
  {
    id: 103,
    title: 'هدفون Orio Wave ANC',
    categoryId: 'audio',
    brand: 'Orio',
    badge: 'محبوب کاربران',
    price: 6290000,
    oldPrice: 7390000,
    rating: 4.9,
    reviewCount: 203,
    image: createArtwork('WAVE ANC', ['#ff7a59', '#f43f5e']),
    gallery: [
      createArtwork('WAVE ANC', ['#ff7a59', '#f43f5e']),
      createArtwork('SOUND', ['#fb7185', '#be185d']),
      createArtwork('NOISE OFF', ['#7f1d1d', '#ef4444']),
    ],
    stock: 18,
    shortDescription: 'نویز کنسلینگ فعال با صدایی گرم و واضح.',
    description:
      'Wave ANC برای رفت‌وآمد شهری و تماس‌های کاری طراحی شده و با بدنه‌ی سبک، ساعت‌ها استفاده‌ی راحت را ممکن می‌کند.',
    specs: [
      { label: 'باتری', value: '38 ساعت' },
      { label: 'اتصال', value: 'Bluetooth 5.4' },
      { label: 'میکروفون', value: 'سه‌گانه' },
    ],
    reviewHighlights: ['بیس کنترل‌شده', 'نویزکنسلینگ مؤثر', 'کیفیت مکالمه‌ی عالی'],
    flags: { featured: true, bestseller: true, newest: false },
  },
  {
    id: 104,
    title: 'ساعت هوشمند Mira Fit S',
    categoryId: 'audio',
    brand: 'Mira',
    badge: 'جدید',
    price: 4890000,
    oldPrice: 0,
    rating: 4.6,
    reviewCount: 58,
    image: createArtwork('FIT S', ['#2563eb', '#06b6d4']),
    gallery: [
      createArtwork('FIT S', ['#2563eb', '#06b6d4']),
      createArtwork('HEALTH', ['#0284c7', '#0ea5e9']),
      createArtwork('SPORT', ['#082f49', '#155e75']),
    ],
    stock: 12,
    shortDescription: 'پایش خواب، ورزش و سلامت با طراحی مینیمال.',
    description:
      'Mira Fit S با بدنه‌ی باریک، سنسورهای سلامت و بند نرم، همراه روزهای پرتحرک شماست.',
    specs: [
      { label: 'نمایشگر', value: 'AMOLED 1.78 اینچ' },
      { label: 'مقاومت', value: '5ATM' },
      { label: 'سنسورها', value: 'ضربان قلب و اکسیژن خون' },
    ],
    reviewHighlights: ['طراحی سبک', 'رابط کاربری روان', 'اعلان‌های سریع'],
    flags: { featured: false, bestseller: true, newest: true },
  },
  {
    id: 105,
    title: 'اسپرسوساز Soma Barista Mini',
    categoryId: 'home',
    brand: 'Soma',
    badge: 'خانه‌ی هوشمند',
    price: 13200000,
    oldPrice: 14900000,
    rating: 4.7,
    reviewCount: 92,
    image: createArtwork('BARISTA', ['#f59e0b', '#f97316']),
    gallery: [
      createArtwork('BARISTA', ['#f59e0b', '#f97316']),
      createArtwork('COFFEE', ['#92400e', '#b45309']),
      createArtwork('LATTE', ['#78350f', '#d97706']),
    ],
    stock: 5,
    shortDescription: 'قهوه‌ی حرفه‌ای در ابعاد جمع‌وجور برای آشپزخانه‌های مدرن.',
    description:
      'Soma Barista Mini با فشار بخار مناسب و بدنه‌ی کم‌جا، هر صبح را به یک تجربه‌ی کافه‌ای تبدیل می‌کند.',
    specs: [
      { label: 'فشار بخار', value: '20 بار' },
      { label: 'مخزن آب', value: '1.2 لیتر' },
      { label: 'جنس بدنه', value: 'استیل مات' },
    ],
    reviewHighlights: ['طعم قهوه‌ی یکنواخت', 'راه‌اندازی سریع', 'طراحی لوکس'],
    flags: { featured: true, bestseller: false, newest: false },
  },
  {
    id: 106,
    title: 'چراغ مطالعه Luma Beam',
    categoryId: 'home',
    brand: 'Luma',
    badge: 'مناسب میزکار',
    price: 2790000,
    oldPrice: 3190000,
    rating: 4.5,
    reviewCount: 39,
    image: createArtwork('BEAM', ['#14b8a6', '#22c55e']),
    gallery: [
      createArtwork('BEAM', ['#14b8a6', '#22c55e']),
      createArtwork('WORK', ['#0f766e', '#15803d']),
      createArtwork('LIGHT', ['#064e3b', '#166534']),
    ],
    stock: 22,
    shortDescription: 'نور قابل تنظیم با طراحی مینیمال و شارژ USB-C.',
    description:
      'چراغ مطالعه‌ی Beam با پایه‌ی نرم، نور سه‌حالته و شارژ آسان، برای فضای کار خانگی و اتاق مطالعه عالی است.',
    specs: [
      { label: 'نور', value: 'سه حالت دمایی' },
      { label: 'شارژ', value: 'USB-C' },
      { label: 'باتری', value: '8 ساعت' },
    ],
    reviewHighlights: ['نور یکنواخت', 'بدون لرزش', 'طراحی مدرن'],
    flags: { featured: false, bestseller: true, newest: false },
  },
  {
    id: 107,
    title: 'کفش روزمره Mira Street',
    categoryId: 'fashion',
    brand: 'Mira',
    badge: 'استایل شهری',
    price: 3590000,
    oldPrice: 4190000,
    rating: 4.4,
    reviewCount: 67,
    image: createArtwork('STREET', ['#6366f1', '#ec4899']),
    gallery: [
      createArtwork('STREET', ['#6366f1', '#ec4899']),
      createArtwork('MOVE', ['#7c3aed', '#db2777']),
      createArtwork('STYLE', ['#4c1d95', '#9d174d']),
    ],
    stock: 9,
    shortDescription: 'کفش سبک و راحت برای استایل روزمره‌ی مینیمال.',
    description:
      'رویه‌ی تنفس‌پذیر و کفی نرم باعث شده Mira Street برای پیاده‌روی و استفاده‌ی روزانه گزینه‌ای خوش‌قیمت و دوست‌داشتنی باشد.',
    specs: [
      { label: 'جنس رویه', value: 'مش تنفس‌پذیر' },
      { label: 'کفی', value: 'فوم سبک' },
      { label: 'مناسب', value: 'روزمره و پیاده‌روی' },
    ],
    reviewHighlights: ['راحتی بالا', 'هماهنگ با استایل روزمره', 'کیفیت دوخت خوب'],
    flags: { featured: false, bestseller: true, newest: true },
  },
  {
    id: 108,
    title: 'کیف دستی Orio Luna',
    categoryId: 'fashion',
    brand: 'Orio',
    badge: 'نسخه محدود',
    price: 4290000,
    oldPrice: 4990000,
    rating: 4.8,
    reviewCount: 44,
    image: createArtwork('LUNA', ['#111827', '#374151']),
    gallery: [
      createArtwork('LUNA', ['#111827', '#374151']),
      createArtwork('DETAIL', ['#1f2937', '#4b5563']),
      createArtwork('CLASSIC', ['#030712', '#1f2937']),
    ],
    stock: 3,
    shortDescription: 'کیفی جمع‌وجور با متریال باکیفیت و طراحی کلاسیک.',
    description:
      'Orio Luna برای استایل‌های رسمی و نیمه‌رسمی طراحی شده و فضای کافی برای لوازم ضروری روزانه را در اختیارتان می‌گذارد.',
    specs: [
      { label: 'جنس', value: 'چرم مصنوعی درجه یک' },
      { label: 'ابعاد', value: '28 × 18 سانتی‌متر' },
      { label: 'بند', value: 'قابل تنظیم' },
    ],
    reviewHighlights: ['دوخت تمیز', 'رنگ‌بندی جذاب', 'ابعاد کاربردی'],
    flags: { featured: true, bestseller: false, newest: false },
  },
]

export const useProductsStore = defineStore('products', {
  state: () => ({
    categories,
    brands,
    products,
  }),

  getters: {
    featuredProducts: (state) => state.products.filter((product) => product.flags.featured),
    bestsellerProducts: (state) => state.products.filter((product) => product.flags.bestseller),
    newestProducts: (state) => state.products.filter((product) => product.flags.newest),
    availableProducts: (state) => state.products.filter((product) => product.stock > 0),
  },

  actions: {
    getById(id) {
      return this.products.find((product) => product.id === Number(id))
    },
    getCategoryById(id) {
      return this.categories.find((category) => category.id === id)
    },
    getByCategory(id) {
      return this.products.filter((product) => product.categoryId === id)
    },
    search(query) {
      const normalizedQuery = String(query || '')
        .trim()
        .toLowerCase()

      if (!normalizedQuery) {
        return this.products
      }

      return this.products.filter((product) => {
        const haystack = [
          product.title,
          product.brand,
          product.badge,
          product.shortDescription,
          product.description,
          this.getCategoryById(product.categoryId)?.title,
        ]
          .filter(Boolean)
          .join(' ')
          .toLowerCase()

        return haystack.includes(normalizedQuery)
      })
    },
    getRelatedProducts(productId) {
      const currentProduct = this.getById(productId)

      if (!currentProduct) {
        return []
      }

      return this.products
        .filter((product) => product.categoryId === currentProduct.categoryId && product.id !== currentProduct.id)
        .slice(0, 4)
    },
  },
})
