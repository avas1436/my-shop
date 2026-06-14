<!-- src/views/admin/product-tabs/ImageTab.vue -->
<template>
  <div class="tab-content page-panel">
    <h2 class="tab-title">مدیریت تصاویر محصول</h2>
    <div class="admin-gallery-wrapper">
      <div class="main-image-holder">
        <img v-if="primaryImage" :src="primaryImage.real_url" :alt="primaryImage.alt_text" />
        <div v-else class="no-image">هیچ تصویری آپلود نشده است</div>
        <div class="image-overlay-info">گالری تصاویر ({{ product.images?.length || 0 }} عکس)</div>
      </div>

      <div class="upload-section mt-3">
        <label class="btn-upload">
          آپلود تصویر جدید
          <input type="file" @change="handleImageUpload" accept="image/*" hidden />
        </label>
      </div>

      <div class="thumb-strip mt-3">
        <div v-for="img in product.images" :key="img.id" class="thumb-container">
          <img
            :src="img.real_url"
            :class="{ active: img.is_primary }"
            @click="setPrimaryImage(img.id)"
            title="انتخاب به عنوان تصویر اصلی"
          />
          <button class="btn-remove-img" @click.stop="deleteImage(img.id)">×</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { productService } from '@/services/productService'
import { computed, inject } from 'vue'

const product = inject('product')
const refreshProductData = inject('refreshProductData')

const primaryImage = computed(() => {
  if (!product.value?.images) return null
  return product.value.images.find((img) => img.is_primary) || product.value.images[0]
})

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  const formData = new FormData()
  formData.append('image', file)
  try {
    await productService.uploadProductImage(product.value.id, formData)
    await refreshProductData()
  } catch (error) {
    alert('خطا در آپلود تصویر جدید')
  }
}

const deleteImage = async (imageId) => {
  if (!confirm('آیا مایل به حذف این تصویر هستید؟')) return
  try {
    await productService.deleteProductImage(product.value.id, imageId)
    await refreshProductData()
  } catch (error) {
    console.error(error)
  }
}

const setPrimaryImage = async (imageId) => {
  try {
    await productService.setPrimaryImage(product.value.id, imageId)
    await refreshProductData()
  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>
.admin-gallery-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.main-image-holder {
  position: relative;
  width: 100%;
  max-width: 400px;
  height: 300px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
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
}
.no-image {
  color: #94a3b8;
  font-weight: bold;
}
.image-overlay-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 0.5rem;
  text-align: center;
  font-size: 0.9rem;
}
.btn-upload {
  background: #5b3df5;
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  display: inline-block;
  font-weight: 600;
}
.thumb-strip {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1rem;
  justify-content: center;
}
.thumb-container {
  position: relative;
  width: 80px;
  height: 80px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
}
.thumb-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.thumb-container img.active {
  border: 3px solid #5b3df5;
}
.btn-remove-img {
  position: absolute;
  top: 2px;
  right: 2px;
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
