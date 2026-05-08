<template>
  <div class="page-shell admin-workflow">
    <section class="page-panel admin-workflow__hero">
      <div class="admin-workflow__hero-copy">
        <span class="pill">سرویس ادمین - ساخت محصول مرحله‌ای</span>
        <h1 class="page-title">محصول جدید را به صورت draft بساز و مرحله‌به‌مرحله تکمیلش کن</h1>
        <p>
          این مسیر با URLهای جداگانه برای هر مرحله ساخته شده تا هم ساخت draft و هم تکمیل تدریجی
          برند، دسته‌بندی، واریانت‌ها، موجودی و رسانه‌ها قابل مدیریت باشد.
        </p>
      </div>

      <div class="admin-workflow__hero-stats">
        <div class="workflow-stat">
          <strong>{{ workflowStats.completed }}</strong>
          <span>گام آماده برای ادامه</span>
        </div>
        <div class="workflow-stat">
          <strong>{{ workflowStats.productStatus }}</strong>
          <span>وضعیت فعلی محصول</span>
        </div>
        <div class="workflow-stat">
          <strong>{{ workflowStats.variantCount }}</strong>
          <span>واریانت ثبت‌شده</span>
        </div>
      </div>
    </section>

    <div class="admin-workflow__layout">
      <aside class="admin-workflow__sidebar">
        <section class="page-panel workflow-sidebar-card">
          <div>
            <h2>نقشه مسیر</h2>
            <p class="workflow-page__intro">هر صفحه یک بخش مشخص از lifecycle محصول را پوشش می‌دهد.</p>
          </div>

          <nav class="workflow-steps">
            <RouterLink
              v-for="step in stepLinks"
              :key="step.key"
              :to="step.to"
              class="workflow-step-link"
              :class="{
                'workflow-step-link--active': step.key === currentStep?.key,
                'workflow-step-link--disabled': step.disabled,
              }"
            >
              <small>مرحله {{ step.index }}</small>
              <strong>{{ step.label }}</strong>
              <span>{{ step.description }}</span>
            </RouterLink>
          </nav>
        </section>

        <section class="page-panel workflow-sidebar-card">
          <div>
            <h3>اسنپ‌شات draft</h3>
            <p class="workflow-page__intro">با ساخت draft، همه صفحات بعدی روی همین شناسه کار می‌کنند.</p>
          </div>

          <div v-if="composer.draftProduct" class="workflow-sidebar-meta">
            <div>
              <small>شناسه محصول</small>
              <strong>#{{ composer.draftProduct.id }}</strong>
            </div>
            <div>
              <small>SKU</small>
              <strong>{{ composer.draftProduct.sku }}</strong>
            </div>
            <div>
              <small>Slug</small>
              <strong>{{ composer.draftProduct.slug }}</strong>
            </div>
            <div>
              <small>دسته / تگ / تصویر</small>
              <strong>
                {{ composer.draftProduct.categories?.length || 0 }} / {{ composer.draftProduct.tags?.length || 0 }} /
                {{ composer.images.length }}
              </strong>
            </div>
          </div>

          <div v-else class="workflow-empty">هنوز draft فعالی در این نشست انتخاب نشده است.</div>

          <div class="workflow-actions">
            <BaseButton
              v-if="rememberedDraftId && !composer.hasDraft"
              type="button"
              variant="secondary"
              size="sm"
              @click="resumeRememberedDraft"
            >
              ادامه draft #{{ rememberedDraftId }}
            </BaseButton>
            <BaseButton
              v-if="composer.hasDraft"
              type="button"
              variant="ghost"
              size="sm"
              :disabled="composer.loading.product"
              @click="refreshCurrentDraft"
            >
              بازخوانی از بک‌اند
            </BaseButton>
          </div>
        </section>

        <section v-if="composer.feedbackMessage || composer.feedbackError" class="page-panel workflow-feedback">
          <p v-if="composer.feedbackMessage" class="workflow-feedback__message">{{ composer.feedbackMessage }}</p>
          <p v-if="composer.feedbackError" class="workflow-feedback__error">{{ composer.feedbackError }}</p>
        </section>
      </aside>

      <section class="page-panel">
        <RouterView />
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'
import { useAdminProductComposerStore } from '@/stores/adminProductComposer'
import {
  ADMIN_PRODUCT_WORKFLOW_STEPS,
  getRememberedDraftProductId,
  getWorkflowStep,
  getWorkflowStepIndex,
  toOptionalInteger,
} from '@/utils/adminProductWorkflow'

const route = useRoute()
const router = useRouter()
const composer = useAdminProductComposerStore()

const currentStep = computed(() => getWorkflowStep(route.meta.workflowStep || 'draft'))
const rememberedDraftId = computed(() => getRememberedDraftProductId())

const workflowStats = computed(() => ({
  completed: composer.hasDraft
    ? ADMIN_PRODUCT_WORKFLOW_STEPS.filter((step) => !step.requiresDraft || composer.hasDraft).length
    : 1,
  productStatus: composer.draftProduct?.status || 'draft',
  variantCount: composer.variants.length,
}))

const stepLinks = computed(() =>
  ADMIN_PRODUCT_WORKFLOW_STEPS.map((step) => {
    const index = getWorkflowStepIndex(step.key) + 1
    const hasRouteProduct = Boolean(composer.draftId)
    const disabled = Boolean(step.requiresDraft && !hasRouteProduct)

    return {
      ...step,
      index,
      disabled,
      to:
        step.requiresDraft && hasRouteProduct
          ? { name: step.routeName, params: { productId: String(composer.draftId) } }
          : { name: step.routeName },
    }
  }),
)

async function ensureWorkflowContext() {
  const requestedProductId = toOptionalInteger(route.params.productId)

  if (requestedProductId) {
    try {
      await composer.hydrateWorkflow(requestedProductId, {
        force: composer.draftProduct?.id !== requestedProductId,
      })
    } catch (error) {
      composer.setFeedback('', error.message)
    }
    return
  }

  await composer.ensureReferenceCatalogs()
}

async function refreshCurrentDraft() {
  if (!composer.draftId) {
    return
  }

  try {
    await composer.hydrateWorkflow(composer.draftId, { force: true })
    composer.setFeedback('اسنپ‌شات محصول دوباره بارگذاری شد.', '')
  } catch (error) {
    composer.setFeedback('', error.message)
  }
}

async function resumeRememberedDraft() {
  if (!rememberedDraftId.value) {
    return
  }

  await router.push({
    name: 'admin-product-basics',
    params: { productId: String(rememberedDraftId.value) },
  })
}

watch(
  () => route.fullPath,
  async () => {
    if (route.meta.requiresDraft && !route.params.productId) {
      await router.replace({ name: 'admin-product-draft' })
      return
    }

    await ensureWorkflowContext()
  },
  { immediate: true },
)
</script>
