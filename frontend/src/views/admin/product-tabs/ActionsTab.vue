<!-- src/views/admin/product-tabs/ActionsTab.vue -->
<template>
  <div class="grid gap-5">
    <!-- هدر -->
    <div class="border-b border-border-light pb-4">
      <h2 class="m-0 text-[1.4rem] font-bold">تنظیمات وضعیت و عملیات نهایی</h2>
      <p class="m-0 mt-1.5 text-sm text-text-muted">
        مدیریت نمایش محصول در فروشگاه و دسترسی به عملیات‌های حساس پایگاه داده.
      </p>
    </div>

    <!-- ─── کارت وضعیت ─── -->
    <section
      class="rounded-xl border border-border-light bg-linear-to-b from-bg-muted to-white shadow-(--shadow-soft) p-5 grid gap-5"
    >
      <!-- وضعیت فعلی -->
      <div class="flex flex-wrap items-center gap-3 pb-4 border-b border-border-light">
        <span class="font-bold text-[1.05rem]">وضعیت نمایش فعلی:</span>
        <span
          class="px-3 py-1.5 rounded-full text-[0.85rem] font-bold"
          :class="productStatusInfo.badgeClass"
        >
          {{ productStatusInfo.label }}
        </span>
      </div>

      <p class="m-0 text-[0.95rem] text-text-muted leading-relaxed">
        {{ productStatusInfo.message }}
      </p>

      <!-- دکمه‌های تغییر وضعیت -->
      <div class="grid grid-cols-3 gap-3 pt-1">
        <BaseButton
          v-if="product.status !== 'active'"
          variant="success"
          size="md"
          block
          :disabled="isChangingStatus"
          @click="handlePublish"
        >
          {{ isChangingStatus ? 'در حال اعمال...' : 'انتشار محصول' }}
        </BaseButton>

        <BaseButton
          v-if="product.status !== 'draft'"
          variant="primary"
          size="md"
          block
          :disabled="isChangingStatus"
          @click="handleDraft"
        >
          {{ isChangingStatus ? 'در حال اعمال...' : 'انتقال به پیش‌نویس' }}
        </BaseButton>

        <BaseButton
          v-if="product.status !== 'inactive'"
          variant="warning"
          size="md"
          block
          :disabled="isChangingStatus"
          @click="handleInactive"
        >
          {{ isChangingStatus ? 'در حال اعمال...' : 'غیرفعال کردن' }}
        </BaseButton>

        <BaseButton
          v-if="product.status !== 'archived'"
          variant="secondary"
          size="md"
          block
          :disabled="isChangingStatus"
          @click="handleArchive"
        >
          {{ isChangingStatus ? 'در حال اعمال...' : 'بایگانی محصول' }}
        </BaseButton>
      </div>
    </section>

    <!-- ─── Danger Zone ─── -->
    <section class="rounded-xl border border-red-200 bg-red-50/40 p-5 grid gap-5">
      <div>
        <h3 class="m-0 text-[1.2rem] font-extrabold text-red-700">عملیات خطرناک (Danger Zone)</h3>
        <p class="m-0 mt-1 text-sm text-danger">
          لطفاً با دقت انتخاب کنید. برخی از این عملیات‌ها غیرقابل بازگشت هستند.
        </p>
      </div>

      <!-- Soft Delete -->
      <div
        class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-dashed border-red-200"
      >
        <div class="grid gap-1">
          <h4 class="m-0 text-[1rem] font-bold text-text-main">
            انتقال به زباله‌دان (Soft Delete)
          </h4>
          <p class="m-0 text-sm text-text-muted leading-relaxed">
            محصول از دید کاربران پنهان می‌شود اما در دیتابیس برای بازیابی احتمالی باقی می‌ماند.
          </p>
        </div>
        <BaseButton
          variant="warning"
          class="shrink-0 sm:min-w-45"
          :disabled="isSoftDeleteProduct"
          @click="handleSoftDelete"
        >
          {{ isSoftDeleteProduct ? 'در حال انتقال...' : 'انتقال به زباله‌دان' }}
        </BaseButton>
      </div>

      <!-- Hard Delete -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div class="grid gap-1">
          <h4 class="m-0 text-[1rem] font-bold text-red-800">حذف دائمی (Hard Delete)</h4>
          <p class="m-0 text-sm text-text-muted leading-relaxed">
            محصول به همراه تمامی اطلاعات وابسته از سیستم پاک شده و
            <strong class="text-red-700">هرگز قابل بازیابی نخواهد بود</strong>.
          </p>
        </div>
        <button
          class="shrink-0 sm:min-w-45 inline-flex items-center justify-center h-12 px-5 rounded-full font-bold text-[0.96rem] text-white bg-linear-to-br from-red-500 to-red-700 shadow-[0_10px_20px_rgba(220,38,38,0.2)] transition-all duration-200 hover:shadow-[0_14px_24px_rgba(220,38,38,0.3)] hover:-translate-y-px disabled:opacity-60 disabled:cursor-not-allowed disabled:translate-y-0 disabled:shadow-none"
          :disabled="isHardDeleteProduct"
          @click="handleHardDelete"
        >
          {{ isHardDeleteProduct ? 'در حال حذف...' : 'حذف از پایگاه داده' }}
        </button>
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

const productStatusInfo = computed(() => {
  const statuses = {
    active: {
      label: 'منتشر شده',
      badgeClass: 'bg-emerald-100 text-emerald-800 shadow-[inset_0_0_0_1px_#bbf7d0]',
      message: 'محصول در فروشگاه قابل مشاهده است و کاربران می‌توانند آن را خریداری کنند.',
    },
    inactive: {
      label: 'غیرفعال',
      badgeClass: 'bg-amber-100 text-amber-800 shadow-[inset_0_0_0_1px_#fde68a]',
      message: 'محصول برای کاربران نمایش داده نمی‌شود و از فروشگاه پنهان است.',
    },
    archived: {
      label: 'بایگانی شده',
      badgeClass: 'bg-slate-100 text-slate-600 shadow-[inset_0_0_0_1px_#e2e8f0]',
      message: 'محصول از چرخه فروش خارج شده و در بایگانی قرار دارد.',
    },
    draft: {
      label: 'پیش‌نویس',
      badgeClass: 'bg-indigo-100 text-indigo-800 shadow-[inset_0_0_0_1px_#c7d2fe]',
      message: 'محصول هنوز منتشر نشده است و فقط برای مدیران قابل مشاهده است.',
    },
  }
  return statuses[product.value.status] ?? statuses.draft
})

async function handlePublish() {
  isChangingStatus.value = true
  try {
    await productService.publishProduct(product.value.id)
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'محصول با موفقیت منتشر شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در انتشار محصول',
    })
  } finally {
    isChangingStatus.value = false
  }
}

async function handleDraft() {
  isChangingStatus.value = true
  try {
    await productService.patchProduct(product.value.id, { status: 'draft' })
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'محصول با موفقیت به پیش‌نویس منتقل شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در پیش‌نویس کردن محصول',
    })
  } finally {
    isChangingStatus.value = false
  }
}

async function handleInactive() {
  isChangingStatus.value = true
  try {
    await productService.patchProduct(product.value.id, { status: 'inactive' })
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'محصول با موفقیت غیرفعال شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در غیرفعال کردن محصول',
    })
  } finally {
    isChangingStatus.value = false
  }
}

async function handleArchive() {
  isChangingStatus.value = true
  try {
    await productService.patchProduct(product.value.id, { status: 'archived' })
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'محصول با موفقیت بایگانی شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در بایگانی محصول',
    })
  } finally {
    isChangingStatus.value = false
  }
}

async function handleHardDelete() {
  if (!confirm('این عملیات غیرقابل بازگشت است. ادامه می‌دهید؟')) return
  isHardDeleteProduct.value = true
  try {
    await productService.hardDelete(product.value.id)
    errorStore.addError({ type: 'success', message: 'محصول برای همیشه حذف شد.' })
    router.push('/admin/products')
  } catch (error) {
    errorStore.addError({ type: 'error', message: getErrorMessage(error.code) })
  } finally {
    isHardDeleteProduct.value = false
  }
}

async function handleSoftDelete() {
  if (!confirm('محصول به زباله‌دان منتقل شود؟')) return
  isSoftDeleteProduct.value = true
  try {
    await productService.softDelete(product.value.id)
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'محصول به زباله‌دان منتقل شد.' })
  } catch (error) {
    errorStore.addError({ type: 'error', message: getErrorMessage(error.code) })
  } finally {
    isSoftDeleteProduct.value = false
  }
}
</script>
