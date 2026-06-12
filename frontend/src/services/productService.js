// src/services/productService.js
import axiosClient from './axiosClient'

const BASE_URL = '/v1/products/admin'

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
