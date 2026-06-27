// src/services/productService.js
import axiosClient from './axiosClient'

const BASE_URL = '/v1/products/admin'

/**
 * ==========================
 *  Product
 * ==========================
 */
export const productService = {
  //    ۱. ایجاد پیش‌نویس محصول جدید
  async createDraft(productData) {
    return await axiosClient.post(`${BASE_URL}/createdraft`, productData)
  },

  // ۲. حذف نرم‌افزاری محصول

  async softDelete(productId) {
    return await axiosClient.delete(`${BASE_URL}/products/soft/${productId}`)
  },

  //  ۳. حذف کامل و همیشگی محصول از دیتابیس

  async hardDelete(productId) {
    return await axiosClient.delete(`${BASE_URL}/products/hard/${productId}`)
  },

  //  ۴. دریافت و مشاهده اطلاعات کامل یک محصول خاص

  async getProductFull(productId) {
    return await axiosClient.get(`${BASE_URL}/products/${productId}/full`)
  },

  //  ۵. به‌روزرسانی جزئی اطلاعات محصول

  async patchProduct(productId, updateData) {
    return await axiosClient.patch(`${BASE_URL}/products/${productId}`, updateData)
  },

  //  ۶. انتشار نهایی محصول

  async publishProduct(productId) {
    return await axiosClient.post(`${BASE_URL}/products/${productId}/publish`, {})
  },
}

/**
 * ==========================
 *  Image
 * ==========================
 */
export const imageService = {
  // ۱. آپلود تصویر برای محصول
  // async uploadImage(productId, imageData) {
  //   return await axiosClient.post(`/v1/images/admin/products/${productId}/images`, imageData)
  // },
  async uploadImage(productId, imageData) {
    const response = await axiosClient.post(
      `/v1/images/admin/products/${productId}/images`,
      imageData,
      {
        headers: {
          // این هدر به اکسایوس می‌گوید که داده‌ها از نوع فرم و فایل هستند
          'Content-Type': 'multipart/form-data',
        },
      },
    )
    return response.data
  },

  // ۲. دریافت لیست تصاویر یک محصول
  async listImages(productId) {
    return await axiosClient.get(`/v1/images/admin/product/${productId}`)
  },

  // ۳. دریافت اطلاعات یک تصویر خاص
  async getImage(imageId) {
    return await axiosClient.get(`/v1/images/admin/image/${imageId}`)
  },

  // ۴. به‌روزرسانی تصویر
  async updateImage(imageId, updateData) {
    return await axiosClient.patch(`/v1/images/admin/images/${imageId}`, updateData)
  },

  // ۵. حذف تصویر
  async deleteImage(imageId) {
    return await axiosClient.delete(`/v1/images/admin/images/${imageId}`)
  },
}

/**
 * ==========================
 *  Brand
 * ==========================
 */
export const brandService = {
  // ۱. ایجاد برند جدید
  async createBrand(brandData) {
    return await axiosClient.post(`/v1/brands/`, brandData)
  },

  // ۲. دریافت لیست تمامی برندها
  async listBrands(search) {
    return await axiosClient.get(`/v1/brands/`, search)
  },

  // ۳. دریافت اطلاعات یک برند خاص
  async getBrand(brandId) {
    return await axiosClient.get(`/v1/brands/${brandId}`)
  },

  // ۴. به‌روزرسانی اطلاعات برند
  async updateBrand(brandId, updateData) {
    return await axiosClient.put(`/v1/brands/${brandId}`, updateData)
  },

  // ۵. حذف برند
  async deleteBrand(brandId) {
    return await axiosClient.delete(`/v1/brands/${brandId}`)
  },
}

/**
 * ==========================
 *  Category
 * ==========================
 */
export const categoryService = {
  // ۱. ایجاد دسته‌بندی جدید
  async createCategory(categoryData) {
    return await axiosClient.post(`/v1/categories/`, categoryData)
  },

  // ۲. دریافت لیست دسته‌بندی‌ها
  async listCategories() {
    return await axiosClient.get(`/v1/categories/`)
  },

  // ۳. دریافت یک دسته‌بندی خاص
  async getCategory(categoryId) {
    return await axiosClient.get(`/v1/categories/${categoryId}`)
  },

  // ۴. به‌روزرسانی دسته‌بندی
  async updateCategory(categoryId, updateData) {
    return await axiosClient.put(`/v1/categories/${categoryId}`, updateData)
  },

  // ۵. حذف دسته‌بندی
  async deleteCategory(categoryId) {
    return await axiosClient.delete(`/v1/categories/${categoryId}`)
  },

  // // ۶. متصل کردن دسته‌بندی‌ها به یک محصول
  // async attachCategories(productId, data) {
  //   return await axiosClient.post(`/v1/categories/${productId}/categories/attach`, data)
  // },

  // // ۷. جدا کردن دسته‌بندی‌ها از یک محصول
  // async detachCategories(productId, data) {
  //   return await axiosClient.post(`/v1/categories/${productId}/categories/detach`, data)
  // },

  // ۸. همگام‌سازی (سینک) دسته‌بندی‌های یک محصول
  async syncCategories(productId, data) {
    const payload = {
      category_ids: data,
    }
    return await axiosClient.put(`/v1/categories/${productId}/categories/sync`, payload)
  },

  // ۹. دریافت لیست کتگوری های والد
  async categoryParents(categoryId) {
    return await axiosClient.get(`/v1/categories/parents/${categoryId}`)
  },
}

/**
 * ==========================
 *  Tag
 * ==========================
 */
export const tagService = {
  // ۱. ایجاد تگ جدید (ادمین)
  async createTag(tagData) {
    return await axiosClient.post(`/v1/tags/admin`, tagData)
  },

  // ۲. دریافت لیست تگ‌ها (ادمین)
  async listTags() {
    return await axiosClient.get(`/v1/tags/admin`)
  },

  // ۳. دریافت یک تگ خاص (ادمین)
  // async getTag(tagId) {
  //   return await axiosClient.get(`/v1/tags/admin/${tagId}`)
  // },

  // ۴. به‌روزرسانی تگ (ادمین)
  async updateTag(tagId, updateData) {
    return await axiosClient.put(`/v1/tags/admin/${tagId}`, updateData)
  },

  // ۵. حذف تگ (ادمین)
  async deleteTag(tagId) {
    return await axiosClient.delete(`/v1/tags/admin/${tagId}`)
  },

  // ۶. متصل کردن تگ‌ها به یک محصول
  // async attachTags(productId, data) {
  //   return await axiosClient.post(`/v1/tags/${productId}/tags/attach`, data)
  // },

  // // ۷. جدا کردن تگ‌ها از یک محصول
  // async detachTags(productId, data) {
  //   return await axiosClient.post(`/v1/tags/${productId}/tags/detach`, data)
  // },

  // ۸. همگام‌سازی (سینک) تگ‌های یک محصول
  async syncTags(productId, data) {
    return await axiosClient.put(`/v1/tags/${productId}/tags/sync`, data)
  },
}

/**
 * ==========================
 *  Attribute
 * ==========================
 */
export const attributeService = {
  // --- ویژگی‌های اصلی ---

  // ۱. ایجاد ویژگی جدید
  async createAttribute(data) {
    return await axiosClient.post(`${BASE_URL}/`, data)
  },

  // ۲. دریافت لیست ویژگی‌ها
  async listAttributes() {
    return await axiosClient.get(`${BASE_URL}/list`)
  },

  // ۳. دریافت یک ویژگی خاص
  async getAttribute(attributeId) {
    return await axiosClient.get(`${BASE_URL}/${attributeId}`)
  },

  // ۴. به‌روزرسانی ویژگی
  async updateAttribute(attributeId, data) {
    return await axiosClient.put(`${BASE_URL}/${attributeId}`, data)
  },

  // ۵. حذف ویژگی
  async deleteAttribute(attributeId) {
    return await axiosClient.delete(`${BASE_URL}/${attributeId}`)
  },

  // --- ویژگی‌های محصول (Product Attributes) ---

  // ۶. ایجاد ویژگی برای محصول
  async createProductAttribute(data) {
    return await axiosClient.post(`${BASE_URL}/product`, data)
  },

  // ۷. دریافت ویژگی یک محصول
  async getProductAttribute(paId) {
    return await axiosClient.get(`${BASE_URL}/product/${paId}`)
  },

  // ۸. به‌روزرسانی ویژگی یک محصول
  async updateProductAttribute(paId, data) {
    return await axiosClient.put(`${BASE_URL}/product/${paId}`, data)
  },

  // ۹. حذف ویژگی یک محصول
  async deleteProductAttribute(paId) {
    return await axiosClient.delete(`${BASE_URL}/product/${paId}`)
  },

  // ۱۰. دریافت لیست تمام ویژگی‌های متصل به محصولات
  async listProductAttributes() {
    return await axiosClient.get(`${BASE_URL}/list/product/list`)
  },

  // --- ویژگی‌های متغیر محصول (Product Variant Attributes) ---

  // ۱۱. ایجاد ویژگی برای متغیر محصول
  async createProductVariantAttribute(data) {
    return await axiosClient.post(`${BASE_URL}/product/variant`, data)
  },

  // ۱۲. دریافت ویژگی یک متغیر محصول
  async getProductVariantAttribute(pvaId) {
    return await axiosClient.get(`${BASE_URL}/product/variant/${pvaId}`)
  },

  // ۱۳. به‌روزرسانی ویژگی یک متغیر محصول
  async updateProductVariantAttribute(pvaId, data) {
    return await axiosClient.put(`${BASE_URL}/product/variant/${pvaId}`, data)
  },

  // ۱۴. حذف ویژگی یک متغیر محصول
  async deleteProductVariantAttribute(pvaId) {
    return await axiosClient.delete(`${BASE_URL}/product/variant/${pvaId}`)
  },

  // ۱۵. دریافت لیست ویژگی‌های متغیر محصولات
  async listProductVariantAttributes() {
    return await axiosClient.get(`${BASE_URL}/list/product/variant`)
  },
}

/**
 * ==========================
 *  Variant
 * ==========================
 */
export const variantService = {
  // ۱. ایجاد متغیر جدید
  async createVariant(variantData) {
    return await axiosClient.post(`/v1/variants/`, variantData)
  },

  // ۲. دریافت لیست متغیرها
  // async listVariants() {
  //   return await axiosClient.get(`/v1/variants/list`)
  // },

  // ۳. دریافت یک متغیر خاص
  // async getVariant(variantId) {
  //   return await axiosClient.get(`/v1/variants/${variantId}`)
  // },

  // ۴. به‌روزرسانی متغیر
  async updateVariant(variantId, updateData) {
    return await axiosClient.put(`/v1/variants/${variantId}`, updateData)
  },

  // ۵. حذف متغیر
  async deleteVariant(variantId) {
    return await axiosClient.delete(`/v1/variants/${variantId}`)
  },
}

/**
 * ==========================
 *  Inventory
 * ==========================
 */
export const inventoryService = {
  // ۱. ایجاد رکورد موجودی جدید
  async createInventory(inventoryData) {
    return await axiosClient.post(`/v1/inventory/`, inventoryData)
  },

  // ۲. دریافت لیست موجودی‌ها
  // async listInventories() {
  //   return await axiosClient.get(`/v1/inventory/list`)
  // },

  // ۳. دریافت یک موجودی خاص
  // async getInventory(inventoryId) {
  //   return await axiosClient.get(`/v1/inventory/${inventoryId}`)
  // },

  // ۴. به‌روزرسانی موجودی
  async updateInventory(inventoryId, updateData) {
    return await axiosClient.put(`/v1/inventory/${inventoryId}`, updateData)
  },

  // ۵. حذف موجودی
  async deleteInventory(inventoryId) {
    return await axiosClient.delete(`/v1/inventory/${inventoryId}`)
  },
}

/**
 * ==========================
 *  Comment
 * ==========================
 */
export const commentService = {
  // ۱. ثبت نظر جدید
  async createComment(commentData) {
    return await axiosClient.post(`${BASE_URL}/`, commentData)
  },

  // ۲. دریافت لیست نظرات
  async listComments() {
    return await axiosClient.get(`${BASE_URL}/`)
  },

  // ۳. به‌روزرسانی نظر
  async updateComment(commentId, updateData) {
    return await axiosClient.put(`${BASE_URL}/${commentId}`, updateData)
  },

  // ۴. حذف نظر
  async deleteComment(commentId) {
    return await axiosClient.delete(`${BASE_URL}/${commentId}`)
  },
}

/**
 * ==========================
 *  Client Product
 * ==========================
 */
export const userProductService = {
  // ۱. دریافت محصولات ویژه صفحه اصلی
  async getHomeFeaturedProducts() {
    return await axiosClient.get(`${BASE_URL}/home`)
  },

  // ۲. جستجو در بین محصولات (پارامترها می‌توانند به صورت کوئری استرینگ ارسال شوند)
  async searchProducts(params) {
    return await axiosClient.get(`${BASE_URL}/search`, { params })
  },

  // ۳. دریافت اطلاعات کامل یک محصول با آیدی
  async getProductById(productId) {
    return await axiosClient.get(`${BASE_URL}/${productId}`)
  },

  // ۴. دریافت اطلاعات کامل یک محصول با اسلاگ (Slug)
  async getProductBySlug(slug) {
    return await axiosClient.get(`${BASE_URL}/slug/${slug}`)
  },
}
