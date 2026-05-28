// src/utils/format.js
const priceFormatter = new Intl.NumberFormat('fa-IR')

export function formatPrice(value) {
  return `${priceFormatter.format(Math.round(value || 0))} تومان`
}

export function formatNumber(value) {
  return priceFormatter.format(Math.round(value || 0))
}

export function normalizeDigits(value) {
  if (!value) return ''
  return String(value)
    .replace(/[۰-۹]/g, (d) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(d)))
    .replace(/\D/g, '')
}

export function formatPhone(value) {
  if (!value) return '-'
  const digits = normalizeDigits(value)
  return digits.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3')
}

export function formatDate(value) {
  if (!value) return '-'
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(value))
}
