<!-- src/views/admin/product-tabs/ImageTab.vue -->
<template>
  <div class="tab-content page-panel">
    <div class="header-section">
      <h2 class="tab-title">مدیریت تصاویر محصول</h2>
      <label class="btn-upload" :class="{ 'is-loading': isUploading }">
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
        <div v-if="isLoadingImages" class="loading-state">در حال دریافت تصاویر...</div>
        <template v-else>
          <img
            v-if="primaryImage"
            :src="primaryImage.real_url"
            :alt="primaryImage.alt_text || 'تصویر محصول'"
          />
          <div v-else class="no-image">هیچ تصویری برای این محصول آپلود نشده است</div>
          <div class="image-overlay-info">گالری تصاویر ({{ images.length }} عکس)</div>
        </template>
      </div>

      <div v-if="images.length > 0" class="thumb-grid mt-4">
        <div
          v-for="img in images"
          :key="img.id"
          class="thumb-container"
          :class="{ active: img.is_primary }"
        >
          <img :src="img.real_url" :alt="img.alt_text" />

          <div v-if="img.is_primary" class="primary-badge">اصلی</div>

          <div class="thumb-actions">
            <button
              v-if="!img.is_primary"
              class="action-btn btn-star"
              @click="setPrimaryImage(img.id)"
              title="انتخاب به عنوان تصویر اصلی"
            >
              ⭐
            </button>
            <button
              class="action-btn btn-edit"
              @click="editAltText(img)"
              title="ویرایش متن جایگزین (Alt Text)"
            >
              ✏️
            </button>
            <button class="action-btn btn-delete" @click="deleteImage(img.id)" title="حذف تصویر">
              🗑️
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

// ==============================
// دریافت دیتای اصلی از پوسته والد (Inject)
// ==============================
const product = inject('product')
const refreshProductData = inject('refreshProductData')
const errorStore = inject('errorStore')

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
  }
}

onMounted(() => {
  fetchImages()
})

// ==============================
// انتخاب تصویر اصلی محصول
// ==============================
const primaryImage = computed(() => {
  if (!images.value || images.value.length === 0) return null
  return images.value.find((img) => img.is_primary) || images.value[0]
})

// ۱. آپلود تصویر
const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  isUploading.value = true
  const formData = new FormData()
  formData.append('image', file)

  try {
    await imageService.uploadImage(product.value.id, formData)
    await fetchImages() // دریافت مجدد تصاویر
    await refreshProductData() // آپدیت اطلاعات پرنت در صورت نیاز
  } catch (error) {
    alert('خطا در آپلود تصویر جدید')
    console.error(error)
  } finally {
    isUploading.value = false
    event.target.value = '' // ریست کردن اینپوت
  }
}

// ۵. حذف تصویر
const deleteImage = async (imageId) => {
  if (!confirm('آیا از حذف این تصویر اطمینان دارید؟')) return
  try {
    await imageService.deleteImage(imageId)
    await fetchImages()
    await refreshProductData()
  } catch (error) {
    console.error('خطا در حذف تصویر:', error)
    alert('حذف تصویر با خطا مواجه شد.')
  }
}

// ۴. به‌روزرسانی تصویر (تنظیم به عنوان اصلی)
const setPrimaryImage = async (imageId) => {
  try {
    await imageService.updateImage(imageId, { is_primary: true })
    await fetchImages()
    await refreshProductData()
  } catch (error) {
    console.error('خطا در تنظیم تصویر اصلی:', error)
  }
}

// ۴. به‌روزرسانی تصویر (ویرایش Alt Text)
const editAltText = async (img) => {
  const currentAlt = img.alt_text || ''
  const newAlt = prompt('متن جایگزین (Alt Text) مناسب برای سئو را وارد کنید:', currentAlt)

  if (newAlt !== null && newAlt !== currentAlt) {
    try {
      await imageService.updateImage(img.id, { alt_text: newAlt })
      await fetchImages()
    } catch (error) {
      console.error('خطا در ویرایش متن جایگزین:', error)
      alert('خطا در ذخیره متن جایگزین.')
    }
  }
}
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

.thumb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
}

.thumb-container {
  position: relative;
  aspect-ratio: 1;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  transition: all 0.2s ease;
}

.thumb-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

/* افکت Hover برای نمایش دکمه‌های روی تصویر کوچک */
.thumb-actions {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.thumb-container:hover .thumb-actions {
  opacity: 1;
}

.action-btn {
  background: white;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  transition:
    transform 0.2s ease,
    background 0.2s;
}

.action-btn:hover {
  transform: scale(1.1);
}

.btn-delete:hover {
  background: #fee2e2;
}
.btn-edit:hover {
  background: #e0f2fe;
}
.btn-star:hover {
  background: #fef08a;
}

.mt-4 {
  margin-top: 1rem;
}
</style>
