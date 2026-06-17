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

      <div v-if="product.inventory?.length" class="admin-variant-grid">
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
          <div class="variant-info">
            <div class="sku-badge">
              <Tag class="icon-xs" />
              SKU: {{ item.sku || 'ثبت نشده' }}
            </div>
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

          <div class="variant-actions-wrapper">
            <div class="toggle-wrapper">
              <!-- تعیین مجاز به فروش بیش از موجودی -->
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

            <!--  تعیین کف محصول که در آن مقدار ارور داریم -->
            <div class="variant-inputs">
              <div class="input-group">
                <label><Activity class="icon-xs text-muted" /> کف موجودی:</label>
                <div class="single-input-wrapper">
                  <input
                    v-model.number="item.low_stock_alert"
                    type="number"
                    min="0"
                    class="modern-input small-input"
                    @change="
                      handleUpdateInventory(item.id, { low_stock_alert: item.low_stock_alert })
                    "
                    :disabled="!item.is_active || isSubmittingInventory"
                  />
                </div>
              </div>

              <!-- ویرایش موجودی -->
              <div class="input-group">
                <label><Box class="icon-xs text-muted" /> موجودی:</label>
                <div class="single-input-wrapper">
                  <input
                    v-model.number="item.quantity"
                    type="number"
                    min="0"
                    class="modern-input small-input"
                    :class="{
                      'input-error':
                        item.is_active !== false && item.quantity <= item.low_stock_alert,
                    }"
                    @change="handleUpdateInventory(item.id, { quantity: item.quantity })"
                    :disabled="!item.is_active || isSubmittingInventory"
                  />
                </div>
              </div>

              <div class="input-group">
                <label><Banknote class="icon-xs text-muted" /> قیمت نهایی (ریال):</label>
                <div class="single-input-wrapper">
                  <input
                    v-model.number="item.final_price"
                    type="number"
                    min="0"
                    class="modern-input medium-input"
                    @change="handleUpdateInventory(item.id, { final_price: item.final_price })"
                    :disabled="!item.is_active || isSubmittingInventory"
                  />
                </div>
              </div>

              <!-- غیر فعال کردن -->
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

                <!-- حذف -->
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
      </div>

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
          <label>تعداد موجودی:</label>
          <div class="single-input-wrapper">
            <input
              v-model.number="newVariant.quantity"
              type="number"
              placeholder="مثلاً: 10"
              class="modern-input"
              min="0"
              :disabled="isSubmittingInventory"
            />
          </div>
        </div>

        <div class="form-group">
          <label>قیمت نهایی (ریال):</label>
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

        <div class="form-group">
          <label class="invisible-label">اکشن</label>
          <button
            class="btn-success w-full"
            @click="submitNewInventory"
            :disabled="isSubmittingInventory"
          >
            <Save class="icon-sm" v-if="!isSubmittingInventory" />
            <Loader2 class="icon-sm spinner" v-else />
            {{ isSubmittingInventory ? 'در حال ثبت...' : 'ثبت موجودی' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
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
const newVariant = ref({ quantity: 0, final_price: null, sku: '' })
const newVariantDef = ref({ name: '', value: '' })

// ==============================
// سابمیت متغیر (Variant) جدید
// ==============================
const submitNewVariant = async () => {
  if (!newVariantDef.value.name) return
  await handleCreateVariant(newVariantDef.value)
  if (!isSubmittingVariant.value && !errorStore.hasError) {
    newVariantDef.value = { name: '', value: '' }
  }
}

// ==============================
// اضافه کردن یک واریانت (تنوع)
// ==============================
const handleCreateVariant = async (variantFormData) => {
  if (!variantFormData) return
  isSubmittingVariant.value = true
  try {
    await variantService.createVariant(variantFormData)
    await refreshProductData()
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در ایجاد متغیر جدید'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isSubmittingVariant.value = false
  }
}

// ==============================
// درخواست آپدیت واریانت (Prompt ساده)
// ==============================
const promptUpdateVariant = async (variant) => {
  const newValue = prompt(`مقدار جدید برای "${variant.name}" را وارد کنید:`, variant.value)
  if (newValue !== null && newValue !== variant.value) {
    await handleUpdateVariant(variant.id, { value: newValue })
  }
}

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
const handleDeleteVariant = async (variantId) => {
  if (!variantId) return
  if (!confirm('آیا از حذف این متغیر مطمئن هستید؟')) return
  isSubmittingVariant.value = true
  try {
    await variantService.deleteVariant(variantId)
    await refreshProductData()
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در حذف متغیر'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isSubmittingVariant.value = false
  }
}

// ==============================
// سابمیت و پاکسازی فرم موجودی جدید
// ==============================
const submitNewInventory = async () => {
  await handleCreateInventory(newVariant.value)
  if (!isSubmittingInventory.value && !errorStore.hasError) {
    newVariant.value = { quantity: 0, final_price: null, sku: '' }
  }
}

// ==============================
// ایجاد رکورد موجودی جدید
// ==============================
const handleCreateInventory = async (inventoryFormData) => {
  if (!inventoryFormData) return
  isSubmittingInventory.value = true
  try {
    await inventoryService.createInventory(inventoryFormData)
    await refreshProductData()
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در ثبت موجودی جدید'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isSubmittingInventory.value = false
  }
}

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
   Base Styles (همان کدهای قبلی شما)
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

/* Badges */
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

/* Form Elements */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.25rem;
}
.align-center {
  align-items: center;
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
.single-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.modern-input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  background: #fff;
  transition: all 0.2s ease;
  color: #1e293b;
}
.modern-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
.modern-input:disabled {
  background: #f1f5f9;
  cursor: not-allowed;
  opacity: 0.7;
}
.input-error {
  border-color: #ef4444 !important;
  background-color: #fef2f2;
  color: #991b1b;
}

/* =========================
   Dynamic Variant Rows (جدید)
========================= */
.admin-variant-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.variant-row-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  flex-wrap: wrap;
  gap: 1.5rem;
  transition: all 0.3s ease;
  border-right: 4px solid #cbd5e1; /* نوار رنگی کنار کارت */
}
.variant-row-card:hover {
  box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.1);
}

/* حالت‌های داینامیک */
.row-inactive {
  opacity: 0.6;
  background: #f8fafc;
  filter: grayscale(0.5);
  border-right-color: #94a3b8;
}
.row-low-stock {
  background: #fffafa;
  border-color: #fca5a5;
  border-right-color: #ef4444;
}
.row-backorder {
  background: #f8fafc;
  border-color: #bfdbfe;
  border-right-color: #3b82f6;
}

.variant-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
  min-width: 200px;
}
.sku-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  color: #64748b;
  font-size: 0.85rem;
  background: #f1f5f9;
  padding: 0.3rem 0.75rem;
  border-radius: 6px;
  width: fit-content;
}
.attributes-wrapper {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.attr-badge {
  background: #f8fafc;
  color: #334155;
  border: 1px solid #e2e8f0;
  padding: 0.3rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
}

/* هشدار موجودی کم */
.low-stock-warning {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  color: #b91c1c;
  font-size: 0.8rem;
  font-weight: 600;
  background: #fef2f2;
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  width: fit-content;
  border: 1px solid #fecaca;
}

/* بخش سمت چپ کارت */
.variant-actions-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-end;
}
.variant-inputs {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  flex-wrap: wrap;
}
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.input-group label {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}
.small-input {
  width: 100px;
}
.medium-input {
  width: 140px;
}
.action-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2px;
}

/* =========================
   Modern Toggle Switch (جدید)
========================= */
.toggle-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.4rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}
.toggle-label-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
}
.modern-toggle {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
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
  transition: 0.3s;
  border-radius: 22px;
}
.toggle-slider:before {
  position: absolute;
  content: '';
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}
.modern-toggle input:checked + .toggle-slider {
  background-color: #3b82f6;
}
.modern-toggle input:disabled + .toggle-slider {
  opacity: 0.5;
  cursor: not-allowed;
}
.modern-toggle input:checked + .toggle-slider:before {
  transform: translateX(18px);
}

/* Buttons */
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
  height: 42px;
}
.btn-success:hover:not(:disabled) {
  background: #059669;
}
.btn-success:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Icon Buttons */
.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-icon:hover:not(:disabled) {
  transform: translateY(-1px);
}
.btn-icon:active:not(:disabled) {
  transform: translateY(0);
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

/* Empty State */
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
</style>
