<!-- src/components/base/BaseInput.vue -->
<template>
  <div class="w-full">
    <label v-if="label" class="block mb-1.5 text-[0.92rem] font-bold text-text-main">
      {{ label }}
    </label>

    <input
      v-bind="$attrs"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full min-h-12 rounded-sm border border-border-light bg-surface-strong text-text-main py-3 px-4 outline-none transition-all duration-200 placeholder:text-text-muted focus:border-primary focus:ring-4 focus:ring-primary/10"
      :class="{ 'border-danger/60 focus:border-danger focus:ring-danger/10': error }"
    />

    <p v-if="error" class="mt-1.5 text-danger text-[0.82rem] font-medium">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: [String, Number], default: '' },
  label: { type: String, default: '' },
  error: { type: String, default: '' },
})

defineEmits(['update:modelValue'])
</script>

<!-- روش استفاده -->
<!--  
 <BaseInput
          v-model="formData.email"
          label="آدرس ایمیل"
          type="email"
          placeholder="example@mail.com"
          :error="errors.email"
        />
-->
