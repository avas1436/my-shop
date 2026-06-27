<!-- src/components/layout.MiniCart.vue -->
<template>
  <Teleport to="body">
    <div v-if="ui.miniCart" class="fixed inset-0 z-70">
      <button
        class="absolute inset-0 w-full h-full border-0 bg-slate-900/40 backdrop-blur-xs cursor-default"
        type="button"
        @click="ui.closeMiniCart()"
      ></button>

      <aside
        class="absolute top-0 right-0 w-[min(420px,100%)] h-full p-5 bg-white/95 border-l border-border-light shadow-(--shadow-custom) grid grid-rows-[auto_1fr_auto] gap-4"
      >
        <div class="flex items-center justify-between gap-3">
          <div>
            <h2 class="m-0 font-bold">سبد خرید شما</h2>
            <p class="m-0 text-text-muted text-[0.88rem] mt-1">
              {{ cart.count }} کالا انتخاب شده است
            </p>
          </div>
          <button
            type="button"
            class="border border-border-light bg-transparent w-10.5 h-10.5 rounded-xl flex items-center justify-center hover:bg-bg-muted transition-colors"
            @click="ui.closeMiniCart()"
          >
            ✕
          </button>
        </div>

        <div
          v-if="cart.items.length === 0"
          class="flex items-center justify-center text-text-muted"
        >
          هنوز محصولی به سبد خرید اضافه نشده است.
        </div>

        <div v-else class="grid gap-4 overflow-y-auto pr-1">
          <article
            v-for="item in cart.items"
            :key="item.id"
            class="grid grid-cols-[84px_1fr_auto] gap-3.5 items-center p-3.5 rounded-[20px] bg-bg-muted"
          >
            <img :src="item.image" :alt="item.title" class="w-21 h-21 object-cover rounded-md" />

            <div class="grid gap-1.5">
              <strong class="text-[0.95rem] line-clamp-1">{{ item.title }}</strong>
              <span class="text-text-muted text-xs">{{ item.badge }}</span>
              <div class="flex items-center justify-between gap-3 mt-1">
                <span class="font-bold text-primary">{{ formatPrice(item.price) }}</span>
                <div
                  class="inline-flex items-center gap-2 border border-border-light rounded-full bg-surface-strong p-1"
                >
                  <button
                    type="button"
                    class="w-7 h-7 flex items-center justify-center border-0 rounded-full bg-bg-muted hover:bg-border-light transition-colors"
                    @click="cart.increase(item.id)"
                  >
                    +
                  </button>
                  <span class="text-sm font-bold w-4 text-center">{{ item.qty }}</span>
                  <button
                    type="button"
                    class="w-7 h-7 flex items-center justify-center border-0 rounded-full bg-bg-muted hover:bg-border-light transition-colors"
                    @click="cart.decrease(item.id)"
                  >
                    −
                  </button>
                </div>
              </div>
            </div>

            <button
              type="button"
              class="border-0 bg-transparent text-danger p-2 hover:bg-danger/10 rounded-lg transition-colors"
              @click="cart.remove(item.id)"
            >
              حذف
            </button>
          </article>
        </div>

        <div class="grid gap-3.5 pt-4 border-t border-border-light">
          <div class="flex items-center justify-between">
            <span class="text-text-muted">مبلغ قابل پرداخت</span>
            <strong class="text-lg">{{ formatPrice(cart.total) }}</strong>
          </div>

          <router-link
            to="/cart"
            class="inline-flex items-center justify-center min-h-13 rounded-md bg-linear-to-br from-primary to-primary-dark text-white font-bold shadow-(--shadow-custom) hover:-translate-y-0.5 transition-transform"
            @click="ui.closeMiniCart()"
          >
            مشاهده سبد و ادامه خرید
          </router-link>
        </div>
      </aside>
    </div>
  </Teleport>
</template>

<script setup>
import { useCartStore } from '@/stores/cartStore'
import { useUIStore } from '@/stores/uiStore'
import { formatPrice } from '@/utils/format'

const cart = useCartStore()
const ui = useUIStore()
</script>
