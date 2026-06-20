<template>
  <div class="w-full">
    <label v-if="label" class="block mb-1.5 text-[0.92rem] font-bold text-text-main">
      {{ label }}
    </label>

    <input
      v-bind="$attrs"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full min-h-[48px] rounded-lg border border-border-light bg-surface-strong text-text-main py-3.5 px-4 outline-none transition-all duration-200 placeholder:text-text-muted focus:border-primary/35 focus:ring-4 focus:ring-primary/10"
    />

    <p v-if="error" class="mt-1.5 text-danger text-[0.82rem]">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: [String, Number],
  label: { type: String, default: '' },
  error: { type: String, default: '' },
})

defineEmits(['update:modelValue'])
</script>
