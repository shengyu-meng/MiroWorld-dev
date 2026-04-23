<template>
  <div class="language-toggle" role="group" aria-label="display language">
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      class="language-button"
      :class="{ active: modelValue === option.value }"
      @click="$emit('update:modelValue', option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
import type { DisplayLanguage } from '@/lib/types'

defineProps<{
  modelValue: DisplayLanguage
}>()

defineEmits<{
  'update:modelValue': [value: DisplayLanguage]
}>()

const options = [
  { value: 'zh', label: '中文' },
  { value: 'en', label: 'EN' },
] as const
</script>
