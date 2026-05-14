import { api } from './api'
import { buildQueryString } from '@/utils/adminProductWorkflowUtils'

export const adminProductWorkflowService = {
  createDraft(payload) {
    return api.postData('/v1/products/admin/createdraft', payload)
  },
  getDraft(productId) {
    return api.getData(`/v1/products/admin/products/${productId}/full`)
  },
  updateProduct(productId, payload) {
    return api.patchData(`/v1/products/admin/products/${productId}`, payload)
  },
  publishProduct(productId) {
    return api.postData(`/v1/products/admin/products/${productId}/publish`, {})
  },
  listBrands(params = {}) {
    return api.getData(`/v1/brands${buildQueryString({ page: 1, size: 100, ...params })}`)
  },
  createBrand(payload) {
    return api.postData('/v1/brands/', payload)
  },
  listTags(params = {}) {
    return api.getData(`/v1/tags/admin${buildQueryString({ page: 1, size: 100, ...params })}`)
  },
  createTag(payload) {
    return api.postData('/v1/tags/admin', payload)
  },
  syncProductTags(productId, tagIds) {
    return api.putData(`/v1/tags/${productId}/tags/sync`, { tag_ids: tagIds })
  },
  listCategories(params = {}) {
    return api.getData(`/v1/categories${buildQueryString({ page: 1, size: 100, ...params })}`)
  },
  createCategory(payload) {
    return api.postData('/v1/categories/', payload)
  },
  syncProductCategories(productId, categoryIds) {
    return api.putData(`/v1/categories/${productId}/categories/sync`, {
      category_ids: categoryIds,
    })
  },
  listAttributes(params = {}) {
    return api.getData(`/v1/attributes/list${buildQueryString({ page: 1, size: 100, ...params })}`)
  },
  createAttribute(payload) {
    return api.postData('/v1/attributes/', payload)
  },
  listProductAttributes(productId) {
    return api.getData(
      `/v1/attributes/list/product/list${buildQueryString({ product_id: productId, page: 1, size: 100 })}`,
    )
  },
  createProductAttribute(payload) {
    return api.postData('/v1/attributes/product', payload)
  },
  listVariants(productId) {
    return api.getData(`/v1/variants/list${buildQueryString({ product_id: productId, page: 1, size: 100 })}`)
  },
  createVariant(payload) {
    return api.postData('/v1/variants/', payload)
  },
  listVariantAttributes(variantId) {
    return api.getData(
      `/v1/attributes/list/product/variant${buildQueryString({ variant_id: variantId, page: 1, size: 100 })}`,
    )
  },
  createVariantAttribute(payload) {
    return api.postData('/v1/attributes/product/variant', payload)
  },
  listInventory(variantId) {
    return api.getData(`/v1/inventory/list${buildQueryString({ variant_id: variantId, page: 1, size: 100 })}`)
  },
  createInventory(payload) {
    return api.postData('/v1/inventory/', payload)
  },
  updateInventory(inventoryId, payload) {
    return api.putData(`/v1/inventory/${inventoryId}`, payload)
  },
  listImages(productId) {
    return api.getData(`/v1/images/admin/product/${productId}`)
  },
  uploadImage(productId, payload) {
    const formData = new FormData()
    formData.append('file', payload.file)
    formData.append('alt_text', payload.alt_text || '')
    formData.append('is_primary', payload.is_primary ? 'true' : 'false')
    formData.append('sort_order', String(payload.sort_order ?? 0))

    return api.postFormData(`/v1/images/admin/products/${productId}`, formData)
  },
  updateImage(imageId, payload) {
    return api.patchData(`/v1/images/admin/images/${imageId}`, payload)
  },
  deleteImage(imageId) {
    return api.deleteData(`/v1/images/admin/images/${imageId}`)
  },
}
