<!-- src/views/admin/product-tabs/GeneralTab.vue -->
<template>
  <div class="animate-[fadeIn_0.3s_ease-in-out] grid gap-8">
    <!-- وضعیت و تنظیمات کلی -->
    <section class="grid gap-4">
      <h3 class="m-0 text-[1rem] font-bold text-text-main border-b border-border-light pb-2">
        وضعیت و تنظیمات کلی
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">وضعیت انتشار (Status)</label>
          <select
            :value="product.status"
            class="w-full border border-border-light rounded-md px-3 py-2.5 text-[0.95rem] bg-white focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all"
            @change="updateField('status', $event.target.value)"
          >
            <option value="draft">پیش‌نویس</option>
            <option value="active">منتشر شده</option>
            <option value="inactive">غیر فعال</option>
            <option value="archived">بایگانی شده</option>
          </select>
        </div>

        <div class="flex items-center gap-6 pt-6">
          <label class="flex items-center gap-2 cursor-pointer font-bold text-[0.9rem]">
            <input
              type="checkbox"
              :checked="product.is_featured"
              class="accent-primary w-4 h-4"
              @change="updateField('is_featured', $event.target.checked)"
            />
            کالای ویژه (Featured)
          </label>
          <label class="flex items-center gap-2 cursor-pointer font-bold text-[0.9rem]">
            <input
              type="checkbox"
              :checked="product.is_digital"
              class="accent-primary w-4 h-4"
              @change="updateField('is_digital', $event.target.checked)"
            />
            کالای دیجیتال
          </label>
        </div>
      </div>
    </section>

    <!-- مشخصات اصلی -->
    <section class="grid gap-4">
      <h3 class="m-0 text-[1rem] font-bold text-text-main border-b border-border-light pb-2">
        مشخصات اصلی
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">نام محصول</label>
          <BaseInput
            :model-value="product.name"
            clearable
            @update:model-value="updateField('name', $event)"
          />
        </div>

        <!-- جستجوی برند -->
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">برند محصول</label>
          <div class="relative">
            <BaseInput
              :model-value="product.brand?.name || brandSearchQuery"
              placeholder="بخشی از نام برند را تایپ کنید..."
              :readonly="!!product.brand?.name"
              clearable
              @update:model-value="brandSearchQuery = $event"
              @clear="removeCurrentBrand"
            />
            <p
              v-if="isSearchingBrand && !product.brand_id"
              class="mt-1.5 text-sm text-text-muted text-center"
            >
              در حال جستجو...
            </p>
            <ul
              v-if="
                brandSearchQuery && searchedBrands.length && !isSearchingBrand && !product.brand_id
              "
              class="absolute top-full right-0 left-0 z-10 mt-1.5 p-0 m-0 list-none border border-border-light rounded-md bg-white shadow-(--shadow-soft) max-h-50 overflow-y-auto"
            >
              <li
                v-for="brand in searchedBrands"
                :key="brand.id"
                class="px-3 py-2.5 cursor-pointer border-b border-border-light last:border-0 hover:bg-bg-muted hover:text-primary transition-colors text-[0.95rem]"
                @click="selectBrand(brand)"
              >
                {{ brand.name }}
              </li>
            </ul>
            <p
              v-if="
                brandSearchQuery && !searchedBrands.length && !isSearchingBrand && !product.brand_id
              "
              class="mt-1.5 text-sm text-text-muted text-center"
            >
              برندی یافت نشد.
            </p>
          </div>
        </div>

        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">کد کالا (SKU)</label>
          <BaseInput
            :model-value="product.sku"
            clearable
            @update:model-value="updateField('sku', $event)"
          />
        </div>

        <div class="grid gap-1.5 sm:col-span-2">
          <label class="text-sm font-bold text-text-muted">توضیحات (Description)</label>
          <textarea
            :value="product.description"
            rows="4"
            class="w-full border border-border-light rounded-md px-3 py-2.5 text-[0.95rem] bg-white font-[inherit] resize-y focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all"
            @input="updateField('description', $event.target.value)"
          />
        </div>
      </div>
    </section>

    <!-- قیمت‌گذاری -->
    <section class="grid gap-4 p-5 rounded-xl bg-bg-muted border border-border-light">
      <h3 class="m-0 text-[1rem] font-bold text-text-main border-b border-border-strong pb-2">
        قیمت‌گذاری و مالیات
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div v-for="field in priceFields" :key="field.key" class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">{{ field.label }}</label>
          <BaseInput
            type="number"
            :model-value="product[field.key]"
            clearable
            @update:model-value="updateField(field.key, $event === '' ? null : Number($event))"
          />
        </div>

        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">واحد پول (Currency Code)</label>
          <select
            :value="product.currency_code"
            class="w-full border border-border-light rounded-md px-3 py-2.5 text-[0.95rem] bg-white focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all"
            @change="updateField('currency_code', $event.target.value)"
          >
            <option value="IRR">ریال</option>
            <option value="IRT">تومان</option>
          </select>
        </div>
      </div>
    </section>

    <!-- ابعاد و لجستیک -->
    <section class="grid gap-4">
      <h3 class="m-0 text-[1rem] font-bold text-text-main border-b border-border-light pb-2">
        ابعاد و لجستیک
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div v-for="field in dimensionFields" :key="field.key" class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">{{ field.label }}</label>
          <BaseInput
            type="number"
            :model-value="product[field.key]"
            clearable
            @update:model-value="updateField(field.key, $event === '' ? null : Number($event))"
          />
        </div>

        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">بارکد جهانی (GTIN)</label>
          <BaseInput
            :model-value="product.gtin"
            clearable
            @update:model-value="updateField('gtin', $event)"
          />
        </div>
      </div>
    </section>

    <!-- سئو -->
    <section class="grid gap-4">
      <h3 class="m-0 text-[1rem] font-bold text-text-main border-b border-border-light pb-2">
        سئو (SEO)
      </h3>
      <div class="grid gap-5">
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">نامک (Slug)</label>
          <BaseInput
            :model-value="product.slug"
            clearable
            @update:model-value="updateField('slug', $event)"
          />
        </div>
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">عنوان متا (Meta Title)</label>
          <BaseInput
            :model-value="product.meta_title"
            clearable
            @update:model-value="updateField('meta_title', $event)"
          />
        </div>
        <div class="grid gap-1.5">
          <label class="text-sm font-bold text-text-muted">توضیحات متا (Meta Description)</label>
          <textarea
            :value="product.meta_description"
            rows="3"
            class="w-full border border-border-light rounded-md px-3 py-2.5 text-[0.95rem] bg-white font-[inherit] resize-y focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all"
            @input="updateField('meta_description', $event.target.value)"
          />
        </div>
      </div>
    </section>

    <!-- دکمه ذخیره -->
    <div class="pt-4 border-t border-border-light">
      <BaseButton variant="primary" size="lg" block :disabled="isLoading" @click="saveAllChanges">
        {{ isLoading ? 'در حال ذخیره‌سازی...' : 'ذخیره تمامی اطلاعات پایه' }}
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { brandService, productService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { inject, ref, watch } from 'vue'

const errorStore = useErrorStore()

const product = inject('product')
const productUpdate = inject('productUpdate')
const isLoading = inject('isLoading')
const refreshProductData = inject('refreshProductData')
const updateField = inject('updateField')

// فیلدهای قیمت‌گذاری — حذف تکرار
const priceFields = [
  { key: 'price', label: 'قیمت اصلی (Price)' },
  { key: 'discount_price', label: 'قیمت با تخفیف (Discount Price)' },
  { key: 'cost_price', label: 'قیمت خرید (Cost Price)' },
  { key: 'tax_rate', label: 'نرخ مالیات (Tax Rate %)' },
]

// فیلدهای ابعاد — حذف تکرار
const dimensionFields = [
  { key: 'weight', label: 'وزن (Weight)' },
  { key: 'width', label: 'عرض (Width)' },
  { key: 'height', label: 'ارتفاع (Height)' },
  { key: 'depth', label: 'عمق/طول (Depth)' },
]

const saveAllChanges = async () => {
  if (Object.keys(productUpdate.value).length === 0) {
    errorStore.addError({ type: 'warning', message: 'تغییری برای ذخیره‌سازی یافت نشد' })
    return
  }
  try {
    isLoading.value = true
    await productService.patchProduct(product.value.id, productUpdate.value)
    productUpdate.value = {}
    await refreshProductData()
    errorStore.addError({ type: 'success', message: 'تغییرات با موفقیت ذخیره شد' })
  } catch (error) {
    const msg = getErrorMessage(error.code) || 'خطایی در به‌روزرسانی محصول رخ داده است'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isLoading.value = false
  }
}

// جستجوی برند
const brandSearchQuery = ref('')
const searchedBrands = ref([])
const isSearchingBrand = ref(false)
let searchTimeout = null

watch(brandSearchQuery, (newQuery) => {
  if (!newQuery?.trim()) {
    searchedBrands.value = []
    return
  }
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    isSearchingBrand.value = true
    try {
      const response = await brandService.listBrands({ search: newQuery })
      searchedBrands.value = response?.items ?? []
    } catch (error) {
      errorStore.addError({
        type: 'error',
        message: `خطا در جستجوی برند: ${error?.detail?.message}`,
      })
      searchedBrands.value = []
    } finally {
      isSearchingBrand.value = false
    }
  }, 500)
})

const selectBrand = (brand) => {
  product.value.brand_id = brand.id
  product.value.brand = { id: brand.id, name: brand.name }
  productUpdate.value.brand_id = brand.id
  brandSearchQuery.value = ''
  searchedBrands.value = []
}

const removeCurrentBrand = () => {
  product.value.brand = null
  product.value.brand_id = null
  productUpdate.value.brand_id = null
  brandSearchQuery.value = ''
}
</script>
