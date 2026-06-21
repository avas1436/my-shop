<!-- src/views/admin/product-tabs/RelationsTab.vue -->
<template>
  <div class="tab-content admin-secondary-layout space-y-6">
    <!-- کارت مدیریت دسته‌بندی‌ها -->
    <BaseCard class="p-6">
      <div class="flex items-center gap-2 mb-6 border-b border-slate-100 pb-3">
        <Link2Icon class="w-5 h-5 text-blue-500" />
        <h3 class="text-base font-bold text-slate-800 m-0">مدیریت و اتصال دسته‌بندی‌ها</h3>
      </div>

      <!-- لیست دسته‌بندی‌های انتخاب شده با Skeleton Loading -->
      <div class="category-paths-list mb-4 space-y-2">
        <div v-if="isLoadingCategories" class="space-y-2">
          <BaseSkeleton height="52px" />
          <BaseSkeleton height="52px" />
          <BaseSkeleton height="52px" />
        </div>

        <div v-else-if="selectedCategories.length === 0" class="text-sm text-slate-400 py-2">
          هیچ دسته‌بندی برای این محصول انتخاب نشده است.
        </div>

        <div v-else v-for="cat in selectedCategories" :key="cat.id" class="category-path-item">
          <!-- نمایش مسیر به صورت Breadcrumb -->
          <div class="path-text flex items-center flex-wrap gap-1.5 text-xs">
            <template v-if="productCategoriesPaths[cat.id]">
              <template v-for="(parent, idx) in productCategoriesPaths[cat.id]" :key="idx">
                <span class="px-2 py-1 bg-slate-100 text-slate-500 rounded-lg">
                  {{ parent.name || parent.title }}
                </span>
                <span class="text-slate-300">/</span>
              </template>
            </template>
            <span class="px-2 py-1 bg-blue-50 text-blue-600 font-bold rounded-lg">
              {{ cat.name || cat.title }}
            </span>
          </div>

          <BaseButton variant="danger-ghost" size="sm" @click.stop="requestDeleteCategory(cat.id)">
            <Trash2Icon class="w-4 h-4" />
          </BaseButton>
        </div>
      </div>

      <!-- بخش جستجو و افزودن دسته‌بندی -->
      <div class="form-group mb-4">
        <label class="block text-sm font-bold text-slate-700 mb-2">جستجو و افزودن دسته‌بندی:</label>
        <div class="relative flex items-center">
          <BaseInput
            v-model="categorySearchQuery"
            type="text"
            placeholder="بخشی از نام کتگوری را تایپ کنید..."
            class="w-full"
            :style="{ paddingRight: '2.5rem' }"
          />
          <SearchIcon class="w-4 h-4 text-slate-400 absolute right-3 pointer-events-none" />

          <button
            v-if="categorySearchQuery"
            type="button"
            class="absolute left-3 text-slate-400 hover:text-red-500 transition-colors"
            @click="categorySearchQuery = ''"
          >
            <XIcon class="w-4 h-4" />
          </button>
        </div>

        <div class="relative">
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
              <span class="text-sm font-medium">{{ category.name || category.title }}</span>
              <span
                v-if="isCategorySelected(category.id)"
                class="text-xs text-green-600 flex items-center gap-1"
              >
                <CheckIcon class="w-3.5 h-3.5" /> (انتخاب شده)
              </span>
              <PlusIcon v-else class="w-4 h-4 text-slate-400" />
            </li>
          </ul>
        </div>
      </div>

      <div class="flex justify-end border-t border-slate-100 pt-4 mt-2">
        <BaseButton variant="primary" size="md" @click="handleSyncCategories" :disabled="isSyncing">
          <Loader2Icon v-if="isSyncing" class="w-4 h-4 animate-spin" />
          <Link2Icon v-else class="w-4 h-4" />
          {{ isSyncing ? 'در حال ذخیره...' : 'ذخیره و همگام‌سازی دسته‌بندی‌ها' }}
        </BaseButton>
      </div>
    </BaseCard>

    <!-- کارت تگ‌ها -->
    <BaseCard class="p-6">
      <div class="flex items-center gap-2 mb-4">
        <TagIcon class="w-5 h-5 text-amber-500" />
        <h3 class="text-base font-bold text-slate-800 m-0">تگ‌ها / برچسب‌ها</h3>
      </div>
      <div
        class="checkbox-list-container bg-slate-50 p-4 rounded-xl border border-slate-100 max-h-48 overflow-y-auto"
      >
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <label
            v-for="tag in allTags"
            :key="tag.id"
            class="flex items-center gap-2 text-sm text-slate-600 cursor-pointer hover:text-slate-900"
          >
            <input
              type="checkbox"
              :checked="isTagAttached(tag.id)"
              @change="toggleTag($event, tag.id)"
              class="rounded border-slate-300 text-blue-600 focus:ring-blue-500/30 w-4 h-4"
            />
            {{ tag.name }}
          </label>
        </div>
      </div>
    </BaseCard>

    <!-- کارت ویژگی‌های فنی -->
    <BaseCard class="p-6">
      <div class="flex items-center gap-2 mb-4">
        <Settings2Icon class="w-5 h-5 text-purple-500" />
        <h3 class="text-base font-bold text-slate-800 m-0">ویژگی‌های فنی محصول</h3>
      </div>

      <div class="space-y-2 mb-4">
        <div
          v-for="attr in product.attributes"
          :key="attr.attribute_id"
          class="flex items-center justify-between bg-slate-50 border border-slate-200/40 p-2.5 rounded-xl gap-4"
        >
          <span class="text-sm font-bold text-slate-700 min-w-[120px]">{{ attr.name }}:</span>
          <BaseInput
            :modelValue="attr.value"
            @update:modelValue="attr.value = $event"
            @blur="patchAttribute(attr.attribute_id, attr.value)"
            class="flex-1"
          />
          <BaseButton
            variant="danger-ghost"
            size="sm"
            @click="requestDeleteAttribute(attr.attribute_id)"
          >
            <Trash2Icon class="w-4 h-4" />
          </BaseButton>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 items-end pt-2 border-t border-slate-100">
        <div>
          <label class="block text-xs font-bold text-slate-500 mb-1">نام ویژگی</label>
          <select
            v-model="newAttribute.id"
            class="w-full h-[48px] bg-white border border-slate-200 rounded-2xl px-3 text-sm outline-none focus:border-blue-500"
          >
            <option value="" disabled>انتخاب نام ویژگی...</option>
            <option v-for="a in availableAttributesList" :key="a.id" :value="a.id">
              {{ a.name }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-500 mb-1">مقدار ویژگی</label>
          <BaseInput v-model="newAttribute.value" placeholder="مقدار..." class="w-full" />
        </div>
        <BaseButton variant="success" size="md" class="h-[48px]" @click="addAttribute">
          <PlusIcon class="w-4 h-4" /> افزودن ویژگی
        </BaseButton>
      </div>
    </BaseCard>

    <!-- مودال تایید حذف دسته‌بندی -->
    <BaseModal :open="showDeleteCategoryConfirm" @close="showDeleteCategoryConfirm = false">
      <div class="text-center space-y-4">
        <div class="w-16 h-16 mx-auto bg-red-50 rounded-full flex items-center justify-center">
          <Trash2Icon class="w-8 h-8 text-red-500" />
        </div>
        <h3 class="text-lg font-bold text-slate-800">آیا اطمینان دارید؟</h3>
        <p class="text-slate-500 text-sm">این دسته‌بندی از محصول حذف خواهد شد.</p>
        <div class="flex gap-3 justify-center pt-2">
          <BaseButton variant="secondary" @click="showDeleteCategoryConfirm = false"
            >انصراف</BaseButton
          >
          <BaseButton variant="danger" @click="confirmDeleteCategory">حذف قطعی</BaseButton>
        </div>
      </div>
    </BaseModal>

    <!-- مودال تایید حذف ویژگی -->
    <BaseModal :open="showDeleteAttributeConfirm" @close="showDeleteAttributeConfirm = false">
      <div class="text-center space-y-4">
        <div class="w-16 h-16 mx-auto bg-red-50 rounded-full flex items-center justify-center">
          <Trash2Icon class="w-8 h-8 text-red-500" />
        </div>
        <h3 class="text-lg font-bold text-slate-800">آیا اطمینان دارید؟</h3>
        <p class="text-slate-500 text-sm">این ویژگی از محصول حذف خواهد شد.</p>
        <div class="flex gap-3 justify-center pt-2">
          <BaseButton variant="secondary" @click="showDeleteAttributeConfirm = false"
            >انصراف</BaseButton
          >
          <BaseButton variant="danger" @click="confirmDeleteAttribute">حذف قطعی</BaseButton>
        </div>
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { categoryService, productService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import {
  CheckIcon,
  Link2Icon,
  Loader2Icon,
  PlusIcon,
  SearchIcon,
  Settings2Icon,
  TagIcon,
  Trash2Icon,
  XIcon,
} from '@lucide/vue'
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
    errorStore.addError({ type: 'success', message: 'دسته‌بندی‌ با موفقیت بروزرسانی شد.' })
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
// منطق تگ‌ها و ویژگی‌ها
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
  background: var(--bg-muted, #f1f5f9);
  padding: 1rem;
  border-radius: var(--radius-lg, 12px);
}

.category-path-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--surface, #ffffff);
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: 1px solid var(--border, #e2e8f0);
  font-size: 0.9rem;
}

.path-separator {
  color: var(--text-muted, #94a3b8);
  margin: 0 0.25rem;
}

.relative-search-container {
  position: relative;
}

.search-results-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--surface, white);
  border: 1px solid var(--border, #cbd5e1);
  border-radius: var(--radius-lg, 12px);
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  list-style: none;
  padding: 0;
  margin: 0.25rem 0 0 0;
  box-shadow: var(--shadow-soft);
}

.clickable-list-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid var(--border, #f1f5f9);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.clickable-list-item:hover {
  background: var(--bg-muted, #f8fafc);
}

.already-selected {
  background: rgba(16, 185, 129, 0.08);
  cursor: not-allowed;
  opacity: 0.7;
}

.checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
  background: var(--bg-muted, #f8fafc);
  padding: 1rem;
  border-radius: var(--radius-lg, 12px);
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
}
</style>
