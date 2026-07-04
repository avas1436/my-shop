// src/utils/errorMessages.js
export const ERROR_MESSAGES = {
  // Auth Codes (401)
  MISSING_TOKEN: 'لطفا وارد حساب کاربری خود شوید.',
  INVALID_TOKEN: 'نشست شما منقضی شده است. لطفا مجددا وارد شوید.',

  // Access Control Codes (403)
  ACCOUNT_INACTIVE: 'حساب کاربری شما غیرفعال شده است.',
  ACCOUNT_DELETED: 'حساب کاربری شما حذف شده است.',
  ACCESS_DENIED: 'شما دسترسی لازم برای انجام این عملیات را ندارید.',
  PHONE_NOT_VERIFIED: 'شماره موبایل شما تایید نشده است.',
  PROFILE_INCOMPLETE: 'لطفا اطلاعات پروفایل خود را تکمیل کنید.',
  SESSION_TOO_OLD: 'به دلایل امنیتی لطفا مجددا وارد شوید.',

  // Rate Limit (429)
  RATE_LIMIT_EXCEEDED:
    'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً کمی صبر کرده و مجدداً تلاش کنید.',
  DEFAULT_429: 'درخواست‌های شما خیلی سریع ارسال شده‌اند. لطفاً چند لحظه دیگر دوباره تلاش کنید.',
  ECONNABORTED: 'پاسخی از سرور دریافت نشد. لطفا مجددا تلاش کنید.',

  // Product & Catalog
  PRODUCT_INVALID_ID: 'شناسه محصول وارد شده نامعتبر است.',
  PRODUCT_NOT_FOUND: 'محصول مورد نظر یافت نشد یا حذف شده است.',
  PRODUCT_DATA_CONFLICT: 'تداخل در اطلاعات کالا؛ نام کالا یا نامک (Slug) تکراری است.',
  PRODUCT_CREATE_FAILED: 'خطایی در ثبت و ایجاد کالا در سیستم رخ داد.',
  PRODUCT_UPDATE_FAILED: 'خطایی در به‌روزرسانی مشخصات کالا رخ داد.',
  PRODUCT_DELETE_FAILED: 'حذف موقت کالا با خطا مواجه شد.',
  PRODUCT_HARD_DELETE_FAILED: 'حذف دائمی کالا از پایگاه داده با خطا مواجه شد.',
  PRODUCT_PUBLISH_FAILED: 'خطایی در فرآیند انتشار نهایی کالا رخ داد.',
  PRODUCT_ALREADY_INACTIVE_OR_DELETED:
    'این محصول غیرفعال یا حذف شده است و امکان انتشار مجدد آن وجود ندارد.',
  PRODUCT_IDENTIFIER_REQUIRED: 'ارسال شناسه (ID) یا نامک (Slug) برای دریافت کالا الزامی است.',
  PAGINATION_INVALID_VALUES: 'مقادیر ارسالی برای صفحه‌بندی کالاها نامعتبر است.',

  // Image Service
  IMAGE_NOT_FOUND: 'تصویر مورد نظر یافت نشد.',
  PRODUCT_IMAGES_NOT_FOUND: 'هیچ تصویری برای این محصول ثبت نشده است.',
  IMAGE_INVALID_FORMAT: 'فرمت تصویر نامعتبر است. لطفاً از فرمت‌های png ،jpg یا webp استفاده کنید.',
  IMAGE_TOO_LARGE: 'حجم تصویر بیش از حد مجاز (حداکثر ۵ مگابایت) است.',

  // Variant & Inventory & Attribute
  VARIANT_NOT_FOUND: 'متغیر (Variant) مورد نظر یافت نشد.',
  INVENTORY_NOT_FOUND: 'رکورد موجودی مورد نظر در سیستم یافت نشد.',
  INVENTORY_ALREADY_EXISTS: 'برای این متغیر کالا، قبلاً رکورد موجودی ایجاد شده است.',

  ATTRIBUTE_NOT_FOUND: 'ویژگی (Attribute) مورد نظر یافت نشد.',
  ATTRIBUTE_NAME_DUPLICATE: 'نام ویژگی وارد شده تکراری است و از قبل وجود دارد.',
  ATTRIBUTE_SLUG_DUPLICATE: 'نامک (Slug) ویژگی وارد شده تکراری است.',

  PRODUCT_ATTRIBUTE_NOT_FOUND: 'ویژگی متصل به محصول یافت نشد.',
  PRODUCT_ATTRIBUTE_DUPLICATE: 'این ویژگی از قبل برای این محصول ثبت شده است.',

  VARIANT_ATTRIBUTE_NOT_FOUND: 'ویژگی متصل به متغیر کالا یافت نشد.',
  VARIANT_ATTRIBUTE_DUPLICATE: 'این ویژگی از قبل برای این متغیر کالا ثبت شده است.',

  // Category & Product-Category
  CATEGORY_NOT_FOUND: 'دسته‌بندی مورد نظر یافت نشد.',
  CATEGORY_NAME_DUPLICATE: 'دسته‌بندی با این نام از قبل وجود دارد.',
  CATEGORY_SLUG_DUPLICATE: 'دسته‌بندی با این نامک (Slug) از قبل وجود دارد.',
  CATEGORY_PARENT_NOT_FOUND: 'دسته‌بندی والد انتخاب شده، در سیستم یافت نشد.',
  CATEGORY_SELF_PARENT: 'یک دسته‌بندی نمی‌تواند خودش را به عنوان والد انتخاب کند.',
  CATEGORY_CYCLE_DETECTED:
    'ساختار درختی نامعتبر؛ دسته‌بندی والد نمی‌تواند از فرزندان خودِ این دسته‌بندی باشد.',
  CATEGORY_HAS_CHILDREN: 'امکان حذف این دسته‌بندی وجود ندارد، زیرا دارای زیرمجموعه (فرزند) است.',
  CATEGORY_PARENT_INACTIVE: 'امکان انتخاب این والد وجود ندارد، زیرا دسته‌بندی والد غیرفعال است.',
  PRODUCT_CATEGORY_MAPPED_NOT_FOUND:
    'برخی از دسته‌بندی‌های ارسالی برای اتصال به محصول، در سیستم وجود ندارند.',
  CATEGORY_PAGINATION_INVALID: 'مقادیر ارسالی برای صفحه‌بندی دسته‌بندی‌ها نامعتبر است.',

  // Tags & Product-Tags
  TAG_NOT_FOUND: 'برچسب مورد نظر یافت نشد.',
  TAG_NAME_DUPLICATE: 'برچسبی با این نام از قبل وجود دارد.',
  TAG_SLUG_DUPLICATE: 'برچسبی با این نامک (Slug) از قبل وجود دارد.',
  TAG_PAGINATION_INVALID: 'مقادیر ارسالی برای صفحه‌بندی برچسب‌ها نامعتبر است.',
  TAG_SOME_NOT_FOUND: 'برخی از برچسب‌های ارسالی در سیستم یافت نشدند.',

  // Comments Module
  COMMENT_INVALID_ID: 'شناسه دیدگاه وارد شده نامعتبر است.',
  COMMENT_NOT_FOUND: 'دیدگاه مورد نظر یافت نشد یا ممکن است حذف شده باشد.',
  COMMENT_PAGINATION_INVALID_VALUES: 'مقادیر ارسالی برای صفحه‌بندی دیدگاه‌ها نامعتبر است.',
  COMMENT_USER_INVALID_ID: 'شناسه کاربر ارسالی برای فیلتر دیدگاه‌ها نامعتبر است.',
  COMMENT_PRODUCT_INVALID_ID: 'شناسه محصول ارسالی برای فیلتر دیدگاه‌ها نامعتبر است.',
  COMMENT_DATA_REQUIRED: 'اطلاعات و متن دیدگاه نمی‌تواند خالی باشد.',
  COMMENT_ACCESS_DENIED: 'شما اجازه تغییر یا حذف این دیدگاه را ندارید.',
  COMMENT_NO_FIELDS_TO_UPDATE: 'هیچ فیلدی برای به‌روزرسانی دیدگاه ارسال نشده است.',
  COMMENT_CREATE_FAILED: 'خطایی در ثبت و ایجاد دیدگاه رخ داد. لطفا مجددا تلاش کنید.',
  COMMENT_UPDATE_FAILED: 'خطایی در ویرایش دیدگاه رخ داد. لطفا مجددا تلاش کنید.',
  COMMENT_DELETE_FAILED: 'خطایی در حذف دیدگاه رخ داد. لطفا مجددا تلاش کنید.',

  // Business Logic
  USER_NOT_FOUND: 'کاربر یافت نشد.',
  INVALID_OTP: 'کد وارد شده نامعتبر است.',
  ALREADY_EXIST_USER: 'این شماره قبلا ثبت نام کرده است.',

  // Defaults
  DEFAULT_4XX: 'درخواست نامعتبر است.',
  DEFAULT_5XX: 'خطایی در سرور رخ داده است. لطفا بعدا تلاش کنید.',
  NETWORK_ERROR: 'ارتباط با سرور برقرار نشد. اینترنت خود را بررسی کنید.',

  REGISTERED: 'کاربر وجود دارد لطفا با رمز عبور وارد شوید.',
  NOT_ACTIVATE_PASSWORD: 'این حساب فاقد رمز عبور می باشد',
  PROFILE_COMPLETED: 'اطلاعات پروفایل شما کامل شده است',
}

export const getErrorMessage = (code) => {
  return ERROR_MESSAGES[code] || null
}
