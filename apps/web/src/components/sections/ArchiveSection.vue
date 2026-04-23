<template>
  <section class="stage-surface" data-testid="archive-section">
    <div class="surface-heading">
      <span class="surface-kicker">05 / Archive</span>
      <h2>Share, log, and calibrate the afterimage.</h2>
    </div>
    <div class="archive-actions">
      <button type="button" class="primary-action" @click="$emit('share')">Generate Share Text</button>
      <button type="button" class="secondary-action" @click="$emit('toggle-calibration')">
        {{ calibrationOpen ? 'Hide Calibration' : 'Open Calibration' }}
      </button>
    </div>
    <article class="share-card">
      <strong>{{ shareSnapshot.title }}</strong>
      <p>{{ shareSnapshot.summary }}</p>
      <small>{{ shareSnapshot.short_excerpt }}</small>
    </article>
    <div class="archive-log">
      <article v-for="entry in decisionLog" :key="entry.entry_id" class="archive-entry">
        <span>{{ entry.input_type }}</span>
        <strong>{{ entry.event_title }}</strong>
        <p>{{ entry.replay_summary }}</p>
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
        placeholder="What actually happened?"
        @input="$emit('update:calibrationDraft', ($event.target as HTMLTextAreaElement).value)"
      ></textarea>
      <button type="button" class="primary-action" @click="$emit('save-calibration')">Save Calibration</button>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  shareSnapshot: {
    title: string
    summary: string
    short_excerpt: string
  }
  decisionLog: Array<{
    entry_id: string
    input_type: string
    event_title: string
    replay_summary: string
  }>
  calibrationSummary: {
    summary: string
  }
  calibrationOpen: boolean
  calibrationDraft: string
  calibrationResult: string
}>()

defineEmits<{
  share: []
  'toggle-calibration': []
  'update:calibrationDraft': [value: string]
  'update:calibrationResult': [value: string]
  'save-calibration': []
}>()
</script>
