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
        <article class="poster-artifact-card">
          <span class="annotation-label">{{ copy.posterArtifact }}</span>
          <div class="poster-artifact-shell">
            <div class="poster-artifact-body">
              <p class="poster-artifact-brand">MIROWORLD</p>
              <h3>{{ shareSnapshot.title }}</h3>
              <p class="poster-artifact-summary">{{ shareSnapshot.summary }}</p>
              <p class="poster-artifact-caption">{{ shareSnapshot.poster_caption }}</p>

              <div class="share-tag-row">
                <span v-for="tag in shareSnapshot.tags" :key="tag" class="share-tag">{{ tag }}</span>
              </div>
            </div>

            <aside class="poster-artifact-side">
              <span class="annotation-label">{{ copy.wallLabel }}</span>
              <p>{{ shareSnapshot.wall_label }}</p>
              <span class="annotation-label">{{ copy.curatorNote }}</span>
              <p>{{ shareSnapshot.curator_note || shareSnapshot.short_excerpt }}</p>
            </aside>
          </div>
        </article>

        <div class="share-detail-grid">
          <article class="share-card export-card">
            <span class="annotation-label">{{ copy.posterCaption }}</span>
            <p>{{ shareSnapshot.poster_caption }}</p>
            <button type="button" class="ghost-action" @click="copyText(copy.copyPosterCaption, shareSnapshot.poster_caption)">
              {{ copy.copyPosterCaption }}
            </button>
          </article>

          <article class="share-card export-card">
            <span class="annotation-label">{{ copy.shortExcerpt }}</span>
            <p>{{ shareSnapshot.short_excerpt }}</p>
            <button type="button" class="ghost-action" @click="copyText(copy.copyWallLabel, shareSnapshot.wall_label)">
              {{ copy.copyWallLabel }}
            </button>
          </article>

          <article class="share-card export-card">
            <span class="annotation-label">{{ copy.archiveSummary }}</span>
            <p>{{ shareSnapshot.archive_summary }}</p>
          </article>
        </div>

        <article class="share-card share-text-card">
          <div class="share-card-header">
            <span class="annotation-label">{{ copy.shareText }}</span>
            <button type="button" class="ghost-action" @click="copyText(copy.copyShareText, shareSnapshot.share_text)">
              {{ copy.copyShareText }}
            </button>
          </div>
          <p class="share-text-body">{{ shareSnapshot.share_text }}</p>
          <small v-if="copyFeedback" class="copy-feedback">{{ copyFeedback }}</small>
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
              <small v-if="entry.cost_changes.length">{{ entry.cost_changes.join(' / ') }}</small>
            </article>
          </div>
        </article>

        <article class="annotation-block archive-panel">
          <span class="annotation-label">{{ copy.calibrationPattern }}</span>
          <div class="calibration-meter">
            <div
              v-for="segment in calibrationSegments"
              :key="segment.key"
              class="calibration-meter-segment"
              :class="`result-${segment.key}`"
              :style="{ flexGrow: segment.count || 1 }"
            >
              <span>{{ segment.label }}</span>
              <strong>{{ segment.count }}</strong>
            </div>
          </div>
          <div class="calibration-pattern-row">
            <span
              v-for="record in calibrationRecords.slice(0, 12)"
              :key="record.calibration_id"
              class="calibration-pattern-dot"
              :class="`result-${record.result}`"
              :title="`${mapResultLabel(record.result)} / ${record.actual_outcome}`"
            ></span>
          </div>
          <p>{{ calibrationSummary.summary }}</p>
        </article>

        <article class="annotation-block archive-panel">
          <span class="annotation-label">{{ copy.calibrationHistory }}</span>
          <div class="calibration-record-list">
            <article v-for="record in calibrationRecords.slice(0, 4)" :key="record.calibration_id" class="calibration-record">
              <strong>{{ mapResultLabel(record.result) }}</strong>
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
import { computed, ref } from 'vue'

import type { CalibrationRecord, ShareArtifact } from '@/lib/types'

const props = defineProps<{
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
    posterArtifact: string
    posterCaption: string
    shortExcerpt: string
    copyWallLabel: string
    copyPosterCaption: string
    copyShareText: string
    calibrationPattern: string
    hit: string
    partial: string
    miss: string
    insufficient_data: string
  }
}>()

defineEmits<{
  share: []
  'toggle-calibration': []
  'update:calibrationDraft': [value: string]
  'update:calibrationResult': [value: string]
  'save-calibration': []
}>()

const copyFeedback = ref('')

const calibrationSegments = computed(() => {
  const counts = {
    hit: 0,
    partial: 0,
    miss: 0,
    insufficient_data: 0,
  }

  for (const record of props.calibrationRecords) {
    counts[record.result] += 1
  }

  return [
    { key: 'hit', count: counts.hit, label: props.copy.hit },
    { key: 'partial', count: counts.partial, label: props.copy.partial },
    { key: 'miss', count: counts.miss, label: props.copy.miss },
    { key: 'insufficient_data', count: counts.insufficient_data, label: props.copy.insufficient_data },
  ] as const
})

async function copyText(label: string, text: string) {
  copyFeedback.value = ''
  if (!navigator.clipboard) return
  try {
    await navigator.clipboard.writeText(text)
    copyFeedback.value = label
  } catch {
    copyFeedback.value = ''
  }
}

function formatTimestamp(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}

function mapResultLabel(result: CalibrationRecord['result']) {
  return props.copy[result]
}
</script>
