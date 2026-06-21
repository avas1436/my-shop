<!-- src/views/admin/product-tabs/ActionsTab.vue -->
<template>
  <div class="tab-content page-panel admin-actions-tab">
    <header class="header-section">
      <h2 class="tab-title">تنظیمات وضعیت و عملیات نهایی</h2>
      <p class="text-muted text-small">
        مدیریت نمایش محصول در فروشگاه و دسترسی به عملیات‌های حساس پایگاه داده.
      </p>
    </header>

    <section class="action-card status-box">
      <div class="card-header">
        <div class="header-content">
          <span class="card-title">وضعیت نمایش فعلی:</span>
          <span class="status-badge" :class="productStatusInfo.badgeClass">
            {{ productStatusInfo.label }}
          </span>
        </div>
      </div>

      <div class="card-body">
        <p class="info-text">
          {{ productStatusInfo.message }}
        </p>

        <div class="action-footer" dir="ltr">
          <BaseButton
            v-if="product.status !== 'active'"
            variant="success"
            size="md"
            :disabled="isChangingStatus"
            class="btn-status-change"
            @click="handlePublish"
          >
            {{ isChangingStatus ? 'در حال اعمال...' : 'انتشار محصول' }}
          </BaseButton>

          <BaseButton
            v-if="product.status !== 'draft'"
            variant="primary"
            size="md"
            :disabled="isChangingStatus"
            class="btn-status-change"
            @click="handleDraft"
          >
            {{ isChangingStatus ? 'در حال اعمال...' : 'انتقال به پیش‌نویس' }}
          </BaseButton>

          <BaseButton
            v-if="product.status !== 'inactive'"
            variant="warning"
            size="md"
            :disabled="isChangingStatus"
            class="btn-status-change"
            @click="handleInactive"
          >
            {{ isChangingStatus ? 'در حال اعمال...' : 'غیرفعال کردن محصول' }}
          </BaseButton>

          <BaseButton
            v-if="product.status !== 'archived'"
            variant="dark"
            size="md"
            :disabled="isChangingStatus"
            class="btn-status-change"
            @click="handleArchive"
          >
            {{ isChangingStatus ? 'در حال اعمال...' : 'بایگانی محصول' }}
          </BaseButton>
        </div>
      </div>
    </section>

    <section class="action-card danger-zone-box mt-4">
      <div class="danger-header">
        <h3 class="danger-title">عملیات خطرناک (Danger Zone)</h3>
        <p class="text-small text-danger">
          لطفاً با دقت انتخاب کنید. برخی از این عملیات‌ها غیرقابل بازگشت هستند.
        </p>
      </div>

      <div class="danger-actions-container">
        <div class="danger-action-row">
          <div class="action-info">
            <h4 class="action-name">انتقال به زباله‌دان (Soft Delete)</h4>
            <p class="action-desc">
              محصول از دید کاربران و لیست اصلی پنهان می‌شود اما همچنان در دیتابیس برای بازیابی
              احتمالی باقی می‌ماند.
            </p>
          </div>
          <BaseButton
            variant="warning"
            class="btn-action"
            :disabled="isSoftDeleteProduct"
            @click="handleSoftDelete"
          >
            {{ isSoftDeleteProduct ? 'در حال انتقال...' : 'انتقال به زباله‌دان' }}
          </BaseButton>
        </div>

        <div class="danger-action-row border-top">
          <div class="action-info">
            <h4 class="action-name text-hard-danger">حذف دائمی (Hard Delete)</h4>
            <p class="action-desc">
              محصول به همراه تمامی اطلاعات وابسته به طور کامل از سیستم پاک شده و
              <strong>هرگز قابل بازیابی نخواهد بود</strong>.
            </p>
          </div>
          <button class="btn-delete-hard" :disabled="isHardDeleteProduct" @click="handleHardDelete">
            {{ isHardDeleteProduct ? 'در حال حذف...' : 'حذف از پایگاه داده' }}
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { productService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { computed, inject, ref } from 'vue'
import { useRouter } from 'vue-router'

const product = inject('product')
const refreshProductData = inject('refreshProductData')
const router = useRouter()
const errorStore = useErrorStore()

const isChangingStatus = ref(false)
const isSoftDeleteProduct = ref(false)
const isHardDeleteProduct = ref(false)

// نمایش توضیحات هر حالت محصول
const productStatusInfo = computed(() => {
  const statuses = {
    active: {
      label: 'منتشر شده',
      badgeClass: 'badge-success',
      message: 'محصول در فروشگاه قابل مشاهده است.',
      actionText: 'غیرفعال کردن محصول',
      actionVariant: 'warning',
      nextStatus: 'inactive',
    },

    inactive: {
      label: 'غیرفعال',
      badgeClass: 'badge-warning',
      message: 'محصول برای کاربران نمایش داده نمی‌شود.',
      actionText: 'فعال‌سازی محصول',
      actionVariant: 'success',
      nextStatus: 'active',
    },

    archived: {
      label: 'بایگانی شده',
      badgeClass: 'badge-archive',
      message: 'محصول از چرخه فروش خارج شده است.',
      actionText: 'انتقال به پیش‌نویس',
      actionVariant: 'primary',
      nextStatus: 'draft',
    },

    draft: {
      label: 'پیش‌نویس',
      badgeClass: 'badge-draft',
      message: 'محصول هنوز منتشر نشده است.',
      actionText: 'انتشار محصول',
      actionVariant: 'success',
      nextStatus: 'active',
    },
  }

  return statuses[product.value.status] || statuses.draft
})

// ==============================
// انتشار نهایی محصول
// ==============================
async function handlePublish() {
  isChangingStatus.value = true
  try {
    await productService.publishProduct(product.value.id)
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'محصول با موفقیت منتشر شد.' })
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در انتشار محصول'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isChangingStatus.value = false
  }
}

// ==============================
// پیش‌نویس کردن محصول
// ==============================
const handleDraft = async () => {
  try {
    isChangingStatus.value = true
    await productService.patchProduct(product.value.id, { status: 'draft' })
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'محصول با موفقیت به پیش‌نویس منتقل شد.' })
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطایی در پیش‌نویس کردن محصول رخ داده است'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isChangingStatus.value = false
  }
}

// ==============================
// غیر فعال کردن محصول
// ==============================
const handleInactive = async () => {
  try {
    isChangingStatus.value = true
    await productService.patchProduct(product.value.id, { status: 'inactive' })
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'محصول با موفقیت غیرفعال شد.' })
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطایی در غیرفعال کردن محصول رخ داده است'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isChangingStatus.value = false
  }
}

// ==============================
// بایگانی کردن محصول
// ==============================
const handleArchive = async () => {
  try {
    isChangingStatus.value = true
    await productService.patchProduct(product.value.id, { status: 'archived' })
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'محصول با موفقیت بایگانی شد.' })
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطایی در بایگانی محصول رخ داده است'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isChangingStatus.value = false
  }
}

// ==============================
// حذف سخت محصول
// ==============================
async function handleHardDelete() {
  if (!confirm('این عملیات غیرقابل بازگشت است. ادامه می‌دهید؟')) return

  isHardDeleteProduct.value = true

  try {
    await productService.hardDelete(product.value.id)

    errorStore.addError({
      type: 'success',
      message: 'محصول برای همیشه حذف شد.',
    })

    router.push('/admin/products')
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code),
    })
  } finally {
    isHardDeleteProduct.value = false
  }
}

// ==============================
// حذف نرم محصول
// ==============================
async function handleSoftDelete() {
  if (!confirm('محصول به زباله‌دان منتقل شود؟')) return

  isSoftDeleteProduct.value = true

  try {
    await productService.softDelete(product.value.id)
    await refreshProductData()

    errorStore.addError({
      type: 'success',
      message: 'محصول به زباله‌دان منتقل شد.',
    })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code),
    })
  } finally {
    isSoftDeleteProduct.value = false
  }
}
</script>

<style scoped>
/* ==============================
   ساختار کلی
============================== */
.admin-actions-tab {
  text-align: right;
  direction: rtl;
  font-family: inherit;
  color: #334155;
}

.header-section {
  margin-bottom: 2rem;
}

.tab-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.4rem;
}

.text-muted {
  color: #64748b;
}
.text-small {
  font-size: 0.875rem;
  line-height: 1.5;
}
.mt-4 {
  margin-top: 1.5rem;
}

/* ==============================
   کارت‌های عملیات (بیس)
============================== */
.action-card {
  border-radius: 12px;
  padding: 1.5rem;
  background-color: #ffffff;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition: box-shadow 0.3s ease;
}

.action-card:hover {
  box-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.05),
    0 4px 6px -2px rgba(0, 0, 0, 0.025);
}

/* ==============================
   بخش وضعیت محصول
============================== */
.status-box {
  border: 1px solid #e2e8f0;
  background: linear-gradient(to bottom, #f8fafc, #ffffff);
}

.card-header {
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.card-title {
  font-weight: 600;
  font-size: 1.05rem;
  color: #1e293b;
}

.status-badge {
  padding: 0.4rem 1rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

/* رنگ‌های وضعیت (Badge) */
.badge-success {
  background: #dcfce7;
  color: #166534;
  box-shadow: 0 0 0 1px #bbf7d0 inset;
}
.badge-warning {
  background: #fef3c7;
  color: #92400e;
  box-shadow: 0 0 0 1px #fde68a inset;
}
.badge-draft {
  background: #e0e7ff;
  color: #3730a3;
  box-shadow: 0 0 0 1px #c7d2fe inset;
}
.badge-archive {
  background: #f1f5f9;
  color: #475569;
  box-shadow: 0 0 0 1px #e2e8f0 inset;
}

.info-text {
  color: #475569;
  line-height: 1.7;
  margin-bottom: 0;
  font-size: 0.95rem;
}

/* ==============================
  استایل جدید و بهبودیافته دکمه‌های وضعیت
  ==============================
*/
.action-footer {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.btn-status-change {
  width: 100%;
  transition: all 0.2s ease;
}

.btn-status-change:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* ==============================
   بخش منطقه خطر (Danger Zone)
============================== */
.danger-zone-box {
  background-color: #fffafb;
  border: 1px solid #fecaca;
}

.danger-header {
  margin-bottom: 1.5rem;
}

.danger-title {
  color: #b91c1c;
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 0.4rem;
}

.text-danger {
  color: #dc2626;
}
.text-hard-danger {
  color: #991b1b !important;
}

.danger-actions-container {
  display: flex;
  flex-direction: column;
}

.danger-action-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 0;
  gap: 1.5rem;
}

.border-top {
  border-top: 1px dashed #fca5a5;
}

.action-name {
  margin: 0 0 0.4rem 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 700;
}

.action-desc {
  margin: 0;
  color: #64748b;
  font-size: 0.85rem;
  line-height: 1.6;
}

/* دکمه‌های منطقه خطر */
.btn-action {
  min-width: 200px;
  flex-shrink: 0;
}

.btn-delete-hard {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 200px;
  flex-shrink: 0;
  height: 48px;
  padding: 0 1.35rem;
  border: none;
  border-radius: 999px;
  background: linear-gradient(135deg, #ef4444, #b91c1c);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.96rem;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(220, 38, 38, 0.2);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.btn-delete-hard:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 14px 24px rgba(220, 38, 38, 0.3);
}

.btn-delete-hard:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
  background: #f87171;
}

/* ==============================
   ریسپانسیو (موبایل)
============================== */
@media (max-width: 768px) {
  .danger-action-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .btn-action,
  .btn-delete-hard {
    width: 100%;
    min-width: auto;
  }
}
</style>
