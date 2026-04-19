<template>
  <div class="admin-products">
    <section class="page-panel admin-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">افزودن محصول جدید</h2>
          <p class="section-subtitle">محصول تازه را به ویترین فروشگاه و پنل مدیریتی اضافه کنید</p>
        </div>
      </div>

      <form class="admin-form" @submit.prevent="submitProduct">
        <BaseInput v-model="form.title" label="عنوان محصول" placeholder="مثلاً ماوس ارگونومیک" />
        <BaseInput v-model="form.brand" label="برند" placeholder="نام برند" />
        <label class="admin-field">
          <span>دسته‌بندی</span>
          <select v-model="form.categoryId">
            <option v-for="category in products.categories" :key="category.id" :value="category.id">
              {{ category.title }}
            </option>
          </select>
        </label>
        <BaseInput v-model="form.price" label="قیمت" placeholder="مثلاً ۴۹۹۰۰۰۰" />
        <BaseInput v-model="form.oldPrice" label="قیمت قبل" placeholder="اختیاری" />
        <BaseInput v-model="form.stock" label="موجودی" placeholder="مثلاً ۱۲" />
        <BaseInput v-model="form.sku" label="SKU" placeholder="مثلاً SV-DG-210" />
        <BaseInput v-model="form.badge" label="برچسب ویترین" placeholder="مثلاً تازه رسید" />
        <BaseInput v-model="form.shortDescription" label="توضیح کوتاه" placeholder="خلاصه‌ای کوتاه برای کارت محصول" />
        <BaseInput v-model="form.description" label="توضیح کامل" placeholder="توضیح کامل برای صفحه محصول" />
        <label class="admin-check">
          <input v-model="form.featured" type="checkbox" />
          در بخش محصولات ویژه نمایش داده شود
        </label>
        <BaseButton block type="submit">افزودن محصول</BaseButton>
      </form>
    </section>

    <section class="page-panel admin-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">مدیریت موجودی و نمایش</h2>
          <p class="section-subtitle">فهرست زنده محصولات قابل ویرایش در همین صفحه</p>
        </div>
      </div>

      <div class="admin-table">
        <article v-for="product in products.products" :key="product.id" class="admin-row">
          <div>
            <strong>{{ product.title }}</strong>
            <p>{{ product.sku }} • {{ product.brand }}</p>
          </div>
          <span>{{ formatPrice(product.price) }}</span>
          <label class="admin-row__stock">
            <span>موجودی</span>
            <input :value="product.stock" type="number" min="0" @change="updateStock(product.id, $event)" />
          </label>
          <button type="button" class="admin-chip" @click="products.toggleFeatured(product.id)">
            {{ product.flags.featured ? 'ویژه' : 'عادی' }}
          </button>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useProductsStore } from '@/stores/products'
import { formatPrice } from '@/utils/format'

const products = useProductsStore()
const form = reactive({
  title: '',
  brand: '',
  categoryId: products.categories[0]?.id || 'digital',
  price: '',
  oldPrice: '',
  stock: '',
  sku: '',
  badge: 'جدید',
  shortDescription: '',
  description: '',
  featured: true,
})

function resetForm() {
  form.title = ''
  form.brand = ''
  form.categoryId = products.categories[0]?.id || 'digital'
  form.price = ''
  form.oldPrice = ''
  form.stock = ''
  form.sku = ''
  form.badge = 'جدید'
  form.shortDescription = ''
  form.description = ''
  form.featured = true
}

function submitProduct() {
  products.createProduct(form)
  resetForm()
}

function updateStock(id, event) {
  products.updateStock(id, event.target.value)
}
</script>

<style scoped>
.admin-products {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 1rem;
}

.admin-card {
  padding: 1.25rem;
}

.admin-form {
  display: grid;
  gap: 0.9rem;
}

.admin-field {
  display: grid;
  gap: 0.45rem;
}

.admin-field span,
.admin-check {
  font-weight: 700;
}

.admin-field select,
.admin-row__stock input {
  min-height: 48px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: var(--surface-strong);
  padding: 0 1rem;
}

.admin-check {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.admin-table {
  display: grid;
  gap: 0.8rem;
}

.admin-row {
  display: grid;
  grid-template-columns: 1.4fr 0.8fr 180px 90px;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  border-radius: 20px;
  background: var(--bg-muted);
}

.admin-row p {
  margin: 0.3rem 0 0;
  color: var(--text-muted);
}

.admin-row__stock {
  display: grid;
  gap: 0.35rem;
}

.admin-chip {
  min-height: 44px;
  border: 0;
  border-radius: 999px;
  background: rgba(91, 61, 245, 0.12);
  color: var(--primary);
  font-weight: 700;
}

@media (max-width: 1180px) {
  .admin-products {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-row {
    grid-template-columns: 1fr;
  }
}
</style>
