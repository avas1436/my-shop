<template>
  <div class="content-grid">
    <section class="page-panel admin-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">تنظیمات فروشگاه</h2>
          <p class="section-subtitle">مواردی که در هدر، فوتر و صفحات پشتیبانی نمایش داده می‌شوند</p>
        </div>
      </div>

      <form class="content-form" @submit.prevent="saveSettings">
        <BaseInput v-model="settings.storeName" label="نام فروشگاه" />
        <BaseInput v-model="settings.supportPhone" label="تلفن پشتیبانی" />
        <BaseInput v-model="settings.supportEmail" label="ایمیل پشتیبانی" />
        <BaseInput v-model="settings.heroMessage" label="پیام اصلی فروشگاه" />
        <BaseInput v-model="settings.fulfillmentWindow" label="بازه ارسال" />
        <BaseButton block type="submit">ذخیره تنظیمات</BaseButton>
      </form>
    </section>

    <section class="page-panel admin-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">کمپین‌ها</h2>
          <p class="section-subtitle">فعال‌سازی یا توقف کمپین‌های نمایشی در پنل مدیریتی</p>
        </div>
      </div>

      <div class="campaign-list">
        <article v-for="campaign in admin.campaigns" :key="campaign.id" class="campaign-item">
          <div>
            <strong>{{ campaign.title }}</strong>
            <p>{{ campaign.channel }} • {{ campaign.budget }}</p>
          </div>
          <button type="button" class="campaign-toggle" @click="admin.toggleCampaign(campaign.id)">
            {{ campaign.active ? 'فعال' : 'غیرفعال' }}
          </button>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useAdminStore } from '@/stores/adminStore'

const admin = useAdminStore()
const settings = reactive({ ...admin.settings })

function saveSettings() {
  admin.updateSettings(settings)
}
</script>

<style scoped>
.content-grid {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 1rem;
}

.admin-card {
  padding: 1.25rem;
}

.content-form,
.campaign-list {
  display: grid;
  gap: 0.85rem;
}

.campaign-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  border-radius: 20px;
  background: var(--bg-muted);
}

.campaign-item p {
  margin: 0.35rem 0 0;
  color: var(--text-muted);
}

.campaign-toggle {
  min-height: 44px;
  padding: 0 1rem;
  border: 0;
  border-radius: 999px;
  background: rgba(91, 61, 245, 0.12);
  color: var(--primary);
  font-weight: 700;
}

@media (max-width: 1080px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .campaign-item {
    flex-direction: column;
    align-items: start;
  }
}
</style>
