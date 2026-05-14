<template>
  <div class="workflow-page">
    <header class="workflow-page__header">
      <div>
        <h2>مرحله ۲ - اطلاعات پایه</h2>
        <p>فیلدهای اصلی محصول را بعد از ساخت draft می‌توانی با route ویرایش محصول تکمیل یا اصلاح کنی.</p>
      </div>
      <div class="workflow-chip-row">
        <span class="workflow-chip workflow-chip--success">API: `PATCH /v1/products/admin/products/{id}`</span>
      </div>
    </header>

    <div v-if="!composer.draftProduct" class="workflow-empty">ابتدا draft محصول را بساز.</div>

    <form v-else class="workflow-form-grid" @submit.prevent="saveBasics">
      <label class="workflow-field workflow-field--full">
        <span>نام محصول</span>
        <input v-model.trim="form.name" class="workflow-field__control" required />
      </label>

      <label class="workflow-field workflow-field--full">
        <span>توضیحات</span>
        <textarea v-model.trim="form.description" class="workflow-textarea" />
      </label>

      <label class="workflow-field">
        <span>قیمت پایه</span>
        <input v-model="form.price" class="workflow-field__control" type="number" min="0" />
      </label>

      <label class="workflow-field">
        <span>قیمت تخفیف</span>
        <input v-model="form.discount_price" class="workflow-field__control" type="number" min="0" />
      </label>

      <label class="workflow-field">
        <span>قیمت تمام‌شده</span>
        <input v-model="form.cost_price" class="workflow-field__control" type="number" min="0" />
      </label>

      <label class="workflow-field">
        <span>نرخ مالیات</span>
        <input v-model="form.tax_rate" class="workflow-field__control" type="number" min="0" max="10000" />
      </label>

      <label class="workflow-field">
        <span>کد ارز</span>
        <input v-model.trim="form.currency_code" class="workflow-field__control" maxlength="3" />
      </label>

      <label class="workflow-field">
        <span>GTIN</span>
        <input v-model.trim="form.gtin" class="workflow-field__control" maxlength="20" />
      </label>

      <label class="workflow-field">
        <span>وزن</span>
        <input v-model="form.weight" class="workflow-field__control" type="number" min="0" step="0.001" />
      </label>

      <label class="workflow-field">
        <span>عرض</span>
        <input v-model="form.width" class="workflow-field__control" type="number" min="0" step="0.01" />
      </label>

      <label class="workflow-field">
        <span>ارتفاع</span>
        <input v-model="form.height" class="workflow-field__control" type="number" min="0" step="0.01" />
      </label>

      <label class="workflow-field">
        <span>عمق</span>
        <input v-model="form.depth" class="workflow-field__control" type="number" min="0" step="0.01" />
      </label>

      <label class="workflow-field workflow-field--full">
        <span>Meta title</span>
        <input v-model.trim="form.meta_title" class="workflow-field__control" maxlength="255" />
      </label>

      <label class="workflow-field workflow-field--full">
        <span>Meta description</span>
        <textarea v-model.trim="form.meta_description" class="workflow-textarea" maxlength="500" />
      </label>

      <div class="workflow-inline workflow-field--full">
        <div class="workflow-toggle">
          <span>محصول شاخص</span>
          <label>
            <input v-model="form.is_featured" type="checkbox" />
            <span>در vitrine نمایش داده شود</span>
          </label>
        </div>

        <div class="workflow-toggle">
          <span>محصول دیجیتال</span>
          <label>
            <input v-model="form.is_digital" type="checkbox" />
            <span>فایل/دانلودی است</span>
          </label>
        </div>
      </div>

      <div class="workflow-actions workflow-field--full">
        <BaseButton type="button" variant="ghost" @click="goToDraft">بازگشت به draft</BaseButton>
        <BaseButton type="submit" :disabled="composer.loading.updateProduct">ذخیره اطلاعات پایه</BaseButton>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'
import { useAdminProductComposerStore } from '@/stores/adminProductComposerStore'
import { toOptionalFloat, toOptionalInteger, toRequiredInteger } from '@/utils/adminProductWorkflowUtils'

const router = useRouter()
const composer = useAdminProductComposerStore()

const form = reactive({
  name: '',
  description: '',
  price: '',
  discount_price: '',
  cost_price: '',
  tax_rate: '0',
  currency_code: 'IRR',
  is_featured: false,
  is_digital: false,
  weight: '',
  width: '',
  height: '',
  depth: '',
  meta_title: '',
  meta_description: '',
  gtin: '',
})

function toPositiveOptionalFloat(value) {
  const parsed = toOptionalFloat(value)
  return parsed && parsed > 0 ? parsed : null
}

watch(
  () => composer.draftProduct,
  (product) => {
    if (!product) {
      return
    }

    form.name = product.name || ''
    form.description = product.description || ''
    form.price = String(product.price ?? '')
    form.discount_price = product.discount_price ?? ''
    form.cost_price = product.cost_price ?? ''
    form.tax_rate = String(product.tax_rate ?? 0)
    form.currency_code = product.currency_code || 'IRR'
    form.is_featured = Boolean(product.is_featured)
    form.is_digital = Boolean(product.is_digital)
    form.weight = product.weight ?? ''
    form.width = product.width ?? ''
    form.height = product.height ?? ''
    form.depth = product.depth ?? ''
    form.meta_title = product.meta_title || ''
    form.meta_description = product.meta_description || ''
    form.gtin = product.gtin || ''
  },
  { immediate: true },
)

async function saveBasics() {
  try {
    await composer.updateProduct({
      name: form.name,
      description: form.description || null,
      price: toRequiredInteger(form.price, 0),
      discount_price: toOptionalInteger(form.discount_price),
      cost_price: toOptionalInteger(form.cost_price),
      tax_rate: toRequiredInteger(form.tax_rate, 0),
      currency_code: (form.currency_code || 'IRR').toUpperCase(),
      is_featured: Boolean(form.is_featured),
      is_digital: Boolean(form.is_digital),
      weight: toPositiveOptionalFloat(form.weight),
      width: toPositiveOptionalFloat(form.width),
      height: toPositiveOptionalFloat(form.height),
      depth: toPositiveOptionalFloat(form.depth),
      meta_title: form.meta_title || null,
      meta_description: form.meta_description || null,
      gtin: form.gtin || null,
    })
  } catch {
    // Feedback is handled in the store.
  }
}

function goToDraft() {
  router.push({ name: 'admin-product-draft' })
}
</script>
