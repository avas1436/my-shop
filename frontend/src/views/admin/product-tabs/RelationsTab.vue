<!-- src/views/admin/product-tabs/RelationsTab.vue -->
<template>
  <div class="grid gap-6">
    <!-- ========================================== -->
    <!-- کارت دسته‌بندی‌ها -->
    <!-- ========================================== -->
    <div class="p-6 bg-white border border-border-light rounded-xl shadow-(--shadow-soft)">
      <div class="flex items-center gap-2 mb-5 border-b border-border-light pb-3">
        <Link2Icon class="w-5 h-5 text-blue-500 shrink-0" />
        <h3 class="m-0 text-[1rem] font-bold">مدیریت و اتصال دسته‌بندی‌ها</h3>
      </div>

      <!-- لیست دسته‌بندی‌های انتخاب‌شده -->
      <div class="grid gap-2 mb-4 p-4 bg-bg-muted rounded-xl">
        <div v-if="isLoadingCategories" class="grid gap-2">
          <BaseSkeleton height="52px" />
          <BaseSkeleton height="52px" />
          <BaseSkeleton height="52px" />
        </div>

        <p
          v-else-if="!selectedCategories.length"
          class="m-0 text-sm text-text-muted py-1 text-center"
        >
          هیچ دسته‌بندی برای این محصول انتخاب نشده است.
        </p>

        <div
          v-else
          v-for="cat in selectedCategories"
          :key="cat.id"
          class="flex items-center justify-between gap-4 px-4 py-3 bg-white border border-border-light rounded-xl shadow-sm"
        >
          <div class="flex flex-wrap items-center gap-1.5 text-xs">
            <template v-if="productCategoriesPaths[cat.id]">
              <template v-for="(parent, idx) in productCategoriesPaths[cat.id]" :key="idx">
                <span class="px-2 py-1 bg-slate-100 text-text-muted rounded-lg">
                  {{ parent.name || parent.title }}
                </span>
                <span class="text-border-strong">/</span>
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

      <!-- جستجو و افزودن دسته‌بندی -->
      <div class="grid gap-1.5 mb-4">
        <label class="text-sm font-bold text-text-muted">جستجو و افزودن دسته‌بندی</label>
        <div class="relative">
          <BaseInput
            v-model="categorySearchQuery"
            type="text"
            placeholder="بخشی از نام کتگوری را تایپ کنید..."
            class="pr-10"
          />
          <SearchIcon
            class="absolute right-15 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted pointer-events-none"
          />
          <button
            v-if="categorySearchQuery"
            type="button"
            class="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-danger transition-colors border-0 bg-transparent cursor-pointer"
            @click="categorySearchQuery = ''"
          >
            <XIcon class="w-4 h-4" />
          </button>
        </div>

        <!-- نتایج جستجوی دسته‌بندی -->
        <ul
          v-if="categorySearchQuery && searchedCategories.length && !isSearchingCategory"
          class="mt-1 p-0 m-0 list-none border border-border-light rounded-xl bg-white shadow-(--shadow-soft) max-h-50 overflow-y-auto z-10 relative"
        >
          <li
            v-for="category in searchedCategories"
            :key="category.id"
            class="flex items-center justify-between px-4 py-3 border-b border-border-light last:border-0 cursor-pointer transition-colors"
            :class="
              isCategorySelected(category.id)
                ? 'bg-emerald-50/80 opacity-70 cursor-not-allowed'
                : 'hover:bg-bg-muted'
            "
            @click="addCategoryToSelection(category)"
          >
            <span class="text-sm font-medium">{{ category.name }}</span>
            <span
              v-if="isCategorySelected(category.id)"
              class="text-xs text-emerald-600 flex items-center gap-1"
            >
              <CheckIcon class="w-3.5 h-3.5" /> انتخاب شده
            </span>
            <PlusIcon v-else class="w-4 h-4 text-text-muted" />
          </li>
        </ul>
      </div>

      <div class="flex justify-end border-t border-border-light pt-4">
        <BaseButton
          variant="primary"
          size="md"
          :disabled="isSyncingCategory"
          @click="handleSyncCategories"
        >
          <Loader2Icon v-if="isSyncingCategory" class="w-4 h-4 animate-spin" />
          <Link2Icon v-else class="w-4 h-4" />
          {{ isSyncingCategory ? 'در حال ذخیره...' : 'ذخیره و همگام‌سازی دسته‌بندی‌ها' }}
        </BaseButton>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- کارت تگ‌ها -->
    <!-- ========================================== -->
    <div class="p-6 bg-white border border-border-light rounded-xl shadow-(--shadow-soft)">
      <div class="flex items-center gap-2 mb-4 border-b border-border-light pb-3">
        <TagIcon class="w-5 h-5 text-amber-500 shrink-0" />
        <h3 class="m-0 text-[1rem] font-bold">تگ‌ها / برچسب‌ها</h3>
      </div>

      <div
        class="bg-bg-muted p-4 rounded-xl border border-border-light max-h-48 overflow-y-auto mb-4"
      >
        <div v-if="allTags.length" class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <label
            v-for="tag in allTags"
            :key="tag.id"
            class="flex items-center gap-2 text-sm text-text-muted cursor-pointer hover:text-text-main"
          >
            <input
              type="checkbox"
              class="accent-primary w-4 h-4 rounded"
              :checked="isTagSelected(tag.id)"
              @change="toggleTag($event, tag.id)"
            />
            {{ tag.name }}
          </label>
        </div>
        <p v-else class="m-0 text-sm text-text-muted text-center py-2">
          هیچ تگی یافت نشد. می‌توانید تگ جدید جستجو و اضافه کنید.
        </p>
      </div>

      <!-- جستجو و افزودن تگ -->
      <div class="grid gap-1.5 mb-4">
        <label class="text-sm font-bold text-text-muted">جستجو و افزودن تگ</label>
        <div class="relative">
          <BaseInput
            v-model="tagSearchQuery"
            type="text"
            placeholder="بخشی از نام تگ را تایپ کنید..."
            class="pr-10"
          />
          <SearchIcon
            class="absolute right-15 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted pointer-events-none"
          />
          <button
            v-if="tagSearchQuery"
            type="button"
            class="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-danger transition-colors border-0 bg-transparent cursor-pointer"
            @click="tagSearchQuery = ''"
          >
            <XIcon class="w-4 h-4" />
          </button>
        </div>

        <!-- نتایج جستجوی تگ -->
        <ul
          v-if="tagSearchQuery && searchedTags.length && !isSearchingTags"
          class="mt-1 p-0 m-0 list-none border border-border-light rounded-xl bg-white shadow-(--shadow-soft) max-h-50 overflow-y-auto z-10 relative"
        >
          <li
            v-for="tag in searchedTags"
            :key="tag.id"
            class="flex items-center justify-between px-4 py-3 border-b border-border-light last:border-0 cursor-pointer transition-colors"
            :class="
              isTagSelected(tag.id)
                ? 'bg-emerald-50/80 opacity-70 cursor-not-allowed'
                : 'hover:bg-bg-muted'
            "
            @click="addTagToSelection(tag)"
          >
            <span class="text-sm font-medium">{{ tag.name }}</span>
            <span
              v-if="isTagSelected(tag.id)"
              class="text-xs text-emerald-600 flex items-center gap-1"
            >
              <CheckIcon class="w-3.5 h-3.5" /> انتخاب شده
            </span>
            <PlusIcon v-else class="w-4 h-4 text-text-muted" />
          </li>
        </ul>
      </div>

      <div class="flex justify-end border-t border-border-light pt-4">
        <BaseButton variant="primary" size="md" :disabled="isSyncingTag" @click="handleSyncTags">
          <Loader2Icon v-if="isSyncingTag" class="w-4 h-4 animate-spin" />
          <Link2Icon v-else class="w-4 h-4" />
          {{ isSyncingTag ? 'در حال ذخیره...' : 'ذخیره و همگام‌سازی تگ‌ها' }}
        </BaseButton>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- کارت ویژگی‌های فنی -->
    <!-- ========================================== -->
    <div class="p-6 bg-white border border-border-light rounded-xl shadow-(--shadow-soft)">
      <div class="flex items-center gap-2 mb-4 border-b border-border-light pb-3">
        <Settings2Icon class="w-5 h-5 text-purple-500 shrink-0" />
        <h3 class="m-0 text-[1rem] font-bold">ویژگی‌های فنی محصول</h3>
      </div>

      <!-- قسمت مربوط به خود محصول -->
      <div class="grid gap-2 mb-4">
        <div
          v-for="attr in product.attributes"
          :key="attr.attribute_id"
          class="flex items-center gap-4 bg-bg-muted border border-border-light p-2.5 rounded-xl shadow-sm"
        >
          <span class="text-sm font-bold text-text-main min-w-30">{{ attr.name }}:</span>
          <BaseInput
            :model-value="attr.value"
            class="flex-1 bg-white"
            @update:model-value="attr.value = $event"
            @blur="patchAttribute(attr.attribute_id, attr.value)"
          />
          <BaseButton
            variant="danger-ghost"
            size="sm"
            @click="requestDeleteAttribute(attr.attribute_id)"
          >
            <Trash2Icon class="w-4 h-4" />
          </BaseButton>
        </div>

        <p v-if="!product.attributes?.length" class="m-0 text-sm text-text-muted text-center py-2">
          هیچ ویژگی فنی برای این محصول ثبت نشده است.
        </p>
      </div>

      <!-- قسمت مربوط به واریانت ها -->
      <div class="grid gap-4 mb-4">
        <!-- حلقه اول: چرخیدن روی واریانت‌هایی که ویژگی دارند -->
        <div
          v-for="variant in activeVariantsWithAttributes"
          :key="variant.id"
          class="border-b pb-4 last:border-0"
        >
          <div class="text-xs font-semibold text-text-muted mb-2 px-1">
            تنوع با شناسه انبار: {{ variant.sku }}
          </div>

          <div class="grid gap-2">
            <!-- حلقه دوم: چرخیدن روی تک‌تک ویژگی‌های آن واریانت -->
            <div
              v-for="attr in variant.attributes"
              :key="attr.attribute_id"
              class="flex items-center gap-4 bg-bg-muted border border-border-light p-2.5 rounded-xl shadow-sm"
            >
              <span class="text-sm font-bold text-text-main min-w-30">{{ attr.name }}:</span>
              <BaseInput
                :model-value="attr.value"
                class="flex-1 bg-white"
                @update:model-value="attr.value = $event"
                @blur="patchAttribute(attr.attribute_id, attr.value)"
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
        </div>

        <!-- پیام در صورت عدم وجود ویژگی برای هیچکدام از واریانت‌ها -->
        <p
          v-if="!activeVariantsWithAttributes.length"
          class="m-0 text-sm text-text-muted text-center py-2"
        >
          هیچ ویژگی فنی برای تنوع‌های این محصول ثبت نشده است.
        </p>
      </div>

      <!-- افزودن ویژگی جدید -->
      <div
        class="grid grid-cols-1 sm:grid-cols-3 gap-3 items-end pt-4 border-t border-border-light"
      >
        <div class="grid gap-1.5">
          <label class="text-xs font-bold text-text-muted">نام ویژگی</label>
          <select
            v-model="newAttribute.id"
            class="w-full h-12 bg-white border border-border-light rounded-xl px-3 text-sm focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all cursor-pointer"
          >
            <option value="" disabled>انتخاب نام ویژگی...</option>
            <option v-for="a in availableAttributesList" :key="a.id" :value="a.id">
              {{ a.name }}
            </option>
          </select>
        </div>
        <div class="grid gap-1.5">
          <label class="text-xs font-bold text-text-muted">مقدار ویژگی</label>
          <BaseInput v-model="newAttribute.value" placeholder="مقدار..." />
        </div>
        <BaseButton variant="success" size="md" class="h-12" @click="addAttribute">
          <PlusIcon class="w-4 h-4" />
          افزودن ویژگی
        </BaseButton>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- مودال‌ها -->
    <!-- ========================================== -->
    <BaseModal :open="showDeleteCategoryConfirm" @close="showDeleteCategoryConfirm = false">
      <div class="text-center grid gap-4">
        <div class="w-16 h-16 mx-auto bg-red-50 rounded-full flex items-center justify-center">
          <Trash2Icon class="w-8 h-8 text-danger" />
        </div>
        <h3 class="m-0 text-lg font-bold">آیا اطمینان دارید؟</h3>
        <p class="m-0 text-text-muted text-sm">این دسته‌بندی از محصول حذف خواهد شد.</p>
        <div class="flex gap-3 justify-center pt-2">
          <BaseButton variant="secondary" @click="showDeleteCategoryConfirm = false"
            >انصراف</BaseButton
          >
          <BaseButton variant="danger" :disabled="isSyncingCategory" @click="confirmDeleteCategory">
            <Loader2Icon v-if="isSyncingCategory" class="w-4 h-4 animate-spin" />
            حذف قطعی
          </BaseButton>
        </div>
      </div>
    </BaseModal>
    <!-- مودال تایید حذف ویژگی فنی -->
    <BaseModal :open="showDeleteAttributeConfirm" @close="showDeleteAttributeConfirm = false">
      <div class="text-center grid gap-4">
        <div class="w-16 h-16 mx-auto bg-red-50 rounded-full flex items-center justify-center">
          <Trash2Icon class="w-8 h-8 text-danger" />
        </div>
        <h3 class="m-0 text-lg font-bold">آیا اطمینان دارید؟</h3>
        <p class="m-0 text-text-muted text-sm">این ویژگی بلافاصله از محصول حذف خواهد شد.</p>
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
import BaseModal from '@/components/base/BaseModal.vue'
import BaseSkeleton from '@/components/base/BaseSkeleton.vue'
import { categoryService, productService, tagService } from '@/services/productService'
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
import { computed, inject, ref, watch } from 'vue'

const product = inject('product')
const refreshProductData = inject('refreshProductData')
const errorStore = useErrorStore()

// ==============================
// دسته‌بندی‌ها
// ==============================
const selectedCategories = ref([])
const isLoadingCategories = ref(false)
const productCategoriesPaths = ref({})
const isSyncingCategory = ref(false)

// مودال حذف دسته‌بندی
const showDeleteCategoryConfirm = ref(false)
const categoryToDelete = ref(null)

const requestDeleteCategory = (catId) => {
  categoryToDelete.value = catId
  showDeleteCategoryConfirm.value = true
}

const confirmDeleteCategory = async () => {
  if (!categoryToDelete.value) return
  showDeleteCategoryConfirm.value = false
  await handleDetachCategories(categoryToDelete.value)
  categoryToDelete.value = null
}

watch(
  () => product.value?.categories,
  (newCats) => {
    if (newCats) selectedCategories.value = [...newCats]
  },
  { immediate: true, deep: true },
)

watch(
  () => selectedCategories.value,
  async (newCats) => {
    if (!newCats?.length) return
    isLoadingCategories.value = true
    for (const cat of newCats) {
      if (productCategoriesPaths.value[cat.id]) continue
      try {
        const response = await categoryService.categoryParents(cat.id)
        let current = response.find((i) => i.parent_id === null)
        const ordered = []
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

// جستجوی دسته‌بندی
const categorySearchQuery = ref('')
const searchedCategories = ref([])
const isSearchingCategory = ref(false)
let categorySearchTimeout = null

watch(categorySearchQuery, (newQuery) => {
  if (!newQuery?.trim()) {
    searchedCategories.value = []
    return
  }
  clearTimeout(categorySearchTimeout)
  categorySearchTimeout = setTimeout(async () => {
    isSearchingCategory.value = true
    try {
      const response = await categoryService.listCategories({ search: newQuery })
      searchedCategories.value = response?.items ?? []
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

const isCategorySelected = (catId) => selectedCategories.value.some((c) => c.id === catId)

const addCategoryToSelection = (category) => {
  if (isCategorySelected(category.id)) return
  selectedCategories.value.push(category)
  categorySearchQuery.value = ''
  searchedCategories.value = []
}

const handleSyncCategories = async () => {
  isSyncingCategory.value = true
  try {
    const categoryIds = selectedCategories.value.map((c) => c.id)
    await categoryService.syncCategories(product.value.id, categoryIds)
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'دسته‌بندی‌ها با موفقیت بروزرسانی شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در همگام‌سازی دسته‌بندی‌ها.',
    })
  } finally {
    isSyncingCategory.value = false
  }
}

const handleDetachCategories = async (catId) => {
  isSyncingCategory.value = true
  try {
    const updatedCategories = selectedCategories.value.filter((c) => c.id !== catId)
    const categoryIds = updatedCategories.map((c) => c.id)
    await categoryService.syncCategories(product.value.id, categoryIds)
    selectedCategories.value = updatedCategories
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'دسته‌بندی با موفقیت حذف شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در حذف دسته‌بندی.',
    })
  } finally {
    isSyncingCategory.value = false
  }
}

// ==============================
// تگ‌ها
// ==============================
const allTags = ref([])
const selectedTags = ref([])

watch(
  () => product.value?.tags,
  (newTags) => {
    if (newTags) {
      allTags.value = [...newTags]
      selectedTags.value = [...newTags]
    }
  },
  { immediate: true, deep: true },
)

// جستجوی تگ‌ها
const tagSearchQuery = ref('')
const searchedTags = ref([])
const isSearchingTags = ref(false)
const isSyncingTag = ref(false)
let tagSearchTimeout = null

watch(tagSearchQuery, (newQuery) => {
  if (!newQuery?.trim()) {
    searchedTags.value = []
    return
  }
  clearTimeout(tagSearchTimeout)
  tagSearchTimeout = setTimeout(async () => {
    isSearchingTags.value = true
    try {
      const response = await tagService.listTags({ search: newQuery })
      searchedTags.value = response?.items ?? []
    } catch (error) {
      errorStore.addError({
        type: 'error',
        message: `خطا در جستجوی تگ: ${error?.detail?.message || 'خطای سرور'}`,
      })
      searchedTags.value = []
    } finally {
      isSearchingTags.value = false
    }
  }, 500)
})

const isTagSelected = (tagId) => selectedTags.value.some((t) => t.id === tagId)

const addTagToSelection = (tag) => {
  if (isTagSelected(tag.id)) return
  selectedTags.value.push(tag)
  allTags.value.push(tag)
  tagSearchQuery.value = ''
  searchedTags.value = []
}

const toggleTag = (event, tagId) => {
  const isChecked = event.target.checked

  if (isChecked) {
    // اگر تیک زده شد: تگ را پیدا کرده و به لیست انتخاب‌شده‌ها اضافه می‌کنیم
    const tag = allTags.value.find((t) => t.id === tagId)
    if (tag && !isTagSelected(tagId)) {
      selectedTags.value.push(tag)
    }
  } else {
    // اگر تیک برداشته شد: تگ را از لیست انتخاب‌شده‌ها حذف می‌کنیم
    selectedTags.value = selectedTags.value.filter((t) => t.id !== tagId)
  }
}

const handleSyncTags = async () => {
  isSyncingTag.value = true
  try {
    const tagIds = selectedTags.value.map((t) => t.id)
    await tagService.syncTags(product.value.id, tagIds)
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'تگ‌ها با موفقیت بروزرسانی شدند.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در همگام‌سازی تگ‌ها.',
    })
  } finally {
    isSyncingTag.value = false
  }
}

// ==============================
// ویژگی‌های فنی
// ==============================
const availableAttributesList = ref([])
const newAttribute = ref({ id: '', value: '' })

// ذخیره لیست واریانت های حاوی ویژگی‌ها و فیلتر کردن آن‌ها برای نمایش فقط واریانت‌هایی که ویژگی دارند
const activeVariantsWithAttributes = computed(() => {
  if (!product.value?.inventory) {
    return []
  }

  // فقط واریانت‌هایی که آرایه attributes آن‌ها عضو دارد را برمی‌گرداند
  return product.value.inventory.filter((item) => item.attributes && item.attributes.length > 0)
})

// مودال حذف ویژگی
const showDeleteAttributeConfirm = ref(false)
const attributeToDelete = ref(null)

const requestDeleteAttribute = (attributeId) => {
  attributeToDelete.value = attributeId
  showDeleteAttributeConfirm.value = true
}

const confirmDeleteAttribute = async () => {
  if (!attributeToDelete.value) return
  showDeleteAttributeConfirm.value = false
  await removeAttribute(attributeToDelete.value)
  attributeToDelete.value = null
}

const patchAttribute = async (attributeId, value) => {
  try {
    await productService.updateAttribute(product.value.id, attributeId, { value })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در بروزرسانی ویژگی.',
    })
  }
}

const addAttribute = async () => {
  if (!newAttribute.value.id || !newAttribute.value.value) {
    errorStore.addError({ type: 'warning', message: 'لطفاً نام و مقدار ویژگی را وارد کنید.' })
    return
  }
  try {
    await productService.attachAttribute(product.value.id, newAttribute.value.id, {
      value: newAttribute.value.value,
    })
    newAttribute.value = { id: '', value: '' }
    await refreshProductData()
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در افزودن ویژگی.',
    })
  }
}

const removeAttribute = async (attributeId) => {
  try {
    await productService.detachAttribute(product.value.id, attributeId)
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'ویژگی با موفقیت حذف شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در حذف ویژگی.',
    })
  }
}
</script>
