<template>
  <section class="scene-section" data-testid="intervention-section">
    <div class="mode-list">
      <button
        v-for="mode in inputModes"
        :key="mode"
        type="button"
        class="mode-chip"
        :class="{ active: mode === currentInputType }"
        @click="$emit('update:currentInputType', mode)"
      >
        <span>{{ inputCopy[mode].label }}</span>
        <small>{{ inputCopy[mode].note }}</small>
      </button>
    </div>

    <div class="intervention-layout">
      <div class="branch-focus-list">
        <article v-for="card in branchCards" :key="card.label" class="branch-focus-card">
          <strong>{{ card.label }}</strong>
          <p>{{ card.description }}</p>
          <ul>
            <li v-for="premise in card.premises.slice(0, 2)" :key="premise">{{ premise }}</li>
          </ul>
        </article>

        <article v-if="branchCards.length === 0" class="branch-focus-card muted">
          <p>{{ emptyCopy }}</p>
        </article>
      </div>

      <div class="compose-panel">
        <textarea
          :value="draft"
          class="intervention-input"
          :placeholder="placeholder"
          @input="$emit('update:draft', ($event.target as HTMLTextAreaElement).value)"
        ></textarea>
        <button type="button" class="primary-action" :disabled="isSubmitting" @click="$emit('submit')">
          {{ isSubmitting ? loadingLabel : submitLabel }}
        </button>
      </div>
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
  submitLabel: string
  loadingLabel: string
  emptyCopy: string
  branchCards: Array<{
    label: string
    description: string
    premises: string[]
    signals_for: string[]
    signals_against: string[]
  }>
  inputCopy: Record<InputType, {
    label: string
    note: string
  }>
}>()

defineEmits<{
  'update:currentInputType': [value: InputType]
  'update:draft': [value: string]
  submit: []
}>()
</script>
