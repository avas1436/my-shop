const priceFormatter = new Intl.NumberFormat('fa-IR')

export function formatPrice(value) {
  return `${priceFormatter.format(Math.round(value || 0))} تومان`
}

export function formatNumber(value) {
  return priceFormatter.format(Math.round(value || 0))
}
