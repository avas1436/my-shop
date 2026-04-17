<template>
  <div class="base-input">
    <label v-if="label" class="base-input__label">
      {{ label }}
    </label>

    <input
      v-bind="$attrs"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="base-input__control"
    />

    <p v-if="error" class="base-input__error">
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

<style scoped>
.base-input {
  width: 100%;
}

.base-input__label {
  display: block;
  margin-bottom: 0.45rem;
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--text);
}

.base-input__control {
  width: 100%;
  min-height: 48px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: var(--surface-strong);
  color: var(--text);
  padding: 0.85rem 1rem;
  outline: none;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    transform 0.2s ease;
}

.base-input__control::placeholder {
  color: var(--text-muted);
}

.base-input__control:focus {
  border-color: rgba(91, 61, 245, 0.35);
  box-shadow: 0 0 0 4px rgba(91, 61, 245, 0.12);
}

.base-input__error {
  margin: 0.45rem 0 0;
  color: var(--danger);
  font-size: 0.82rem;
}
</style>
