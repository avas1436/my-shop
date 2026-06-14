<!-- src/views/admin/AdminProductDetailView.vue -->
<template>
  <div v-if="isLoading" class="admin-loading">
    <p>در حال بارگذاری پوسته ادمین با ساختار تب‌بندی...</p>
  </div>

  <div v-else-if="product" class="page-shell admin-storefront-mode">
    <div class="tabs-header-wrapper">
      <div class="tabs-navigation">
        <router-link :to="{ name: 'AdminProductGeneral' }" active-class="active">
          اطلاعات پایه
        </router-link>
        <router-link :to="{ name: 'AdminProductImages' }" active-class="active">
          تصاویر
        </router-link>
        <router-link :to="{ name: 'AdminProductInventory' }" active-class="active">
          موجودی و تنوع
        </router-link>
        <router-link :to="{ name: 'AdminProductRelations' }" active-class="active">
          دسته‌بندی و ویژگی‌ها
        </router-link>
        <router-link :to="{ name: 'AdminProductComments' }" active-class="active">
          نظرات
        </router-link>
        <router-link :to="{ name: 'AdminProductActions' }" active-class="active">
          وضعیت و عملیات نهایی
        </router-link>
      </div>
    </div>

    <router-view></router-view>

    <div class="timestamps-footer page-panel">
      <span v-if="product.created_at"
        >ساخته شده در: {{ formatPrsianDate(product.created_at) }}</span
      >
      <span v-if="product.updated_at"
        >آخرین بروزرسانی: {{ formatPrsianDate(product.updated_at) }}</span
      >
      <span v-if="product.published_at"
        >تاریخ انتشار: {{ formatPrsianDate(product.published_at) }}</span
      >
    </div>
  </div>

  <div v-else class="page-shell">
    <section class="empty-state">محصول مورد نظر جهت مدیریت یافت نشد.</section>
  </div>
</template>

<script setup>
import { productService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { formatPrsianDate } from '@/utils/format'
import { onMounted, provide, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const errorStore = useErrorStore()

const isLoading = ref(true)
const product = ref(null)
const productUpdate = ref({})

// متد اصلی دریافت اطلاعات از سرور
const loadAllAdminData = async () => {
  try {
    isLoading.value = true
    const pId = route.params.product_id
    const response = await productService.getProductFull(pId)
    product.value = response
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطایی در دریافت اطلاعات رخ داده است'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isLoading.value = false
  }
}

// متد رفرش کردن داده‌ها پس از تغییرات در فرزندان
const refreshProductData = async () => {
  if (!product.value?.id) return
  const response = await productService.getProductFull(product.value.id)
  product.value = response
}

// متد ثبت تغییرات فیلدها در آبجکت پچ (Patch Object)
const updateField = (key, value) => {
  if (product.value) {
    product.value[key] = value
  }
  productUpdate.value[key] = value
}

onMounted(() => {
  loadAllAdminData()
})

// تزریق متغیرها و متدها به تمام کامپوننت‌های فرزند (تب‌ها)
provide('product', product)
provide('productUpdate', productUpdate)
provide('isLoading', isLoading)
provide('refreshProductData', refreshProductData)
provide('updateField', updateField)
</script>

<style scoped>
.admin-storefront-mode {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  direction: rtl;
}
.tabs-header-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.tabs-navigation {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  overflow-y: hidden;
}
.tabs-navigation a {
  text-decoration: none;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
  white-space: nowrap;
}
.tabs-navigation a:hover {
  color: #334155;
  background: #f8fafc;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}
.tabs-navigation a.active {
  color: #5b3df5;
  border-bottom-color: #5b3df5;
}
.timestamps-footer {
  display: flex;
  gap: 1.5rem;
  font-size: 0.85rem;
  color: #94a3b8;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 1rem;
}
.admin-loading {
  text-align: center;
  padding: 4rem;
  font-weight: 700;
  font-size: 1.2rem;
  color: #475569;
}
.page-panel {
  background: var(--surface, #fff);
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
</style>
