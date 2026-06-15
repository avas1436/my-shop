<!-- src/views/admin/product-tabs/ImageTab.vue -->
<template>
  <div class="tab-content page-panel">
    <div class="header-section">
      <h2 class="tab-title">مدیریت تصاویر محصول</h2>
      <label class="btn-upload" :class="{ 'is-loading': isUploading }">
        <component
          :is="isUploading ? Loader2Icon : UploadIcon"
          class="w-4 h-4 icon-left"
          :class="{ 'animate-spin': isUploading }"
        />
        {{ isUploading ? 'در حال آپلود...' : 'آپلود تصویر جدید' }}
        <input
          type="file"
          @change="handleImageUpload"
          accept="image/*"
          hidden
          :disabled="isUploading"
        />
      </label>
    </div>

    <div class="admin-gallery-wrapper">
      <div class="main-image-holder">
        <div v-if="isLoadingImages" class="loading-state">
          <Loader2Icon class="w-5 h-5 animate-spin mx-auto mb-2" />
          در حال دریافت تصاویر...
        </div>
        <template v-else>
          <img
            v-if="primaryImage"
            :src="primaryImage.real_url"
            :alt="primaryImage.alt_text || 'تصویر محصول'"
          />
          <div v-else class="no-image">
            <ImageMinusIcon class="w-12 h-12 text-gray-400 mb-2 mx-auto" />
            <p>هیچ تصویری برای این محصول آپلود نشده است</p>
          </div>
          <div class="image-overlay-info">گالری تصاویر ({{ images.length }} عکس)</div>
        </template>
      </div>

      <div v-if="sortedImages.length > 0" class="thumb-grid">
        <div
          v-for="img in sortedImages"
          :key="img.id"
          class="thumb-container"
          :class="{ active: img.is_primary }"
          @click.stop="selectedImage = img"
          style="cursor: pointer"
        >
          <img :src="img.real_url" :alt="img.alt_text" />

          <div v-if="img.is_primary" class="primary-badge">
            <StarIcon class="w-3 h-3 fill-current icon-left" />
            اصلی
          </div>

          <div class="thumb-actions">
            <button
              v-if="!img.is_primary"
              class="action-btn btn-star"
              @click.stop="setPrimaryImage(img.id)"
              title="انتخاب به عنوان تصویر اصلی"
            >
              <StarIcon class="w-4 h-4" />
            </button>
            <button
              class="action-btn btn-edit"
              @click.stop="editAltText(img)"
              title="ویرایش متن جایگزین (Alt Text)"
            >
              <PencilIcon class="w-4 h-4" />
            </button>
            <button
              class="action-btn btn-delete"
              @click.stop="deleteImage(img.id)"
              title="حذف تصویر"
            >
              <Trash2Icon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue'

import { imageService } from '@/services/productService'
import { getErrorMessage } from '@/utils/errorMessages'

// آیکون‌های مورد نیاز از Lucide
import { useErrorStore } from '@/stores/errorStore'
import {
  ImageMinus as ImageMinusIcon,
  Loader2 as Loader2Icon,
  Pencil as PencilIcon,
  Star as StarIcon,
  Trash2 as Trash2Icon,
  Upload as UploadIcon,
} from '@lucide/vue'

const errorStore = useErrorStore()

// ==============================
// دریافت دیتای اصلی از پوسته والد (Inject)
// ==============================
const product = inject('product')

// State های داخلی
const images = ref([])
const isUploading = ref(false)
const isLoadingImages = ref(false)

// ==============================
// دریافت لیست تصاویر از سرور
// ==============================
const fetchImages = async () => {
  if (!product.value?.id) return
  isLoadingImages.value = true
  try {
    const response = await imageService.listImages(product.value.id)
    images.value = response
  } catch (error) {
    const msg = getErrorMessage(error.code) || error.message || 'خطا در دریافت لیست تصاویر'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isLoadingImages.value = false
    selectedImage.value = null
  }
}

onMounted(() => {
  fetchImages()
})

// ==============================
// انتخاب تصویر اصلی محصول
// ==============================
const selectedImage = ref(null)

const primaryImage = computed(() => {
  if (selectedImage.value) return selectedImage.value

  if (!images.value || images.value.length === 0) return null

  return images.value.find((img) => img.is_primary) || images.value[0]
})

// ==============================
// آپلود تصویر
// ==============================
const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  isUploading.value = true

  // ایجاد فروم دیتا دقیقاً مطابق با ورودی‌های Form در بک‌اند
  const formData = new FormData()

  // کلید فایل باید 'file' باشد چون در بک‌اند نوشتی file: UploadFile
  formData.append('file', file)

  // ارسال بقیه موارد به صورت خالی
  formData.append('alt_text', '')
  formData.append('is_primary', '')
  formData.append('sort_order', '')

  try {
    await imageService.uploadImage(product.value.id, formData)
    await fetchImages() // دریافت مجدد تصاویر
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در آپلود تصویر جدید'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isUploading.value = false
    event.target.value = '' // ریست کردن اینپوت
  }
}

// ==============================
// حذف تصویر
// ==============================
const deleteImage = async (imageId) => {
  if (!confirm('آیا از حذف این تصویر اطمینان دارید؟')) return
  try {
    await imageService.deleteImage(imageId)
    await fetchImages()
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'حذف تصویر با خطا مواجه شد.'
    errorStore.addError({ type: 'error', message: msg })
  }
}

// ==============================
// انتخاب یک عکس به عنوان عکس اصلی
// ==============================
const setPrimaryImage = async (imageId) => {
  try {
    await imageService.updateImage(imageId, { is_primary: true })
    await fetchImages()
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در تنظیم تصویر اصلی'
    errorStore.addError({ type: 'error', message: msg })
  }
}

// ==============================
// ویرایش متن توضیحی عکس
// ==============================
const editAltText = async (img) => {
  const currentAlt = img.alt_text || ''
  const newAlt = prompt('متن جایگزین (Alt Text) مناسب برای سئو را وارد کنید:', currentAlt)

  if (newAlt !== null && newAlt !== currentAlt) {
    try {
      await imageService.updateImage(img.id, { alt_text: newAlt })
      await fetchImages()
    } catch (error) {
      const msg = getErrorMessage(error.code) || 'خطا در ذخیره متن جایگزین.'
      errorStore.addError({ type: 'error', message: msg })
    }
  }
}

// =========================================================
// مرتب‌سازی تصاویر بر اساس فیلد
// =========================================================
const sortedImages = computed(() => {
  if (!images.value) return []

  return [...images.value].sort((a, b) => {
    // تصویر اصلی همیشه در ابتدای لیست قرار بگیرد
    if (a.is_primary && !b.is_primary) return -1
    if (!a.is_primary && b.is_primary) return 1

    // مرتب‌سازی صعودی بر اساس sort_order
    return (a.sort_order || 0) - (b.sort_order || 0)
  })
})
</script>

<style scoped>
.page-panel {
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 1rem;
}

.tab-title {
  margin: 0;
  font-size: 1.25rem;
  color: #1e293b;
  font-weight: bold;
}

.admin-gallery-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.main-image-holder {
  position: relative;
  width: 100%;
  height: 350px;
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  overflow: hidden;
}

.main-image-holder img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.no-image,
.loading-state {
  color: #64748b;
  font-weight: 500;
  font-size: 1.1rem;
}

.image-overlay-info {
  position: absolute;
  bottom: 0;
  width: 100%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  color: white;
  padding: 1rem 0.5rem 0.5rem;
  text-align: center;
  font-size: 0.95rem;
  font-weight: 500;
}

.btn-upload {
  background: #4f46e5;
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition:
    background-color 0.2s,
    transform 0.1s;
  display: inline-block;
}

.btn-upload:hover {
  background: #4338ca;
}

.btn-upload:active {
  transform: scale(0.98);
}

.btn-upload.is-loading {
  background: #94a3b8;
  cursor: not-allowed;
}

/* شبکه تصاویر کوچک در سمت چپ */
.thumb-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 100px));
  gap: 1rem;
  margin-top: 0 !important;
}

.thumb-container {
  position: relative;
  overflow: hidden;
  border-radius: 12px;

  transition: all 0.25s ease;
}

.thumb-container img {
  transition: transform 0.3s ease;
}

.thumb-container:hover img {
  transform: scale(1.05);
}

.thumb-container:hover {
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.15);
}

.thumb-container.active {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
}

.primary-badge {
  position: absolute;
  top: 6px;
  left: 6px;
  background: #4f46e5;
  color: white;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-weight: bold;
}

.thumb-actions {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(4px);

  color: #fff;
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;

  opacity: 0;
  transform: translateY(8px) scale(0.96);

  transition:
    opacity 0.3s ease,
    transform 0.3s cubic-bezier(0.22, 1, 0.36, 1),
    backdrop-filter 0.3s ease;
}

.thumb-container:hover .thumb-actions {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.thumb-actions button:hover {
  background: rgba(255, 255, 255, 0.22);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px) scale(1.08);
}

.action-btn {
  width: 24px;
  height: 24px;

  border: none;
  border-radius: 6px;

  background: transparent;
  color: #e2e8f0;

  display: flex;
  align-items: center;
  justify-content: center;

  transition: all 0.2s ease;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

.action-btn:hover {
  transform: scale(1.1);
}

.btn-star:hover {
  background: rgba(250, 204, 21, 0.15);
  color: #facc15;
}

.btn-edit:hover {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.mt-4 {
  margin-top: 1rem;
}

.icon-left {
  margin-left: 0.5rem;
  display: inline-block;
  vertical-align: middle;
}
.animate-spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* ریسپانسیو برای موبایل */
@media (max-width: 768px) {
  .admin-gallery-wrapper {
    flex-direction: column; /* زیر هم قرار گرفتن در نمایشگرهای کوچک */
  }
  .main-image-holder {
    max-width: 100%;
  }
}
</style>
