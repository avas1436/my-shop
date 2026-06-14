<!-- src/views/admin/product-tabs/ActionsTab.vue -->
<template>
  <div class="tab-content page-panel admin-actions-tab">
    <h2 class="tab-title">تنظیمات وضعیت و عملیات نهایی محصول</h2>

    <div class="status-status-box">
      <div class="status-indicator-large">
        <span>وضعیت فعلی کالا در سیستم:</span>
        <strong :class="product.status === 'active' ? 'text-success' : 'text-warning'">
          {{ product.status === 'active' ? 'منتشر شده (Active)' : 'پیش‌نویس (Draft)' }}
        </strong>
      </div>
      <p class="text-small muted mt-2">
        وقتی محصول در وضعیت پیش‌نویس باشد، در ویترین فروشگاه به کاربران نمایش داده نمی‌شود.
      </p>
    </div>

    <div class="danger-zone-box mt-4">
      <h3 class="danger-title">عملیات مدیریتی خطرناک</h3>
      <div class="action-buttons-vertical">
        <BaseButton
          v-if="product && product.status !== 'active'"
          variant="success"
          size="lg"
          @click="handlePublish"
          class="w-100 mb-2"
        >
          انتشار نهایی محصول در سایت
        </BaseButton>

        <button class="btn-delete-hard-large" @click="handleHardDelete">
          حذف دائمی و قطعی محصول از پایگاه داده
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { productService } from '@/services/productService'
import { inject } from 'vue'
import { useRouter } from 'vue-router'

const product = inject('product')
const router = useRouter()

async function handlePublish() {
  try {
    await productService.publishProduct(product.value.id)
    product.value.status = 'active'
    alert('محصول با موفقیت منتشر شد.')
  } catch (error) {
    alert('خطا در انتشار محصول')
  }
}

async function handleHardDelete() {
  if (!confirm('آیا از حذف همیشگی این محصول اطمینان دارید؟ این عملیات غیرقابل بازگشت خواهد بود!'))
    return
  try {
    await productService.hardDelete(product.value.id)
    router.push('/admin/products')
  } catch (error) {
    alert('خطا در حذف قطعی کالا')
  }
}
</script>

<style scoped>
.admin-actions-tab {
  text-align: right;
}
.status-status-box {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  padding: 1rem;
  border-radius: 8px;
}
.status-indicator-large {
  display: flex;
  justify-content: space-between;
  font-size: 1.1rem;
}
.text-success {
  color: #16a34a;
}
.text-warning {
  color: #d97706;
}
.danger-zone-box {
  border: 1px solid #fca5a5;
  background: #fff5f5;
  padding: 1.25rem;
  border-radius: 8px;
}
.danger-title {
  color: #dc2626;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}
.action-buttons-vertical {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.btn-delete-hard-large {
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  width: 100%;
  transition: background 0.2s;
}
.btn-delete-hard-large:hover {
  background: #b91c1c;
}
</style>
