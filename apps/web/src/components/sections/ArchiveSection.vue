<template>
  <section class="scene-section" data-testid="archive-section">
    <div class="archive-actions">
      <button type="button" class="primary-action" @click="$emit('share')">{{ copy.share }}</button>
      <button type="button" class="secondary-action" @click="$emit('toggle-calibration')">
        {{ calibrationOpen ? copy.hideCalibration : copy.openCalibration }}
      </button>
    </div>

    <article class="share-card">
      <span class="annotation-label">{{ copy.curatorNote }}</span>
      <strong>{{ shareSnapshot.title }}</strong>
      <p>{{ shareSnapshot.summary }}</p>
      <small>{{ shareSnapshot.curator_note || shareSnapshot.short_excerpt }}</small>
    </article>

    <div class="archive-log">
      <article v-for="entry in decisionLog" :key="entry.entry_id" class="archive-entry">
        <span>{{ entry.input_type }}</span>
        <strong>{{ entry.event_title }}</strong>
        <p>{{ entry.replay_summary }}</p>
        <small v-if="entry.cost_changes.length">{{ entry.cost_changes.join(' · ') }}</small>
      </article>
    </div>

    <div v-if="calibrationOpen" class="calibration-drawer" data-testid="calibration-drawer">
      <p>{{ calibrationSummary.summary }}</p>
      <select :value="calibrationResult" class="calibration-field" @change="$emit('update:calibrationResult', ($event.target as HTMLSelectElement).value)">
        <option value="hit">hit</option>
        <option value="partial">partial</option>
        <option value="miss">miss</option>
        <option value="insufficient_data">insufficient_data</option>
      </select>
      <textarea
        :value="calibrationDraft"
        class="intervention-input"
        :placeholder="copy.actualOutcomePlaceholder"
        @input="$emit('update:calibrationDraft', ($event.target as HTMLTextAreaElement).value)"
      ></textarea>
      <button type="button" class="primary-action" @click="$emit('save-calibration')">{{ copy.saveCalibration }}</button>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { ShareArtifact } from '@/lib/types'

defineProps<{
  shareSnapshot: ShareArtifact
  decisionLog: Array<{
    entry_id: string
    input_type: string
    event_title: string
    replay_summary: string
    cost_changes: string[]
  }>
  calibrationSummary: {
    summary: string
  }
  calibrationOpen: boolean
  calibrationDraft: string
  calibrationResult: string
  copy: {
    share: string
    openCalibration: string
    hideCalibration: string
    saveCalibration: string
    actualOutcomePlaceholder: string
    decisionLog: string
    curatorNote: string
  }
}>()

defineEmits<{
  share: []
  'toggle-calibration': []
  'update:calibrationDraft': [value: string]
  'update:calibrationResult': [value: string]
  'save-calibration': []
}>()
</script>
