<!-- src/views/admin/product-tabs/InventoryTab.vue -->
<template>
  <div class="tab-content page-panel form-container" dir="rtl">
    <div class="header-section flex-between">
      <h2 class="tab-title">
        <Layers class="icon-md" />
        مدیریت موجودی و تنوع‌ها
      </h2>

      <div
        class="stock-status-badge"
        :class="product.is_in_stock ? 'status-in-stock' : 'status-out-of-stock'"
      >
        <PackageCheck v-if="product.is_in_stock" class="icon-sm" />
        <PackageX v-else class="icon-sm" />
        موجودی کل انبار: {{ product.total_available_quantity || 0 }} عدد ({{
          product.is_in_stock ? 'موجود در انبار' : 'ناموجود'
        }})
      </div>
    </div>

    <div class="form-section card">
      <h3 class="specs-heading">
        <Package class="icon-sm" />
        موجودی‌های ثبت شده در انبار
      </h3>

      <template v-if="product.inventory?.length">
        <div
          v-for="item in product.inventory"
          :key="item.id"
          class="variant-row-card"
          :class="{
            'row-inactive': item.is_active === false,
            'row-low-stock': item.is_active !== false && item.quantity <= item.low_stock_alert,
            'row-backorder':
              item.is_active !== false &&
              item.allow_backorder &&
              item.quantity > item.low_stock_alert,
          }"
        >
          <div class="variant-top-bar">
            <div class="variant-info">
              <div class="attributes-group">
                <div class="attributes-wrapper">
                  <span v-for="attr in item.attributes" :key="attr.attribute_id" class="attr-badge">
                    {{ attr.name }}: <strong>{{ attr.value }}</strong>
                  </span>
                </div>
                <div
                  v-if="item.is_active !== false && item.quantity <= item.low_stock_alert"
                  class="low-stock-warning"
                >
                  <AlertTriangle class="icon-xs" />
                  توجه: موجودی به محدوده خطر رسیده است!
                </div>
              </div>
            </div>

            <div class="toggle-wrapper">
              <label class="modern-toggle">
                <input
                  type="checkbox"
                  :checked="item.allow_backorder"
                  @change="
                    handleUpdateInventory(item.id, { allow_backorder: !item.allow_backorder })
                  "
                  :disabled="!item.is_active || isSubmittingInventory"
                />
                <span class="toggle-slider"></span>
              </label>
              <span class="toggle-label-text">فروش بیش از موجودی</span>
            </div>
          </div>
          <div class="variant-inputs-grid">
            <div class="input-group sku-group">
              <label><Tag class="icon-xs text-muted" /> کد کالا (SKU):</label>
              <div class="single-input-wrapper">
                <input
                  v-model="item.sku"
                  type="text"
                  placeholder="ثبت نشده"
                  class="modern-input"
                  @change="handleUpdateVariant(item.variant_id, { sku: item.sku })"
                  :disabled="!item.is_active || isSubmittingInventory"
                />
              </div>
            </div>

            <div class="input-group">
              <label><Banknote class="icon-xs text-muted" /> قیمت واریانت (ریال):</label>
              <div class="single-input-wrapper">
                <input
                  v-model.number="item.price"
                  type="number"
                  min="0"
                  class="modern-input"
                  @change="handleUpdateVariant(item.variant_id, { price: item.price })"
                  :disabled="!item.is_active || isSubmittingInventory"
                />
              </div>
            </div>

            <div class="input-group text-center-input">
              <label><Box class="icon-xs text-muted" /> موجودی:</label>
              <div class="single-input-wrapper">
                <input
                  v-model.number="item.quantity"
                  type="number"
                  min="0"
                  class="modern-input"
                  :class="{
                    'input-error':
                      item.is_active !== false && item.quantity <= item.low_stock_alert,
                  }"
                  @change="handleUpdateInventory(item.id, { quantity: item.quantity })"
                  :disabled="!item.is_active || isSubmittingInventory"
                />
              </div>
            </div>

            <div class="input-group text-center-input">
              <label><Activity class="icon-xs text-muted" /> کف موجودی:</label>
              <div class="single-input-wrapper">
                <input
                  v-model.number="item.low_stock_alert"
                  type="number"
                  min="0"
                  class="modern-input"
                  @change="
                    handleUpdateInventory(item.id, { low_stock_alert: item.low_stock_alert })
                  "
                  :disabled="!item.is_active || isSubmittingInventory"
                />
              </div>
            </div>

            <div class="input-group readonly-group">
              <label>
                <Calculator class="icon-xs text-muted" />
                قیمت نهایی:
              </label>

              <div class="final-price-display">
                <span class="price-value">
                  {{ Number(item.final_price || product.final_price).toLocaleString('fa-IR') }}
                </span>

                <span class="price-unit">ریال</span>
              </div>
            </div>

            <div class="input-group action-buttons-wrapper full-span">
              <label class="invisible-label">عملیات</label>
              <div class="action-buttons">
                <button
                  :class="
                    item.is_active !== false
                      ? 'btn-icon btn-icon-warning'
                      : 'btn-icon btn-icon-success'
                  "
                  @click="handleUpdateVariant(item.variant_id, { is_active: !item.is_active })"
                  :title="item.is_active ? 'غیرفعال کردن موجودی' : 'فعال کردن موجودی'"
                  :disabled="isSubmittingInventory"
                >
                  <PowerOff v-if="item.is_active !== false" class="icon-sm" />
                  <Power v-else class="icon-sm" />
                </button>
                <button
                  class="btn-icon btn-icon-danger"
                  @click="handleDeleteInventory(item.id)"
                  title="حذف این رکورد موجودی"
                  :disabled="isSubmittingInventory"
                >
                  <Trash2 class="icon-sm" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </template>

      <div v-else class="empty-state">
        <Box class="icon-xl text-muted mb-3 opacity-50" />
        <p class="empty-text">هیچ رکورد موجودی برای این محصول ثبت نشده است.</p>
      </div>
    </div>

    <div class="form-section card bg-slate-50">
      <h4 class="specs-heading">
        <PlusCircle class="icon-sm" />
        ثبت رکورد موجودی جدید
      </h4>
      <div class="form-grid align-center mt-3">
        <div class="form-group">
          <label>رنگ:</label>
          <div class="single-input-wrapper">
            <input
              v-model="newVariant.color"
              type="text"
              placeholder="مثلاً: مشکی"
              class="modern-input"
              :disabled="isSubmittingInventory"
            />
          </div>
        </div>
        <div class="form-group">
          <label>سایز:</label>
          <div class="single-input-wrapper">
            <input
              v-model="newVariant.size"
              type="text"
              placeholder="مثلاً: XL"
              class="modern-input"
              :disabled="isSubmittingInventory"
            />
          </div>
        </div>
        <div class="form-group">
          <label>جنس:</label>
          <div class="single-input-wrapper">
            <input
              v-model="newVariant.material"
              type="text"
              placeholder="مثلاً: چرم"
              class="modern-input"
              :disabled="isSubmittingInventory"
            />
          </div>
        </div>

        <div class="form-group">
          <label>تعداد موجودی:</label>
          <div class="single-input-wrapper">
            <input
              v-model.number="newVariant.quantity"
              type="number"
              placeholder="مثلاً: 25"
              class="modern-input"
              min="0"
              :disabled="isSubmittingInventory"
            />
          </div>
        </div>
        <div class="form-group">
          <label>قیمت (ریال):</label>
          <div class="single-input-wrapper">
            <input
              v-model.number="newVariant.final_price"
              type="number"
              placeholder="مثلاً: 150000"
              class="modern-input"
              min="0"
              :disabled="isSubmittingInventory"
            />
          </div>
        </div>
        <div class="form-group">
          <label>کد کالا SKU (اختیاری):</label>
          <div class="single-input-wrapper">
            <input
              v-model="newVariant.sku"
              type="text"
              placeholder="SKU-12345"
              class="modern-input"
              :disabled="isSubmittingInventory"
            />
          </div>
        </div>

        <div class="form-group submit-button-group">
          <label class="invisible-label">اکشن</label>
          <BaseButton
            variant="success"
            size="md"
            :disabled="isSubmittingInventory"
            class="btn-success w-full"
            @click="submitNewInventory"
          >
            <Save class="icon-sm" v-if="!isSubmittingInventory" />
            <Loader2 class="icon-sm spinner" v-else />
            {{ isSubmittingInventory ? 'در حال ثبت...' : 'ثبت موجودی جدید' }}
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { inventoryService, variantService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { inject, ref } from 'vue'

// Import Lucide Icons (Updated to support modern styling)
import {
  Activity,
  AlertTriangle,
  Banknote,
  Box,
  Calculator,
  Layers,
  Loader2,
  Package,
  PackageCheck,
  PackageX,
  PlusCircle,
  Power,
  PowerOff,
  Save,
  Tag,
  Trash2,
} from '@lucide/vue'

const isSubmittingInventory = ref(false)
const isSubmittingVariant = ref(false)
const errorStore = useErrorStore()

// ==============================
// دریافت دیتای اصلی از پوسته والد (Inject)
// ==============================
const product = inject('product')
const refreshProductData = inject('refreshProductData')

// فرم‌های ایجاد دیتا
const newVariant = ref({
  quantity: 0,
  final_price: null,
  sku: '',
  color: '',
  size: '',
  material: '',
  low_stock_alert: 5,
})
// const newVariantDef = ref({ name: '', value: '' })

// ==============================
// سابمیت زنجیره‌ای: ساخت واریانت و سپس ثبت موجودی
// ==============================
const submitNewInventory = async () => {
  // گرفتن آیدی محصول
  const productId = product.value?.id || product.id
  if (!productId) {
    errorStore.addError({ type: 'error', message: 'اطلاعات محصول معتبر یافت نشد.' })
    return
  }

  isSubmittingInventory.value = true
  try {
    // مرحله اول: ایجاد واریانت (تنوع کالا)
    const variantPayload = {
      price: Number(newVariant.value.final_price || 0),
      is_active: true,
      product_id: productId,
      color: newVariant.value.color || null,
      size: newVariant.value.size || null,
      material: newVariant.value.material || null,
    }

    // فرستادن درخواست به سرویس واریانت
    const variantResponse = await variantService.createVariant(variantPayload)

    // استخراج آیدی واریانت ساخته شده از خروجی
    const createdVariantId = variantResponse?.id

    if (!createdVariantId) {
      throw new Error('واریانت با موفقیت ساخته شد اما آیدی آن در پاسخ سرور یافت نشد.')
    }

    // مرحله دوم: ایجاد رکورد موجودی با استفاده از آیدی مرحله قبل
    const inventoryPayload = {
      variant_id: createdVariantId,
      quantity: Number(newVariant.value.quantity || 0),
      reserved_quantity: 0,
      low_stock_alert: Number(newVariant.value.low_stock_alert || 5),
      allow_backorder: false,
    }

    // فرستادن درخواست به سرویس موجودی
    await inventoryService.createInventory(inventoryPayload)

    // مرحله سوم: به‌روزرسانی کل دیتای کامپوننت
    await refreshProductData()

    // پاکسازی فرم پس از موفقیت
    newVariant.value = {
      quantity: 0,
      final_price: null,
      sku: '',
      color: '',
      size: '',
      material: '',
      low_stock_alert: 5,
    }
  } catch (error) {
    // مدیریت و نمایش خطا در هر کدام از مراحل بالا
    const msg = getErrorMessage(error.code) || error.message || 'خطا در ثبت همزمان ویژگی و موجودی'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isSubmittingInventory.value = false
  }
}

// ==============================
// اضافه کردن یک واریانت (تنوع)
// ==============================
// const handleCreateVariant = async (variantFormData) => {
//   if (!variantFormData) return
//   isSubmittingVariant.value = true
//   try {
//     await variantService.createVariant(variantFormData)
//     await refreshProductData()
//   } catch (error) {
//     const msg = getErrorMessage(error.code) || 'خطا در ایجاد متغیر جدید'
//     errorStore.addError({ type: 'error', message: msg })
//   } finally {
//     isSubmittingVariant.value = false
//   }
// }

// ==============================
// ویرایش واریانت
// ==============================
const handleUpdateVariant = async (variantId, updateData) => {
  if (!variantId || !updateData) return
  isSubmittingVariant.value = true
  try {
    await variantService.updateVariant(variantId, updateData)
    await refreshProductData()
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در به‌روزرسانی متغیر'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isSubmittingVariant.value = false
  }
}

// ==============================
// حذف یک واریانت
// ==============================
// const handleDeleteVariant = async (variantId) => {
//   if (!variantId) return
//   if (!confirm('آیا از حذف این متغیر مطمئن هستید؟')) return
//   isSubmittingVariant.value = true
//   try {
//     await variantService.deleteVariant(variantId)
//     await refreshProductData()
//   } catch (error) {
//     const msg = getErrorMessage(error.code) || 'خطا در حذف متغیر'
//     errorStore.addError({ type: 'error', message: msg })
//   } finally {
//     isSubmittingVariant.value = false
//   }
// }

// ==============================
// سابمیت و پاکسازی فرم موجودی جدید
// ==============================
// const submitNewInventory = async () => {
//   await handleCreateInventory(newVariant.value)
//   if (!isSubmittingInventory.value && !errorStore.hasError) {
//     newVariant.value = { quantity: 0, final_price: null, sku: '' }
//   }
// }

// ==============================
// ایجاد رکورد موجودی جدید
// ==============================
// const handleCreateInventory = async (inventoryFormData) => {
//   if (!inventoryFormData) return
//   isSubmittingInventory.value = true
//   try {
//     await inventoryService.createInventory(inventoryFormData)
//     await refreshProductData()
//   } catch (error) {
//     const msg = getErrorMessage(error.code) || 'خطا در ثبت موجودی جدید'
//     errorStore.addError({ type: 'error', message: msg })
//   } finally {
//     isSubmittingInventory.value = false
//   }
// }

// ==============================
// به‌روزرسانی موجودی
// ==============================
const handleUpdateInventory = async (inventoryId, updateData) => {
  if (!inventoryId || !updateData) return
  isSubmittingInventory.value = true
  try {
    await inventoryService.updateInventory(inventoryId, updateData)
    await refreshProductData()
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در به‌روزرسانی موجودی'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isSubmittingInventory.value = false
  }
}

// ==============================
// حذف موجودی
// ==============================
const handleDeleteInventory = async (inventoryId) => {
  if (!inventoryId) return
  if (!confirm('آیا از حذف این رکورد موجودی مطمئن هستید؟')) return
  isSubmittingInventory.value = true
  try {
    await inventoryService.deleteInventory(inventoryId)
    await refreshProductData()
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در حذف رکورد موجودی'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isSubmittingInventory.value = false
  }
}
</script>

<style scoped>
/* =========================
   Base Styles
========================= */
.form-container {
  font-family:
    system-ui,
    -apple-system,
    sans-serif;
  color: #334155;
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.w-full {
  width: 100%;
}
.mt-3 {
  margin-top: 1rem;
}
.mb-3 {
  margin-bottom: 1rem;
}
.text-muted {
  color: #64748b;
}
.opacity-50 {
  opacity: 0.5;
}
.icon-xs {
  width: 16px;
  height: 16px;
}
.icon-sm {
  width: 18px;
  height: 18px;
}
.icon-md {
  width: 22px;
  height: 22px;
}
.icon-xl {
  width: 48px;
  height: 48px;
}
.spinner {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

.header-section {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}
.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}
.tab-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}
.card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
.bg-slate-50 {
  background-color: #f8fafc;
}

.specs-heading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1.25rem;
  border-bottom: 1px dashed #cbd5e1;
  padding-bottom: 0.75rem;
}

/* Status Badges */
.stock-status-badge {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
}
.status-in-stock {
  background-color: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}
.status-out-of-stock {
  background-color: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

/* =========================
   تغییرات ساختاری استایل ردیف‌ها (کارت جدید)
========================= */
.admin-variant-grid {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.variant-row-card {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
  transition: all 0.25s ease;
  border-right: 4px solid #94a3b8;
  gap: 1rem;
}
.variant-row-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
  border-color: #cbd5e1;
}

/* وضعیت‌های داینامیک ردیف */
.row-inactive {
  opacity: 0.65;
  background: #f8fafc;
  border-right-color: #cbd5e1;
}
.row-low-stock {
  background: #fffbfb;
  border-color: #fecaca;
  border-right-color: #ef4444;
}
.row-backorder {
  background: #fdfcff;
  border-color: #dbeafe;
  border-right-color: #3b82f6;
}

/* نوار بالای هر کارت تنوع */
.variant-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px dashed #f1f5f9;
  padding-bottom: 0.75rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.attributes-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}
.attributes-wrapper {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.attr-badge {
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #e2e8f0;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
}
.low-stock-warning {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  color: #dc2626;
  font-size: 0.8rem;
  font-weight: 700;
  background: #fef2f2;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  border: 1px solid #fee2e2;
}

/* =========================
   شبکه ورودی‌ها (تراز بندی خطی عالی)
========================= */
.variant-inputs-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1rem;
}

@media (max-width: 1100px) {
  .variant-inputs-grid {
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1.25rem;
  }
  .action-buttons-wrapper {
    grid-column: span 3;
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-items: flex-end;
  }
  .action-buttons-wrapper .invisible-label {
    display: none;
  }
}
@media (max-width: 768px) {
  .variant-inputs-grid {
    grid-template-columns: 1fr 1fr;
  }
  .action-buttons-wrapper {
    grid-column: span 2;
  }
}

/* استایل فیلدها */
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.input-group label {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.8rem;
  font-weight: 700;
  color: #475569;
  white-space: nowrap;
}
.single-input-wrapper {
  width: 100%;
}
.modern-input {
  width: 100%;
  padding: 0.55rem 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
  background: #fff;
  transition: all 0.2s ease;
  color: #1e293b;
}
.modern-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
.modern-input:disabled:not(.readonly-input) {
  background: #f8fafc;
  cursor: not-allowed;
  opacity: 0.6;
}
.input-error {
  border-color: #ef4444 !important;
  background-color: #fff5f5;
  color: #b91c1c;
}

.sku-group {
  grid-column: span 2;
  min-width: 220px;
}

.sku-group .modern-input {
  font-family: monospace;
  letter-spacing: 0.5px;
}

/* شخصی‌سازی فیلد قیمت نهایی سیستمی */
.readonly-input {
  background-color: #f1f5f9 !important;
  color: #64748b !important;
  border-color: #e2e8f0 !important;
  font-weight: 600;
  cursor: help;
}

.text-center-input .modern-input {
  text-align: center;
}

/* دکمه‌ها */
.action-buttons-wrapper {
  grid-column: span 1;
  flex-direction: column;
  gap: 0.4rem;
  order: 6;
  justify-content: flex-end;
}
.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

/* سوییچ مدرن */
.toggle-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f8fafc;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}
.toggle-label-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}
.modern-toggle {
  position: relative;
  display: inline-block;
  width: 38px;
  height: 20px;
}
.modern-toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #cbd5e1;
  transition: 0.2s;
  border-radius: 20px;
}
.toggle-slider:before {
  position: absolute;
  content: '';
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.2s;
  border-radius: 50%;
}
.modern-toggle input:checked + .toggle-slider {
  background-color: #22c55e;
}
.modern-toggle input:checked + .toggle-slider:before {
  transform: translateX(18px);
}
.modern-toggle input:disabled + .toggle-slider {
  opacity: 0.5;
  cursor: not-allowed;
}

/* فرم ثبت جدید پایین صفحه */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.25rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}
.invisible-label {
  visibility: hidden;
}

.btn-success {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #10b981;
  color: #fff;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  height: 40px;
}
.btn-success:hover:not(:disabled) {
  background: #059669;
}
.btn-success:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 8px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-icon:hover:not(:disabled) {
  transform: translateY(-1px);
}
.btn-icon:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon-danger {
  background: #fef2f2;
  border-color: #fecaca;
  color: #ef4444;
}
.btn-icon-danger:hover:not(:disabled) {
  background: #ef4444;
  color: #ffffff;
}

.btn-icon-warning {
  background: #fffbeb;
  border-color: #fde68a;
  color: #d97706;
}
.btn-icon-warning:hover:not(:disabled) {
  background: #f59e0b;
  color: #ffffff;
}

.btn-icon-success {
  background: #ecfdf5;
  border-color: #bbf7d0;
  color: #16a34a;
}
.btn-icon-success:hover:not(:disabled) {
  background: #22c55e;
  color: #ffffff;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
}
.empty-text {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

.final-price-display {
  height: 42px;
  padding: 0 12px;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;

  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);

  border: 1px solid #93c5fd;
  border-radius: 10px;

  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);

  transition: all 0.2s ease;
}

.final-price-display:hover {
  border-color: #60a5fa;
}

.price-value {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1d4ed8;
  direction: ltr;
}

.price-unit {
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1.25rem;
}

.submit-button-group {
  /* در دسکتاپ: رفتن به ردیف دوم، ستون ششم (سمت چپ‌ترین ستون) */
  grid-column: 6;
  grid-row: 2;

  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

/* برای مطمئن شدن از اینکه دکمه پهن نمی‌شود و متن داخلش جا می‌گیرد */
.submit-button-group :deep(button),
.submit-button-group .btn-success {
  width: max-content !important; /* به اندازه متن داخلش کش بیاید، نه بیشتر */
  min-width: 160px;
  padding: 0.6rem 1.5rem;
  align-self: flex-end; /* چسبیدن به لبه چپ در حالت RTL */
}

/* اصلاح تراز در حالت تبلت و موبایل */
@media (max-width: 1100px) {
  .form-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  .submit-button-group {
    grid-column: 1 / -1; /* در موبایل کل عرض را بگیرد */
    grid-row: auto;
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
  }
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .submit-button-group {
    grid-column: 1 / -1;
    grid-row: auto;
  }
  .submit-button-group :deep(button),
  .submit-button-group .btn-success {
    width: 100% !important; /* فقط در موبایل تمام‌عرض شود */
  }
}
</style>
