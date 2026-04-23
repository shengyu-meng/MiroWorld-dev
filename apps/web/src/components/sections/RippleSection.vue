<template>
  <section class="scene-section ripple-section" data-testid="ripple-section">
    <article class="ripple-callout-card">
      <span class="annotation-label">{{ copy.latestBendLabel }}</span>
      <p class="surface-callout">{{ latestBend || emptyCopy }}</p>
    </article>

    <div class="ripple-atlas-grid">
      <article class="ripple-continuity-card" data-testid="ripple-continuity-explorer">
        <header class="ripple-track-header">
          <div>
            <span class="annotation-label">{{ copy.continuityAtlas }}</span>
            <p class="surface-callout">{{ copy.continuityNote }}</p>
          </div>
        </header>

        <div class="ripple-event-rail">
          <button
            v-for="node in continuityNodes"
            :key="node.event.event_id"
            type="button"
            class="ripple-event-node"
            :class="{ active: node.event.event_id === selectedEventId }"
            :data-testid="`ripple-event-node-${node.event.event_id}`"
            @click="$emit('select-event', node.event.event_id)"
          >
            <span>{{ node.track.stage }}</span>
            <strong>{{ node.event.title }}</strong>
            <small>{{ confidenceLabel }} / {{ formatConfidence(node.track.confidence) }}</small>
            <p>{{ node.rippleSummary }}</p>
          </button>
        </div>
      </article>

      <article v-if="selectedEvent" class="ripple-focus-card" data-testid="ripple-focus-card">
        <span class="annotation-label">{{ copy.focusEvent }}</span>
        <strong>{{ selectedEvent.title }}</strong>
        <p>{{ selectedEvent.summary }}</p>

        <div class="event-meta-list">
          <span class="event-meta-pill">{{ selectedEvent.stage }}</span>
          <span class="event-meta-pill">{{ copy.branchSpread }} / {{ selectedEvent.branches.length }}</span>
          <span class="event-meta-pill">{{ copy.evidenceDensity }} / {{ selectedEvent.evidence_notes.length }}</span>
        </div>

        <div class="ripple-branch-focus">
          <button
            v-for="branch in selectedEvent.branches.slice(0, 4)"
            :key="branch.branch_id"
            type="button"
            class="branch-chip ripple-branch-chip"
            :class="{ active: branch.branch_id === selectedBranchId }"
            @click="$emit('select-branch', selectedEvent.event_id, branch.branch_id)"
          >
            <span class="annotation-label">{{ branch.visibility === 'primary' ? labels.primary : labels.alternate }}</span>
            <strong>{{ branch.label }}</strong>
            <small>{{ confidenceLabel }} / {{ formatConfidence(branch.effective_confidence ?? branch.confidence) }}</small>
            <small>{{ labels.actionVector }} / {{ branch.player_influence }}</small>
          </button>
        </div>
      </article>
    </div>

    <div class="ripple-track-card">
      <header class="ripple-track-header">
        <span class="annotation-label">{{ copy.rippleTrack }}</span>
      </header>
      <div class="ripple-track-list">
        <article
          v-for="(node, index) in continuityNodes"
          :key="`${node.event.event_id}-${node.branchLabel}`"
          class="ripple-track-node"
        >
          <span class="ripple-track-index">{{ String(index + 1).padStart(2, '0') }}</span>
          <div class="ripple-track-copy">
            <small>{{ node.track.stage }} / {{ node.branchLabel }}</small>
            <strong>{{ node.event.title }}</strong>
            <p>{{ node.rippleSummary }}</p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { KeyEvent } from '@/lib/types'

interface WorldlineTrackNode {
  event_id: string
  title: string
  stage: string
  primary_branch_id: string
  primary_branch_label: string
  confidence: number
}

const props = defineProps<{
  latestBend: string
  emptyCopy: string
  events: KeyEvent[]
  worldlineTrack: WorldlineTrackNode[]
  selectedEventId: string
  selectedBranchId: string
  rippleCards: Array<{
    title: string
    summary: string
    branch_label: string
  }>
  labels: {
    primary: string
    alternate: string
    actionVector: string
  }
  confidenceLabel: string
  copy: {
    rippleTrack: string
    latestBendLabel: string
    continuityAtlas: string
    continuityNote: string
    focusEvent: string
    branchSpread: string
    evidenceDensity: string
  }
}>()

defineEmits<{
  'select-event': [eventId: string]
  'select-branch': [eventId: string, branchId: string]
}>()

const continuityNodes = computed(() => {
  const trackSource = props.worldlineTrack.length
    ? props.worldlineTrack
    : props.events.map((event) => ({
        event_id: event.event_id,
        title: event.title,
        stage: event.stage,
        primary_branch_id: event.branches[0]?.branch_id ?? '',
        primary_branch_label: event.branches[0]?.label ?? '',
        confidence: event.branches[0]?.effective_confidence ?? event.branches[0]?.confidence ?? 0,
      }))

  return trackSource
    .map((track, index) => {
      const event = props.events.find((candidate) => candidate.event_id === track.event_id)
      if (!event) return null

        return {
          track,
          event,
          branchLabel: props.rippleCards[index]?.branch_label ?? track.primary_branch_label,
          rippleSummary: props.rippleCards[index]?.summary ?? event.summary ?? props.latestBend ?? props.emptyCopy,
        }
      })
    .filter((node): node is {
      track: WorldlineTrackNode
      event: KeyEvent
      branchLabel: string
      rippleSummary: string
    } => Boolean(node))
})

const selectedEvent = computed(() => (
  continuityNodes.value.find((node) => node.event.event_id === props.selectedEventId)?.event
  ?? continuityNodes.value[0]?.event
  ?? null
))

function formatConfidence(value: number) {
  return `${Math.round(value * 100)}%`
}
</script>
