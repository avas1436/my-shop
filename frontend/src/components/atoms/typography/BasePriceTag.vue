<template>
  <div
    :class="[
      'base-price-tag',
      `base-price-tag-${size}`
    ]"
  >
    <!-- Main Price -->
    <div class="base-price-tag__main">
      <span class="base-price-tag__amount">{{ formattedPrice }}</span>
      <span v-if="showCurrency" class="base-price-tag__currency">
        {{ currencyLabel }}
      </span>
    </div>

    <!-- Original price (strikethrough) -->
    <div v-if="originalPrice && hasDiscount" class="base-price-tag__original">
      <span class="base-price-tag__original-amount">
        {{ formattedOriginalPrice }}
      </span>
      <span v-if="showCurrency" class="base-price-tag__currency">
        {{ currencyLabel }}
      </span>
    </div>

    <!-- Discount percent -->
    <span v-if="hasDiscount" class="base-price-tag__discount">
      {{ discountPercent }}٪ تخفیف
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  price: {
    type: [Number, String],
    required: true
  },
  originalPrice: {
    type: [Number, String],
    default: null
  },
  currency: {
    type: String,
    default: 'toman',
    validator: (value) => ['toman', 'rial'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  showCurrency: {
    type: Boolean,
    default: true
  }
})

// number formatting
const formatNumber = (num) => new Intl.NumberFormat('fa-IR').format(num)

const formattedPrice = computed(() => formatNumber(props.price))
const formattedOriginalPrice = computed(() => formatNumber(props.originalPrice))

const currencyLabel = computed(() => {
  if (!props.showCurrency) return ''
  return props.currency === 'toman' ? 'تومان' : 'ریال'
})

const hasDiscount = computed(() => {
  return props.originalPrice &&
    Number(props.originalPrice) > Number(props.price)
})

const discountPercent = computed(() => {
  if (!hasDiscount.value) return 0
  const discount =
    ((Number(props.originalPrice) - Number(props.price)) /
      Number(props.originalPrice)) *
    100
  return Math.round(discount)
})
</script>

<style scoped>
.base-price-tag {
  display: inline-flex;
  flex-direction: column;
  gap: 0.25rem;
  font-family: 'Vazirmatn', sans-serif;
}

/* Main Price */
.base-price-tag__main {
  display: flex;
  align-items: baseline;
  gap: 0.375rem;
  color: var(--color-text-primary, #1a1a1a);
}

.base-price-tag__amount {
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.base-price-tag__currency {
  font-weight: 500;
  color: var(--color-text-secondary, #6b7280);
}

/* Original Price */
.base-price-tag__original {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
  opacity: 0.6;
}

.base-price-tag__original-amount {
  text-decoration: line-through;
  font-weight: 500;
  color: var(--color-text-muted, #9ca3af);
  font-variant-numeric: tabular-nums;
}

/* Discount Badge */
.base-price-tag__discount {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  padding: 0.125rem 0.5rem;
  background-color: var(--color-error, #ef4444);
  color: white;
  border-radius: 0.25rem;
  font-weight: 600;
  font-size: 0.75rem;
}

/* Sizes */
.base-price-tag-sm .base-price-tag__amount {
  font-size: 0.875rem;
}

.base-price-tag-sm .base-price-tag__currency {
  font-size: 0.75rem;
}

.base-price-tag-sm .base-price-tag__original-amount {
  font-size: 0.75rem;
}

.base-price-tag-md .base-price-tag__amount {
  font-size: 1.125rem;
}

.base-price-tag-md .base-price-tag__currency {
  font-size: 0.875rem;
}

.base-price-tag-md .base-price-tag__original-amount {
  font-size: 0.875rem;
}

.base-price-tag-lg .base-price-tag__amount {
  font-size: 1.5rem;
}

.base-price-tag-lg .base-price-tag__currency {
  font-size: 1rem;
}

.base-price-tag-lg .base-price-tag__original-amount {
  font-size: 1rem;
}

.base-price-tag-xl .base-price-tag__amount {
  font-size: 2rem;
}

.base-price-tag-xl .base-price-tag__currency {
  font-size: 1.25rem;
}

.base-price-tag-xl .base-price-tag__original-amount {
  font-size: 1.125rem;
}
</style>
