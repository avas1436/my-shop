<!-- src/views/admin/product-tabs/InventoryTab.vue -->
<template>
  <div class="tab-content page-panel">
    <div class="detail-actions admin-inventory-section">
      <h3 class="inventory-title">مدیریت زنده تنوع‌ها (رنگ / سایز)</h3>

      <div class="detail-rating admin-meta-row mb-3">
        <span
          :class="product.is_in_stock ? 'text-success' : 'text-danger'"
          style="font-weight: bold"
        >
          موجودی کل انبار: {{ product.total_available_quantity }} عدد ({{
            product.is_in_stock ? 'موجود در انبار' : 'ناموجود'
          }})
        </span>
      </div>

      <div v-if="product.inventory?.length" class="admin-variant-grid">
        <div v-for="item in product.inventory" :key="item.id" class="variant-row-card">
          <div class="variant-info">
            <span class="muted text-small d-block">SKU: {{ item.sku || 'ثبت نشده' }}</span>
            <span v-for="attr in item.attributes" :key="attr.attribute_id" class="attr-badge">
              {{ attr.name }}: {{ attr.value }}
            </span>
          </div>
          <div class="variant-inputs">
            <label>
              <span>موجودی:</span>
              <input
                v-model.number="item.quantity"
                type="number"
                @change="patchVariant(item.id, 'quantity', item.quantity)"
              />
            </label>
            <label>
              <span>قیمت نهایی (ریال):</span>
              <input
                v-model.number="item.final_price"
                type="number"
                @change="patchVariant(item.id, 'final_price', item.final_price)"
              />
            </label>
            <button class="btn-icon-danger" @click="deleteInventory(item.id)" title="حذف تنوع">
              🗑️
            </button>
          </div>
        </div>
      </div>

      <h4 class="mt-4 specs-heading">ثبت تنوع و موجودی جدید</h4>
      <div class="add-inventory-form">
        <input
          v-model.number="newVariant.quantity"
          type="number"
          placeholder="تعداد موجودی"
          class="base-input-field"
        />
        <input
          v-model.number="newVariant.final_price"
          type="number"
          placeholder="قیمت نهایی"
          class="base-input-field"
        />
        <input
          v-model="newVariant.sku"
          type="text"
          placeholder="کد کالا SKU (اختیاری)"
          class="base-input-field"
        />
        <button class="btn-add" @click="addInventory">ثبت موجودی جدید</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { productService } from '@/services/productService'
import { inject, ref } from 'vue'

const product = inject('product')
const refreshProductData = inject('refreshProductData')

const newVariant = ref({ quantity: 0, final_price: null, sku: '' })

async function patchVariant(inventoryId, subField, value) {
  try {
    await productService.updateInventory(inventoryId, { [subField]: value })
  } catch (error) {
    console.error('خطا در پچ داده انبار')
  }
}

async function addInventory() {
  if (newVariant.value.quantity === null || newVariant.value.quantity < 0) return
  try {
    await productService.createInventory(product.value.id, newVariant.value)
    newVariant.value = { quantity: 0, final_price: null, sku: '' }
    await refreshProductData()
  } catch (error) {
    alert('خطا در ثبت موجودی جدید')
  }
}

async function deleteInventory(inventoryId) {
  if (!confirm('آیا مایل به حذف این قلم تنوع هستید؟')) return
  try {
    await productService.deleteInventory(inventoryId)
    await refreshProductData()
  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>
.admin-inventory-section {
  text-align: right;
}
.inventory-title {
  margin-bottom: 1rem;
  color: #1e293b;
}
.admin-variant-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.variant-row-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  flex-wrap: wrap;
  gap: 1rem;
}
.variant-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.attr-badge {
  background: #e2e8f0;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  margin-left: 0.5rem;
  display: inline-block;
}
.variant-inputs {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}
.variant-inputs label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}
.variant-inputs input {
  width: 100px;
  padding: 0.4rem;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
}
.add-inventory-form {
  display: flex;
  gap: 0.5rem;
  background: #fff;
  padding: 1rem;
  border-radius: 8px;
  border: 1px dashed #bbf7d0;
  flex-wrap: wrap;
}
.add-inventory-form input {
  flex: 1;
  min-width: 120px;
}
.btn-add {
  background: #10b981;
  color: #fff;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
.btn-icon-danger {
  background: none;
  border: none;
  color: #ef4444;
  font-size: 1.2rem;
  cursor: pointer;
}
.text-success {
  color: #10b981;
}
.text-danger {
  color: #ef4444;
}
</style>
