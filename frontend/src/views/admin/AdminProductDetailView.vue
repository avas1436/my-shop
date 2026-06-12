<template>
  <div v-if="isLoading" class="admin-loading">
    <p>در حال بارگذاری پوسته ادمین با ساختار ویترین...</p>
  </div>

  <div v-else-if="product" class="page-shell admin-storefront-mode">
    <div class="admin-top-bar">
      <div class="status-info">
        <span>وضعیت کالا:</span>
        <select v-model="product.status" @change="patchField('status', product.status)">
          <option value="draft">پیش‌نویس (Draft)</option>
          <option value="active">منتشر شده (Active)</option>
        </select>
        <span class="sku-preview">کد کالا: {{ product.sku }}</span>

        <div class="quick-toggles">
          <label class="toggle-label">
            <input
              type="checkbox"
              v-model="product.is_featured"
              @change="patchField('is_featured', product.is_featured)"
            />
            کالای ویژه (Featured)
          </label>
          <label class="toggle-label">
            <input
              type="checkbox"
              v-model="product.is_digital"
              @change="patchField('is_digital', product.is_digital)"
            />
            کالای دیجیتال
          </label>
        </div>
      </div>

      <div class="action-buttons">
        <BaseButton
          v-if="product.status !== 'active'"
          variant="success"
          size="sm"
          @click="handlePublish"
        >
          🚀 انتشار سریع
        </BaseButton>
        <button class="btn-delete-hard" @click="handleHardDelete">حذف دائمی</button>
        <router-link to="/admin/products" class="btn-back">بازگشت</router-link>
      </div>
    </div>

    <section class="detail-layout page-panel">
      <div class="admin-gallery-wrapper">
        <div class="main-image-holder">
          <img v-if="primaryImage" :src="primaryImage.real_url" :alt="primaryImage.alt_text" />
          <div class="image-overlay-info">گالری تصاویر ({{ product.images?.length || 0 }} عکس)</div>
        </div>
        <div class="thumb-strip">
          <img
            v-for="img in product.images"
            :key="img.id"
            :src="img.real_url"
            :class="{ active: img.is_primary }"
          />
        </div>
      </div>

      <div class="detail-content">
        <div class="detail-meta">
          <span class="inline-select">
            برند:
            <select v-model="product.brand.id" @change="patchField('brand_id', product.brand.id)">
              <option :value="product.brand?.id">{{ product.brand?.name || 'انتخاب برند' }}</option>
            </select>
          </span>
          <span class="muted">SKU: {{ product.sku }}</span>
        </div>

        <h1 class="page-title detail-title admin-editable-text">
          <input
            v-model="product.name"
            type="text"
            placeholder="نام محصول را وارد کنید"
            @change="patchField('name', product.name)"
          />
        </h1>

        <div class="page-description admin-editable-textarea">
          <textarea
            v-model="product.description"
            placeholder="توضیحات محصول..."
            @change="patchField('description', product.description)"
          ></textarea>
        </div>

        <div class="detail-rating admin-meta-row">
          <div>
            <strong>دسته‌بندی: </strong>
            <span v-for="cat in product.categories" :key="cat.id" class="badge-cat">{{
              cat.name
            }}</span>
          </div>
          <span class="muted" :class="{ 'text-danger': !product.is_in_stock }">
            موجودی کل انبار: {{ product.total_available_quantity }} عدد ({{
              product.is_in_stock ? 'موجود' : 'ناموجود'
            }})
          </span>
        </div>

        <div class="detail-pricing admin-pricing-box">
          <div class="price-fields">
            <div class="field-item">
              <label>قیمت اصلی ({{ product.currency_code }}):</label>
              <input
                v-model.number="product.price"
                type="number"
                @change="patchField('price', product.price)"
              />
            </div>
            <div class="field-item">
              <label>قیمت با تخفیف:</label>
              <input
                v-model.number="product.discount_price"
                type="number"
                @change="patchField('discount_price', product.discount_price)"
              />
            </div>
            <div class="field-item">
              <label>قیمت خرید (Cost):</label>
              <input
                v-model.number="product.cost_price"
                type="number"
                @change="patchField('cost_price', product.cost_price)"
              />
            </div>
          </div>
          <div class="calculated-pills">
            <span class="pill tax-pill">مالیات: ٪{{ product.tax_rate / 100 }}</span>
            <span v-if="product.discount_percent > 0" class="pill discount-pill"
              >٪{{ product.discount_percent }} تخفیف</span
            >
            <span class="pill info-pill">قیمت نهایی: {{ product.final_price }}</span>
            <span class="pill info-pill">قیمت با مالیات: {{ product.price_with_tax }}</span>
          </div>
        </div>

        <div v-if="product.inventory?.length" class="detail-actions admin-inventory-section">
          <h3 class="inventory-title">مدیریت زنده تنوع‌ها (رنگ / سایز)</h3>
          <div class="admin-variant-grid">
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
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="admin-secondary-layout">
      <section class="page-panel admin-settings-panel">
        <h3 class="specs-heading">ابعاد و لجستیک</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>وزن (گرم/کیلوگرم):</label>
            <input
              type="text"
              v-model="product.weight"
              @change="patchField('weight', product.weight)"
              placeholder="مثلا 350.000"
            />
          </div>
          <div class="form-group">
            <label>طول:</label>
            <input
              type="number"
              v-model.number="product.length"
              @change="patchField('length', product.length)"
              placeholder="0"
            />
          </div>
          <div class="form-group">
            <label>عرض (Width):</label>
            <input
              type="number"
              v-model.number="product.width"
              @change="patchField('width', product.width)"
              placeholder="0"
            />
          </div>
          <div class="form-group">
            <label>ارتفاع (Height):</label>
            <input
              type="number"
              v-model.number="product.height"
              @change="patchField('height', product.height)"
              placeholder="0"
            />
          </div>
          <div class="form-group">
            <label>بارکد جهانی (GTIN):</label>
            <input
              type="text"
              v-model="product.gtin"
              @change="patchField('gtin', product.gtin)"
              placeholder="GTIN/UPC..."
            />
          </div>
        </div>
      </section>

      <section class="page-panel admin-settings-panel">
        <h3 class="specs-heading">سئو (SEO)</h3>
        <div class="form-grid single-col">
          <div class="form-group">
            <label>نامک (Slug):</label>
            <input type="text" v-model="product.slug" @change="patchField('slug', product.slug)" />
          </div>
          <div class="form-group">
            <label>عنوان متا (Meta Title):</label>
            <input
              type="text"
              v-model="product.meta_title"
              @change="patchField('meta_title', product.meta_title)"
              placeholder="در صورت خالی بودن، نام کالا استفاده می‌شود"
            />
          </div>
          <div class="form-group">
            <label>توضیحات متا (Meta Description):</label>
            <textarea
              v-model="product.meta_description"
              @change="patchField('meta_description', product.meta_description)"
              rows="3"
              placeholder="توضیحات کوتاه برای گوگل..."
            ></textarea>
          </div>
        </div>
      </section>

      <section class="page-panel admin-settings-panel">
        <h3 class="specs-heading">ویژگی‌های کالا (Attributes)</h3>
        <ul class="detail-specs admin-specs-list">
          <li v-for="spec in product.attributes" :key="spec.attribute_id">
            <span>{{ spec.name }}</span>
            <input
              v-model="spec.value"
              type="text"
              @change="patchAttribute(spec.attribute_id, spec.value)"
            />
          </li>
        </ul>
      </section>
    </div>

    <section class="detail-extra admin-tags-section page-panel">
      <h3 class="specs-heading">برچسب‌ها / هشتگ‌های متصل به محصول</h3>
      <div class="admin-tags-flow">
        <span v-for="tag in product.tags" :key="tag.id" class="tag-pill"> # {{ tag.name }} </span>
      </div>

      <div class="timestamps-footer">
        <span v-if="product.created_at">ساخته شده در: {{ formatDate(product.created_at) }}</span>
        <span v-if="product.updated_at">آخرین بروزرسانی: {{ formatDate(product.updated_at) }}</span>
        <span v-if="product.published_at"
          >تاریخ انتشار: {{ formatDate(product.published_at) }}</span
        >
      </div>
    </section>
  </div>

  <div v-else class="page-shell">
    <section class="empty-state">محصول مورد نظر جهت مدیریت یافت نشد.</section>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import { productService } from '@/services/productService'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const isLoading = ref(true)
const product = ref(null)

const loadAdminProductData = async () => {
  try {
    isLoading.value = true
    const pId = route.params.product_id
    const response = await productService.getProductFull(pId)
    product.value = response.data || response
  } catch (error) {
    console.error('خطا در بارگذاری اطلاعات ادمین:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadAdminProductData()
})

const primaryImage = computed(() => {
  if (!product.value?.images) return null
  return product.value.images.find((img) => img.is_primary) || product.value.images[0]
})

// مبدل ساده تاریخ برای نمایش خواناتر اطلاعات دیتابیس
const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

async function patchField(fieldName, value) {
  try {
    await productService.patchProduct(product.value.id, { [fieldName]: value })
    // بازخوانی مقادیر محاسبه شده مالی در صورت تغییر فیلدهای قیمت‌گذاری
    if (['price', 'discount_price', 'cost_price', 'tax_rate'].includes(fieldName)) {
      const reload = await productService.getProductFull(product.value.id)
      product.value = reload.data || reload
    }
  } catch (error) {
    alert(`خطا در به‌روزرسانی آنی فیلد: ${fieldName}`)
  }
}

async function patchVariant(inventoryId, subField, value) {
  try {
    await productService.patchProduct(product.value.id, {
      inventory_update: { id: inventoryId, [subField]: value },
    })
  } catch (error) {
    console.error('خطا در پچ تنوع کالا')
  }
}

async function patchAttribute(attributeId, value) {
  try {
    await productService.patchProduct(product.value.id, {
      attribute_update: { id: attributeId, value: value },
    })
  } catch (error) {
    console.error('خطا در پچ ویژگی')
  }
}

async function handlePublish() {
  try {
    await productService.publishProduct(product.value.id)
    product.value.status = 'active'
  } catch (error) {
    alert('خطا در انتشار محصول')
  }
}

async function handleHardDelete() {
  if (!confirm('آیا از حذف همیشگی این محصول از کل پایگاه داده مطمئن هستید؟')) return
  try {
    await productService.hardDelete(product.value.id)
    router.push('/admin/products')
  } catch (error) {
    alert('خطا در حذف کالا')
  }
}
</script>

<style scoped>
/* حفظ اصالت کلاس‌های قبلی + استایل‌های جدید */
.admin-storefront-mode {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  direction: rtl;
}

.admin-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #0f172a;
  color: #fff;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  flex-wrap: wrap;
  gap: 1rem;
}

.status-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.status-info select {
  background: #1e293b;
  color: #fff;
  border: 1px solid #475569;
  padding: 0.4rem;
  border-radius: 6px;
}

.quick-toggles {
  display: flex;
  gap: 1rem;
  border-right: 1px solid #334155;
  padding-right: 1rem;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  cursor: pointer;
  color: #cbd5e1;
}

.sku-preview {
  color: #94a3b8;
  font-size: 0.9rem;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.btn-delete-hard {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
}

.btn-back {
  background: #334155;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.detail-layout {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 2rem;
  padding: 2rem;
  background: var(--surface, #fff);
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.admin-gallery-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

.thumb-strip {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.thumb-strip img {
  width: 60px;
  height: 60px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  object-fit: cover;
}

.thumb-strip img.active {
  border-color: #5b3df5;
}

.admin-editable-text input {
  width: 100%;
  border: 1px solid transparent;
  font-size: 2rem;
  font-weight: 800;
  outline: none;
  background: transparent;
  padding: 0.2rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.admin-editable-text input:focus,
.admin-editable-textarea textarea:focus {
  border-color: #5b3df5;
  background: #f8fafc;
}

.admin-editable-textarea textarea {
  width: 100%;
  min-height: 100px;
  border: 1px solid transparent;
  font-size: 1rem;
  line-height: 1.6;
  resize: vertical;
  background: transparent;
  outline: none;
  font-family: inherit;
  border-radius: 6px;
}

.admin-pricing-box {
  background: #f8fafc;
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  margin-top: 1rem;
}

.price-fields {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.field-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex: 1;
  min-width: 120px;
}

.field-item label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748b;
}

.field-item input {
  height: 40px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  padding: 0 0.75rem;
  font-weight: 700;
  font-size: 1rem;
}

.calculated-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.pill {
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
}

.tax-pill {
  background: #e0f2fe;
  color: #0284c7;
}
.discount-pill {
  background: #fee2e2;
  color: #dc2626;
}
.info-pill {
  background: #f1f5f9;
  color: #475569;
}

.badge-cat {
  background: #f1f5f9;
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  font-size: 0.85rem;
  margin-right: 0.4rem;
}

.text-danger {
  color: #dc2626;
}

.admin-inventory-section {
  background: #f0fdf4;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid #bbf7d0;
  margin-top: 1.5rem;
}

.inventory-title {
  font-size: 0.95rem;
  color: #166534;
  margin-bottom: 0.75rem;
}

.admin-variant-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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

.variant-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.text-small {
  font-size: 0.75rem;
}

.attr-badge {
  background: #dcfce7;
  color: #166534;
  padding: 0.2rem 0.5rem;
  font-size: 0.8rem;
  border-radius: 4px;
}

.variant-inputs {
  display: flex;
  gap: 0.75rem;
}

.variant-inputs label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
}

.variant-inputs input {
  width: 90px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  text-align: center;
}

/* ساختار بخش دوم (سئو و ابعاد) */
.admin-secondary-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.admin-settings-panel {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.specs-heading {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: #334155;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 0.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-grid.single-col {
  grid-template-columns: 1fr;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  font-family: inherit;
  font-size: 0.9rem;
  outline: none;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #5b3df5;
}

.admin-specs-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.admin-specs-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
}

.admin-specs-list input {
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0.3rem 0.6rem;
  text-align: right;
  font-weight: 600;
  width: 150px;
}

.admin-tags-flow {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.tag-pill {
  background: #f1f5f9;
  color: #475569;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
}

.timestamps-footer {
  display: flex;
  gap: 1.5rem;
  border-top: 1px dashed #cbd5e1;
  padding-top: 1rem;
  font-size: 0.8rem;
  color: #94a3b8;
  flex-wrap: wrap;
}

.admin-loading {
  text-align: center;
  padding: 4rem;
  font-weight: 700;
}
</style>
