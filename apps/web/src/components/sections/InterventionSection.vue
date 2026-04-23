<template>
  <section class="stage-surface" data-testid="intervention-section">
    <div class="surface-heading">
      <span class="surface-kicker">02 / Intervention</span>
      <h2>Intervene with declared intent.</h2>
    </div>
    <div class="intervention-layout">
      <div class="mode-list">
        <button
          v-for="mode in inputModes"
          :key="mode"
          type="button"
          class="mode-chip"
          :class="{ active: mode === currentInputType }"
          @click="$emit('update:currentInputType', mode)"
        >
          {{ mode }}
        </button>
      </div>
      <textarea
        :value="draft"
        class="intervention-input"
        :placeholder="placeholder"
        @input="$emit('update:draft', ($event.target as HTMLTextAreaElement).value)"
      ></textarea>
      <button type="button" class="primary-action" :disabled="isSubmitting" @click="$emit('submit')">
        {{ isSubmitting ? 'Bending…' : 'Run Replay' }}
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { InputType } from '@/lib/types'

defineProps<{
  inputModes: InputType[]
  currentInputType: InputType
  draft: string
  isSubmitting: boolean
  placeholder: string
}>()

defineEmits<{
  'update:currentInputType': [value: InputType]
  'update:draft': [value: string]
  submit: []
}>()
</script>
