<!-- src/views/admin/product-tabs/RelationsTab.vue -->
<template>
  <div class="grid gap-5">
    <!-- ─── دسته‌بندی‌ها ─── -->
    <div class="p-5 bg-white border border-border-light rounded-xl shadow-(--shadow-soft)">
      <div class="flex items-center gap-2 mb-5 border-b border-border-light pb-3">
        <Link2Icon class="w-5 h-5 text-blue-500 shrink-0" />
        <h3 class="m-0 text-[1rem] font-bold">مدیریت و اتصال دسته‌بندی‌ها</h3>
      </div>

      <div class="grid gap-2 mb-4 p-4 bg-bg-muted rounded-xl">
        <div v-if="isLoadingCategories" class="grid gap-2">
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
          class="flex items-center justify-between gap-4 px-4 py-3 bg-white border border-border-light rounded-xl"
        >
          <div class="flex flex-wrap items-center gap-1.5 text-xs">
            <template v-if="productCategoriesPaths[cat.id]">
              <template v-for="(parent, idx) in productCategoriesPaths[cat.id]" :key="idx">
                <span class="px-2 py-1 bg-slate-100 text-text-muted rounded-lg">{{
                  parent.name || parent.title
                }}</span>
                <span class="text-text-muted">/</span>
              </template>
            </template>
            <span class="px-2 py-1 bg-blue-50 text-blue-600 font-bold rounded-lg">{{
              cat.name || cat.title
            }}</span>
          </div>
          <BaseButton variant="danger-ghost" size="sm" @click.stop="requestDeleteCategory(cat.id)">
            <Trash2Icon class="w-4 h-4" />
          </BaseButton>
        </div>
      </div>

      <div class="grid gap-1.5 mb-4">
        <label class="text-sm font-bold text-text-muted">جستجو و افزودن دسته‌بندی</label>
        <div class="relative">
          <BaseInput
            v-model="categorySearchQuery"
            placeholder="بخشی از نام کتگوری را تایپ کنید..."
          />
          <button
            v-if="categorySearchQuery"
            type="button"
            class="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-danger transition-colors border-0 bg-transparent cursor-pointer"
            @click="categorySearchQuery = ''"
          >
            <XIcon class="w-4 h-4" />
          </button>
          <ul
            v-if="categorySearchQuery && searchedCategories.length && !isSearchingCategory"
            class="absolute top-full right-0 left-0 z-20 mt-1 p-0 m-0 list-none border border-border-light rounded-xl bg-white shadow-(--shadow-soft) max-h-50 overflow-y-auto"
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

    <!-- ─── تگ‌ها ─── -->
    <div class="p-5 bg-white border border-border-light rounded-xl shadow-(--shadow-soft)">
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
          هیچ تگی یافت نشد. از جستجو برای افزودن تگ استفاده کنید.
        </p>
      </div>

      <div class="grid gap-1.5 mb-4">
        <label class="text-sm font-bold text-text-muted">جستجو و افزودن تگ</label>
        <div class="relative">
          <BaseInput v-model="tagSearchQuery" placeholder="بخشی از نام تگ را تایپ کنید..." />
          <button
            v-if="tagSearchQuery"
            type="button"
            class="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-danger transition-colors border-0 bg-transparent cursor-pointer"
            @click="tagSearchQuery = ''"
          >
            <XIcon class="w-4 h-4" />
          </button>
          <ul
            v-if="tagSearchQuery && searchedTags.length && !isSearchingTags"
            class="absolute top-full right-0 left-0 z-20 mt-1 p-0 m-0 list-none border border-border-light rounded-xl bg-white shadow-(--shadow-soft) max-h-50 overflow-y-auto"
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
      </div>

      <div class="flex justify-end border-t border-border-light pt-4">
        <BaseButton variant="primary" size="md" :disabled="isSyncingTag" @click="handleSyncTags">
          <Loader2Icon v-if="isSyncingTag" class="w-4 h-4 animate-spin" />
          <Link2Icon v-else class="w-4 h-4" />
          {{ isSyncingTag ? 'در حال ذخیره...' : 'ذخیره و همگام‌سازی تگ‌ها' }}
        </BaseButton>
      </div>
    </div>

    <!-- ─── ویژگی‌های فنی محصول ─── -->
    <div class="p-5 bg-white border border-border-light rounded-xl shadow-(--shadow-soft)">
      <div class="flex items-center gap-2 mb-4 border-b border-border-light pb-3">
        <Settings2Icon class="w-5 h-5 text-purple-500 shrink-0" />
        <h3 class="m-0 text-[1rem] font-bold">ویژگی‌های فنی محصول</h3>
      </div>

      <div class="grid gap-2 mb-4">
        <template v-if="product.attributes?.length">
          <div
            v-for="attr in product.attributes"
            :key="attr.id"
            class="flex items-center gap-3 bg-bg-muted border border-border-light p-2.5 rounded-xl"
          >
            <span class="text-sm font-bold text-text-main min-w-30 shrink-0">{{ attr.name }}:</span>
            <BaseInput
              :model-value="attr.value"
              class="flex-1"
              @update:model-value="attr.value = $event"
              @blur="patchProductAttribute(attr.product_attribute_id, attr.value)"
            />
            <BaseButton
              variant="danger-ghost"
              size="sm"
              @click="requestDeleteAttribute(attr.product_attribute_id)"
            >
              <Trash2Icon class="w-4 h-4" />
            </BaseButton>
          </div>
        </template>
        <p
          v-else
          class="m-0 text-sm text-text-muted text-center py-4 bg-bg-muted border border-border-light rounded-xl"
        >
          هیچ ویژگی فنی برای این محصول ثبت نشده است.
        </p>
      </div>

      <div class="grid gap-3 pt-4 border-t border-dashed border-border-light">
        <label class="text-sm font-bold text-text-muted">افزودن ویژگی جدید</label>
        <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
          <div class="relative w-full sm:w-1/2">
            <BaseInput
              v-model="productAttrSearch"
              placeholder="جستجوی نام ویژگی..."
              @focus="newAttribute.id = ''"
            />
            <ul
              v-if="productAttrSearch && searchedAttributes.length && !newAttribute.id"
              class="absolute top-full right-0 left-0 z-20 mt-1 p-0 m-0 list-none bg-white border border-border-light rounded-xl shadow-(--shadow-soft) max-h-50 overflow-y-auto"
            >
              <li
                v-for="sa in searchedAttributes"
                :key="sa.id"
                class="px-4 py-2.5 hover:bg-bg-muted cursor-pointer text-sm border-b border-border-light last:border-0"
                @click="selectProductAttribute(sa)"
              >
                {{ sa.name }}
              </li>
            </ul>
          </div>
          <BaseInput
            v-model="newAttribute.value"
            placeholder="مقدار ویژگی..."
            class="w-full sm:w-1/2"
          />
          <BaseButton
            variant="primary"
            size="md"
            class="w-full sm:w-auto shrink-0"
            @click="addProductAttribute"
          >
            <PlusIcon class="w-4 h-4" /> افزودن
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- ─── ویژگی‌های واریانت‌ها ─── -->
    <div class="p-5 bg-white border border-border-light rounded-xl shadow-(--shadow-soft)">
      <div class="flex items-center gap-2 mb-4 border-b border-border-light pb-3">
        <Settings2Icon class="w-5 h-5 text-indigo-500 shrink-0" />
        <h3 class="m-0 text-[1rem] font-bold">ویژگی‌های تنوع‌ها (Variants)</h3>
      </div>

      <p
        v-if="!product.inventory?.length"
        class="m-0 text-sm text-text-muted text-center py-4 border border-border-light rounded-xl bg-bg-muted"
      >
        هیچ تنوعی برای این محصول تعریف نشده است.
      </p>

      <div v-else class="grid gap-5">
        <div
          v-for="variant in product.inventory"
          :key="variant.id"
          class="border border-border-light p-4 rounded-xl bg-white"
        >
          <div
            class="flex items-center justify-between bg-bg-muted px-3 py-2 rounded-lg mb-3 text-xs font-semibold text-text-muted"
          >
            <span
              >SKU: <span class="font-mono font-bold text-text-main">{{ variant.sku }}</span></span
            >
          </div>

          <div class="grid gap-2 mb-4">
            <template v-if="variant.attributes?.length">
              <div
                v-for="attr in variant.attributes"
                :key="attr.id"
                class="flex items-center gap-3 bg-bg-muted border border-border-light p-2.5 rounded-xl"
              >
                <span class="text-sm font-bold text-text-main min-w-30 shrink-0"
                  >{{ attr.name }}:</span
                >
                <BaseInput
                  :model-value="attr.value"
                  class="flex-1"
                  @update:model-value="attr.value = $event"
                  @blur="
                    patchProductVariantAttribute(attr.product_variant_attribute_id, attr.value)
                  "
                />
                <BaseButton
                  variant="danger-ghost"
                  size="sm"
                  @click="removeProductVariantAttribute(attr.product_variant_attribute_id)"
                >
                  <Trash2Icon class="w-4 h-4" />
                </BaseButton>
              </div>
            </template>
            <p
              v-else
              class="m-0 text-sm text-text-muted text-center py-3 border border-dashed border-border-light rounded-xl bg-bg-muted"
            >
              هیچ ویژگی‌ای برای این تنوع ثبت نشده است.
            </p>
          </div>

          <div class="grid gap-3 pt-3 border-t border-dashed border-border-light">
            <label class="text-xs font-bold text-text-muted">افزودن ویژگی جدید به این تنوع</label>
            <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
              <div class="relative w-full sm:w-1/2">
                <BaseInput
                  :model-value="variant.tmp_search || ''"
                  placeholder="جستجوی نام ویژگی..."
                  @update:model-value="(val) => searchVariantAttributes(variant, val)"
                />
                <ul
                  v-if="
                    variant.tmp_search &&
                    activeSearchingVariantId === variant.id &&
                    getFilteredVariantAttributes(variant).length &&
                    !variant.tmp_attribute_id
                  "
                  class="absolute top-full right-0 left-0 z-20 mt-1 p-0 m-0 list-none bg-white border border-border-light rounded-xl shadow-(--shadow-soft) max-h-50 overflow-y-auto"
                >
                  <li
                    v-for="sa in getFilteredVariantAttributes(variant)"
                    :key="sa.id"
                    class="px-4 py-2.5 hover:bg-bg-muted cursor-pointer text-sm border-b border-border-light last:border-0"
                    @click="selectVariantAttribute(variant, sa)"
                  >
                    {{ sa.name }}
                  </li>
                </ul>
              </div>
              <BaseInput
                v-model="variant.tmp_value"
                placeholder="مقدار ویژگی..."
                class="w-full sm:w-1/2"
              />
              <BaseButton
                variant="primary"
                size="md"
                class="w-full sm:w-auto shrink-0"
                @click="addProductVariantAttribute(variant)"
              >
                <PlusIcon class="w-4 h-4" /> افزودن
              </BaseButton>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ─── مودال حذف دسته‌بندی ─── -->
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

    <!-- ─── مودال حذف ویژگی ─── -->
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
import { attributeService, categoryService, tagService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import {
  CheckIcon,
  Link2Icon,
  Loader2Icon,
  PlusIcon,
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
// دسته‌بندی‌ها
// ==============================
const selectedCategories = ref([])
const isLoadingCategories = ref(false)
const productCategoriesPaths = ref({})
const isSyncingCategory = ref(false)
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
    await categoryService.syncCategories(
      product.value.id,
      selectedCategories.value.map((c) => c.id),
    )
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
    const updated = selectedCategories.value.filter((c) => c.id !== catId)
    await categoryService.syncCategories(
      product.value.id,
      updated.map((c) => c.id),
    )
    selectedCategories.value = updated
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
const isSyncingTag = ref(false)
const tagSearchQuery = ref('')
const searchedTags = ref([])
const isSearchingTags = ref(false)
let tagSearchTimeout = null

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
  if (!allTags.value.some((t) => t.id === tag.id)) allTags.value.push(tag)
  tagSearchQuery.value = ''
  searchedTags.value = []
}

const toggleTag = (event, tagId) => {
  if (event.target.checked) {
    const tag = allTags.value.find((t) => t.id === tagId)
    if (tag && !isTagSelected(tagId)) selectedTags.value.push(tag)
  } else {
    selectedTags.value = selectedTags.value.filter((t) => t.id !== tagId)
  }
}

const handleSyncTags = async () => {
  isSyncingTag.value = true
  try {
    await tagService.syncTags(
      product.value.id,
      selectedTags.value.map((t) => t.id),
    )
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
// ویژگی‌های فنی محصول
// ==============================
const showDeleteAttributeConfirm = ref(false)
const attributeToDelete = ref(null)
const searchedAttributes = ref([])
const isSearchingAttributes = ref(false)
let attributeSearchTimeout = null

const searchAttributes = (query) => {
  if (!query?.trim()) {
    searchedAttributes.value = []
    return
  }
  clearTimeout(attributeSearchTimeout)
  attributeSearchTimeout = setTimeout(async () => {
    isSearchingAttributes.value = true
    try {
      const response = await attributeService.listAttributes({ search: query })
      searchedAttributes.value = response?.items ?? []
    } catch (error) {
      errorStore.addError({
        type: 'error',
        message: `خطا در جستجوی ویژگی: ${error?.detail?.message || 'خطای سرور'}`,
      })
      searchedAttributes.value = []
    } finally {
      isSearchingAttributes.value = false
    }
  }, 400)
}

const productAttrSearch = ref('')
const newAttribute = ref({ id: '', value: '' })

watch(productAttrSearch, searchAttributes)

const selectProductAttribute = (sa) => {
  newAttribute.value.id = sa.id
  productAttrSearch.value = sa.name
  searchedAttributes.value = []
}

const patchProductAttribute = async (productAttributeId, value) => {
  try {
    await attributeService.updateProductAttribute(productAttributeId, {
      product_id: product.value.id,
      value,
    })
    errorStore.addError({ type: 'success', message: 'ویژگی با موفقیت بروزرسانی شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در بروزرسانی ویژگی.',
    })
  }
}

const addProductAttribute = async () => {
  if (!newAttribute.value.id || !newAttribute.value.value) {
    errorStore.addError({ type: 'warning', message: 'لطفاً نام و مقدار ویژگی را وارد کنید.' })
    return
  }
  try {
    await attributeService.createProductAttribute({
      product_id: product.value.id,
      attribute_id: newAttribute.value.id,
      value: newAttribute.value.value,
    })
    newAttribute.value = { id: '', value: '' }
    productAttrSearch.value = ''
    await refreshProductData()
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در افزودن ویژگی.',
    })
  }
}

const requestDeleteAttribute = (attributeId) => {
  attributeToDelete.value = attributeId
  showDeleteAttributeConfirm.value = true
}

const confirmDeleteAttribute = async () => {
  if (!attributeToDelete.value) return
  const success = await removeProductAttribute(attributeToDelete.value)
  if (success) {
    showDeleteAttributeConfirm.value = false
    attributeToDelete.value = null
  }
}

const removeProductAttribute = async (attributeId) => {
  try {
    await attributeService.deleteProductAttribute(attributeId, {
      product_id: product.value.id,
      product_attribute_id: attributeId,
    })
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'ویژگی با موفقیت حذف شد.' })
    return true
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در حذف ویژگی.',
    })
    return false
  }
}

// ==============================
// ویژگی واریانت
// ==============================
const activeSearchingVariantId = ref(null)

const searchVariantAttributes = (variant, query) => {
  variant.tmp_search = query
  variant.tmp_attribute_id = ''
  activeSearchingVariantId.value = variant.id
  if (!query?.trim()) {
    searchedAttributes.value = []
    return
  }
  clearTimeout(attributeSearchTimeout)
  attributeSearchTimeout = setTimeout(async () => {
    isSearchingAttributes.value = true
    try {
      const response = await attributeService.listAttributes({ search: query })
      searchedAttributes.value = response?.items ?? []
    } catch (error) {
      errorStore.addError({
        type: 'error',
        message: `خطا در جستجوی ویژگی: ${error?.detail?.message || 'خطای سرور'}`,
      })
      searchedAttributes.value = []
    } finally {
      isSearchingAttributes.value = false
    }
  }, 400)
}

const getFilteredVariantAttributes = (variant) => {
  if (!searchedAttributes.value || activeSearchingVariantId.value !== variant.id) return []
  return searchedAttributes.value.filter(
    (sa) =>
      !variant.attributes?.some((attr) => attr.attribute_id === sa.id || attr.name === sa.name),
  )
}

const selectVariantAttribute = (variant, sa) => {
  variant.tmp_attribute_id = sa.id
  variant.tmp_search = sa.name
  activeSearchingVariantId.value = null
}

const patchProductVariantAttribute = async (productVariantAttributeId, value) => {
  try {
    await attributeService.updateProductVariantAttribute(productVariantAttributeId, {
      product_id: product.value.id,
      value,
    })
    errorStore.addError({ type: 'success', message: 'ویژگی با موفقیت بروزرسانی شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در بروزرسانی ویژگی.',
    })
  }
}

const addProductVariantAttribute = async (variant) => {
  if (!variant.tmp_attribute_id || !variant.tmp_value) {
    errorStore.addError({
      type: 'warning',
      message: 'لطفاً نام و مقدار ویژگی را از لیست انتخاب و وارد کنید.',
    })
    return
  }
  try {
    await attributeService.createProductVariantAttribute({
      product_id: product.value.id,
      variant_id: variant.variant_id,
      attribute_id: variant.tmp_attribute_id,
      value: variant.tmp_value,
    })
    variant.tmp_attribute_id = ''
    variant.tmp_value = ''
    variant.tmp_search = ''
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'ویژگی با موفقیت به تنوع اضافه شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در افزودن ویژگی به تنوع.',
    })
  }
}

const removeProductVariantAttribute = async (productVariantAttributeId) => {
  try {
    await attributeService.deleteProductVariantAttribute(productVariantAttributeId, {
      product_id: product.value.id,
      product_variant_attribute_id: productVariantAttributeId,
    })
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
