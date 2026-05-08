import { defineStore } from 'pinia'
import { adminProductWorkflowApi } from '@/services/adminProductWorkflow'
import { getRememberedDraftProductId, rememberDraftProductId } from '@/utils/adminProductWorkflow'

function getDefaultLoadingState() {
  return {
    draft: false,
    product: false,
    references: false,
    brands: false,
    tags: false,
    categories: false,
    attributes: false,
    productAttributes: false,
    variants: false,
    inventory: false,
    variantAttributes: false,
    images: false,
    publish: false,
    updateProduct: false,
  }
}

function pageItems(payload) {
  return payload?.items || []
}

export const useAdminProductComposerStore = defineStore('admin-product-composer', {
  state: () => ({
    draftProduct: null,
    brands: [],
    tags: [],
    categories: [],
    attributes: [],
    productAttributes: [],
    variants: [],
    variantAttributes: [],
    images: [],
    inventoryRecord: null,
    activeVariantId: null,
    selectedTagIds: [],
    selectedCategoryIds: [],
    feedbackMessage: '',
    feedbackError: '',
    referencesLoaded: false,
    loading: getDefaultLoadingState(),
  }),
  getters: {
    draftId: (state) => state.draftProduct?.id || getRememberedDraftProductId(),
    activeVariant(state) {
      return state.variants.find((variant) => variant.id === state.activeVariantId) || null
    },
    hasDraft: (state) => Boolean(state.draftProduct?.id),
  },
  actions: {
    setFeedback(message = '', error = '') {
      this.feedbackMessage = message
      this.feedbackError = error
    },
    clearFeedback() {
      this.setFeedback('', '')
    },
    resetDetailCollections() {
      this.productAttributes = []
      this.variants = []
      this.variantAttributes = []
      this.images = []
      this.inventoryRecord = null
      this.activeVariantId = null
      this.selectedTagIds = []
      this.selectedCategoryIds = []
    },
    setDraftProduct(product) {
      this.draftProduct = product
      rememberDraftProductId(product?.id || null)
      this.selectedTagIds = (product?.tags || []).map((tag) => tag.id)
      this.selectedCategoryIds = (product?.categories || []).map((category) => category.id)
    },
    async ensureReferenceCatalogs({ force = false } = {}) {
      if (this.referencesLoaded && !force) {
        return
      }

      this.loading.references = true
      this.loading.brands = true
      this.loading.tags = true
      this.loading.categories = true
      this.loading.attributes = true

      const results = await Promise.allSettled([
        adminProductWorkflowApi.listBrands(),
        adminProductWorkflowApi.listTags(),
        adminProductWorkflowApi.listCategories(),
        adminProductWorkflowApi.listAttributes(),
      ])

      const [brandsResult, tagsResult, categoriesResult, attributesResult] = results

      if (brandsResult.status === 'fulfilled') {
        this.brands = pageItems(brandsResult.value)
      }
      if (tagsResult.status === 'fulfilled') {
        this.tags = pageItems(tagsResult.value)
      }
      if (categoriesResult.status === 'fulfilled') {
        this.categories = pageItems(categoriesResult.value)
      }
      if (attributesResult.status === 'fulfilled') {
        this.attributes = pageItems(attributesResult.value)
      }

      const firstRejected = results.find((result) => result.status === 'rejected')
      if (firstRejected) {
        this.setFeedback('', firstRejected.reason?.message || 'بارگذاری داده‌های پایه کامل نشد.')
      } else {
        this.referencesLoaded = true
      }

      this.loading.references = false
      this.loading.brands = false
      this.loading.tags = false
      this.loading.categories = false
      this.loading.attributes = false
    },
    async hydrateWorkflow(productId, { force = false } = {}) {
      await this.ensureReferenceCatalogs()

      if (!productId) {
        return
      }

      if (!force && this.draftProduct?.id === productId) {
        return
      }

      this.loading.product = true

      try {
        const product = await adminProductWorkflowApi.getDraft(productId)
        this.setDraftProduct(product)
        await Promise.all([this.loadProductAttributes(), this.loadVariants(), this.loadImages()])
      } finally {
        this.loading.product = false
      }
    },
    async refreshDraftProduct() {
      if (!this.draftId) {
        return null
      }

      const product = await adminProductWorkflowApi.getDraft(this.draftId)
      this.setDraftProduct(product)
      return product
    },
    async createDraft(payload) {
      this.loading.draft = true
      this.clearFeedback()

      try {
        const product = await adminProductWorkflowApi.createDraft(payload)
        this.setDraftProduct(product)
        this.resetDetailCollections()
        await this.hydrateWorkflow(product.id, { force: true })
        this.setFeedback(`draft محصول #${product.id} ساخته شد.`, '')
        return product
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.draft = false
      }
    },
    async updateProduct(payload, successMessage = 'تغییرات محصول ذخیره شد.') {
      if (!this.draftId) {
        return null
      }

      this.loading.updateProduct = true
      this.clearFeedback()

      try {
        await adminProductWorkflowApi.updateProduct(this.draftId, payload)
        await this.refreshDraftProduct()
        this.setFeedback(successMessage, '')
        return this.draftProduct
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.updateProduct = false
      }
    },
    async publishProduct() {
      if (!this.draftId) {
        return null
      }

      this.loading.publish = true
      this.clearFeedback()

      try {
        await adminProductWorkflowApi.publishProduct(this.draftId)
        await this.refreshDraftProduct()
        this.setFeedback('محصول با موفقیت منتشر شد.', '')
        return this.draftProduct
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.publish = false
      }
    },
    async createBrand(payload) {
      this.loading.brands = true
      this.clearFeedback()

      try {
        await adminProductWorkflowApi.createBrand(payload)
        const response = await adminProductWorkflowApi.listBrands()
        this.brands = pageItems(response)
        this.setFeedback('برند جدید ساخته شد.', '')
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.brands = false
      }
    },
    async createTag(payload) {
      this.loading.tags = true
      this.clearFeedback()

      try {
        await adminProductWorkflowApi.createTag(payload)
        const response = await adminProductWorkflowApi.listTags()
        this.tags = pageItems(response)
        this.setFeedback('تگ جدید ساخته شد.', '')
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.tags = false
      }
    },
    async syncTags(tagIds) {
      if (!this.draftId) {
        return null
      }

      this.loading.tags = true
      this.clearFeedback()

      try {
        const response = await adminProductWorkflowApi.syncProductTags(this.draftId, tagIds)
        this.selectedTagIds = response.current || []
        await this.refreshDraftProduct()
        this.setFeedback('تگ‌های محصول ذخیره شدند.', '')
        return response
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.tags = false
      }
    },
    async createCategory(payload) {
      this.loading.categories = true
      this.clearFeedback()

      try {
        await adminProductWorkflowApi.createCategory(payload)
        const response = await adminProductWorkflowApi.listCategories()
        this.categories = pageItems(response)
        this.setFeedback('دسته جدید ساخته شد.', '')
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.categories = false
      }
    },
    async syncCategories(categoryIds) {
      if (!this.draftId) {
        return null
      }

      this.loading.categories = true
      this.clearFeedback()

      try {
        const response = await adminProductWorkflowApi.syncProductCategories(this.draftId, categoryIds)
        this.selectedCategoryIds = response.current || []
        await this.refreshDraftProduct()
        this.setFeedback('دسته‌های محصول ذخیره شدند.', '')
        return response
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.categories = false
      }
    },
    async createAttribute(payload) {
      this.loading.attributes = true
      this.clearFeedback()

      try {
        await adminProductWorkflowApi.createAttribute(payload)
        const response = await adminProductWorkflowApi.listAttributes()
        this.attributes = pageItems(response)
        this.setFeedback('اتریبیوت جدید ساخته شد.', '')
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.attributes = false
      }
    },
    async loadProductAttributes() {
      if (!this.draftId) {
        this.productAttributes = []
        return
      }

      this.loading.productAttributes = true

      try {
        const response = await adminProductWorkflowApi.listProductAttributes(this.draftId)
        this.productAttributes = pageItems(response)
      } finally {
        this.loading.productAttributes = false
      }
    },
    async createProductAttribute(payload) {
      if (!this.draftId) {
        return null
      }

      this.loading.productAttributes = true
      this.clearFeedback()

      try {
        const response = await adminProductWorkflowApi.createProductAttribute(payload)
        await Promise.all([this.loadProductAttributes(), this.refreshDraftProduct()])
        this.setFeedback('ویژگی محصول ثبت شد.', '')
        return response
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.productAttributes = false
      }
    },
    async loadVariants() {
      if (!this.draftId) {
        this.variants = []
        this.activeVariantId = null
        return
      }

      this.loading.variants = true

      try {
        const response = await adminProductWorkflowApi.listVariants(this.draftId)
        this.variants = pageItems(response)

        if (!this.variants.some((variant) => variant.id === this.activeVariantId)) {
          this.activeVariantId = this.variants[0]?.id || null
        }

        if (this.activeVariantId) {
          await Promise.all([this.loadInventory(), this.loadVariantAttributes()])
        } else {
          this.inventoryRecord = null
          this.variantAttributes = []
        }
      } finally {
        this.loading.variants = false
      }
    },
    async createVariant(payload) {
      if (!this.draftId) {
        return null
      }

      this.loading.variants = true
      this.clearFeedback()

      try {
        const variant = await adminProductWorkflowApi.createVariant(payload)
        await this.loadVariants()
        this.activeVariantId = variant.id
        await Promise.all([this.loadInventory(), this.loadVariantAttributes(), this.refreshDraftProduct()])
        this.setFeedback(`واریانت #${variant.id} ساخته شد.`, '')
        return variant
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.variants = false
      }
    },
    async selectVariant(variantId) {
      this.activeVariantId = variantId
      await Promise.all([this.loadInventory(), this.loadVariantAttributes()])
    },
    async loadVariantAttributes() {
      if (!this.activeVariantId) {
        this.variantAttributes = []
        return
      }

      this.loading.variantAttributes = true

      try {
        const response = await adminProductWorkflowApi.listVariantAttributes(this.activeVariantId)
        this.variantAttributes = pageItems(response)
      } finally {
        this.loading.variantAttributes = false
      }
    },
    async createVariantAttribute(payload) {
      if (!this.activeVariantId) {
        return null
      }

      this.loading.variantAttributes = true
      this.clearFeedback()

      try {
        const response = await adminProductWorkflowApi.createVariantAttribute(payload)
        await Promise.all([this.loadVariantAttributes(), this.refreshDraftProduct()])
        this.setFeedback('ویژگی واریانت ثبت شد.', '')
        return response
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.variantAttributes = false
      }
    },
    async loadInventory() {
      if (!this.activeVariantId) {
        this.inventoryRecord = null
        return
      }

      this.loading.inventory = true

      try {
        const response = await adminProductWorkflowApi.listInventory(this.activeVariantId)
        this.inventoryRecord = pageItems(response)[0] || null
      } finally {
        this.loading.inventory = false
      }
    },
    async saveInventory(payload) {
      if (!this.activeVariantId) {
        return null
      }

      this.loading.inventory = true
      this.clearFeedback()

      try {
        if (this.inventoryRecord?.id) {
          this.inventoryRecord = await adminProductWorkflowApi.updateInventory(this.inventoryRecord.id, payload)
          this.setFeedback('موجودی واریانت به‌روزرسانی شد.', '')
        } else {
          this.inventoryRecord = await adminProductWorkflowApi.createInventory({
            ...payload,
            variant_id: this.activeVariantId,
          })
          this.setFeedback('موجودی واریانت ساخته شد.', '')
        }

        await this.refreshDraftProduct()
        return this.inventoryRecord
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.inventory = false
      }
    },
    async loadImages() {
      if (!this.draftId) {
        this.images = []
        return
      }

      this.loading.images = true

      try {
        this.images = await adminProductWorkflowApi.listImages(this.draftId)
      } finally {
        this.loading.images = false
      }
    },
    async uploadImage(payload) {
      if (!this.draftId) {
        return null
      }

      this.loading.images = true
      this.clearFeedback()

      try {
        const response = await adminProductWorkflowApi.uploadImage(this.draftId, payload)
        await Promise.all([this.loadImages(), this.refreshDraftProduct()])
        this.setFeedback('تصویر محصول آپلود شد.', '')
        return response
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.images = false
      }
    },
    async updateImage(imageId, payload) {
      this.loading.images = true
      this.clearFeedback()

      try {
        const response = await adminProductWorkflowApi.updateImage(imageId, payload)
        await Promise.all([this.loadImages(), this.refreshDraftProduct()])
        this.setFeedback('اطلاعات تصویر ذخیره شد.', '')
        return response
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.images = false
      }
    },
    async deleteImage(imageId) {
      this.loading.images = true
      this.clearFeedback()

      try {
        await adminProductWorkflowApi.deleteImage(imageId)
        await Promise.all([this.loadImages(), this.refreshDraftProduct()])
        this.setFeedback('تصویر حذف شد.', '')
      } catch (error) {
        this.setFeedback('', error.message)
        throw error
      } finally {
        this.loading.images = false
      }
    },
  },
})
