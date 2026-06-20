<!-- src/views/admin/product-tabs/RelationsTab.vue -->
<template>
  <div class="tab-content admin-secondary-layout">
    <section class="page-panel admin-settings-panel mb-4">
      <h3 class="specs-heading">مدیریت و اتصال دسته‌بندی‌ها</h3>

      <div v-if="isLoadingCategories" class="text-sm text-gray-500 mb-2">
        در حال دریافت مسیر دسته‌بندی‌ها...
      </div>

      <div class="category-paths-list mb-3">
        <div v-if="selectedCategories.length === 0" class="text-sm text-gray-500">
          هیچ دسته‌بندی برای این محصول انتخاب نشده است.
        </div>
        <div v-for="cat in selectedCategories" :key="cat.id" class="category-path-item">
          <span class="path-text">
            <template v-if="productCategoriesPaths[cat.id]">
              <span v-for="(parent, idx) in productCategoriesPaths[cat.id]" :key="idx">
                {{ parent.name || parent.title }}
                <span class="path-separator"> / </span>
              </span>
            </template>
            <strong class="current-cat-name">{{ cat.name || cat.title }}</strong>
          </span>
          <button
            class="btn-icon-danger-sm"
            @click.stop="handleDetachCategories(cat.id)"
            title="حذف از لیست"
          >
            <Trash2Icon class="w-4 h-4" />
          </button>
        </div>
      </div>

      <div class="form-group relative-search-container">
        <label>جستجو و افزودن دسته‌بندی:</label>
        <div class="single-input-wrapper">
          <BaseInput
            v-model="categorySearchQuery"
            type="text"
            placeholder="بخشی از نام کتگوری را تایپ کنید..."
            class="base-input-field"
          />
          <BaseButton
            v-if="categorySearchQuery"
            type="button"
            class="clear-btn"
            @click="categorySearchQuery = ''"
          >
            ×
          </BaseButton>
        </div>

        <p v-if="isSearchingCategory" class="search-loading">در حال جستجو...</p>

        <ul
          v-if="categorySearchQuery && searchedCategories.length && !isSearchingCategory"
          class="search-results-dropdown"
        >
          <li
            v-for="category in searchedCategories"
            :key="category.id"
            @click="addCategoryToSelection(category)"
            class="clickable-list-item"
            :class="{ 'already-selected': isCategorySelected(category.id) }"
          >
            {{ category.name || category.title }}
            <span v-if="isCategorySelected(category.id)" class="text-xs text-green-600"
              >(انتخاب شده)</span
            >
          </li>
        </ul>

        <p
          v-if="categorySearchQuery && !searchedCategories.length && !isSearchingCategory"
          class="no-results"
        >
          کتگوری یافت نشد.
        </p>
      </div>

      <div class="mt-4">
        <button class="btn-primary" @click="handleSyncCategories" :disabled="isSyncing">
          {{ isSyncing ? 'در حال ذخیره...' : 'ذخیره و همگام‌سازی دسته‌بندی‌ها' }}
        </button>
      </div>
    </section>

    <section class="page-panel admin-settings-panel mb-4">
      <h3 class="specs-heading">تگ‌ها / برچسب‌ها</h3>
      <div class="checkbox-list">
        <label v-for="tag in allTags" :key="tag.id" class="checkbox-item">
          <input
            type="checkbox"
            :checked="isTagAttached(tag.id)"
            @change="toggleTag($event, tag.id)"
          />
          {{ tag.name }}
        </label>
      </div>
    </section>

    <section class="page-panel admin-settings-panel">
      <h3 class="specs-heading">ویژگی‌های فنی محصول (Specifications)</h3>
      <ul class="admin-specs-list">
        <li v-for="attr in product.attributes" :key="attr.attribute_id">
          <strong>{{ attr.name }}:</strong>
          <input
            type="text"
            v-model="attr.value"
            @change="patchAttribute(attr.attribute_id, attr.value)"
            class="spec-inline-input"
          />
          <button class="btn-icon-danger" @click="removeAttribute(attr.attribute_id)">×</button>
        </li>
      </ul>

      <div class="add-attribute-form mt-3">
        <select v-model="newAttribute.id" class="base-input-field">
          <option value="" disabled>انتخاب نام ویژگی...</option>
          <option v-for="a in availableAttributesList" :key="a.id" :value="a.id">
            {{ a.name }}
          </option>
        </select>
        <input
          v-model="newAttribute.value"
          type="text"
          placeholder="مقدار ویژگی..."
          class="base-input-field"
        />
        <button class="btn-add" @click="addAttribute">افزودن</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { categoryService, productService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { Trash2Icon } from '@lucide/vue'
import { inject, ref, watch } from 'vue'

const product = inject('product')
const refreshProductData = inject('refreshProductData')
const errorStore = useErrorStore()

// ==============================
// State های مربوط به دسته‌بندی
// ==============================
const selectedCategories = ref([])
const isLoadingCategories = ref(false)
const productCategoriesPaths = ref({})
const isSyncing = ref(false)

// State های جستجو
const categorySearchQuery = ref('')
const searchedCategories = ref([])
const isSearchingCategory = ref(false)
let searchTimeout = null

// مقداردهی اولیه دسته‌بندی‌های انتخاب‌شده بر اساس دیتای محصول
watch(
  () => product.value?.categories,
  (newCats) => {
    if (newCats) {
      // ایجاد یک کپی از دسته‌بندی‌های محصول برای ویرایش محلی
      selectedCategories.value = [...newCats]
    }
  },
  { immediate: true, deep: true },
)

// دریافت والدهای دسته‌بندی‌های انتخاب شده
watch(
  () => selectedCategories.value,
  async (newCats) => {
    if (!newCats || !newCats.length) return

    isLoadingCategories.value = true
    for (const cat of newCats) {
      try {
        if (productCategoriesPaths.value[cat.id]) continue
        const response = await categoryService.categoryParents(cat.id)

        // ساخت مپ برای جستجوی سریع تر
        const map = new Map(response.map((item) => [item.id, item]))

        // کتگوری ریشه
        let current = response.find((i) => i.parent_id === null)

        // یک لیست برای مرتب کردن کتگوری ها
        const ordered = []

        // یک حلقه برای رسیدن به آخرین کتگوری
        while (current) {
          ordered.push(current)
          current = response.find((i) => i.parent_id === current.id)
        }

        productCategoriesPaths.value[cat.id] = ordered
      } catch (error) {
        console.error(`خطا در دریافت مسیر کتگوری ${cat.id}:`, error)
      }
    }
    isLoadingCategories.value = false
  },
  { deep: true, immediate: true },
)

// ==============================
// منطق جستجو و انتخاب دسته‌بندی
// ==============================
watch(categorySearchQuery, (newQuery) => {
  if (!newQuery || newQuery.trim() === '') {
    searchedCategories.value = []
    return
  }

  if (searchTimeout) clearTimeout(searchTimeout)

  searchTimeout = setTimeout(async () => {
    isSearchingCategory.value = true
    try {
      const response = await categoryService.listCategories({ search: newQuery })
      searchedCategories.value = response?.items || []
    } catch (error) {
      errorStore.addError({
        type: 'error',
        message: `خطا در جستجوی کتگوری: ${error?.detail?.message || 'خطای سرور'}`,
      })
      searchedCategories.value = []
    } finally {
      isSearchingCategory.value = false
    }
  }, 500)
})

const isCategorySelected = (catId) => {
  return selectedCategories.value.some((c) => c.id === catId)
}

const addCategoryToSelection = (category) => {
  if (!isCategorySelected(category.id)) {
    selectedCategories.value.push(category)
  }
  // پس از انتخاب، فیلد جستجو را پاک می‌کنیم
  categorySearchQuery.value = ''
  searchedCategories.value = []
}

const removeCategoryFromSelection = (catId) => {
  selectedCategories.value = selectedCategories.value.filter((c) => c.id !== catId)
}

// ==============================
// منطق همگام‌سازی و جداسازی یک کتگوری
// ==============================
const handleSyncCategories = async () => {
  isSyncing.value = true
  try {
    // استخراج لیست آیدی‌ها از آبجکت‌های انتخاب‌شده
    const categoryIds = selectedCategories.value.map((c) => c.id)

    // ارسال به سرویس syncCategories
    await categoryService.syncCategories(product.value.id, categoryIds)

    // بروزرسانی دیتای کلی محصول در فرانت
    await refreshProductData()
    alert('دسته‌بندی‌ها با موفقیت همگام‌سازی شدند.')
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطا در همگام‌سازی دسته‌بندی‌ها.'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isSyncing.value = false
  }
}

const handleDetachCategories = async (catId) => {
  if (!confirm('آیا از حذف این دسته‌بندی اطمینان دارید؟')) return
  isSyncing.value = true
  try {
    // ۱. دسته‌بندی مورد نظر را از استیت لوکال حذف می‌کنیم
    const updatedCategories = selectedCategories.value.filter((c) => c.id !== catId)

    // ۲. آرایه‌ای از آیدی‌های باقی‌مانده می‌سازیم
    const categoryIds = updatedCategories.map((c) => c.id)

    // ۳. لیست جدید را به همان سرویس می‌فرستیم
    await categoryService.syncCategories(product.value.id, categoryIds)

    // ۴. اعمال تغییرات در فرانت‌اند
    selectedCategories.value = updatedCategories
    await refreshProductData()

    errorStore.addError({ type: 'success', message: 'دسته‌بندی‌ با موفقیت حذف شد.' })
  } catch (error) {
    console.error('خطا در حذف دسته‌بندی:', error)
    const msg = getErrorMessage(error.code) || 'خطا در حذف دسته‌بندی‌.'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isSyncing.value = false
  }
}

// ==============================
// منطق تگ‌ها و ویژگی‌ها (بدون تغییر)
// ==============================
const allTags = ref([]) // فرض بر این است که از جایی پر می‌شود
const availableAttributesList = ref([]) // فرض بر این است که از جایی پر می‌شود
const newAttribute = ref({ id: '', value: '' })

const isTagAttached = (tagId) => product.value?.tags?.some((t) => t.id === tagId)

const toggleTag = async (event, tagId) => {
  try {
    if (event.target.checked) {
      await productService.attachTag(product.value.id, tagId)
    } else {
      await productService.detachTag(product.value.id, tagId)
    }
    await refreshProductData()
  } catch (error) {
    console.error(error)
  }
}

const patchAttribute = async (attributeId, value) => {
  try {
    await productService.updateAttribute(product.value.id, attributeId, { value })
  } catch (error) {
    console.error(error)
  }
}

const addAttribute = async () => {
  if (!newAttribute.value.id || !newAttribute.value.value) return
  try {
    await productService.attachAttribute(product.value.id, newAttribute.value.id, {
      value: newAttribute.value.value,
    })
    newAttribute.value = { id: '', value: '' }
    await refreshProductData()
  } catch (error) {
    console.error(error)
  }
}

const removeAttribute = async (attributeId) => {
  if (!confirm('این ویژگی از محصول حذف شود؟')) return
  try {
    await productService.detachAttribute(product.value.id, attributeId)
    await refreshProductData()
  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>
.admin-secondary-layout {
  text-align: right;
  direction: rtl;
}
.category-paths-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 1rem;
  border-radius: 8px;
}
.category-path-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  font-size: 0.9rem;
}
.path-separator {
  color: #94a3b8;
  margin: 0 0.25rem;
}
.current-cat-name {
  color: #0f172a;
}
.btn-icon-danger-sm {
  background: none;
  border: none;
  color: #ef4444;
  font-size: 1.2rem;
  cursor: pointer;
  line-height: 1;
  padding: 0 0.25rem;
}

/* استایل‌های جدید برای نتایج جستجو */
.relative-search-container {
  position: relative;
}
.search-results-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  list-style: none;
  padding: 0;
  margin: 0.25rem 0 0 0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.clickable-list-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
}
.clickable-list-item:hover {
  background: #f8fafc;
}
.already-selected {
  background: #f0fdf4;
  cursor: not-allowed;
  opacity: 0.7;
}

/* بقیه استایل‌های قبلی */
.checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
}
.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
}
.admin-specs-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.admin-specs-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  gap: 1rem;
}
.spec-inline-input {
  flex: 1;
  padding: 0.3rem;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
}
.add-attribute-form {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}
.add-attribute-form select,
.add-attribute-form input {
  flex: 1;
  min-width: 150px;
}
.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}
.btn-primary:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}
</style>
