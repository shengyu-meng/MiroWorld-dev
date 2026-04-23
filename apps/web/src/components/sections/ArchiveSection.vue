<template>
  <section class="scene-section archive-section" data-testid="archive-section">
    <div class="archive-actions">
      <button type="button" class="primary-action" @click="$emit('share')">{{ copy.share }}</button>
      <button type="button" class="secondary-action" @click="$emit('toggle-calibration')">
        {{ calibrationOpen ? copy.hideCalibration : copy.openCalibration }}
      </button>
    </div>

    <div class="archive-grid">
      <div class="archive-main">
        <article class="share-card share-card--hero">
          <span class="annotation-label">{{ copy.curatorNote }}</span>
          <strong>{{ shareSnapshot.title }}</strong>
          <p>{{ shareSnapshot.summary }}</p>
          <small>{{ shareSnapshot.curator_note || shareSnapshot.short_excerpt }}</small>

          <div class="share-tag-row">
            <span v-for="tag in shareSnapshot.tags" :key="tag" class="share-tag">{{ tag }}</span>
          </div>
        </article>

        <div class="share-detail-grid">
          <article class="share-card">
            <span class="annotation-label">{{ copy.wallLabel }}</span>
            <p>{{ shareSnapshot.wall_label }}</p>
          </article>

          <article class="share-card">
            <span class="annotation-label">{{ copy.archiveSummary }}</span>
            <p>{{ shareSnapshot.archive_summary }}</p>
          </article>
        </div>

        <article class="share-card share-text-card">
          <span class="annotation-label">{{ copy.shareText }}</span>
          <p class="share-text-body">{{ shareSnapshot.share_text }}</p>
        </article>
      </div>

      <aside class="archive-side">
        <article class="annotation-block archive-panel">
          <span class="annotation-label">{{ copy.decisionLog }}</span>
          <div class="archive-log">
            <article v-for="entry in decisionLog" :key="entry.entry_id" class="archive-entry">
              <span>{{ entry.input_type }}</span>
              <strong>{{ entry.event_title }}</strong>
              <small>{{ formatTimestamp(entry.created_at) }}</small>
              <p>{{ entry.content }}</p>
              <small>{{ entry.replay_summary }}</small>
              <small v-if="entry.cost_changes.length">{{ entry.cost_changes.join(' · ') }}</small>
            </article>
          </div>
        </article>

        <article class="annotation-block archive-panel">
          <span class="annotation-label">{{ copy.calibrationHistory }}</span>
          <p>{{ calibrationSummary.summary }}</p>
          <div class="calibration-record-list">
            <article v-for="record in calibrationRecords.slice(0, 4)" :key="record.calibration_id" class="calibration-record">
              <strong>{{ record.result }}</strong>
              <small>{{ formatTimestamp(record.created_at) }}</small>
              <p>{{ record.actual_outcome }}</p>
            </article>
            <p v-if="calibrationRecords.length === 0" class="archive-empty">{{ copy.actualOutcomePlaceholder }}</p>
          </div>
        </article>
      </aside>
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
import type { CalibrationRecord, ShareArtifact } from '@/lib/types'

defineProps<{
  shareSnapshot: ShareArtifact
  decisionLog: Array<{
    entry_id: string
    created_at: string
    input_type: string
    event_title: string
    content: string
    replay_summary: string
    cost_changes: string[]
  }>
  calibrationSummary: {
    summary: string
  }
  calibrationRecords: CalibrationRecord[]
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
    shareText: string
    wallLabel: string
    archiveSummary: string
    calibrationHistory: string
  }
}>()

defineEmits<{
  share: []
  'toggle-calibration': []
  'update:calibrationDraft': [value: string]
  'update:calibrationResult': [value: string]
  'save-calibration': []
}>()

function formatTimestamp(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}
</script>
