<!-- src/components/base/BaseModal.vue -->
<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="open" class="fixed inset-0 grid place-items-center z-50 p-4">
        <div
          class="absolute inset-0 bg-text-main/40 backdrop-blur-sm"
          @click="$emit('close')"
        ></div>

        <div
          class="relative w-full max-w-140 bg-surface-strong rounded-lg shadow-custom border border-border-strong p-6 md:p-8 z-10 overflow-y-auto max-h-[calc(100vh-32px)]"
        >
          <button
            @click="$emit('close')"
            class="absolute top-4 left-4 text-text-muted hover:text-text-main transition-colors cursor-pointer"
          >
            ✕
          </button>

          <div class="mt-2">
            <slot />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  open: { type: Boolean, default: false },
})

defineEmits(['close'])
</script>

<!-- روش استفاده -->
<!--
 هرجایی که میخوایم بدون تغییر صفحه یک صفحه باز بشه و توش چیزی نمایش داده بشه
   -->
<!--
 <BaseModal :open="isModalOpen" @close="isModalOpen = false">
      
      <div class="flex flex-col gap-5">
        <div>
          <h3 class="text-xl font-bold text-text-main">فرم ثبت نام کاربر</h3>
          <p class="text-sm text-text-muted mt-1">اطلاعات کاربر جدید را وارد کنید.</p>
        </div>

        <BaseInput label="نام و نام خانوادگی" placeholder="مثلا: علی محمدی" />
        <BaseInput label="شماره تماس" placeholder="۰۹۱۲۰۰۰۰۰۰۰" />

        <div class="flex gap-3 mt-2 justify-end">
          <BaseButton variant="secondary" size="sm" @click="isModalOpen = false">
            انصراف
          </BaseButton>
          <BaseButton variant="success" size="sm" @click="saveUser">
            ذخیره کاربر
          </BaseButton>
        </div>
      </div>

    </BaseModal>
-->
