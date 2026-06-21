// src/utils/format.js
const priceFormatter = new Intl.NumberFormat('fa-IR')

export function formatPrice(value) {
  return `${priceFormatter.format(Math.round(value || 0))} تومان`
}

export function formatNumber(value) {
  return priceFormatter.format(Math.round(value || 0))
}

// تابع کمکی برای تبدیل به اعداد فارسی
export function toPersianDigits(value) {
  if (value === null || value === undefined) return ''
  const persianDigits = '۰۱۲۳۴۵۶۷۸۹'
  return String(value).replace(/[0-9]/g, (char) => persianDigits[char])
}

// تابع اصلی برای فرمت شماره تماس
export function formatPhone(value) {
  if (!value) return '-'

  let cleaned = String(value).replace(/\D/g, '')

  if (cleaned.length !== 11) {
    return toPersianDigits(cleaned)
  }

  // فرمت کردن به شکل 0913 238 7312
  const formatted = cleaned.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3')

  // اضافه کردن \u200E برای حفظ جهت چپ‌به‌راست در نمایش
  return '\u200E' + toPersianDigits(formatted)
}

export function formatDate(value) {
  if (!value) return '-'
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(value))
}

export function formatPrsianDate(dateString) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
