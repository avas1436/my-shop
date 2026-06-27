<!-- src/views/admin/product-tabs/InventoryTab.vue -->
<template>
  <div class="animate-[fadeIn_0.3s_ease-in-out] grid gap-6">
    <!-- هدر -->
    <div
      class="flex flex-wrap items-center justify-between gap-4 border-b border-border-light pb-4"
    >
      <h2 class="m-0 flex items-center gap-2 text-[1.3rem] font-bold">
        <Layers class="w-5 h-5 shrink-0" />
        مدیریت موجودی و تنوع‌ها
      </h2>
      <span
        class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full font-bold text-[0.9rem] border"
        :class="
          product.is_in_stock
            ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
            : 'bg-red-50 text-red-600 border-red-200'
        "
      >
        <PackageCheck v-if="product.is_in_stock" class="w-4 h-4" />
        <PackageX v-else class="w-4 h-4" />
        موجودی کل انبار: {{ product.total_available_quantity || 0 }} عدد ({{
          product.is_in_stock ? 'موجود' : 'ناموجود'
        }})
      </span>
    </div>

    <!-- لیست موجودی‌ها -->
    <section
      class="grid gap-4 p-5 bg-white border border-border-light rounded-xl shadow-(--shadow-soft)"
    >
      <h3
        class="m-0 flex items-center gap-2 text-[1.1rem] font-bold border-b border-dashed border-border-strong pb-3"
      >
        <Package class="w-4 h-4" />
        موجودی‌های ثبت شده در انبار
      </h3>

      <template v-if="product.inventory?.length">
        <div
          v-for="item in product.inventory"
          :key="item.id"
          class="grid gap-4 p-5 rounded-xl border border-r-4 transition-all duration-200 hover:shadow-md"
          :class="{
            'opacity-60 bg-slate-50 border-r-slate-300 border-slate-200': item.is_active === false,
            'bg-red-50/50 border-r-red-500 border-red-200':
              item.is_active !== false && item.quantity <= item.low_stock_alert,
            'bg-blue-50/30 border-r-blue-400 border-blue-200':
              item.is_active !== false &&
              item.allow_backorder &&
              item.quantity > item.low_stock_alert,
            'bg-white border-r-slate-300 border-border-light':
              item.is_active !== false &&
              !item.allow_backorder &&
              item.quantity > item.low_stock_alert,
          }"
        >
          <!-- نوار بالا: attributes + toggle -->
          <div
            class="flex flex-wrap items-center justify-between gap-4 border-b border-dashed border-slate-100 pb-3"
          >
            <div class="flex flex-wrap items-center gap-3">
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="attr in item.attributes"
                  :key="attr.attribute_id"
                  class="px-3 py-1 rounded-md bg-slate-100 border border-border-light text-[0.85rem] text-text-main"
                >
                  {{ attr.name }}: <strong>{{ attr.value }}</strong>
                </span>
              </div>
              <span
                v-if="item.is_active !== false && item.quantity <= item.low_stock_alert"
                class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-red-50 border border-red-200 text-red-600 text-[0.8rem] font-bold"
              >
                <AlertTriangle class="w-3.5 h-3.5" />
                موجودی به محدوده خطر رسیده!
              </span>
            </div>

            <!-- toggle فروش بیش از موجودی -->
            <label
              class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 border border-border-light cursor-pointer"
            >
              <span class="text-[0.85rem] font-bold text-text-muted">فروش بیش از موجودی</span>
              <div
                class="relative w-9.5 h-5 rounded-full transition-colors duration-200 cursor-pointer"
                :class="item.allow_backorder ? 'bg-green-500' : 'bg-slate-300'"
                @click="
                  !isSubmittingInventory &&
                  item.is_active &&
                  handleUpdateInventory(item.id, { allow_backorder: !item.allow_backorder })
                "
              >
                <span
                  class="absolute top-0.75 w-3.5 h-3.5 rounded-full bg-white shadow transition-all duration-200"
                  :class="item.allow_backorder ? 'right-0.75' : 'right-4.25'"
                />
              </div>
            </label>
          </div>

          <!-- شبکه فیلدها -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div class="grid gap-1 lg:col-span-2">
              <label
                class="flex items-center gap-1 text-[0.8rem] font-bold text-text-muted whitespace-nowrap"
              >
                <Tag class="w-3.5 h-3.5" /> کد کالا (SKU)
              </label>
              <input
                v-model="item.sku"
                type="text"
                placeholder="ثبت نشده"
                class="w-full px-3 py-2 border border-border-light rounded-lg text-[0.9rem] font-mono bg-white focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                :disabled="!item.is_active || isSubmittingInventory"
                @change="handleUpdateVariant(item.variant_id, { sku: item.sku })"
              />
            </div>

            <div class="grid gap-1">
              <label
                class="flex items-center gap-1 text-[0.8rem] font-bold text-text-muted whitespace-nowrap"
              >
                <Banknote class="w-3.5 h-3.5" /> قیمت (ریال)
              </label>
              <input
                v-model.number="item.price"
                type="number"
                min="0"
                class="w-full px-3 py-2 border border-border-light rounded-lg text-[0.9rem] bg-white text-center focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                :disabled="!item.is_active || isSubmittingInventory"
                @change="handleUpdateVariant(item.variant_id, { price: item.price })"
              />
            </div>

            <div class="grid gap-1">
              <label
                class="flex items-center gap-1 text-[0.8rem] font-bold text-text-muted whitespace-nowrap"
              >
                <Box class="w-3.5 h-3.5" /> موجودی
              </label>
              <input
                v-model.number="item.quantity"
                type="number"
                min="0"
                class="w-full px-3 py-2 border rounded-lg text-[0.9rem] bg-white text-center focus:outline-none focus:ring-2 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                :class="
                  item.is_active !== false && item.quantity <= item.low_stock_alert
                    ? 'border-red-400 bg-red-50 text-red-700 focus:border-red-400 focus:ring-red-200'
                    : 'border-border-light focus:border-primary focus:ring-primary/10'
                "
                :disabled="!item.is_active || isSubmittingInventory"
                @change="handleUpdateInventory(item.id, { quantity: item.quantity })"
              />
            </div>

            <div class="grid gap-1">
              <label
                class="flex items-center gap-1 text-[0.8rem] font-bold text-text-muted whitespace-nowrap"
              >
                <Activity class="w-3.5 h-3.5" /> کف موجودی
              </label>
              <input
                v-model.number="item.low_stock_alert"
                type="number"
                min="0"
                class="w-full px-3 py-2 border border-border-light rounded-lg text-[0.9rem] bg-white text-center focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                :disabled="!item.is_active || isSubmittingInventory"
                @change="handleUpdateInventory(item.id, { low_stock_alert: item.low_stock_alert })"
              />
            </div>

            <!-- قیمت نهایی -->
            <div class="grid gap-1">
              <label
                class="flex items-center gap-1 text-[0.8rem] font-bold text-text-muted whitespace-nowrap"
              >
                <Calculator class="w-3.5 h-3.5" /> قیمت نهایی
              </label>
              <div
                class="h-10.5 flex items-center justify-center gap-1.5 rounded-lg border border-blue-300 bg-linear-to-br from-blue-50 to-blue-100 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)]"
              >
                <span class="text-[0.95rem] font-extrabold text-blue-700 dir-ltr">
                  {{ Number(item.final_price || product.final_price).toLocaleString('fa-IR') }}
                </span>
                <span class="text-[0.75rem] font-bold text-text-muted">ریال</span>
              </div>
            </div>

            <!-- دکمه‌های عملیات -->
            <div class="flex items-end justify-end gap-2 lg:col-span-6">
              <button
                type="button"
                class="inline-flex items-center justify-center w-10.5 h-10.5 rounded-lg border transition-all duration-200 hover:-translate-y-px disabled:opacity-50 disabled:cursor-not-allowed"
                :class="
                  item.is_active !== false
                    ? 'bg-amber-50 border-amber-200 text-amber-600 hover:bg-amber-500 hover:text-white'
                    : 'bg-emerald-50 border-emerald-200 text-emerald-600 hover:bg-emerald-500 hover:text-white'
                "
                :title="item.is_active ? 'غیرفعال کردن' : 'فعال کردن'"
                :disabled="isSubmittingInventory"
                @click="handleUpdateVariant(item.variant_id, { is_active: !item.is_active })"
              >
                <PowerOff v-if="item.is_active !== false" class="w-4 h-4" />
                <Power v-else class="w-4 h-4" />
              </button>
              <button
                type="button"
                class="inline-flex items-center justify-center w-10.5 h-10.5 rounded-lg border bg-red-50 border-red-200 text-red-500 transition-all duration-200 hover:bg-red-500 hover:text-white hover:-translate-y-px disabled:opacity-50 disabled:cursor-not-allowed"
                title="حذف رکورد موجودی"
                :disabled="isSubmittingInventory"
                @click="handleDeleteInventory(item.id)"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </template>

      <div
        v-else
        class="flex flex-col items-center justify-center py-12 px-4 bg-bg-muted rounded-xl border border-dashed border-border-strong"
      >
        <Box class="w-12 h-12 text-text-muted opacity-40 mb-3" />
        <p class="m-0 text-text-muted">هیچ رکورد موجودی برای این محصول ثبت نشده است.</p>
      </div>
    </section>

    <!-- فرم ثبت موجودی جدید -->
    <section class="grid gap-4 p-5 bg-bg-muted border border-border-light rounded-xl">
      <h4
        class="m-0 flex items-center gap-2 text-[1.1rem] font-bold border-b border-dashed border-border-strong pb-3"
      >
        <PlusCircle class="w-4 h-4" />
        ثبت رکورد موجودی جدید
      </h4>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">رنگ</label>
          <BaseInput
            v-model="newVariant.color"
            placeholder="مثلاً: مشکی"
            :disabled="isSubmittingInventory"
          />
        </div>
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">سایز</label>
          <BaseInput
            v-model="newVariant.size"
            placeholder="مثلاً: XL"
            :disabled="isSubmittingInventory"
          />
        </div>
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">جنس</label>
          <BaseInput
            v-model="newVariant.material"
            placeholder="مثلاً: چرم"
            :disabled="isSubmittingInventory"
          />
        </div>
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">تعداد موجودی</label>
          <BaseInput
            v-model.number="newVariant.quantity"
            type="number"
            placeholder="مثلاً: 25"
            :disabled="isSubmittingInventory"
          />
        </div>
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">قیمت (ریال)</label>
          <BaseInput
            v-model.number="newVariant.final_price"
            type="number"
            placeholder="مثلاً: 150000"
            :disabled="isSubmittingInventory"
          />
        </div>
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">کد کالا SKU (اختیاری)</label>
          <BaseInput
            v-model="newVariant.sku"
            placeholder="SKU-12345"
            :disabled="isSubmittingInventory"
          />
        </div>
      </div>

      <div class="flex justify-end pt-2">
        <BaseButton
          variant="success"
          size="md"
          :disabled="isSubmittingInventory"
          @click="submitNewInventory"
        >
          <Loader2 v-if="isSubmittingInventory" class="w-4 h-4 animate-spin" />
          <Save v-else class="w-4 h-4" />
          {{ isSubmittingInventory ? 'در حال ثبت...' : 'ثبت موجودی جدید' }}
        </BaseButton>
      </div>
    </section>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { inventoryService, variantService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
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
import { inject, ref } from 'vue'

const errorStore = useErrorStore()
const product = inject('product')
const refreshProductData = inject('refreshProductData')

const isSubmittingInventory = ref(false)
const isSubmittingVariant = ref(false)

const newVariant = ref({
  quantity: 0,
  final_price: null,
  sku: '',
  color: '',
  size: '',
  material: '',
  low_stock_alert: 5,
})

const resetNewVariant = () => {
  newVariant.value = {
    quantity: 0,
    final_price: null,
    sku: '',
    color: '',
    size: '',
    material: '',
    low_stock_alert: 5,
  }
}

const submitNewInventory = async () => {
  const productId = product.value?.id || product.id
  if (!productId) {
    errorStore.addError({ type: 'error', message: 'اطلاعات محصول معتبر یافت نشد.' })
    return
  }
  isSubmittingInventory.value = true
  try {
    const variantResponse = await variantService.createVariant({
      price: Number(newVariant.value.final_price || 0),
      is_active: true,
      product_id: productId,
      color: newVariant.value.color || null,
      size: newVariant.value.size || null,
      material: newVariant.value.material || null,
    })
    const createdVariantId = variantResponse?.id
    if (!createdVariantId) throw new Error('آیدی واریانت در پاسخ سرور یافت نشد.')
    await inventoryService.createInventory({
      variant_id: createdVariantId,
      quantity: Number(newVariant.value.quantity || 0),
      reserved_quantity: 0,
      low_stock_alert: Number(newVariant.value.low_stock_alert || 5),
      allow_backorder: false,
    })
    await refreshProductData()
    resetNewVariant()
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || error.message || 'خطا در ثبت موجودی',
    })
  } finally {
    isSubmittingInventory.value = false
  }
}

const handleUpdateVariant = async (variantId, updateData) => {
  if (!variantId || !updateData) return
  isSubmittingVariant.value = true
  try {
    await variantService.updateVariant(variantId, updateData)
    await refreshProductData()
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در به‌روزرسانی واریانت',
    })
  } finally {
    isSubmittingVariant.value = false
  }
}

const handleUpdateInventory = async (inventoryId, updateData) => {
  if (!inventoryId || !updateData) return
  isSubmittingInventory.value = true
  try {
    await inventoryService.updateInventory(inventoryId, updateData)
    await refreshProductData()
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در به‌روزرسانی موجودی',
    })
  } finally {
    isSubmittingInventory.value = false
  }
}

const handleDeleteInventory = async (inventoryId) => {
  if (!inventoryId || !confirm('آیا از حذف این رکورد موجودی مطمئن هستید؟')) return
  isSubmittingInventory.value = true
  try {
    await inventoryService.deleteInventory(inventoryId)
    await refreshProductData()
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در حذف رکورد موجودی',
    })
  } finally {
    isSubmittingInventory.value = false
  }
}
</script>
