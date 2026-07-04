<!-- src/views/admin/product-tabs/CommentsTab.vue -->
<template>
  <div class="grid gap-5">
    <!-- هدر + آمار -->
    <div
      class="flex flex-wrap items-center justify-between gap-3 border-b border-border-light pb-4"
    >
      <div>
        <h2 class="m-0 text-[1.25rem] font-bold">مدیریت نظرات کاربران</h2>
        <p class="m-0 mt-1 text-sm text-text-muted">
          {{ commentsList.length }} نظر ثبت شده
          <span v-if="averageRating" class="mr-2 text-amber-500 font-bold">
            ★ {{ averageRating.toFixed(1) }}
          </span>
        </p>
      </div>
    </div>

    <!-- لیست نظرات -->
    <div v-if="commentsList.length" class="grid gap-4">
      <div
        v-for="com in commentsList"
        :key="com.id"
        class="grid gap-3 p-4 bg-bg-muted border border-border-light rounded-xl transition-all duration-200 hover:shadow-(--shadow-soft)"
      >
        <!-- متا: نام + تاریخ + امتیاز -->
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <strong class="text-[0.95rem]">{{ com.author_name || 'کاربر مهمان' }}</strong>
            <span
              v-if="com.rating"
              class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-600 text-xs font-bold"
            >
              ★ {{ com.rating }}
            </span>
          </div>
          <div class="flex items-center gap-3 text-xs text-text-muted">
            <span>ثبت: {{ formatPrsianDate(com.created_at) }}</span>
            <span v-if="com.updated_at !== com.created_at"
              >ویرایش: {{ formatPrsianDate(com.updated_at) }}</span
            >
          </div>
        </div>

        <!-- متن نظر -->
        <p class="m-0 text-[0.95rem] text-text-main leading-relaxed">{{ com.content }}</p>

        <!-- فرم ویرایش -->
        <div v-if="editingId === com.id" class="grid gap-3 pt-3 border-t border-border-light">
          <div class="grid gap-1.5">
            <label class="text-xs font-bold text-text-muted">نام نویسنده</label>
            <BaseInput v-model="editForm.author_name" placeholder="نام نویسنده..." />
          </div>
          <div class="grid gap-1.5">
            <label class="text-xs font-bold text-text-muted">متن نظر</label>
            <textarea
              v-model="editForm.content"
              rows="3"
              class="w-full border border-border-light rounded-xl px-4 py-3 text-[0.95rem] bg-white font-[inherit] resize-y focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all"
            />
          </div>
          <div class="grid gap-1.5">
            <label class="text-xs font-bold text-text-muted">امتیاز (۱ تا ۵)</label>
            <BaseInput
              v-model.number="editForm.rating"
              type="number"
              min="1"
              max="5"
              placeholder="امتیاز..."
            />
          </div>
          <div class="flex gap-2 justify-end">
            <BaseButton variant="secondary" size="sm" @click="cancelEdit">انصراف</BaseButton>
            <BaseButton variant="primary" size="sm" :disabled="isSaving" @click="saveEdit(com.id)">
              <Loader2Icon v-if="isSaving" class="w-3.5 h-3.5 animate-spin" />
              ذخیره تغییرات
            </BaseButton>
          </div>
        </div>

        <!-- دکمه‌های عملیات -->
        <div v-else class="flex items-center justify-end gap-2 pt-2 border-t border-border-light">
          <BaseButton variant="ghost" size="sm" @click="startEdit(com)">
            <PencilIcon class="w-3.5 h-3.5" />
            ویرایش
          </BaseButton>
          <BaseButton
            variant="danger-ghost"
            size="sm"
            :disabled="isDeletingId === com.id"
            @click="deleteComment(com.id)"
          >
            <Loader2Icon v-if="isDeletingId === com.id" class="w-3.5 h-3.5 animate-spin" />
            <Trash2Icon v-else class="w-3.5 h-3.5" />
            حذف نظر
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- empty state -->
    <div
      v-else
      class="flex flex-col items-center justify-center py-12 text-center bg-bg-muted border border-dashed border-border-strong rounded-xl"
    >
      <MessageSquareIcon class="w-10 h-10 text-text-muted opacity-40 mb-3" />
      <p class="m-0 text-text-muted">هیچ نظری برای این محصول ثبت نشده است.</p>
    </div>
  </div>
</template>

<script setup>
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { commentService } from '@/services/productService'
import { useErrorStore } from '@/stores/errorStore'
import { getErrorMessage } from '@/utils/errorMessages'
import { formatPrsianDate } from '@/utils/format'
import { Loader2Icon, MessageSquareIcon, PencilIcon, Trash2Icon } from '@lucide/vue'
import { inject, onMounted, ref } from 'vue'

const product = inject('product')
const errorStore = useErrorStore()

const commentsList = ref([])
const averageRating = ref(0)

onMounted(() => {
  commentsList.value = product.value.comments || []
  averageRating.value = product.value.average_rating || 0
})

// ─── حذف نظر ───
const isDeletingId = ref(null)

async function deleteComment(commentId) {
  if (!confirm('آیا از حذف این نظر اطمینان دارید؟')) return
  isDeletingId.value = commentId
  try {
    await commentService.deleteComment(commentId)
    commentsList.value = commentsList.value.filter((c) => c.id !== commentId)
    errorStore.addError({ type: 'success', message: 'نظر با موفقیت حذف شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در حذف نظر.',
    })
  } finally {
    isDeletingId.value = null
  }
}

// ─── ویرایش نظر ───
const editingId = ref(null)
const isSaving = ref(false)
const editForm = ref({ author_name: '', content: '', rating: '' })

function startEdit(com) {
  editingId.value = com.id
  editForm.value = {
    author_name: com.author_name || '',
    content: com.content || '',
    rating: com.rating || '',
  }
}

function cancelEdit() {
  editingId.value = null
  editForm.value = { author_name: '', content: '', rating: '' }
}

async function saveEdit(commentId) {
  if (!editForm.value.content?.trim()) {
    errorStore.addError({ type: 'warning', message: 'متن نظر نمی‌تواند خالی باشد.' })
    return
  }
  isSaving.value = true
  try {
    const updated = await commentService.updateComment(commentId, {
      author_name: editForm.value.author_name,
      content: editForm.value.content,
      rating: editForm.value.rating ? Number(editForm.value.rating) : null,
    })
    const idx = commentsList.value.findIndex((c) => c.id === commentId)
    if (idx !== -1) commentsList.value[idx] = { ...commentsList.value[idx], ...updated }
    cancelEdit()
    errorStore.addError({ type: 'success', message: 'نظر با موفقیت ویرایش شد.' })
  } catch (error) {
    errorStore.addError({
      type: 'error',
      message: getErrorMessage(error.code) || 'خطا در ویرایش نظر.',
    })
  } finally {
    isSaving.value = false
  }
}
</script>
