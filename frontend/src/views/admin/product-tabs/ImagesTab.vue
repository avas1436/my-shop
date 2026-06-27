<!-- src/views/admin/product-tabs/ImagesTab.vue -->
<template>
  <div class="grid gap-6">
    <!-- هدر -->
    <div class="flex items-center justify-between gap-4 border-b border-border-light pb-4">
      <h2 class="m-0 text-[1.25rem] font-bold">مدیریت تصاویر محصول</h2>
      <label
        class="inline-flex items-center gap-2 px-4 py-2 rounded-md font-bold cursor-pointer transition-all duration-200 select-none"
        :class="
          isUploading
            ? 'bg-slate-400 text-white cursor-not-allowed'
            : 'bg-primary text-white hover:bg-primary-dark active:scale-[0.98]'
        "
      >
        <component
          :is="isUploading ? Loader2Icon : UploadIcon"
          class="w-4 h-4"
          :class="{ 'animate-spin': isUploading }"
        />
        {{ isUploading ? 'در حال آپلود...' : 'آپلود تصویر جدید' }}
        <input
          type="file"
          accept="image/*"
          hidden
          :disabled="isUploading"
          @change="handleImageUpload"
        />
      </label>
    </div>

    <!-- گالری -->
    <div class="grid gap-6">
      <!-- تصویر اصلی -->
      <div
        class="relative w-full h-87.5 border-2 border-dashed border-border-strong rounded-xl flex items-center justify-center bg-bg-muted overflow-hidden"
      >
        <div v-if="isLoadingImages" class="text-center text-text-muted font-medium">
          <Loader2Icon class="w-5 h-5 animate-spin mx-auto mb-2" />
          در حال دریافت تصاویر...
        </div>
        <template v-else>
          <img
            v-if="primaryImage"
            :src="primaryImage.real_url"
            :alt="primaryImage.alt_text || 'تصویر محصول'"
            class="max-w-full max-h-full object-contain transition-transform duration-300"
          />
          <div v-else class="text-center text-text-muted">
            <ImageMinusIcon class="w-12 h-12 mx-auto mb-2 opacity-40" />
            <p class="m-0 font-medium">هیچ تصویری برای این محصول آپلود نشده است</p>
          </div>
          <div
            class="absolute bottom-0 w-full bg-linear-to-t from-slate-900/70 to-transparent text-white text-center text-[0.95rem] font-medium py-3 px-2"
          >
            گالری تصاویر ({{ images.length }} عکس)
          </div>
        </template>
      </div>

      <!-- thumbnail ها -->
      <div
        v-if="sortedImages.length"
        class="grid grid-cols-[repeat(auto-fill,minmax(100px,100px))] gap-4"
      >
        <div
          v-for="img in sortedImages"
          :key="img.id"
          class="relative overflow-hidden rounded-xl cursor-pointer border-2 transition-all duration-200 group"
          :class="
            img.is_primary
              ? 'border-primary shadow-[0_0_0_3px_rgba(91,61,245,0.2)]'
              : 'border-transparent hover:shadow-[0_8px_24px_rgba(15,23,42,0.15)]'
          "
          @click.stop="selectedImage = img"
        >
          <img
            :src="img.real_url"
            :alt="img.alt_text"
            class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />

          <!-- badge تصویر اصلی -->
          <div
            v-if="img.is_primary"
            class="absolute top-1.5 left-1.5 flex items-center gap-1 bg-primary text-white text-[0.7rem] font-bold px-1.5 py-0.5 rounded"
          >
            <StarIcon class="w-3 h-3 fill-current" />
            اصلی
          </div>

          <!-- دکمه‌های hover -->
          <div
            class="absolute inset-0 flex items-center justify-center gap-3 bg-slate-900/55 backdrop-blur-xs opacity-0 translate-y-2 scale-[0.96] group-hover:opacity-100 group-hover:translate-y-0 group-hover:scale-100 transition-all duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]"
          >
            <button
              v-if="!img.is_primary"
              type="button"
              title="تصویر اصلی"
              class="w-6 h-6 flex items-center justify-center rounded-md bg-transparent text-slate-200 border-0 transition-all duration-200 hover:bg-yellow-400/15 hover:text-yellow-300 hover:-translate-y-0.5"
              @click.stop="setPrimaryImage(img.id)"
            >
              <StarIcon class="w-3.5 h-3.5" />
            </button>
            <button
              type="button"
              title="ویرایش Alt"
              class="w-6 h-6 flex items-center justify-center rounded-md bg-transparent text-slate-200 border-0 transition-all duration-200 hover:bg-blue-400/15 hover:text-blue-300 hover:-translate-y-0.5"
              @click.stop="editAltText(img)"
            >
              <PencilIcon class="w-3.5 h-3.5" />
            </button>
            <button
              type="button"
              title="حذف"
              class="w-6 h-6 flex items-center justify-center rounded-md bg-transparent text-slate-200 border-0 transition-all duration-200 hover:bg-red-400/15 hover:text-red-300 hover:-translate-y-0.5"
              @click.stop="deleteImage(img.id)"
            >
              <Trash2Icon class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { imageService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import {
  ImageMinus as ImageMinusIcon,
  Loader2 as Loader2Icon,
  Pencil as PencilIcon,
  Star as StarIcon,
  Trash2 as Trash2Icon,
  Upload as UploadIcon,
} from '@lucide/vue'
import { computed, inject, onMounted, ref } from 'vue'

const errorStore = useErrorStore()
const product = inject('product')

const images = ref([])
const isUploading = ref(false)
const isLoadingImages = ref(false)
const selectedImage = ref(null)

const fetchImages = async () => {
  if (!product.value?.id) return
  isLoadingImages.value = true
  try {
    images.value = await imageService.listImages(product.value.id)
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || error.message || 'خطا در دریافت لیست تصاویر',
    })
  } finally {
    isLoadingImages.value = false
    selectedImage.value = null
  }
}

onMounted(fetchImages)

const primaryImage = computed(() => {
  if (selectedImage.value) return selectedImage.value
  if (!images.value?.length) return null
  return images.value.find((img) => img.is_primary) ?? images.value[0]
})

const sortedImages = computed(() => {
  if (!images.value?.length) return []
  return [...images.value].sort((a, b) => {
    if (a.is_primary !== b.is_primary) return a.is_primary ? -1 : 1
    return (a.sort_order || 0) - (b.sort_order || 0)
  })
})

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  isUploading.value = true
  const formData = new FormData()
  formData.append('file', file)
  formData.append('alt_text', '')
  formData.append('is_primary', '')
  formData.append('sort_order', '')
  try {
    await imageService.uploadImage(product.value.id, formData)
    await fetchImages()
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در آپلود تصویر جدید',
    })
  } finally {
    isUploading.value = false
    event.target.value = ''
  }
}

const deleteImage = async (imageId) => {
  if (!confirm('آیا از حذف این تصویر اطمینان دارید؟')) return
  try {
    await imageService.deleteImage(imageId)
    await fetchImages()
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'حذف تصویر با خطا مواجه شد.',
    })
  }
}

const setPrimaryImage = async (imageId) => {
  try {
    await imageService.updateImage(imageId, { is_primary: true })
    await fetchImages()
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در تنظیم تصویر اصلی',
    })
  }
}

const editAltText = async (img) => {
  const newAlt = prompt('متن جایگزین (Alt Text) مناسب برای سئو را وارد کنید:', img.alt_text || '')
  if (newAlt !== null && newAlt !== img.alt_text) {
    try {
      await imageService.updateImage(img.id, { alt_text: newAlt })
      await fetchImages()
    } catch (error) {
      errorStore.addError({
        type: 'error',
        message: getErrorMessage(error.code) || 'خطا در ذخیره متن جایگزین.',
      })
    }
  }
}
</script>
