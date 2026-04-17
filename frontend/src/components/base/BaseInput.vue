<template>
  <div class="w-full">
    <label v-if="label" class="block mb-1 text-sm font-medium">
      {{ label }}
    </label>

    <input
      v-bind="$attrs"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500 transition"
    />

    <p v-if="error" class="text-xs text-red-500 mt-1">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: [String, Number],
  label: { type: String, default: '' },
  error: { type: String, default: '' }
})

defineEmits(['update:modelValue'])
</script>
