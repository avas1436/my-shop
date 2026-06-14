<!-- src/views/admin/product-tabs/RelationsTab.vue -->
<template>
  <div class="tab-content admin-secondary-layout">
    <section class="page-panel admin-settings-panel mb-4">
      <h3 class="specs-heading">اتصال به دسته‌بندی‌ها</h3>
      <div class="checkbox-list">
        <label v-for="cat in allCategories" :key="cat.id" class="checkbox-item">
          <input
            type="checkbox"
            :checked="isCategoryAttached(cat.id)"
            @change="toggleCategory($event, cat.id)"
          />
          {{ cat.title }}
        </label>
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
import { productService } from '@/services/productService'
import { inject, onMounted, ref } from 'vue'

const product = inject('product')
const refreshProductData = inject('refreshProductData')

// متغیرها برای ذخیره کل دیتای دریافتی جهت چک‌باکس‌ها
const allCategories = ref([])
const allTags = ref([])
const availableAttributesList = ref([])

const newAttribute = ref({ id: '', value: '' })

const isCategoryAttached = (catId) => product.value?.categories?.some((c) => c.id === catId)
const isTagAttached = (tagId) => product.value?.tags?.some((t) => t.id === tagId)

// بارگذاری مقادیر اولیه برای لیست‌ها در زمان بالا آمدن تب
onMounted(async () => {
  try {
    // نکته: متدهای مربوط به دریافت کل دسته‌ها و برچسب‌ها را بر اساس ساختار پروژه خود صدا بزنید
    const cats = (await productService.getCategoriesList?.()) || { items: [] }
    allCategories.value = cats.items
    const tags = (await productService.getTagsList?.()) || { items: [] }
    allTags.value = tags.items
    const attrs = (await productService.getAvailableAttributes?.()) || { items: [] }
    availableAttributesList.value = attrs.items
  } catch (err) {
    console.error('خطا در بارگذاری موجودیت‌های ارتباطی', err)
  }
})

const toggleCategory = async (event, catId) => {
  try {
    if (event.target.checked) {
      await productService.attachCategory(product.value.id, catId)
    } else {
      await productService.detachCategory(product.value.id, catId)
    }
    await refreshProductData()
  } catch (error) {
    console.error(error)
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
}
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
</style>
