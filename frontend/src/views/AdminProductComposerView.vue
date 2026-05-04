<template>
  <div class="page-shell admin-composer">
    <section class="page-panel page-hero composer-hero">
      <div class="composer-hero__content">
        <span class="pill">سرویس ادمین - ساخت محصول مرحله‌ای</span>
        <h1 class="page-title">محصول را به صورت draft بساز و وابستگی‌ها را قدم‌به‌قدم کامل کن</h1>
        <p class="page-description">
          این صفحه بر اساس روت‌های فعلی بک‌اند ساخته شده است. هر بخش دقیقاً نشان می‌دهد الان چه
          چیزی از سمت API قابل انجام است و برای چه قدم‌هایی هنوز روت تکمیلی لازم داریم.
        </p>
      </div>

      <div class="composer-hero__meta">
        <div class="hero-metric">
          <strong>{{ supportedRoutes.length }}</strong>
          <span>گام قابل استفاده</span>
        </div>
        <div class="hero-metric hero-metric--warning">
          <strong>{{ missingRoutes.length }}</strong>
          <span>گپ بک‌اند</span>
        </div>
      </div>
    </section>

    <section v-if="feedback.message || feedback.error" class="page-panel feedback-strip">
      <p v-if="feedback.message" class="feedback-strip__message">{{ feedback.message }}</p>
      <p v-if="feedback.error" class="feedback-strip__error">{{ feedback.error }}</p>
    </section>

    <section class="status-grid">
      <BaseCard
        v-for="item in routeCoverage"
        :key="item.title"
        class="status-card"
        :class="item.available ? 'status-card--ready' : 'status-card--missing'"
      >
        <div class="status-card__head">
          <strong>{{ item.title }}</strong>
          <span class="status-badge">{{ item.available ? 'پوشش داده شده' : 'نیازمند روت' }}</span>
        </div>
        <p>{{ item.description }}</p>
        <code>{{ item.route }}</code>
      </BaseCard>
    </section>

    <section class="composer-grid">
      <BaseCard class="composer-section">
        <div class="section-headline">
          <div>
            <h2>۱) ساخت draft اولیه</h2>
            <p>فقط فیلدهایی که همین حالا در `POST /v1/products/admin/createdraft` پشتیبانی می‌شوند.</p>
          </div>
          <BaseButton
            type="button"
            variant="secondary"
            size="sm"
            :disabled="loading.draft || !draftProduct"
            @click="resetDraftForm"
          >
            فرم جدید
          </BaseButton>
        </div>

        <form class="form-grid" @submit.prevent="submitDraft">
          <label class="field field--full">
            <span>نام محصول</span>
            <input v-model.trim="draftForm.name" class="field__control" required />
          </label>

          <label class="field field--full">
            <span>توضیحات</span>
            <textarea v-model.trim="draftForm.description" class="field__control field__control--textarea" />
          </label>

          <label class="field">
            <span>قیمت</span>
            <input v-model="draftForm.price" class="field__control" type="number" min="1" required />
          </label>

          <label class="field">
            <span>قیمت تخفیف</span>
            <input v-model="draftForm.discount_price" class="field__control" type="number" min="0" />
          </label>

          <label class="field">
            <span>قیمت تمام‌شده</span>
            <input v-model="draftForm.cost_price" class="field__control" type="number" min="0" />
          </label>

          <label class="field">
            <span>نرخ مالیات</span>
            <input v-model="draftForm.tax_rate" class="field__control" type="number" min="0" />
          </label>

          <label class="field">
            <span>وزن</span>
            <input v-model="draftForm.weight" class="field__control" type="number" min="0" step="0.001" />
          </label>

          <label class="field">
            <span>GTIN</span>
            <input v-model.trim="draftForm.gtin" class="field__control" maxlength="20" />
          </label>

          <label class="field field--full">
            <span>Meta title</span>
            <input v-model.trim="draftForm.meta_title" class="field__control" maxlength="255" />
          </label>

          <label class="field field--full">
            <span>Meta description</span>
            <textarea
              v-model.trim="draftForm.meta_description"
              class="field__control field__control--textarea"
              maxlength="500"
            />
          </label>

          <label class="toggle">
            <input v-model="draftForm.is_digital" type="checkbox" />
            <span>محصول دیجیتال است</span>
          </label>

          <div class="actions-row field--full">
            <BaseButton type="submit" size="lg" :disabled="loading.draft || !canCreateDraft">
              {{ loading.draft ? 'در حال ساخت draft...' : draftProduct ? 'ساخت draft جدید' : 'ایجاد draft' }}
            </BaseButton>
          </div>
        </form>
      </BaseCard>

      <BaseCard class="composer-section">
        <div class="section-headline">
          <div>
            <h2>اسنپ‌شات draft جاری</h2>
            <p>بعد از ساخت draft، بقیه گام‌ها با این شناسه محصول ادامه پیدا می‌کنند.</p>
          </div>
          <BaseButton
            v-if="draftProduct"
            type="button"
            variant="ghost"
            size="sm"
            :disabled="loading.resume"
            @click="refreshDraftContext"
          >
            بازخوانی از بک‌اند
          </BaseButton>
        </div>

        <div v-if="draftProduct" class="snapshot-grid">
          <div class="snapshot-item">
            <span>شناسه</span>
            <strong>#{{ draftProduct.id }}</strong>
          </div>
          <div class="snapshot-item">
            <span>SKU</span>
            <strong>{{ draftProduct.sku }}</strong>
          </div>
          <div class="snapshot-item">
            <span>Slug</span>
            <strong>{{ draftProduct.slug }}</strong>
          </div>
          <div class="snapshot-item">
            <span>وضعیت</span>
            <strong>{{ draftProduct.status }}</strong>
          </div>
          <div class="snapshot-item">
            <span>قیمت نهایی</span>
            <strong>{{ formatCurrency(draftProduct.final_price) }}</strong>
          </div>
          <div class="snapshot-item">
            <span>درصد تخفیف</span>
            <strong>{{ draftProduct.discount_percent }}%</strong>
          </div>
        </div>

        <div v-else class="empty-state compact-empty">
          ابتدا draft محصول را بساز تا مراحل بعدی فعال شوند.
        </div>

        <div class="missing-route-callout">
          <strong>گپ مهم بک‌اند:</strong>
          <span>
            برای ویرایش دوباره فیلدهای پایه، برند، وضعیت انتشار و featured هنوز route به‌روزرسانی محصول
            نداریم.
          </span>
        </div>
      </BaseCard>
    </section>

    <section class="composer-grid composer-grid--single">
      <BaseCard class="composer-section">
        <div class="section-headline">
          <div>
            <h2>۲) برند</h2>
            <p>فعلاً فقط می‌توان لیست برندها را دید یا برند جدید ساخت؛ اتصال برند به محصول route ندارد.</p>
          </div>
          <span class="section-tag section-tag--warning">نیازمند route اتصال برند</span>
        </div>

        <div class="inline-form">
          <label class="field">
            <span>نام برند</span>
            <input v-model.trim="brandForm.name" class="field__control" />
          </label>
          <label class="field">
            <span>Slug برند</span>
            <input v-model.trim="brandForm.slug" class="field__control" />
          </label>
          <div class="inline-form__actions">
            <BaseButton type="button" :disabled="loading.brands" @click="createBrand">ساخت برند</BaseButton>
          </div>
        </div>

        <div class="collection-grid">
          <div v-for="brand in brands" :key="brand.id" class="collection-item">
            <strong>{{ brand.name }}</strong>
            <span>{{ brand.slug || 'بدون slug' }}</span>
          </div>
        </div>
      </BaseCard>

      <BaseCard class="composer-section" :class="{ 'composer-section--disabled': !draftProduct }">
        <div class="section-headline">
          <div>
            <h2>۳) تگ‌ها</h2>
            <p>ساخت تگ جدید و sync کردن آن با محصول از API فعلی پشتیبانی می‌شود.</p>
          </div>
          <span class="section-tag" :class="draftProduct ? 'section-tag--ready' : 'section-tag--muted'">
            {{ draftProduct ? 'فعال' : 'بعد از draft' }}
          </span>
        </div>

        <div class="inline-form">
          <label class="field">
            <span>نام تگ</span>
            <input v-model.trim="tagForm.name" class="field__control" />
          </label>
          <label class="field">
            <span>Slug تگ</span>
            <input v-model.trim="tagForm.slug" class="field__control" />
          </label>
          <div class="inline-form__actions">
            <BaseButton type="button" :disabled="loading.tags" @click="createTag">ساخت تگ</BaseButton>
          </div>
        </div>

        <div class="picker-grid">
          <label v-for="tag in tags" :key="tag.id" class="picker-item">
            <input v-model="selectedTagIds" :value="tag.id" type="checkbox" :disabled="!draftProduct" />
            <span>{{ tag.name }}</span>
          </label>
        </div>

        <div class="actions-row">
          <BaseButton type="button" :disabled="!draftProduct || loading.tags" @click="syncTags">
            ذخیره تگ‌های محصول
          </BaseButton>
          <span class="helper-text">پس از refresh صفحه، بازخوانی تگ‌های متصل هنوز route اختصاصی ندارد.</span>
        </div>
      </BaseCard>

      <BaseCard class="composer-section" :class="{ 'composer-section--disabled': !draftProduct }">
        <div class="section-headline">
          <div>
            <h2>۴) دسته‌بندی‌ها</h2>
            <p>ساخت دسته و sync آن با محصول در دسترس است.</p>
          </div>
          <span class="section-tag" :class="draftProduct ? 'section-tag--ready' : 'section-tag--muted'">
            {{ draftProduct ? 'فعال' : 'بعد از draft' }}
          </span>
        </div>

        <div class="inline-form">
          <label class="field">
            <span>نام دسته</span>
            <input v-model.trim="categoryForm.name" class="field__control" />
          </label>
          <label class="field">
            <span>Slug دسته</span>
            <input v-model.trim="categoryForm.slug" class="field__control" />
          </label>
          <label class="field">
            <span>Parent ID</span>
            <input v-model="categoryForm.parent_id" class="field__control" type="number" min="1" />
          </label>
          <div class="inline-form__actions">
            <BaseButton type="button" :disabled="loading.categories" @click="createCategory">ساخت دسته</BaseButton>
          </div>
        </div>

        <div class="picker-grid">
          <label v-for="category in categories" :key="category.id" class="picker-item">
            <input
              v-model="selectedCategoryIds"
              :value="category.id"
              type="checkbox"
              :disabled="!draftProduct"
            />
            <span>{{ category.name }}</span>
          </label>
        </div>

        <div class="actions-row">
          <BaseButton type="button" :disabled="!draftProduct || loading.categories" @click="syncCategories">
            ذخیره دسته‌های محصول
          </BaseButton>
        </div>
      </BaseCard>

      <BaseCard class="composer-section" :class="{ 'composer-section--disabled': !draftProduct }">
        <div class="section-headline">
          <div>
            <h2>۵) اتریبیوت‌های محصول</h2>
            <p>اول definition اتریبیوت را بساز، بعد مقدار آن را روی خود محصول ثبت کن.</p>
          </div>
          <span class="section-tag" :class="draftProduct ? 'section-tag--ready' : 'section-tag--muted'">
            {{ draftProduct ? `${productAttributes.length} مقدار ثبت شده` : 'بعد از draft' }}
          </span>
        </div>

        <div class="inline-form">
          <label class="field">
            <span>نام اتریبیوت</span>
            <input v-model.trim="attributeForm.name" class="field__control" />
          </label>
          <label class="field">
            <span>Slug اتریبیوت</span>
            <input v-model.trim="attributeForm.slug" class="field__control" />
          </label>
          <div class="inline-form__actions">
            <BaseButton type="button" :disabled="loading.attributes" @click="createAttribute">ساخت اتریبیوت</BaseButton>
          </div>
        </div>

        <div class="inline-form">
          <label class="field">
            <span>اتریبیوت محصول</span>
            <select v-model="productAttributeForm.attribute_id" class="field__control" :disabled="!draftProduct">
              <option value="">انتخاب اتریبیوت</option>
              <option v-for="attribute in attributes" :key="attribute.id" :value="String(attribute.id)">
                {{ attribute.name }}
              </option>
            </select>
          </label>
          <label class="field">
            <span>مقدار</span>
            <input v-model.trim="productAttributeForm.value" class="field__control" :disabled="!draftProduct" />
          </label>
          <div class="inline-form__actions">
            <BaseButton type="button" :disabled="!draftProduct || loading.productAttributes" @click="createProductAttribute">
              افزودن مقدار
            </BaseButton>
          </div>
        </div>

        <div class="collection-grid">
          <div v-for="item in productAttributes" :key="item.id" class="collection-item">
            <strong>{{ resolveAttributeName(item.attribute_id) }}</strong>
            <span>{{ item.value }}</span>
          </div>
        </div>
      </BaseCard>

      <BaseCard class="composer-section" :class="{ 'composer-section--disabled': !draftProduct }">
        <div class="section-headline">
          <div>
            <h2>۶) واریانت‌ها</h2>
            <p>بعد از draft می‌توان واریانت ساخت و سپس inventory و variant-attribute را به آن اضافه کرد.</p>
          </div>
          <span class="section-tag" :class="draftProduct ? 'section-tag--ready' : 'section-tag--muted'">
            {{ draftProduct ? `${variants.length} واریانت` : 'بعد از draft' }}
          </span>
        </div>

        <div class="inline-form">
          <label class="field">
            <span>قیمت واریانت</span>
            <input v-model="variantForm.price" class="field__control" type="number" min="0" :disabled="!draftProduct" />
          </label>
          <label class="toggle">
            <input v-model="variantForm.is_active" type="checkbox" :disabled="!draftProduct" />
            <span>واریانت فعال باشد</span>
          </label>
          <div class="inline-form__actions">
            <BaseButton type="button" :disabled="!draftProduct || loading.variants" @click="createVariant">
              ساخت واریانت
            </BaseButton>
          </div>
        </div>

        <div class="variant-list">
          <button
            v-for="variant in variants"
            :key="variant.id"
            type="button"
            class="variant-item"
            :class="{ 'variant-item--active': activeVariantId === variant.id }"
            @click="activeVariantId = variant.id"
          >
            <strong>SKU: {{ variant.sku }}</strong>
            <span>{{ formatCurrency(variant.price || draftProduct?.final_price || 0) }}</span>
          </button>
        </div>

        <div v-if="activeVariant" class="nested-panels">
          <div class="nested-panel">
            <div class="section-headline section-headline--compact">
              <div>
                <h3>۷) موجودی واریانت</h3>
                <p>برای هر واریانت یک رکورد inventory ساخته یا به‌روزرسانی می‌شود.</p>
              </div>
            </div>

            <div class="inline-form inline-form--dense">
              <label class="field">
                <span>تعداد</span>
                <input v-model="inventoryForm.quantity" class="field__control" type="number" min="0" />
              </label>
              <label class="field">
                <span>رزرو شده</span>
                <input v-model="inventoryForm.reserved_quantity" class="field__control" type="number" min="0" />
              </label>
              <label class="field">
                <span>آستانه هشدار</span>
                <input v-model="inventoryForm.low_stock_alert" class="field__control" type="number" min="0" />
              </label>
              <label class="toggle">
                <input v-model="inventoryForm.allow_backorder" type="checkbox" />
                <span>اجازه backorder</span>
              </label>
              <div class="inline-form__actions">
                <BaseButton type="button" :disabled="loading.inventory" @click="saveInventory">
                  {{ inventoryRecord ? 'به‌روزرسانی موجودی' : 'ساخت موجودی' }}
                </BaseButton>
              </div>
            </div>

            <div v-if="inventoryRecord" class="inventory-card">
              <strong>موجودی قابل فروش: {{ inventoryRecord.available_quantity }}</strong>
              <span>{{ inventoryRecord.is_in_stock ? 'در انبار' : 'ناموجود' }}</span>
            </div>
          </div>

          <div class="nested-panel">
            <div class="section-headline section-headline--compact">
              <div>
                <h3>۸) اتریبیوت‌های واریانت</h3>
                <p>مثلاً رنگ، سایز یا هر ویژگی وابسته به واریانت.</p>
              </div>
            </div>

            <div class="inline-form inline-form--dense">
              <label class="field">
                <span>اتریبیوت واریانت</span>
                <select v-model="variantAttributeForm.attribute_id" class="field__control">
                  <option value="">انتخاب اتریبیوت</option>
                  <option v-for="attribute in attributes" :key="attribute.id" :value="String(attribute.id)">
                    {{ attribute.name }}
                  </option>
                </select>
              </label>
              <label class="field">
                <span>مقدار</span>
                <input v-model.trim="variantAttributeForm.value" class="field__control" />
              </label>
              <div class="inline-form__actions">
                <BaseButton type="button" :disabled="loading.variantAttributes" @click="createVariantAttribute">
                  افزودن اتریبیوت
                </BaseButton>
              </div>
            </div>

            <div class="collection-grid">
              <div v-for="item in variantAttributes" :key="item.id" class="collection-item">
                <strong>{{ resolveAttributeName(item.attribute_id) }}</strong>
                <span>{{ item.value }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state compact-empty">
          یک واریانت بساز یا انتخاب کن تا inventory و variant-attribute فعال شوند.
        </div>
      </BaseCard>

      <BaseCard class="composer-section" :class="{ 'composer-section--disabled': !draftProduct }">
        <div class="section-headline">
          <div>
            <h2>۹) تصاویر محصول</h2>
            <p>upload و list از سمت بک‌اند آماده است؛ update/delete تصویر فعلی path بهتری لازم دارد.</p>
          </div>
          <span class="section-tag section-tag--warning">update/delete نیازمند بازطراحی route</span>
        </div>

        <div class="inline-form inline-form--dense">
          <label class="field">
            <span>فایل تصویر</span>
            <input class="field__control" type="file" accept="image/*" :disabled="!draftProduct" @change="onImageChange" />
          </label>
          <label class="field">
            <span>Alt text</span>
            <input v-model.trim="imageForm.alt_text" class="field__control" :disabled="!draftProduct" />
          </label>
          <label class="field">
            <span>Sort order</span>
            <input v-model="imageForm.sort_order" class="field__control" type="number" min="0" :disabled="!draftProduct" />
          </label>
          <label class="toggle">
            <input v-model="imageForm.is_primary" type="checkbox" :disabled="!draftProduct" />
            <span>تصویر اصلی</span>
          </label>
          <div class="inline-form__actions">
            <BaseButton type="button" :disabled="!draftProduct || loading.images" @click="uploadImage">
              آپلود تصویر
            </BaseButton>
          </div>
        </div>

        <div class="image-grid">
          <article v-for="image in images" :key="image.id" class="image-item">
            <img :src="image.url" :alt="image.alt_text || draftProduct?.name || 'product image'" />
            <div class="image-item__meta">
              <strong>{{ image.is_primary ? 'تصویر اصلی' : `ترتیب ${image.sort_order}` }}</strong>
              <span>{{ image.alt_text || 'بدون alt text' }}</span>
            </div>
          </article>
        </div>
      </BaseCard>

      <BaseCard class="composer-section">
        <div class="section-headline">
          <div>
            <h2>روت‌های پیشنهادی برای تکمیل workflow</h2>
            <p>این‌ها مهم‌ترین روت‌هایی هستند که فرانت برای کامل شدن مسیر ساخت محصول هنوز لازم دارد.</p>
          </div>
        </div>

        <div class="missing-route-list">
          <article v-for="item in missingRoutes" :key="item.route" class="missing-route-item">
            <strong>{{ item.title }}</strong>
            <code>{{ item.route }}</code>
            <p>{{ item.description }}</p>
          </article>
        </div>
      </BaseCard>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import { adminProductWorkflowApi } from '@/services/adminProductWorkflow'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const route = useRoute()
const user = useUserStore()

const routeCoverage = [
  {
    title: 'ساخت draft',
    route: 'POST /v1/products/admin/createdraft',
    description: 'نسخه اولیه محصول را با فیلدهای پایه می‌سازد.',
    available: true,
  },
  {
    title: 'تگ‌های محصول',
    route: 'PUT /v1/tags/{product_id}/tags/sync',
    description: 'sync تگ‌ها برای محصول موجود است.',
    available: true,
  },
  {
    title: 'دسته‌های محصول',
    route: 'PUT /v1/categories/{product_id}/categories/sync',
    description: 'sync دسته‌ها برای محصول موجود است.',
    available: true,
  },
  {
    title: 'اتریبیوت محصول',
    route: 'POST /v1/attributes/product',
    description: 'می‌توان attribute definition را به محصول متصل کرد.',
    available: true,
  },
  {
    title: 'برند محصول',
    route: 'PATCH /v1/products/admin/products/{product_id}',
    description: 'فعلاً route برای set کردن brand_id روی محصول وجود ندارد.',
    available: false,
  },
  {
    title: 'ویرایش draft',
    route: 'PATCH /v1/products/admin/products/{product_id}',
    description: 'برای تغییر price, meta, status, featured و publish باید route اضافه شود.',
    available: false,
  },
  {
    title: 'بازخوانی full detail',
    route: 'GET /v1/products/admin/products/{product_id}/full',
    description: 'محصول فعلی relationها را در response برنمی‌گرداند و resume را ناقص می‌کند.',
    available: false,
  },
  {
    title: 'انتشار و لیست draftها',
    route: 'POST /v1/products/admin/products/{product_id}/publish + GET /v1/products/admin',
    description: 'برای ادامه کار ادمین روی draftهای قبلی لازم است.',
    available: false,
  },
]

const supportedRoutes = computed(() => routeCoverage.filter((item) => item.available))
const missingRoutes = computed(() => routeCoverage.filter((item) => !item.available))

const feedback = reactive({
  message: '',
  error: '',
})

const loading = reactive({
  draft: false,
  resume: false,
  brands: false,
  tags: false,
  categories: false,
  attributes: false,
  productAttributes: false,
  variants: false,
  inventory: false,
  variantAttributes: false,
  images: false,
})

const draftProduct = ref(null)

const brands = ref([])
const tags = ref([])
const categories = ref([])
const attributes = ref([])
const productAttributes = ref([])
const variants = ref([])
const activeVariantId = ref(null)
const variantAttributes = ref([])
const images = ref([])
const inventoryRecord = ref(null)

const selectedTagIds = ref([])
const selectedCategoryIds = ref([])

const draftForm = reactive(getDefaultDraftForm())
const brandForm = reactive({
  name: '',
  slug: '',
})
const tagForm = reactive({
  name: '',
  slug: '',
})
const categoryForm = reactive({
  name: '',
  slug: '',
  parent_id: '',
})
const attributeForm = reactive({
  name: '',
  slug: '',
})
const productAttributeForm = reactive({
  attribute_id: '',
  value: '',
})
const variantForm = reactive({
  price: '',
  is_active: true,
})
const inventoryForm = reactive(getDefaultInventoryForm())
const variantAttributeForm = reactive({
  attribute_id: '',
  value: '',
})
const imageForm = reactive({
  file: null,
  alt_text: '',
  is_primary: false,
  sort_order: '0',
})

const activeVariant = computed(() =>
  variants.value.find((variant) => variant.id === activeVariantId.value) || null,
)
const canCreateDraft = computed(() => draftForm.name && Number.parseInt(draftForm.price, 10) > 0)
const isAdmin = computed(() => user.profile?.role === 'admin')

function getDefaultDraftForm() {
  return {
    name: '',
    description: '',
    price: '',
    discount_price: '',
    cost_price: '',
    tax_rate: '0',
    is_digital: false,
    weight: '',
    meta_title: '',
    meta_description: '',
    gtin: '',
  }
}

function getDefaultInventoryForm() {
  return {
    quantity: '0',
    reserved_quantity: '0',
    low_stock_alert: '5',
    allow_backorder: false,
  }
}

function setFeedback(message = '', error = '') {
  feedback.message = message
  feedback.error = error
}

function clearFeedback() {
  setFeedback('', '')
}

function toOptionalInteger(value) {
  if (value === '' || value === null || value === undefined) {
    return null
  }

  const parsed = Number.parseInt(value, 10)
  return Number.isNaN(parsed) ? null : parsed
}

function toRequiredInteger(value, fallback = 0) {
  const parsed = Number.parseInt(value, 10)
  return Number.isNaN(parsed) ? fallback : parsed
}

function toOptionalFloat(value) {
  if (value === '' || value === null || value === undefined) {
    return null
  }

  const parsed = Number.parseFloat(value)
  return Number.isNaN(parsed) ? null : parsed
}

function formatCurrency(value) {
  return new Intl.NumberFormat('fa-IR').format(Number(value || 0))
}

function resolveAttributeName(attributeId) {
  return attributes.value.find((attribute) => attribute.id === attributeId)?.name || `#${attributeId}`
}

function resetDraftForm() {
  Object.assign(draftForm, getDefaultDraftForm())
  clearFeedback()
}

function resetInventoryState() {
  inventoryRecord.value = null
  Object.assign(inventoryForm, getDefaultInventoryForm())
}

function syncInventoryForm(record) {
  if (!record) {
    resetInventoryState()
    return
  }

  inventoryRecord.value = record
  inventoryForm.quantity = String(record.quantity)
  inventoryForm.reserved_quantity = String(record.reserved_quantity)
  inventoryForm.low_stock_alert = String(record.low_stock_alert)
  inventoryForm.allow_backorder = Boolean(record.allow_backorder)
}

async function loadReferenceCatalogs() {
  loading.brands = true
  loading.tags = true
  loading.categories = true
  loading.attributes = true

  const results = await Promise.allSettled([
    adminProductWorkflowApi.listBrands(),
    adminProductWorkflowApi.listTags(),
    adminProductWorkflowApi.listCategories(),
    adminProductWorkflowApi.listAttributes(),
  ])

  const [brandsResult, tagsResult, categoriesResult, attributesResult] = results

  if (brandsResult.status === 'fulfilled') {
    brands.value = brandsResult.value.items || []
  }
  if (tagsResult.status === 'fulfilled') {
    tags.value = tagsResult.value.items || []
  }
  if (categoriesResult.status === 'fulfilled') {
    categories.value = categoriesResult.value.items || []
  }
  if (attributesResult.status === 'fulfilled') {
    attributes.value = attributesResult.value.items || []
  }

  const firstRejected = results.find((result) => result.status === 'rejected')
  if (firstRejected) {
    setFeedback('', firstRejected.reason?.message || 'بارگذاری برخی از داده‌های پایه با خطا روبه‌رو شد.')
  }

  loading.brands = false
  loading.tags = false
  loading.categories = false
  loading.attributes = false
}

async function loadProductAttributes() {
  if (!draftProduct.value) {
    productAttributes.value = []
    return
  }

  loading.productAttributes = true
  try {
    const response = await adminProductWorkflowApi.listProductAttributes(draftProduct.value.id)
    productAttributes.value = response.items || []
  } finally {
    loading.productAttributes = false
  }
}

async function loadVariants() {
  if (!draftProduct.value) {
    variants.value = []
    activeVariantId.value = null
    return
  }

  loading.variants = true
  try {
    const response = await adminProductWorkflowApi.listVariants(draftProduct.value.id)
    variants.value = response.items || []

    if (!variants.value.some((variant) => variant.id === activeVariantId.value)) {
      activeVariantId.value = variants.value[0]?.id || null
    }
  } finally {
    loading.variants = false
  }
}

async function loadVariantAttributes() {
  if (!activeVariantId.value) {
    variantAttributes.value = []
    return
  }

  loading.variantAttributes = true
  try {
    const response = await adminProductWorkflowApi.listVariantAttributes(activeVariantId.value)
    variantAttributes.value = response.items || []
  } finally {
    loading.variantAttributes = false
  }
}

async function loadInventory() {
  if (!activeVariantId.value) {
    resetInventoryState()
    return
  }

  loading.inventory = true
  try {
    const response = await adminProductWorkflowApi.listInventory(activeVariantId.value)
    syncInventoryForm((response.items || [])[0] || null)
  } finally {
    loading.inventory = false
  }
}

async function loadImages() {
  if (!draftProduct.value) {
    images.value = []
    return
  }

  loading.images = true
  try {
    images.value = await adminProductWorkflowApi.listImages(draftProduct.value.id)
  } finally {
    loading.images = false
  }
}

async function refreshDraftContext() {
  if (!draftProduct.value) {
    return
  }

  loading.resume = true
  clearFeedback()

  try {
    draftProduct.value = await adminProductWorkflowApi.getDraft(draftProduct.value.id)
    selectedTagIds.value = []
    selectedCategoryIds.value = []
    await Promise.all([loadProductAttributes(), loadVariants(), loadImages()])
    setFeedback('اسنپ‌شات draft از بک‌اند بازخوانی شد.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.resume = false
  }
}

async function resumeDraft(productId) {
  loading.resume = true
  clearFeedback()

  try {
    draftProduct.value = await adminProductWorkflowApi.getDraft(productId)
    selectedTagIds.value = []
    selectedCategoryIds.value = []
    await Promise.all([loadProductAttributes(), loadVariants(), loadImages()])
    setFeedback(`draft محصول #${productId} بازیابی شد.`, '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.resume = false
  }
}

async function submitDraft() {
  loading.draft = true
  clearFeedback()

  try {
    draftProduct.value = await adminProductWorkflowApi.createDraft({
      name: draftForm.name,
      description: draftForm.description,
      price: toRequiredInteger(draftForm.price, 0),
      discount_price: toOptionalInteger(draftForm.discount_price),
      cost_price: toOptionalInteger(draftForm.cost_price),
      tax_rate: toRequiredInteger(draftForm.tax_rate, 0),
      is_digital: Boolean(draftForm.is_digital),
      weight: toOptionalFloat(draftForm.weight),
      meta_title: draftForm.meta_title || null,
      meta_description: draftForm.meta_description || null,
      gtin: draftForm.gtin || null,
    })

    selectedTagIds.value = []
    selectedCategoryIds.value = []
    productAttributes.value = []
    variants.value = []
    variantAttributes.value = []
    images.value = []
    activeVariantId.value = null
    resetInventoryState()

    await router.replace({
      name: 'admin-product-composer',
      query: {
        productId: String(draftProduct.value.id),
      },
    })

    setFeedback(`draft محصول با شناسه #${draftProduct.value.id} ساخته شد.`, '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.draft = false
  }
}

async function createBrand() {
  if (!brandForm.name) {
    setFeedback('', 'نام برند را وارد کنید.')
    return
  }

  loading.brands = true
  clearFeedback()

  try {
    await adminProductWorkflowApi.createBrand({
      name: brandForm.name,
      slug: brandForm.slug || null,
    })
    Object.assign(brandForm, { name: '', slug: '' })
    const response = await adminProductWorkflowApi.listBrands()
    brands.value = response.items || []
    setFeedback('برند جدید ساخته شد. برای اتصال آن به محصول هنوز route لازم داریم.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.brands = false
  }
}

async function createTag() {
  if (!tagForm.name) {
    setFeedback('', 'نام تگ را وارد کنید.')
    return
  }

  loading.tags = true
  clearFeedback()

  try {
    await adminProductWorkflowApi.createTag({
      name: tagForm.name,
      slug: tagForm.slug || null,
    })
    Object.assign(tagForm, { name: '', slug: '' })
    const response = await adminProductWorkflowApi.listTags()
    tags.value = response.items || []
    setFeedback('تگ جدید ساخته شد.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.tags = false
  }
}

async function syncTags() {
  if (!draftProduct.value) {
    return
  }

  loading.tags = true
  clearFeedback()

  try {
    const response = await adminProductWorkflowApi.syncProductTags(draftProduct.value.id, selectedTagIds.value)
    selectedTagIds.value = response.current || []
    setFeedback('تگ‌های محصول با موفقیت sync شدند.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.tags = false
  }
}

async function createCategory() {
  if (!categoryForm.name) {
    setFeedback('', 'نام دسته را وارد کنید.')
    return
  }

  loading.categories = true
  clearFeedback()

  try {
    await adminProductWorkflowApi.createCategory({
      name: categoryForm.name,
      slug: categoryForm.slug || null,
      description: null,
      is_active: true,
      parent_id: toOptionalInteger(categoryForm.parent_id),
    })
    Object.assign(categoryForm, { name: '', slug: '', parent_id: '' })
    const response = await adminProductWorkflowApi.listCategories()
    categories.value = response.items || []
    setFeedback('دسته جدید ساخته شد.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.categories = false
  }
}

async function syncCategories() {
  if (!draftProduct.value) {
    return
  }

  loading.categories = true
  clearFeedback()

  try {
    const response = await adminProductWorkflowApi.syncProductCategories(
      draftProduct.value.id,
      selectedCategoryIds.value,
    )
    selectedCategoryIds.value = response.current || []
    setFeedback('دسته‌های محصول با موفقیت sync شدند.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.categories = false
  }
}

async function createAttribute() {
  if (!attributeForm.name) {
    setFeedback('', 'نام اتریبیوت را وارد کنید.')
    return
  }

  loading.attributes = true
  clearFeedback()

  try {
    await adminProductWorkflowApi.createAttribute({
      name: attributeForm.name,
      slug: attributeForm.slug || null,
    })
    Object.assign(attributeForm, { name: '', slug: '' })
    const response = await adminProductWorkflowApi.listAttributes()
    attributes.value = response.items || []
    setFeedback('اتریبیوت جدید ساخته شد.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.attributes = false
  }
}

async function createProductAttribute() {
  if (!draftProduct.value) {
    return
  }

  if (!productAttributeForm.attribute_id || !productAttributeForm.value) {
    setFeedback('', 'اتریبیوت و مقدار آن را کامل کنید.')
    return
  }

  loading.productAttributes = true
  clearFeedback()

  try {
    await adminProductWorkflowApi.createProductAttribute({
      product_id: draftProduct.value.id,
      attribute_id: toRequiredInteger(productAttributeForm.attribute_id),
      value: productAttributeForm.value,
    })
    Object.assign(productAttributeForm, { attribute_id: '', value: '' })
    await loadProductAttributes()
    setFeedback('مقدار اتریبیوت روی محصول ثبت شد.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.productAttributes = false
  }
}

async function createVariant() {
  if (!draftProduct.value) {
    return
  }

  loading.variants = true
  clearFeedback()

  try {
    const variant = await adminProductWorkflowApi.createVariant({
      product_id: draftProduct.value.id,
      price: toOptionalInteger(variantForm.price),
      is_active: Boolean(variantForm.is_active),
    })
    Object.assign(variantForm, { price: '', is_active: true })
    await loadVariants()
    activeVariantId.value = variant.id
    setFeedback(`واریانت #${variant.id} ساخته شد.`, '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.variants = false
  }
}

async function saveInventory() {
  if (!activeVariantId.value) {
    return
  }

  loading.inventory = true
  clearFeedback()

  try {
    const basePayload = {
      quantity: toRequiredInteger(inventoryForm.quantity, 0),
      reserved_quantity: toRequiredInteger(inventoryForm.reserved_quantity, 0),
      low_stock_alert: toRequiredInteger(inventoryForm.low_stock_alert, 0),
      allow_backorder: Boolean(inventoryForm.allow_backorder),
    }

    if (inventoryRecord.value) {
      syncInventoryForm(
        await adminProductWorkflowApi.updateInventory(inventoryRecord.value.id, basePayload),
      )
      setFeedback('موجودی واریانت به‌روزرسانی شد.', '')
    } else {
      syncInventoryForm(
        await adminProductWorkflowApi.createInventory({
          ...basePayload,
          variant_id: activeVariantId.value,
        }),
      )
      setFeedback('موجودی واریانت ساخته شد.', '')
    }
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.inventory = false
  }
}

async function createVariantAttribute() {
  if (!activeVariantId.value) {
    return
  }

  if (!variantAttributeForm.attribute_id || !variantAttributeForm.value) {
    setFeedback('', 'اتریبیوت و مقدار واریانت را کامل کنید.')
    return
  }

  loading.variantAttributes = true
  clearFeedback()

  try {
    await adminProductWorkflowApi.createVariantAttribute({
      variant_id: activeVariantId.value,
      attribute_id: toRequiredInteger(variantAttributeForm.attribute_id),
      value: variantAttributeForm.value,
    })
    Object.assign(variantAttributeForm, { attribute_id: '', value: '' })
    await loadVariantAttributes()
    setFeedback('اتریبیوت واریانت ثبت شد.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.variantAttributes = false
  }
}

function onImageChange(event) {
  imageForm.file = event.target.files?.[0] || null
}

async function uploadImage() {
  if (!draftProduct.value || !imageForm.file) {
    setFeedback('', 'برای آپلود، فایل تصویر را انتخاب کنید.')
    return
  }

  loading.images = true
  clearFeedback()

  try {
    await adminProductWorkflowApi.uploadImage(draftProduct.value.id, imageForm)
    Object.assign(imageForm, {
      file: null,
      alt_text: '',
      is_primary: false,
      sort_order: '0',
    })
    await loadImages()
    setFeedback('تصویر محصول آپلود شد.', '')
  } catch (error) {
    setFeedback('', error.message)
  } finally {
    loading.images = false
  }
}

watch(activeVariantId, async () => {
  try {
    await Promise.all([loadInventory(), loadVariantAttributes()])
  } catch (error) {
    setFeedback('', error.message)
  }
})

onMounted(async () => {
  await loadReferenceCatalogs()

  const requestedProductId = toOptionalInteger(route.query.productId)
  if (requestedProductId) {
    await resumeDraft(requestedProductId)
  }

  if (user.isAuthenticated && !user.profile && !user.profileLoading) {
    try {
      await user.fetchProfile({ silent: true })
    } catch {
      // The page can still be explored even if profile fetch fails.
    }
  }

  if (user.isAuthenticated && user.profile && !isAdmin.value) {
    setFeedback('', 'حساب کاربری فعلی ادمین نیست؛ درخواست‌های مدیریتی ممکن است با 403 برگردند.')
  }
})
</script>

<style scoped>
.admin-composer {
  gap: 1.25rem;
}

.composer-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) minmax(280px, 0.8fr);
  gap: 1.5rem;
  align-items: center;
  overflow: hidden;
  background:
    radial-gradient(circle at left top, rgba(255, 176, 32, 0.18), transparent 28%),
    radial-gradient(circle at right bottom, rgba(15, 157, 129, 0.16), transparent 32%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(242, 246, 255, 0.88));
}

.composer-hero__meta {
  display: grid;
  gap: 1rem;
}

.hero-metric {
  padding: 1.2rem 1.35rem;
  border-radius: var(--radius-md);
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(255, 255, 255, 0.78);
}

.hero-metric strong {
  display: block;
  font-size: 2.2rem;
  line-height: 1;
  color: var(--success);
}

.hero-metric--warning strong {
  color: var(--warning);
}

.hero-metric span {
  display: block;
  margin-top: 0.35rem;
  color: var(--text-muted);
}

.feedback-strip {
  padding: 1rem 1.25rem;
}

.feedback-strip__message,
.feedback-strip__error {
  margin: 0;
  font-weight: 700;
}

.feedback-strip__message {
  color: var(--success);
}

.feedback-strip__error {
  color: var(--danger);
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.status-card {
  padding: 1.15rem;
  display: grid;
  gap: 0.75rem;
}

.status-card--ready {
  border-color: rgba(15, 157, 129, 0.2);
}

.status-card--missing {
  border-color: rgba(255, 176, 32, 0.22);
}

.status-card__head {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 0.75rem;
}

.status-card p,
.missing-route-item p {
  margin: 0;
  color: var(--text-muted);
}

.status-card code,
.missing-route-item code {
  display: block;
  padding: 0.8rem 0.9rem;
  border-radius: var(--radius-sm);
  background: rgba(15, 23, 42, 0.04);
  color: var(--text);
  font-size: 0.85rem;
  overflow-wrap: anywhere;
}

.status-badge,
.section-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.4rem 0.75rem;
  border-radius: 999px;
  font-size: 0.84rem;
  font-weight: 700;
}

.section-tag--ready,
.status-card--ready .status-badge {
  background: rgba(15, 157, 129, 0.12);
  color: var(--success);
}

.section-tag--warning,
.status-card--missing .status-badge {
  background: rgba(255, 176, 32, 0.16);
  color: #9a6400;
}

.section-tag--muted {
  background: rgba(100, 116, 139, 0.12);
  color: var(--text-muted);
}

.composer-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.composer-grid--single {
  grid-template-columns: 1fr;
}

.composer-section {
  padding: 1.4rem;
  display: grid;
  gap: 1.15rem;
}

.composer-section--disabled {
  opacity: 0.72;
}

.section-headline {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 1rem;
}

.section-headline--compact h3 {
  margin-bottom: 0.15rem;
}

.section-headline h2,
.section-headline h3 {
  margin: 0;
}

.section-headline p,
.missing-route-callout span {
  margin: 0.35rem 0 0;
  color: var(--text-muted);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.field,
.toggle {
  display: grid;
  gap: 0.45rem;
}

.field span,
.toggle span {
  font-weight: 700;
}

.field--full {
  grid-column: 1 / -1;
}

.field__control {
  width: 100%;
  min-height: 48px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.95);
  padding: 0.8rem 0.95rem;
  color: var(--text);
  outline: none;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.field__control:focus {
  border-color: rgba(15, 157, 129, 0.38);
  box-shadow: 0 0 0 4px rgba(15, 157, 129, 0.12);
}

.field__control--textarea {
  min-height: 120px;
  resize: vertical;
}

.toggle {
  align-content: center;
  justify-items: start;
}

.toggle input {
  width: 18px;
  height: 18px;
}

.actions-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.helper-text {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.snapshot-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
}

.snapshot-item,
.inventory-card,
.collection-item,
.variant-item,
.missing-route-item,
.nested-panel {
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.84);
}

.snapshot-item {
  padding: 1rem;
  display: grid;
  gap: 0.35rem;
}

.snapshot-item span,
.collection-item span,
.image-item__meta span {
  color: var(--text-muted);
}

.compact-empty {
  padding: 1.25rem;
}

.missing-route-callout {
  display: flex;
  align-items: start;
  gap: 0.6rem;
  padding: 1rem 1.1rem;
  border-radius: var(--radius-md);
  border: 1px dashed rgba(255, 176, 32, 0.32);
  background: rgba(255, 176, 32, 0.08);
}

.inline-form {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
  align-items: end;
}

.inline-form--dense {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.inline-form__actions {
  display: flex;
  align-items: center;
  min-height: 48px;
}

.picker-grid,
.collection-grid,
.image-grid {
  display: grid;
  gap: 0.85rem;
}

.picker-grid {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.picker-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.9rem 1rem;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.84);
}

.collection-grid {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.collection-item {
  padding: 0.95rem 1rem;
  display: grid;
  gap: 0.25rem;
}

.variant-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.85rem;
}

.variant-item {
  padding: 1rem;
  display: grid;
  gap: 0.35rem;
  text-align: right;
}

.variant-item--active {
  border-color: rgba(15, 157, 129, 0.28);
  box-shadow: 0 14px 34px rgba(15, 157, 129, 0.12);
}

.nested-panels {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.nested-panel {
  padding: 1rem;
  display: grid;
  gap: 0.9rem;
}

.inventory-card {
  padding: 0.95rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.image-grid {
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.image-item {
  overflow: hidden;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.92);
}

.image-item img {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
}

.image-item__meta {
  padding: 0.9rem 1rem 1rem;
  display: grid;
  gap: 0.25rem;
}

.missing-route-list {
  display: grid;
  gap: 0.9rem;
}

.missing-route-item {
  padding: 1rem;
  display: grid;
  gap: 0.7rem;
}

@media (max-width: 1100px) {
  .status-grid,
  .composer-grid,
  .nested-panels,
  .composer-hero {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 820px) {
  .form-grid,
  .inline-form,
  .inline-form--dense,
  .snapshot-grid {
    grid-template-columns: 1fr;
  }

  .section-headline,
  .inventory-card {
    flex-direction: column;
    align-items: start;
  }
}
</style>
