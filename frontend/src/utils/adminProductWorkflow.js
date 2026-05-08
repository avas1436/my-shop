export const ADMIN_PRODUCT_WORKFLOW_STORAGE_KEY = 'shop_admin_product_workflow_draft_id'

export const ADMIN_PRODUCT_WORKFLOW_STEPS = [
  {
    key: 'draft',
    label: 'ساخت draft',
    description: 'هویت اولیه محصول را ثبت کن.',
    routeName: 'admin-product-draft',
  },
  {
    key: 'basics',
    label: 'اطلاعات پایه',
    description: 'نام، قیمت، سئو و وضعیت‌های پایه را کامل کن.',
    routeName: 'admin-product-basics',
    requiresDraft: true,
  },
  {
    key: 'organization',
    label: 'برند و دسته‌بندی',
    description: 'برند، تگ‌ها و دسته‌ها را متصل کن.',
    routeName: 'admin-product-organization',
    requiresDraft: true,
  },
  {
    key: 'attributes',
    label: 'اتریبیوت‌ها',
    description: 'ویژگی‌های محصول را ثبت کن.',
    routeName: 'admin-product-attributes',
    requiresDraft: true,
  },
  {
    key: 'variants',
    label: 'واریانت و موجودی',
    description: 'واریانت‌ها، انبار و attributeهای وابسته را اضافه کن.',
    routeName: 'admin-product-variants',
    requiresDraft: true,
  },
  {
    key: 'media',
    label: 'رسانه',
    description: 'تصاویر محصول را مدیریت کن.',
    routeName: 'admin-product-media',
    requiresDraft: true,
  },
  {
    key: 'review',
    label: 'بازبینی و انتشار',
    description: 'وضعیت نهایی را چک کن و محصول را publish کن.',
    routeName: 'admin-product-review',
    requiresDraft: true,
  },
]

export function getWorkflowStep(stepKey) {
  return ADMIN_PRODUCT_WORKFLOW_STEPS.find((step) => step.key === stepKey) || null
}

export function getWorkflowStepIndex(stepKey) {
  return ADMIN_PRODUCT_WORKFLOW_STEPS.findIndex((step) => step.key === stepKey)
}

export function toOptionalInteger(value) {
  if (value === '' || value === null || value === undefined) {
    return null
  }

  const parsed = Number.parseInt(value, 10)
  return Number.isNaN(parsed) ? null : parsed
}

export function toRequiredInteger(value, fallback = 0) {
  const parsed = Number.parseInt(value, 10)
  return Number.isNaN(parsed) ? fallback : parsed
}

export function toOptionalFloat(value) {
  if (value === '' || value === null || value === undefined) {
    return null
  }

  const parsed = Number.parseFloat(value)
  return Number.isNaN(parsed) ? null : parsed
}

export function formatCurrency(value) {
  return new Intl.NumberFormat('fa-IR').format(Number(value || 0))
}

export function rememberDraftProductId(productId) {
  if (typeof window === 'undefined') {
    return
  }

  if (productId) {
    window.sessionStorage.setItem(ADMIN_PRODUCT_WORKFLOW_STORAGE_KEY, String(productId))
    return
  }

  window.sessionStorage.removeItem(ADMIN_PRODUCT_WORKFLOW_STORAGE_KEY)
}

export function getRememberedDraftProductId() {
  if (typeof window === 'undefined') {
    return null
  }

  return toOptionalInteger(window.sessionStorage.getItem(ADMIN_PRODUCT_WORKFLOW_STORAGE_KEY))
}
