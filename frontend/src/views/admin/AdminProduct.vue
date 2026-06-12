<!-- src/views/admin/AdminProductsView.vue -->
<template>
  <div class="admin-products">
    <section class="page-panel admin-card collapsible-section" :class="{ 'is-open': isFormOpen }">
      <div class="section-head clickable-head" @click="toggleForm">
        <div>
          <h2 class="section-title">
            <span>افزودن محصول جدید (پیش‌نویس)</span>
            <span class="badge-status">{{ isFormOpen ? 'بستن فرم' : 'باز کردن فرم' }}</span>
          </h2>
          <p class="section-subtitle">مشخصات اولیه محصول را برای ایجاد پیش‌نویس وارد کنید</p>
        </div>
        <span class="toggle-icon">▼</span>
      </div>

      <div class="collapsible-body">
        <form class="admin-form" @submit.prevent="handleSubmit">
          <div class="form-grid">
            <div class="form-group">
              <BaseInput
                v-model="form.name"
                label="نام محصول"
                placeholder="مثلاً ماوس ارگونومیک"
                required
                :class="{ 'has-error': fieldErrors.name }"
              />
              <span v-if="fieldErrors.name" class="error-text field-error">
                {{ fieldErrors.name[0] }}
              </span>
            </div>

            <div class="form-group">
              <label class="admin-field">
                <span>برند</span>
                <select v-model.number="form.brand_id" required>
                  <option disabled value="">انتخاب برند</option>
                  <option v-for="brand in products.brands" :key="brand.id" :value="brand.id">
                    {{ brand.name }}
                  </option>
                </select>
              </label>
              <span v-if="fieldErrors.brand_id" class="error-text field-error">
                {{ fieldErrors.brand_id[0] }}
              </span>
            </div>

            <div class="form-group">
              <BaseInput
                v-model.number="form.price"
                type="number"
                min="1"
                label="قیمت (ریال/تومان)"
                placeholder="مثلاً ۴۹۹۰۰۰۰"
                required
                :class="{ 'has-error': fieldErrors.price }"
              />
              <span v-if="fieldErrors.price" class="error-text field-error">
                {{ fieldErrors.price[0] }}
              </span>
            </div>

            <div class="form-group">
              <BaseInput
                v-model.number="form.discount_price"
                type="number"
                min="0"
                label="قیمت با تخفیف"
                placeholder="اختیاری (در صورت عدم تخفیف 0)"
              />
            </div>

            <div class="form-group">
              <BaseInput
                v-model.number="form.cost_price"
                type="number"
                min="0"
                label="قیمت خرید (هزینه تمام شده)"
                placeholder="مثلاً ۳۵۰۰۰۰۰"
              />
            </div>

            <div class="form-group">
              <BaseInput
                v-model.number="form.tax_rate"
                type="number"
                min="0"
                max="100"
                label="نرخ مالیات"
                placeholder="995 = 9.5%"
              />
            </div>

            <div class="form-group">
              <BaseInput
                v-model.number="form.weight"
                type="number"
                min="0"
                label="وزن (گرم)"
                placeholder="مثلاً 150"
              />
            </div>

            <div class="form-group">
              <BaseInput
                v-model="form.gtin"
                label="کد GTIN / بارکد"
                placeholder="مثلاً 626054541212"
              />
            </div>

            <div class="form-group">
              <BaseInput
                v-model="form.meta_title"
                label="عنوان مِتا (SEO)"
                placeholder="عنوان برای موتورهای جستجو"
              />
            </div>

            <div class="form-group">
              <BaseInput
                v-model="form.meta_description"
                label="توضیحات مِتا (SEO)"
                placeholder="توضیحات خلاصه برای گوگل"
              />
            </div>

            <div class="form-group full-width">
              <BaseInput
                v-model="form.description"
                label="توضیحات کامل"
                placeholder="توضیحات اولیه پیش‌نویس محصول..."
              />
            </div>
          </div>

          <div class="form-footer">
            <label class="admin-check">
              <input v-model="form.is_digital" type="checkbox" />
              این محصول دانلودی / دیجیتال است
            </label>

            <p v-if="errorMessage" class="error-text global-error">{{ errorMessage }}</p>

            <BaseButton block type="submit" :disabled="isLoading">
              {{ isLoading ? 'در حال ایجاد پیش‌نویس...' : 'افزودن و تکمیل محصول' }}
            </BaseButton>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { ROUTES } from '@/router/routeNames'
import { productService } from '@/services/productService'
import { useProductsStore } from '@/stores/products'
import { getErrorMessage } from '@/utils/errorMessages'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const products = useProductsStore()

// وضعیت باز یا بسته بودن فرم ایجاد پیش‌نویس
const isFormOpen = ref(false)

const isLoading = ref(false)
const errorMessage = ref('')
const fieldErrors = ref({})

const form = reactive({
  name: '',
  description: '',
  price: 1,
  discount_price: 0,
  cost_price: 0,
  tax_rate: 0,
  is_digital: false,
  weight: 0,
  meta_title: '',
  meta_description: '',
  gtin: '',
  brand_id: '',
})

// onMounted(async () => {
//   try {
//     if (products.fetchAdminInitialData) {
//       await products.fetchAdminInitialData()
//     }
//   } catch (error) {
//     errorMessage.value = 'خطا در دریافت اطلاعات اولیه از سرور'
//   }
// })

function toggleForm() {
  isFormOpen.value = !isFormOpen.value
}

function resetForm() {
  form.name = ''
  form.description = ''
  form.price = 1
  form.discount_price = 0
  form.cost_price = 0
  form.tax_rate = 0
  form.is_digital = false
  form.weight = 0
  form.meta_title = ''
  form.meta_description = ''
  form.gtin = ''
  form.brand_id = ''
}

async function handleSubmit() {
  errorMessage.value = ''
  fieldErrors.value = {}
  isLoading.value = true

  try {
    const response = await productService.createDraft({ ...form })
    resetForm()

    if (response?.id || response?.data?.id) {
      const targetId = response.id || response.data.id

      // ریدایرکت زنده به صفحه ویرایش ویترینی کالا
      router.push({
        name: ROUTES.ADMIN_PRODUCT_DETAIL,
        params: { product_id: targetId },
      })
    }
  } catch (error) {
    if (error.response?.data?.errors) {
      fieldErrors.value = error.response.data.errors
    } else {
      errorMessage.value = getErrorMessage(error.code || error.message)
    }
  } finally {
    isLoading.value = false
  }
}

// async function handleSoftDelete(id) {
//   if (!confirm('آیا از انتقال این محصول به زباله‌دان مطمئن هستید؟')) return

//   try {
//     await productService.softDelete(id)
//     if (products.removeProductFromStore) {
//       products.removeProductFromStore(id)
//     }
//   } catch (error) {
//     alert('خطا در حذف محصول')
//   }
// }

// function goToDetail(id) {
//   router.push({
//     name: ROUTES.ADMIN_PRODUCT_DETAIL,
//     params: { product_id: id },
//   })
// }
</script>

<style scoped>
/* کانتینر اصلی صفحه: حالا به شکل تک ستونی و تمام عرض چیده می‌شود */
.admin-products {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
  max-width: 100%;
}

.admin-card {
  padding: 1.5rem;
  background: var(--surface, #fff);
  border-radius: 16px;
  border: 1px solid var(--border, #e2e8f0);
}

/* استایل‌های بخش تاشو */
.collapsible-section {
  transition: all 0.3s ease-in-out;
}

.clickable-head {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  user-select: none;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.badge-status {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  background: var(--bg-muted, #f1f5f9);
  color: var(--primary, #5b3df5);
  border-radius: 20px;
  font-weight: 500;
}

.toggle-icon {
  font-size: 0.85rem;
  color: var(--text-muted);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* مدیریت انیمیشن بدنه فرم بر اساس وضعیت کامپوننت */
.collapsible-body {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.collapsible-section.is-open .collapsible-body {
  grid-template-rows: 1fr;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px dashed var(--border, #e2e8f0);
}

.admin-form {
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ساختار گرید هوشمند برای باز شدن عریض فرم در دسکتاپ */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.full-width {
  grid-column: 1 / -1;
}

.admin-field {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.admin-field span,
.admin-check {
  font-weight: 700;
  font-size: 0.9rem;
}

.admin-field select,
.admin-row__stock input {
  min-height: 48px;
  border-radius: 12px;
  border: 1px solid var(--border, #e2e8f0);
  background: var(--surface-strong, #f8fafc);
  padding: 0 1rem;
  width: 100%;
}

.form-footer {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border, #e2e8f0);
}

.admin-check {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.error-text {
  color: #ef4444;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.has-error :deep(input) {
  border-color: #ef4444 !important;
}

/* استایل‌های لیست محصولات پایین صفحه */
.admin-table {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-top: 1rem;
}

.admin-row {
  display: grid;
  grid-template-columns: 2fr 1fr 150px 200px;
  gap: 1rem;
  align-items: center;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  background: var(--bg-muted, #f8fafc);
  border: 1px solid var(--border, #e2e8f0);
}

.admin-row p {
  margin: 0.3rem 0 0;
  color: var(--text-muted, #64748b);
  font-size: 0.85rem;
}

.price-tag {
  font-weight: 600;
}

.admin-row__stock {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.85rem;
}

.admin-row__stock input {
  min-height: 38px;
  border-radius: 8px;
  text-align: center;
}

.admin-actions {
  display: flex;
  gap: 0.5rem;
}

.admin-chip {
  flex: 1;
  min-height: 40px;
  border: 0;
  border-radius: 8px;
  background: rgba(91, 61, 245, 0.08);
  color: var(--primary, #5b3df5);
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}

.admin-chip:hover {
  background: rgba(91, 61, 245, 0.15);
}

.btn-delete-soft {
  padding: 0 1rem;
  min-height: 40px;
  border: 0;
  border-radius: 8px;
  background: rgba(239, 68, 68, 0.08);
  color: #ef4444;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-delete-soft:hover {
  background: rgba(239, 68, 68, 0.15);
}

/* انیمیشن چرخش آیکون فلش هنگام باز شدن */
.collapsible-section.is-open .toggle-icon {
  transform: rotate(180deg);
}

/* واکنش‌گرایی برای مانیتورهای کوچک و موبایل */
@media (max-width: 1024px) {
  .admin-row {
    grid-template-columns: 1.5fr 1fr 120px 180px;
  }
}

@media (max-width: 768px) {
  .admin-row {
    grid-template-columns: 1fr;
    gap: 0.8rem;
  }
  .admin-actions {
    margin-top: 0.5rem;
  }
}
</style>
