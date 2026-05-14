<template>
  <div class="workflow-page">
    <header class="workflow-page__header">
      <div>
        <h2>مرحله ۱ - ساخت draft اولیه</h2>
        <p>در این صفحه فقط اسکلت اولیه محصول ساخته می‌شود تا بقیه مراحل روی همان شناسه ادامه پیدا کنند.</p>
      </div>
      <div class="workflow-chip-row">
        <span class="workflow-chip workflow-chip--success">API: `POST /v1/products/admin/createdraft`</span>
      </div>
    </header>

    <div class="workflow-alert">
      <strong>شروع مسیر</strong>
      <p>
        پس از ساخت draft، به صورت خودکار وارد صفحه اطلاعات پایه می‌شوی و از آنجا می‌توانی برند،
        دسته‌بندی، اتریبیوت، واریانت و تصاویر را جداگانه تکمیل کنی.
      </p>
    </div>

    <form class="workflow-form-grid" @submit.prevent="submitDraft">
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
        <input v-model="form.price" class="workflow-field__control" type="number" min="1" required />
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
        <span>وزن</span>
        <input v-model="form.weight" class="workflow-field__control" type="number" min="0" step="0.001" />
      </label>

      <label class="workflow-field">
        <span>GTIN</span>
        <input v-model.trim="form.gtin" class="workflow-field__control" maxlength="20" />
      </label>

      <label class="workflow-field workflow-field--full">
        <span>Meta title</span>
        <input v-model.trim="form.meta_title" class="workflow-field__control" maxlength="255" />
      </label>

      <label class="workflow-field workflow-field--full">
        <span>Meta description</span>
        <textarea v-model.trim="form.meta_description" class="workflow-textarea" maxlength="500" />
      </label>

      <div class="workflow-toggle workflow-field--full">
        <span>نوع محصول</span>
        <label>
          <input v-model="form.is_digital" type="checkbox" />
          <span>محصول دیجیتال است</span>
        </label>
      </div>

      <div class="workflow-actions workflow-field--full">
        <BaseButton type="submit" size="lg" :disabled="composer.loading.draft || !canSubmit">
          {{ composer.loading.draft ? 'در حال ساخت draft...' : 'ایجاد draft و رفتن به مرحله بعد' }}
        </BaseButton>
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue'
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
  is_digital: false,
  weight: '',
  meta_title: '',
  meta_description: '',
  gtin: '',
})

const canSubmit = computed(() => form.name && toRequiredInteger(form.price, 0) > 0)

async function submitDraft() {
  try {
    const product = await composer.createDraft({
      name: form.name,
      description: form.description,
      price: toRequiredInteger(form.price, 0),
      discount_price: toOptionalInteger(form.discount_price),
      cost_price: toOptionalInteger(form.cost_price),
      tax_rate: toRequiredInteger(form.tax_rate, 0),
      is_digital: Boolean(form.is_digital),
      weight: toOptionalFloat(form.weight),
      meta_title: form.meta_title || null,
      meta_description: form.meta_description || null,
      gtin: form.gtin || null,
    })

    await router.push({
      name: 'admin-product-basics',
      params: { productId: String(product.id) },
    })
  } catch {
    // Feedback is handled in the store.
  }
}
</script>
