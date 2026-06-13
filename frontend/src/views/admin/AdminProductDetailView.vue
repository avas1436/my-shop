<template>
  <div v-if="isLoading" class="admin-loading">
    <p>در حال بارگذاری پوسته ادمین با ساختار تب‌بندی...</p>
  </div>

  <div v-else-if="product" class="page-shell admin-storefront-mode">
    <div class="tabs-header-wrapper">
      <div class="tabs-navigation">
        <button :class="{ active: currentTab === 'general' }" @click="currentTab = 'general'">
          اطلاعات پایه
        </button>
        <button :class="{ active: currentTab === 'images' }" @click="currentTab = 'images'">
          تصاویر
        </button>
        <button :class="{ active: currentTab === 'inventory' }" @click="currentTab = 'inventory'">
          موجودی و تنوع
        </button>
        <button :class="{ active: currentTab === 'relations' }" @click="currentTab = 'relations'">
          دسته‌بندی و ویژگی‌ها
        </button>
        <button :class="{ active: currentTab === 'comments' }" @click="currentTab = 'comments'">
          نظرات
        </button>
        <button :class="{ active: currentTab === 'actions' }" @click="currentTab = 'actions'">
          وضعیت و عملیات نهایی
        </button>
      </div>
    </div>

    <div v-if="currentTab === 'general'" class="tab-content page-panel">
      <h2 class="tab-title">ویرایش اطلاعات پایه محصول</h2>

      <div class="form-section">
        <h3 class="specs-heading">وضعیت و تنظیمات کلی</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>وضعیت انتشار (Status):</label>
            <select v-model="product.status">
              <option value="draft">پیش‌نویس</option>
              <option value="active">منتشر شده</option>
              <option value="inactive">غیر فعال</option>
              <option value="archived">بایگانی شده</option>
            </select>
          </div>
          <div class="form-group toggle-group">
            <label class="toggle-label">
              <input type="checkbox" v-model="product.is_featured" />
              کالای ویژه (Featured)
            </label>
            <label class="toggle-label">
              <input type="checkbox" v-model="product.is_digital" />
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
            <input v-model="product.name" type="text" />
          </div>

          <div class="form-group">
            <label>جستجوی نام برند:</label>
            <div class="brand-search-container">
              <input
                v-model="brandSearchQuery"
                type="text"
                placeholder="بخشی از نام برند را تایپ کنید..."
              />
              <p v-if="isSearchingBrand" class="search-loading">در حال جستجو...</p>

              <ul
                v-if="brandSearchQuery && searchedBrands.length && !isSearchingBrand"
                class="brand-search-results"
              >
                <li
                  v-for="brand in searchedBrands"
                  :key="brand.id"
                  @click="selectBrand(brand)"
                  class="clickable-brand-item"
                >
                  {{ brand.name }} (ID: {{ brand.id }})
                </li>
              </ul>

              <p
                v-if="brandSearchQuery && !searchedBrands.length && !isSearchingBrand"
                class="no-results"
              >
                برندی یافت نشد.
              </p>
            </div>
          </div>

          <div class="form-group">
            <label>آیدی برند:</label>
            <input
              v-model.number="product.brand_id"
              type="number"
              placeholder="وارد کردن مستقیم آیدی"
            />
          </div>

          <div class="form-group">
            <label>کد کالا (SKU):</label>
            <input v-model="product.sku" type="text" />
          </div>
          <div class="form-group full-width">
            <label>توضیحات (Description):</label>
            <textarea v-model="product.description" rows="4"></textarea>
          </div>
        </div>
      </div>

      <div class="form-section admin-pricing-box">
        <h3 class="specs-heading">قیمت‌گذاری و مالیات</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>قیمت اصلی (Price):</label>
            <input v-model.number="product.price" type="number" />
          </div>
          <div class="form-group">
            <label>قیمت با تخفیف (Discount Price):</label>
            <input v-model.number="product.discount_price" type="number" />
          </div>
          <div class="form-group">
            <label>قیمت خرید (Cost Price):</label>
            <input v-model.number="product.cost_price" type="number" />
          </div>
          <div class="form-group">
            <label>نرخ مالیات (Tax Rate %):</label>
            <input v-model.number="product.tax_rate" type="number" />
          </div>
          <div class="form-group">
            <label>واحد پول (Currency Code):</label>
            <input v-model="product.currency_code" type="text" placeholder="مثال: IRI یا IRT" />
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3 class="specs-heading">ابعاد و لجستیک</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>وزن (Weight):</label>
            <input type="number" v-model.number="product.weight" />
          </div>
          <div class="form-group">
            <label>عرض (Width):</label>
            <input type="number" v-model.number="product.width" />
          </div>
          <div class="form-group">
            <label>ارتفاع (Height):</label>
            <input type="number" v-model.number="product.height" />
          </div>
          <div class="form-group">
            <label>عمق/طول (Depth):</label>
            <input type="number" v-model.number="product.depth" />
          </div>
          <div class="form-group">
            <label>بارکد جهانی (GTIN):</label>
            <input type="text" v-model="product.gtin" />
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3 class="specs-heading">سئو (SEO)</h3>
        <div class="form-grid">
          <div class="form-group full-width">
            <label>نامک (Slug):</label>
            <input type="text" v-model="product.slug" />
          </div>
          <div class="form-group full-width">
            <label>عنوان متا (Meta Title):</label>
            <input type="text" v-model="product.meta_title" />
          </div>
          <div class="form-group full-width">
            <label>توضیحات متا (Meta Description):</label>
            <textarea v-model="product.meta_description" rows="3"></textarea>
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

    <div v-else-if="currentTab === 'images'" class="tab-content page-panel">
      <div class="admin-gallery-wrapper">
        <div class="main-image-holder">
          <img v-if="primaryImage" :src="primaryImage.real_url" :alt="primaryImage.alt_text" />
          <div v-else class="no-image">بدون تصویر</div>
          <div class="image-overlay-info">گالری تصاویر ({{ product.images?.length || 0 }} عکس)</div>
        </div>

        <div class="upload-section">
          <label class="btn-upload">
            آپلود تصویر جدید
            <input type="file" @change="handleImageUpload" accept="image/*" hidden />
          </label>
        </div>

        <div class="thumb-strip">
          <div v-for="img in product.images" :key="img.id" class="thumb-container">
            <img
              :src="img.real_url"
              :class="{ active: img.is_primary }"
              @click="setPrimaryImage(img.id)"
              title="برای انتخاب به عنوان تصویر اصلی کلیک کنید"
            />
            <button class="btn-remove-img" @click.stop="deleteImage(img.id)">×</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="currentTab === 'inventory'" class="tab-content page-panel">
      <div class="detail-actions admin-inventory-section">
        <h3 class="inventory-title">مدیریت زنده تنوع‌ها (رنگ / سایز)</h3>

        <div class="detail-rating admin-meta-row mb-3">
          <span class="muted" :class="{ 'text-danger': !product.is_in_stock }">
            موجودی کل انبار: {{ product.total_available_quantity }} عدد ({{
              product.is_in_stock ? 'موجود' : 'ناموجود'
            }})
          </span>
        </div>

        <div v-if="product.inventory?.length" class="admin-variant-grid">
          <div v-for="item in product.inventory" :key="item.id" class="variant-row-card">
            <div class="variant-info">
              <span class="muted text-small">{{ item.sku }}</span>
              <span v-for="attr in item.attributes" :key="attr.attribute_id" class="attr-badge">
                {{ attr.name }}: {{ attr.value }}
              </span>
            </div>
            <div class="variant-inputs">
              <label>
                <span>موجودی:</span>
                <input
                  v-model.number="item.quantity"
                  type="number"
                  @change="patchVariant(item.id, 'quantity', item.quantity)"
                />
              </label>
              <label>
                <span>قیمت نهایی:</span>
                <input
                  v-model.number="item.final_price"
                  type="number"
                  @change="patchVariant(item.id, 'final_price', item.final_price)"
                />
              </label>
              <button class="btn-icon-danger" @click="deleteInventory(item.id)" title="حذف تنوع">
                🗑️
              </button>
            </div>
          </div>
        </div>

        <div class="add-inventory-form">
          <input v-model.number="newVariant.quantity" type="number" placeholder="تعداد" />
          <input
            v-model.number="newVariant.final_price"
            type="number"
            placeholder="قیمت نهایی (اختیاری)"
          />
          <input v-model="newVariant.sku" type="text" placeholder="SKU (اختیاری)" />
          <button class="btn-add" @click="addInventory">ثبت موجودی جدید</button>
        </div>
      </div>
    </div>

    <div v-else-if="currentTab === 'relations'" class="tab-content admin-secondary-layout">
      <section class="page-panel admin-settings-panel">
        <h3 class="specs-heading">اتصال دسته‌بندی‌ها</h3>
        <div class="checkbox-list">
          <label v-for="cat in categoriesList" :key="cat.id" class="checkbox-item">
            <input
              type="checkbox"
              :checked="isCategoryAttached(cat.id)"
              @change="toggleCategory($event, cat.id)"
            />
            {{ cat.name }}
          </label>
        </div>
      </section>

      <section class="page-panel admin-settings-panel">
        <h3 class="specs-heading">اتصال برچسب‌ها (Tags)</h3>
        <div class="checkbox-list">
          <label v-for="tag in tagsList" :key="tag.id" class="checkbox-item">
            <input
              type="checkbox"
              :checked="isTagAttached(tag.id)"
              @change="toggleTag($event, tag.id)"
            />
            #{{ tag.name }}
          </label>
        </div>
      </section>

      <section class="page-panel admin-settings-panel" style="grid-column: 1 / -1">
        <h3 class="specs-heading">ویژگی‌های کالا (Attributes)</h3>
        <ul class="detail-specs admin-specs-list">
          <li v-for="spec in product.attributes" :key="spec.attribute_id">
            <span>{{ spec.name }}</span>
            <div class="spec-actions">
              <input
                v-model="spec.value"
                type="text"
                @change="patchAttribute(spec.attribute_id, spec.value)"
              />
              <button
                class="btn-icon-danger"
                @click="removeAttribute(spec.attribute_id)"
                title="حذف ویژگی"
              >
                ×
              </button>
            </div>
          </li>
        </ul>

        <div class="add-attribute-form mt-3">
          <select v-model="newAttribute.id">
            <option value="" disabled>انتخاب ویژگی جدید...</option>
            <option v-for="attr in attributesList" :key="attr.id" :value="attr.id">
              {{ attr.name }}
            </option>
          </select>
          <input v-model="newAttribute.value" type="text" placeholder="مقدار ویژگی" />
          <button class="btn-add" @click="addAttribute">افزودن</button>
        </div>
      </section>
    </div>

    <div v-else-if="currentTab === 'comments'" class="tab-content page-panel admin-settings-panel">
      <h3 class="specs-heading">نظرات کاربران</h3>
      <div v-if="commentsList.length" class="comments-wrapper">
        <div v-for="comment in commentsList" :key="comment.id" class="comment-card">
          <div class="comment-header">
            <strong>{{ comment.user_name || 'کاربر مهمان' }}</strong>
            <span class="text-small muted">{{ formatPrsianDate(comment.created_at) }}</span>
          </div>
          <p class="comment-body">{{ comment.content }}</p>
          <div class="comment-actions">
            <button class="btn-icon-danger text-small" @click="deleteComment(comment.id)">
              حذف نظر
            </button>
          </div>
        </div>
      </div>
      <div v-else class="text-small muted">تا کنون نظری برای این کالا ثبت نشده است.</div>
    </div>

    <div v-else-if="currentTab === 'actions'" class="tab-content page-panel admin-actions-tab">
      <h2 class="tab-title">تنظیمات وضعیت و عملیات نهایی محصول</h2>

      <div class="status-status-box">
        <div class="status-indicator-large">
          <span>وضعیت فعلی کالا در سیستم:</span>
          <strong :class="product.status === 'active' ? 'text-success' : 'text-warning'">
            {{ product.status === 'active' ? '🟢 منتشر شده (Active)' : '🟡 پیش‌نویس (Draft)' }}
          </strong>
        </div>
        <p class="text-small muted mt-2">
          وقتی محصول در وضعیت پیش‌نویس باشد، در ویترین فروشگاه به کاربران نمایش داده نمی‌شود. با زدن
          دکمه انتشار نهایی، محصول برای عموم در دسترس خواهد بود.
        </p>
      </div>

      <div class="danger-zone-box mt-3">
        <h3 class="danger-title">عملیات مدیریتی</h3>
        <div class="action-buttons-vertical">
          <BaseButton
            v-if="product && product.status !== 'active'"
            variant="success"
            size="lg"
            @click="handlePublish"
            class="w-100 mb-2"
          >
            🚀 انتشار نهایی محصول در سایت
          </BaseButton>

          <div class="separator" v-if="product && product.status !== 'active'"></div>

          <p class="text-small text-danger mb-2">
            <strong>منطقه حساس:</strong> حذف دائمی باعث پاک شدن محصول از دیتابیس و گالری تصاویر
            خواهد شد.
          </p>
          <button class="btn-delete-hard-large" @click="handleHardDelete">
            🗑️ حذف دائمی و قطعی محصول
          </button>
        </div>
      </div>
    </div>

    <div class="timestamps-footer page-panel">
      <span v-if="product.created_at"
        >ساخته شده در: {{ formatPrsianDate(product.created_at) }}</span
      >
      <span v-if="product.updated_at"
        >آخرین بروزرسانی: {{ formatPrsianDate(product.updated_at) }}</span
      >
      <span v-if="product.published_at"
        >تاریخ انتشار: {{ formatPrsianDate(product.published_at) }}</span
      >
    </div>
  </div>

  <div v-else class="page-shell">
    <section class="empty-state">محصول مورد نظر جهت مدیریت یافت نشد.</section>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { brandService, productService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { formatPrsianDate } from '@/utils/format'
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute() // اطلاعات مسیر فعلی
const router = useRouter() // رفتن به مسیر های دیگه

const isLoading = ref(true)
const product = ref(null)

// کنترل تب فعلی
const currentTab = ref('general')

// استیت‌های فرم‌های ایجاد سریع
const newVariant = ref({ quantity: 0, final_price: null, sku: '' })
const newAttribute = ref({ id: '', value: '' })

// ==============================
// واکشی تمامی اطلاعات مورد نیاز
// ==============================
const loadAllAdminData = async () => {
  try {
    isLoading.value = true
    const pId = route.params.product_id

    // واکشی دیتای محصول
    const response = await productService.getProductFull(pId)
    product.value = response
  } catch (error) {
    const errorStore = useErrorStore()
    const msg = getErrorMessage(error.code) || 'خطایی رخ داده است'

    errorStore.addError({
      type: 'error',
      message: msg,
    })
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadAllAdminData()
})

// ==============================
// توابع ویرایش پایه
// ==============================
const productUpdate = ref({})

const refreshProductData = async () => {
  const response = await productService.getProductFull(product.value.id)
  product.value = response
}

// ذخیره تمامی اطلاعات در یک درخواست واحد (جایگزین patchField)
const saveAllChanges = async () => {
  try {
    isLoading.value = true

    // ارسال کل آبجکت محصول به بک‌اند
    await productService.updateProduct(product.value.id, productUpdate.value)

    // فراخوانی مجدد اطلاعات برای اطمینان از صحت دیتا
    await refreshProductData()

    // نمایش پیام موفقیت
    const errorStore = useErrorStore()
    errorStore.addError({
      type: 'success',
      message: 'تغییرات با موفقیت ذخیره شد',
    })
  } catch (error) {
    // استفاده از الگوی ارور هندلینگ اختصاصی
    const errorStore = useErrorStore()
    const msg = getErrorMessage(error.code) || 'خطایی در به‌روزرسانی محصول رخ داده است'

    errorStore.addError({
      type: 'error',
      message: msg,
    })
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

// گوش دادن به تغییرات اینپوت جستجو برای ارسال ریکوئست به بک‌اند
watch(brandSearchQuery, (newQuery) => {
  // اگر فیلد خالی شد، لیست نتایج را پاک کن
  if (!newQuery || newQuery.trim() === '') {
    searchedBrands.value = []
    return
  }

  // پاک کردن تایمر قبلی (Debounce)
  if (searchTimeout) clearTimeout(searchTimeout)

  // تنظیم تایمر جدید (۵۰۰ میلی‌ثانیه تاخیر)
  searchTimeout = setTimeout(async () => {
    isSearchingBrand.value = true
    try {
      // ارسال درخواست به روتر جستجوی برند با پارامتر search
      const response = await brandService.listBrands({
        search: newQuery,
      })

      // استخراج لیست برندها دقیقاً بر اساس ساختار JSON شما
      if (response && response.data && response.data.items) {
        searchedBrands.value = response.data.items
      } else {
        searchedBrands.value = []
      }
    } catch (error) {
      const errorStore = useErrorStore()
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

// انتخاب برند از لیست و پر کردن خودکار آیدی
const selectBrand = (brand) => {
  product.value.brand_id = brand.id
  brandSearchQuery.value = brand.name // نمایش نام برند در فیلد جستجو
  searchedBrands.value = [] // بستن منوی نتایج
}

// ==============================
// پردازش‌های تصویر
// ==============================
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
    alert('خطا در آپلود تصویر')
  }
}

const deleteImage = async (imageId) => {
  if (!confirm('تصویر حذف شود؟')) return
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

// ==============================
// اتصالات (Categories & Tags)
// ==============================
const isCategoryAttached = (catId) => product.value.categories?.some((c) => c.id === catId)
const isTagAttached = (tagId) => product.value.tags?.some((t) => t.id === tagId)

const toggleCategory = async (event, catId) => {
  try {
    if (event.target.checked) {
      await productService.attachCategory(product.value.id, catId)
    } else {
      await productService.detachCategory(product.value.id, catId)
    }
    await refreshProductData()
  } catch (error) {
    alert('خطا در تغییر دسته‌بندی')
  }
}

const toggleTag = async (event, tagId) => {
  try {
    if (event.target.checked) {
      await productService.attachTag(product.value.id, tagId)
    } else {
      await productService.detachTag(product.value.id, tagId)
    }
    await refreshProductData()
  } catch (error) {
    alert('خطا در تغییر برچسب')
  }
}

// ==============================
// موجودی (Inventory)
// ==============================
async function patchVariant(inventoryId, subField, value) {
  try {
    await productService.updateInventory(inventoryId, { [subField]: value })
  } catch (error) {
    console.error('خطا در پچ تنوع کالا')
  }
}

async function addInventory() {
  if (newVariant.value.quantity === null) return
  try {
    await productService.createInventory(product.value.id, newVariant.value)
    newVariant.value = { quantity: 0, final_price: null, sku: '' }
    await refreshProductData()
  } catch (error) {
    alert('خطا در ثبت موجودی')
  }
}

async function deleteInventory(inventoryId) {
  if (!confirm('این تنوع حذف شود؟')) return
  try {
    await productService.deleteInventory(inventoryId)
    await refreshProductData()
  } catch (error) {
    console.error(error)
  }
}

// ==============================
// ویژگی‌ها (Attributes)
// ==============================
async function patchAttribute(attributeId, value) {
  try {
    await productService.updateProductAttribute(product.value.id, attributeId, { value })
  } catch (error) {
    console.error('خطا در پچ ویژگی')
  }
}

async function addAttribute() {
  if (!newAttribute.value.id || !newAttribute.value.value) return
  try {
    await productService.attachAttribute(product.value.id, newAttribute.value)
    newAttribute.value = { id: '', value: '' }
    await refreshProductData()
  } catch (error) {
    alert('خطا در افزودن ویژگی')
  }
}

async function removeAttribute(attributeId) {
  if (!confirm('ویژگی حذف شود؟')) return
  try {
    await productService.detachAttribute(product.value.id, attributeId)
    await refreshProductData()
  } catch (error) {
    console.error(error)
  }
}

// ==============================
// نظرات (Comments)
// ==============================
async function deleteComment(commentId) {
  if (!confirm('آیا از حذف این نظر اطمینان دارید؟')) return
  try {
    await productService.deleteComment(commentId)
    commentsList.value = commentsList.value.filter((c) => c.id !== commentId)
  } catch (error) {
    alert('خطا در حذف نظر')
  }
}

// ==============================
// عملیات اصلی محصول
// ==============================
async function handlePublish() {
  try {
    await productService.publishProduct(product.value.id)
    product.value.status = 'active'
    alert('محصول با موفقیت منتشر شد.')
  } catch (error) {
    alert('خطا در انتشار محصول')
  }
}

async function handleHardDelete() {
  if (
    !confirm('آیا از حذف همیشگی این محصول از کل پایگاه داده مطمئن هستید؟ غیرقابل بازگشت خواهد بود!')
  )
    return
  try {
    await productService.hardDelete(product.value.id)
    router.push('/admin/products')
  } catch (error) {
    alert('خطا در حذف کالا')
  }
}
</script>

<style scoped>
.admin-storefront-mode {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  direction: rtl;
}

/* ساختار هدر تب‌ها برای قرار گرفتن دکمه بازگشت در کنار آن */
.tabs-header-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

/* استایل‌های مربوط به سیستم تب‌ها */
.tabs-navigation {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  overflow-y: hidden;
}
.tabs-navigation button {
  background: transparent;
  border: none;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
  white-space: nowrap;
}
.tabs-navigation button:hover {
  color: #334155;
  background: #f8fafc;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}
.tabs-navigation button.active {
  color: #5b3df5;
  border-bottom-color: #5b3df5;
}

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

.tab-title {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  color: #1e293b;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 0.5rem;
}

/* استایل‌های تب عملیات نهایی */
.admin-actions-tab {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.status-status-box {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  padding: 1.5rem;
  border-radius: 8px;
}
.status-indicator-large {
  display: flex;
  gap: 1rem;
  font-size: 1.1rem;
  align-items: center;
}
.danger-zone-box {
  border: 1px solid #fca5a5;
  background: #fff5f5;
  padding: 1.5rem;
  border-radius: 8px;
}
.danger-title {
  color: #991b1b;
  font-size: 1.05rem;
  margin-bottom: 1rem;
  font-weight: bold;
}
.action-buttons-vertical {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
}
.separator {
  height: 1px;
  background: #fee2e2;
  margin: 0.5rem 0;
}
.btn-delete-hard-large {
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  transition: background 0.2s;
  font-size: 0.95rem;
  text-align: center;
}
.btn-delete-hard-large:hover {
  background: #b91c1c;
}
.btn-back {
  background: #475569;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background 0.2s;
}
.btn-back:hover {
  background: #334155;
}

/* استایل‌های فرم تب اول */
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
.form-group input,
.form-group select,
.form-group textarea {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0.6rem 0.75rem;
  font-family: inherit;
  font-size: 0.95rem;
  background: #fff;
  transition: border-color 0.2s;
  width: 100%;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #5b3df5;
  outline: none;
  box-shadow: 0 0 0 2px rgba(91, 61, 245, 0.1);
}

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

.text-success {
  color: #16a34a;
}
.text-warning {
  color: #d97706;
}

/* نگهداری استایل‌های دیگر پنل‌ها */
.page-panel {
  background: var(--surface, #fff);
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
.admin-secondary-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}
.admin-gallery-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.main-image-holder {
  position: relative;
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 12px;
  min-height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image-holder img {
  max-width: 100%;
  max-height: 340px;
  object-fit: contain;
}

.image-overlay-info {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  padding: 0.25rem 0.6rem;
  font-size: 0.75rem;
  border-radius: 4px;
}
.upload-section {
  text-align: center;
}
.btn-upload {
  background: #e2e8f0;
  color: #334155;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: bold;
  border: 1px solid #cbd5e1;
  display: inline-block;
}
.thumb-strip {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.thumb-container {
  position: relative;
  display: inline-block;
}
.thumb-strip img {
  width: 70px;
  height: 70px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  object-fit: cover;
  cursor: pointer;
}
.thumb-strip img.active {
  border-color: #5b3df5;
}
.btn-remove-img {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.specs-heading {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: #334155;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 0.5rem;
}

.admin-pricing-box {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}
.admin-inventory-section {
  background: #f0fdf4;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #bbf7d0;
}

.inventory-title {
  font-size: 1rem;
  color: #166534;
  margin-bottom: 1rem;
}

.admin-variant-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.variant-row-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #dcfce7;
  flex-wrap: wrap;
  gap: 1rem;
}

.add-inventory-form {
  display: flex;
  gap: 0.5rem;
  background: #fff;
  padding: 1rem;
  border-radius: 8px;
  border: 1px dashed #bbf7d0;
}
.btn-add {
  background: #10b981;
  color: #fff;
  border: none;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}
.btn-icon-danger {
  background: none;
  border: none;
  color: #ef4444;
  font-size: 1.2rem;
  cursor: pointer;
}
.checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
}
.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
}

.admin-specs-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}
.add-attribute-form {
  display: flex;
  gap: 0.5rem;
}
.comment-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  background: #f8fafc;
  margin-bottom: 1rem;
}

.timestamps-footer {
  display: flex;
  /* flex-direction: column; */
  gap: 1.5rem;
  font-size: 0.85rem;
  color: #94a3b8;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 1rem;
}

.admin-loading {
  text-align: center;
  padding: 4rem;
  font-weight: 700;
  font-size: 1.2rem;
  color: #475569;
}
.w-100 {
  width: 100%;
}
.mb-2 {
  margin-bottom: 0.5rem;
}
.mb-3 {
  margin-bottom: 1rem;
}
.mt-2 {
  margin-top: 0.5rem;
}
.mt-3 {
  margin-top: 1rem;
}

.brand-search-results {
  list-style: none;
  padding: 0;
  margin: 5px 0 0 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  max-height: 150px;
  overflow-y: auto;
  background-color: #fff;
  position: absolute; /* برای قرارگیری روی سایر المان‌ها در صورت نیاز */
  z-index: 10;
}

.clickable-brand-item {
  padding: 8px 12px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.clickable-brand-item:hover {
  background-color: #f0f0f0;
}

.no-results {
  font-size: 0.9em;
  color: #888;
  margin-top: 5px;
}

.form-actions {
  margin-top: 20px;
  text-align: left;
}

.btn-save {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-save:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
