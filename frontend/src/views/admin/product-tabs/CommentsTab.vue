<!-- src/views/admin/product-tabs/CommentsTab.vue -->
<template>
  <div class="tab-content page-panel admin-settings-panel">
    <h2 class="tab-title">مدیریت نظرات کاربران</h2>

    <div v-if="commentsList.length" class="comments-vertical-list">
      <div v-for="com in commentsList" :key="com.id" class="comment-node-card">
        <div class="comment-meta">
          <strong>{{ com.user_fullname || 'کاربر مهمان' }}</strong>
          <span class="date-tag">{{ formatPrsianDate(com.created_at) }}</span>
        </div>
        <p class="comment-body-text">{{ com.text }}</p>
        <div class="comment-actions">
          <button class="btn-delete-comment" @click="deleteComment(com.id)">حذف نظر</button>
        </div>
      </div>
    </div>
    <div v-else class="empty-comments">هیچ نظری برای این محصول ثبت نشده است.</div>
  </div>
</template>

<script setup>
import { productService } from '@/services/productService'
import { formatPrsianDate } from '@/utils/format'
import { inject, onMounted, ref } from 'vue'

const product = inject('product')
const commentsList = ref([])

onMounted(async () => {
  if (product.value?.id) {
    try {
      const response = (await productService.getProductComments?.(product.value.id)) || []
      commentsList.value = response
    } catch (err) {
      console.error(err)
    }
  }
})

async function deleteComment(commentId) {
  if (!confirm('آیا از حذف این نظر اطمینان دارید؟')) return
  try {
    await productService.deleteComment(commentId)
    commentsList.value = commentsList.value.filter((c) => c.id !== commentId)
  } catch (error) {
    alert('خطا در حذف نظر')
  }
}
</script>

<style scoped>
.admin-settings-panel {
  text-align: right;
}
.comments-vertical-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.comment-node-card {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}
.comment-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}
.comment-body-text {
  font-size: 0.95rem;
  color: #334155;
  line-height: 1.6;
}
.comment-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}
.btn-delete-comment {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}
.empty-comments {
  text-align: center;
  color: #94a3b8;
  padding: 2rem;
}
</style>
