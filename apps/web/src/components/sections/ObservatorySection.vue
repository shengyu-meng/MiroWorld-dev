<template>
  <section class="scene-section" data-testid="observatory-section">
    <div class="event-list observatory-grid">
      <article
        v-for="event in events"
        :key="event.event_id"
        class="event-card"
        :class="{ active: event.event_id === selectedEventId }"
      >
        <button type="button" class="event-header" @click="$emit('select-event', event.event_id)">
          <span>{{ event.stage }}</span>
          <strong>{{ event.title }}</strong>
        </button>

        <p>{{ event.summary }}</p>

        <ul class="event-note-list">
          <li v-for="note in event.evidence_notes.slice(0, 2)" :key="`${event.event_id}-${note}`">{{ note }}</li>
        </ul>

        <div class="event-meta-list">
          <span
            v-for="entity in event.affected_entities.slice(0, 3)"
            :key="`${event.event_id}-${entity}`"
            class="event-meta-pill"
          >
            {{ labels.affected }} / {{ entity }}
          </span>
        </div>

        <div class="branch-list">
          <button
            v-for="branch in event.branches"
            :key="branch.branch_id"
            type="button"
            class="branch-chip"
            :class="{ active: branch.branch_id === selectedBranchId }"
            @click="$emit('select-branch', event.event_id, branch.branch_id)"
          >
            <span>{{ branch.label }}</span>
            <small>{{ branch.visibility === 'primary' ? labels.primary : labels.alternate }}</small>
            <span>{{ Math.round(branch.confidence * 100) }}%</span>
          </button>
        </div>
      </article>
    </div>

    <article v-if="selectedEvent" class="comparison-board">
      <header class="comparison-board-header">
        <div>
          <span class="annotation-label">{{ labels.comparisonBoard }}</span>
          <strong>{{ selectedEvent.title }}</strong>
        </div>
        <p>{{ selectedEvent.summary }}</p>
      </header>

      <div class="comparison-board-grid">
        <button
          v-for="branch in selectedEvent.branches"
          :key="branch.branch_id"
          type="button"
          class="comparison-branch-card"
          :class="{ active: branch.branch_id === selectedBranchId }"
          @click="$emit('select-branch', selectedEvent.event_id, branch.branch_id)"
        >
          <span class="annotation-label">{{ branch.visibility === 'primary' ? labels.primary : labels.alternate }}</span>
          <strong>{{ branch.label }}</strong>
          <small>{{ labels.confidenceLabel }} / {{ formatConfidence(branch.effective_confidence ?? branch.confidence) }}</small>
          <p>{{ branch.description }}</p>
          <small>{{ labels.costHint }} / {{ branch.cost_hint }}</small>
          <small>{{ labels.actionVector }} / {{ branch.player_influence }}</small>
        </button>
      </div>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { KeyEvent } from '@/lib/types'

const props = defineProps<{
  events: KeyEvent[]
  selectedEventId: string
  selectedBranchId: string
  labels: {
    primary: string
    alternate: string
    affected: string
    comparisonBoard: string
    confidenceLabel: string
    costHint: string
    actionVector: string
  }
}>()

defineEmits<{
  'select-event': [eventId: string]
  'select-branch': [eventId: string, branchId: string]
}>()

const selectedEvent = computed(() => props.events.find((event) => event.event_id === props.selectedEventId) ?? props.events[0] ?? null)

function formatConfidence(value: number) {
  return `${Math.round(value * 100)}%`
}
</script>
