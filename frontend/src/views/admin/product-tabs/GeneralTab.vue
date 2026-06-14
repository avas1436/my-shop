<!-- src/views/admin/product-tabs/GeneralTab.vue -->
<template>
  <div class="tab-content page-panel">
    <h2 class="tab-title">ویرایش اطلاعات پایه محصول</h2>

    <div class="form-section">
      <h3 class="specs-heading">وضعیت و تنظیمات کلی</h3>
      <div class="form-grid">
        <div class="form-group">
          <label>وضعیت انتشار (Status):</label>
          <div class="single-input-wrapper">
            <select
              :value="product.status"
              @change="updateField('status', $event.target.value)"
              class="base-input-field"
              :class="{ 'has-value': product.status }"
            >
              <option value="draft">پیش‌نویس</option>
              <option value="active">منتشر شده</option>
              <option value="inactive">غیر فعال</option>
              <option value="archived">بایگانی شده</option>
            </select>
          </div>
        </div>
        <div class="form-group toggle-group">
          <label class="toggle-label">
            <input
              type="checkbox"
              :checked="product.is_featured"
              @change="updateField('is_featured', $event.target.checked)"
            />
            کالای ویژه (Featured)
          </label>
          <label class="toggle-label">
            <input
              type="checkbox"
              :checked="product.is_digital"
              @change="updateField('is_digital', $event.target.checked)"
            />
            کالای دیجیتال
          </label>
        </div>
      </div>
    </div>

    <div class="form-section">
      <h3 class="specs-heading">مشخصات اصلی</h3>
      <div class="form-grid">
        <div class="form-group">
          <label>نام محصول:</label>
          <div class="single-input-wrapper">
            <input
              :value="product.name"
              @input="updateField('name', $event.target.value)"
              type="text"
              class="base-input-field"
              :class="{ 'has-value': product.name }"
            />
            <button
              v-if="product.name"
              type="button"
              class="clear-btn"
              @click="updateField('name', '')"
              title="پاک کردن"
            >
              ×
            </button>
          </div>
        </div>

        <div class="form-group">
          <label>برند محصول:</label>
          <div class="brand-search-container">
            <div class="single-input-wrapper">
              <input
                :value="product.brand && product.brand.name ? product.brand.name : brandSearchQuery"
                @input="(e) => (brandSearchQuery = e.target.value)"
                type="text"
                placeholder="بخشی از نام برند را تایپ کنید..."
                :readonly="product.brand && product.brand.name"
                class="base-input-field"
                :class="{ 'has-value': product.brand && product.brand.name }"
              />
              <button
                v-if="product.brand && product.brand.name"
                type="button"
                class="clear-btn"
                @click="removeCurrentBrand"
                title="حذف برند و جستجوی مجدد"
              >
                ×
              </button>
            </div>

            <p v-if="isSearchingBrand && !product.brand_id" class="search-loading">
              در حال جستجو...
            </p>

            <ul
              v-if="
                brandSearchQuery && searchedBrands.length && !isSearchingBrand && !product.brand_id
              "
              class="brand-search-results"
            >
              <li
                v-for="brand in searchedBrands"
                :key="brand.id"
                @click="selectBrand(brand)"
                class="clickable-brand-item"
              >
                {{ brand.name }}
              </li>
            </ul>

            <p
              v-if="
                brandSearchQuery && !searchedBrands.length && !isSearchingBrand && !product.brand_id
              "
              class="no-results"
            >
              برندی یافت نشد.
            </p>
          </div>
        </div>

        <div class="form-group">
          <label>کد کالا (SKU):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.sku"
              @input="updateField('sku', $event.target.value)"
              type="text"
              class="base-input-field"
              :class="{ 'has-value': product.sku }"
            />
            <button
              v-if="product.sku"
              type="button"
              class="clear-btn"
              @click="updateField('sku', '')"
              title="پاک کردن"
            >
              ×
            </button>
          </div>
        </div>

        <div class="form-group full-width">
          <label>توضیحات (Description):</label>
          <div class="single-input-wrapper">
            <textarea
              :value="product.description"
              @input="updateField('description', $event.target.value)"
              rows="4"
              class="base-input-field"
              :class="{ 'has-value': product.description }"
            ></textarea>
            <button
              v-if="product.description"
              type="button"
              class="clear-btn textarea-clear"
              @click="updateField('description', '')"
              title="پاک کردن"
            >
              ×
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="form-section admin-pricing-box">
      <h3 class="specs-heading">قیمت‌گذاری و مالیات</h3>
      <div class="form-grid">
        <div class="form-group">
          <label>قیمت اصلی (Price):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.price"
              @input="
                updateField(
                  'price',
                  $event.target.value === '' ? null : Number($event.target.value),
                )
              "
              type="number"
              class="base-input-field"
              :class="{ 'has-value': product.price !== null && product.price !== '' }"
            />
            <button
              v-if="product.price !== null && product.price !== ''"
              type="button"
              class="clear-btn"
              @click="updateField('price', null)"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>قیمت با تخفیف (Discount Price):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.discount_price"
              @input="
                updateField(
                  'discount_price',
                  $event.target.value === '' ? null : Number($event.target.value),
                )
              "
              type="number"
              class="base-input-field"
              :class="{
                'has-value': product.discount_price !== null && product.discount_price !== '',
              }"
            />
            <button
              v-if="product.discount_price !== null && product.discount_price !== ''"
              type="button"
              class="clear-btn"
              @click="updateField('discount_price', null)"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>قیمت خرید (Cost Price):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.cost_price"
              @input="
                updateField(
                  'cost_price',
                  $event.target.value === '' ? null : Number($event.target.value),
                )
              "
              type="number"
              class="base-input-field"
              :class="{ 'has-value': product.cost_price !== null && product.cost_price !== '' }"
            />
            <button
              v-if="product.cost_price !== null && product.cost_price !== ''"
              type="button"
              class="clear-btn"
              @click="updateField('cost_price', null)"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>نرخ مالیات (Tax Rate %):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.tax_rate"
              @input="
                updateField(
                  'tax_rate',
                  $event.target.value === '' ? null : Number($event.target.value),
                )
              "
              type="number"
              class="base-input-field"
              :class="{ 'has-value': product.tax_rate !== null && product.tax_rate !== '' }"
            />
            <button
              v-if="product.tax_rate !== null && product.tax_rate !== ''"
              type="button"
              class="clear-btn"
              @click="updateField('tax_rate', null)"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>واحد پول (Currency Code):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.currency_code"
              @input="updateField('currency_code', $event.target.value)"
              type="text"
              placeholder="مثال: IRI یا IRT"
              class="base-input-field"
              :class="{ 'has-value': product.currency_code }"
            />
            <button
              v-if="product.currency_code"
              type="button"
              class="clear-btn"
              @click="updateField('currency_code', '')"
            >
              ×
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="form-section">
      <h3 class="specs-heading">ابعاد و لجستیک</h3>
      <div class="form-grid">
        <div class="form-group">
          <label>وزن (Weight):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.weight"
              @input="
                updateField(
                  'weight',
                  $event.target.value === '' ? null : Number($event.target.value),
                )
              "
              type="number"
              class="base-input-field"
              :class="{ 'has-value': product.weight !== null && product.weight !== '' }"
            />
            <button
              v-if="product.weight !== null && product.weight !== ''"
              type="button"
              class="clear-btn"
              @click="updateField('weight', null)"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>عرض (Width):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.width"
              @input="
                updateField(
                  'width',
                  $event.target.value === '' ? null : Number($event.target.value),
                )
              "
              type="number"
              class="base-input-field"
              :class="{ 'has-value': product.width !== null && product.width !== '' }"
            />
            <button
              v-if="product.width !== null && product.width !== ''"
              type="button"
              class="clear-btn"
              @click="updateField('width', null)"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>ارتفاع (Height):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.height"
              @input="
                updateField(
                  'height',
                  $event.target.value === '' ? null : Number($event.target.value),
                )
              "
              type="number"
              class="base-input-field"
              :class="{ 'has-value': product.height !== null && product.height !== '' }"
            />
            <button
              v-if="product.height !== null && product.height !== ''"
              type="button"
              class="clear-btn"
              @click="updateField('height', null)"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>عمق/طول (Depth):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.depth"
              @input="
                updateField(
                  'depth',
                  $event.target.value === '' ? null : Number($event.target.value),
                )
              "
              type="number"
              class="base-input-field"
              :class="{ 'has-value': product.depth !== null && product.depth !== '' }"
            />
            <button
              v-if="product.depth !== null && product.depth !== ''"
              type="button"
              class="clear-btn"
              @click="updateField('depth', null)"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>بارکد جهانی (GTIN):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.gtin"
              @input="updateField('gtin', $event.target.value)"
              type="text"
              class="base-input-field"
              :class="{ 'has-value': product.gtin }"
            />
            <button
              v-if="product.gtin"
              type="button"
              class="clear-btn"
              @click="updateField('gtin', '')"
            >
              ×
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="form-section">
      <h3 class="specs-heading">سئو (SEO)</h3>
      <div class="form-grid">
        <div class="form-group full-width">
          <label>نامک (Slug):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.slug"
              @input="updateField('slug', $event.target.value)"
              type="text"
              class="base-input-field"
              :class="{ 'has-value': product.slug }"
            />
            <button
              v-if="product.slug"
              type="button"
              class="clear-btn"
              @click="updateField('slug', '')"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group full-width">
          <label>عنوان متا (Meta Title):</label>
          <div class="single-input-wrapper">
            <input
              :value="product.meta_title"
              @input="updateField('meta_title', $event.target.value)"
              type="text"
              class="base-input-field"
              :class="{ 'has-value': product.meta_title }"
            />
            <button
              v-if="product.meta_title"
              type="button"
              class="clear-btn"
              @click="updateField('meta_title', '')"
            >
              ×
            </button>
          </div>
        </div>
        <div class="form-group full-width">
          <label>توضیحات متا (Meta Description):</label>
          <div class="single-input-wrapper">
            <textarea
              :value="product.meta_description"
              @input="updateField('meta_description', $event.target.value)"
              rows="3"
              class="base-input-field"
              :class="{ 'has-value': product.meta_description }"
            ></textarea>
            <button
              v-if="product.meta_description"
              type="button"
              class="clear-btn textarea-clear"
              @click="updateField('meta_description', '')"
            >
              ×
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="form-actions mt-4 border-top pt-4">
      <BaseButton
        variant="primary"
        size="lg"
        @click="saveAllChanges"
        :disabled="isLoading"
        class="w-100"
      >
        {{ isLoading ? 'در حال ذخیره‌سازی...' : ' ذخیره تمامی اطلاعات پایه' }}
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { brandService, productService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { inject, ref, watch } from 'vue'

const errorStore = useErrorStore()

// ==============================
// دریافت دیتای اصلی از پوسته والد (Inject)
// ==============================
const product = inject('product')
const productUpdate = inject('productUpdate')
const isLoading = inject('isLoading')
const refreshProductData = inject('refreshProductData')
const updateField = inject('updateField')

// ==============================
// ذخیره اطلاعات پایه محصول
// ==============================
const saveAllChanges = async () => {
  try {
    isLoading.value = true

    // بررسی اینکه آیا اصلاً دیتایی تغییر کرده است یا خیر
    if (Object.keys(productUpdate.value).length === 0) {
      errorStore.addError({ type: 'warning', message: 'تغییری برای ذخیره‌سازی یافت نشد' })
      isLoading.value = false
      return
    }

    // ارسال فقط تغییرات به بک‌اند
    await productService.patchProduct(product.value.id, productUpdate.value)

    // پاک کردن آبجکت تغییرات پس از ذخیره موفق
    productUpdate.value = {}

    await refreshProductData()

    errorStore.addError({ type: 'success', message: 'تغییرات با موفقیت ذخیره شد' })
  } catch (error) {
    console.log(error)
    const msg = getErrorMessage(error.code) || 'خطایی در به‌روزرسانی محصول رخ داده است'
    errorStore.addError({ type: 'error', message: msg })
  } finally {
    isLoading.value = false
  }
}

// ==============================
// متغیرهای مربوط به جستجوی برند
// ==============================
const brandSearchQuery = ref('')
const searchedBrands = ref([])
const isSearchingBrand = ref(false)
let searchTimeout = null

watch(brandSearchQuery, (newQuery) => {
  if (!newQuery || newQuery.trim() === '') {
    searchedBrands.value = []
    return
  }
  if (searchTimeout) clearTimeout(searchTimeout)

  searchTimeout = setTimeout(async () => {
    isSearchingBrand.value = true
    try {
      const response = await brandService.listBrands({ search: newQuery })
      if (response && response.items) {
        searchedBrands.value = response.items
      } else {
        searchedBrands.value = []
      }
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
  productUpdate.value.brand_id = brand.id // اضافه کردن تغییرات برند به productUpdate
  brandSearchQuery.value = ''
  searchedBrands.value = []
}

const removeCurrentBrand = () => {
  product.value.brand = null
  product.value.brand_id = null
  productUpdate.value.brand_id = null // ثبت حذف برند در productUpdate
  brandSearchQuery.value = ''
}
</script>

<style scoped>
/* انیمیشن لود شدن تب */
.tab-content {
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* تیترهای داخلی */
.tab-title {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  color: #1e293b;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 0.5rem;
}
.specs-heading {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: #334155;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 0.5rem;
}

/* شبکه بندی فرم ها */
.form-section {
  margin-bottom: 2rem;
}
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.25rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-group.full-width {
  grid-column: 1 / -1;
}
.form-group label {
  font-size: 0.85rem;
  color: #475569;
  font-weight: 600;
}

/* ==================
   استایل‌های یکپارچه فیلدها 
   ================== */
.single-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.base-input-field {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0.6rem 0.75rem;
  font-family: inherit;
  font-size: 0.95rem;
  background: #fff;
  transition: all 0.2s;
  box-sizing: border-box;
}

.base-input-field:focus {
  border-color: #5b3df5;
  outline: none;
  box-shadow: 0 0 0 2px rgba(91, 61, 245, 0.1);
}

.base-input-field.has-value {
  background-color: #f1f5f9;
  border-color: #e2e8f0;
  color: #334155;
  padding-left: 2rem; /* فضا برای دکمه حذف */
}

/* دکمه پاک کردن فیلدها */
.clear-btn {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.25rem;
  font-weight: bold;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: color 0.2s;
}

.clear-btn:hover {
  color: #ef4444;
}

.clear-btn.textarea-clear {
  top: 12px;
  transform: none;
}

/* استایل های مربوط به جستجوی برند */
.brand-search-container {
  position: relative;
  width: 100%;
}
.brand-search-results {
  position: absolute;
  top: 100%;
  right: 0;
  left: 0;
  z-index: 10;
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0 0;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #fff;
  max-height: 200px;
  overflow-y: auto;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.clickable-brand-item {
  padding: 0.75rem;
  cursor: pointer;
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.2s;
}
.clickable-brand-item:last-child {
  border-bottom: none;
}
.clickable-brand-item:hover {
  background: #f1f5f9;
  color: #5b3df5;
}
.search-loading,
.no-results {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #64748b;
  text-align: center;
}

/* چک باکس های وضعیت */
.toggle-group {
  flex-direction: row;
  align-items: center;
  gap: 1.5rem;
  padding-top: 1.5rem;
}
.toggle-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  color: #334155;
}

/* پنل ها و المان های کاربردی */
.admin-pricing-box {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}
.w-100 {
  width: 100%;
}
.mt-4 {
  margin-top: 1.5rem;
}
.pt-4 {
  padding-top: 1.5rem;
}
.border-top {
  border-top: 1px solid #e2e8f0;
}
</style>
