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
]

export function getWorkflowStep(stepKey) {
  return ADMIN_PRODUCT_WORKFLOW_STEPS.find((step) => step.key === stepKey) || null
}

export function getWorkflowStepIndex(stepKey) {
  return ADMIN_PRODUCT_WORKFLOW_STEPS.findIndex((step) => step.key === stepKey)
}

export function buildQueryString(params = {}) {
  const searchParams = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') {
      return
    }

    searchParams.set(key, String(value))
  })

  const query = searchParams.toString()
  return query ? `?${query}` : ''
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
