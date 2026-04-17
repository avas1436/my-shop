<template>
  <div class="page-shell">
    <section class="page-panel page-hero">
      <span class="pill">تکمیل سفارش</span>
      <h1 class="page-title">فرایند خرید در سه مرحله ساده</h1>
      <p class="page-description">
        اطلاعات ارسال، روش تحویل و پرداخت را انتخاب کنید تا سفارش شما آماده ثبت شود.
      </p>
    </section>

    <section v-if="cart.items.length" class="checkout-layout">
      <div class="page-panel checkout-main">
        <div class="checkout-steps">
          <button
            v-for="item in steps"
            :key="item.id"
            type="button"
            class="checkout-step"
            :class="{ 'checkout-step--active': step === item.id, 'checkout-step--done': step > item.id }"
            @click="step = item.id"
          >
            <span>{{ item.id }}</span>
            {{ item.label }}
          </button>
        </div>

        <div v-if="step === 1" class="checkout-panel">
          <BaseInput v-model="form.name" label="نام گیرنده" placeholder="مثلاً آوا رضایی" />
          <BaseInput v-model="form.phone" label="شماره تماس" placeholder="۰۹۱۲..." />
          <BaseInput v-model="form.address" label="آدرس کامل" placeholder="شهر، خیابان، پلاک..." />
          <BaseButton block @click="step = 2">ادامه به روش ارسال</BaseButton>
        </div>

        <div v-else-if="step === 2" class="checkout-panel">
          <label v-for="option in shippingOptions" :key="option.id" class="checkout-option">
            <input v-model="shippingMethod" type="radio" :value="option.id" />
            <div>
              <strong>{{ option.title }}</strong>
              <p>{{ option.description }}</p>
            </div>
            <span>{{ option.price }}</span>
          </label>
          <BaseButton block @click="step = 3">ادامه به پرداخت</BaseButton>
        </div>

        <div v-else class="checkout-panel">
          <label v-for="option in paymentOptions" :key="option.id" class="checkout-option">
            <input v-model="paymentMethod" type="radio" :value="option.id" />
            <div>
              <strong>{{ option.title }}</strong>
              <p>{{ option.description }}</p>
            </div>
          </label>
          <BaseButton block @click="completeOrder">ثبت نهایی سفارش</BaseButton>
        </div>
      </div>

      <aside class="page-panel checkout-summary">
        <h2>خلاصه سفارش</h2>
        <div class="checkout-summary__row">
          <span>جمع کالاها</span>
          <strong>{{ formatPrice(cart.subtotal) }}</strong>
        </div>
        <div class="checkout-summary__row">
          <span>ارسال</span>
          <strong>{{ cart.shipping ? formatPrice(cart.shipping) : 'رایگان' }}</strong>
        </div>
        <div class="checkout-summary__row checkout-summary__row--total">
          <span>قابل پرداخت</span>
          <strong>{{ formatPrice(cart.total) }}</strong>
        </div>

        <ul class="checkout-summary__items">
          <li v-for="item in cart.items" :key="item.id">
            <span>{{ item.title }} × {{ item.qty }}</span>
            <strong>{{ formatPrice(item.price * item.qty) }}</strong>
          </li>
        </ul>
      </aside>
    </section>

    <section v-else class="empty-state">
      برای تکمیل خرید، ابتدا محصولی به سبد خرید اضافه کنید.
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useCartStore } from '@/stores/cartStore'
import { formatPrice } from '@/utils/format'

const step = ref(1)
const cart = useCartStore()

const steps = [
  { id: 1, label: 'اطلاعات گیرنده' },
  { id: 2, label: 'ارسال' },
  { id: 3, label: 'پرداخت' },
]

const shippingOptions = [
  { id: 'express', title: 'ارسال اکسپرس', description: 'تحویل ۲۴ تا ۴۸ ساعته در شهرهای اصلی', price: 'رایگان' },
  { id: 'post', title: 'پست پیشتاز', description: 'مناسب شهرهای دیگر با هزینه اقتصادی', price: '۸۹٬۰۰۰ تومان' },
]

const paymentOptions = [
  { id: 'online', title: 'پرداخت اینترنتی', description: 'پرداخت امن با درگاه بانکی' },
  { id: 'wallet', title: 'کیف پول و کارت هدیه', description: 'استفاده از اعتبار و کدهای تخفیف' },
]

const form = ref({
  name: '',
  phone: '',
  address: '',
})

const shippingMethod = ref('express')
const paymentMethod = ref('online')

function completeOrder() {
  cart.clear()
  step.value = 1
}
</script>

<style scoped>
.checkout-layout {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 1.25rem;
}

.checkout-main,
.checkout-summary {
  padding: 1.25rem;
}

.checkout-steps {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.8rem;
  margin-bottom: 1rem;
}

.checkout-step {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.55rem;
  min-height: 52px;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: var(--surface-strong);
  color: var(--text-muted);
  font-weight: 700;
}

.checkout-step span {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--bg-muted);
}

.checkout-step--active,
.checkout-step--done {
  color: var(--primary);
  border-color: rgba(91, 61, 245, 0.18);
  background: rgba(91, 61, 245, 0.08);
}

.checkout-panel {
  display: grid;
  gap: 1rem;
}

.checkout-option {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.9rem;
  align-items: center;
  padding: 1rem;
  border-radius: 18px;
  background: var(--bg-muted);
}

.checkout-option p,
.checkout-summary__items {
  margin: 0;
}

.checkout-summary {
  display: grid;
  gap: 1rem;
  align-content: start;
  position: sticky;
  top: 132px;
  height: fit-content;
}

.checkout-summary h2 {
  margin: 0;
}

.checkout-summary__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.checkout-summary__row--total {
  padding-top: 0.8rem;
  border-top: 1px solid var(--border);
}

.checkout-summary__items {
  padding: 0;
  list-style: none;
  display: grid;
  gap: 0.75rem;
}

.checkout-summary__items li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  color: var(--text-muted);
}

@media (max-width: 920px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }

  .checkout-summary {
    position: static;
  }
}

@media (max-width: 640px) {
  .checkout-steps {
    grid-template-columns: 1fr;
  }

  .checkout-option {
    grid-template-columns: 1fr;
  }
}
</style>
