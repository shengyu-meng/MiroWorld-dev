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

    <div class="ripple-path-archive-card" data-testid="ripple-path-archive">
      <header class="ripple-track-header">
        <div>
          <span class="annotation-label">{{ copy.pathArchive }}</span>
          <p class="surface-callout">{{ copy.pathArchiveNote }}</p>
        </div>
      </header>

      <div class="ripple-path-grid">
        <article v-for="path in pathVariants" :key="path.key" class="ripple-path-column">
          <span class="annotation-label">{{ path.label }}</span>
          <div class="ripple-path-stack">
            <button
              v-for="node in path.nodes"
              :key="`${path.key}-${node.event.event_id}`"
              type="button"
              class="ripple-path-node"
              :class="{ active: node.event.event_id === selectedEventId && node.branch.branch_id === selectedBranchId }"
              :data-testid="`ripple-path-node-${path.key}-${node.event.event_id}`"
              @click="$emit('select-branch', node.event.event_id, node.branch.branch_id)"
            >
              <small>{{ node.event.stage }}</small>
              <strong>{{ node.event.title }}</strong>
              <span>{{ node.branch.label }}</span>
              <small>{{ confidenceLabel }} / {{ formatConfidence(node.branch.effective_confidence ?? node.branch.confidence) }}</small>
              <p>{{ node.branch.cost_hint || node.branch.description }}</p>
            </button>
          </div>
        </article>
      </div>
    </div>

    <div class="ripple-replay-set-card" data-testid="ripple-replay-set-library">
      <header class="ripple-track-header">
        <div>
          <span class="annotation-label">{{ copy.replaySetLibrary }}</span>
          <p class="surface-callout">{{ copy.replaySetLibraryNote }}</p>
        </div>
      </header>

      <div class="ripple-replay-set-grid">
        <button
          v-for="set in replaySets"
          :key="set.key"
          type="button"
          class="ripple-replay-set-entry"
          :class="{ active: set.key === selectedReplaySetKey }"
          :data-testid="`replay-set-${set.key}`"
          @click="selectedReplaySetKey = set.key"
        >
          <div class="ripple-replay-set-header">
            <span class="annotation-label">{{ set.label }}</span>
            <small>{{ set.eventCount }} {{ copy.eventCount }}</small>
          </div>

          <p>{{ set.note }}</p>

          <div class="ripple-replay-set-meta">
            <span class="event-meta-pill">{{ copy.setConfidence }} / {{ formatConfidence(set.averageConfidence) }}</span>
            <span class="event-meta-pill">{{ copy.setPressure }} / {{ set.averagePressure }}</span>
            <span class="event-meta-pill">{{ copy.setAlternateCount }} / {{ set.alternateCount }}</span>
          </div>
        </button>
      </div>
    </div>

    <div class="ripple-history-archive-card" data-testid="ripple-replay-history">
      <header class="ripple-track-header">
        <div>
          <span class="annotation-label">{{ copy.replayHistory }}</span>
          <p class="surface-callout">{{ copy.replayHistoryNote }}</p>
        </div>
      </header>

      <div class="ripple-history-stack">
        <button
          v-for="entry in historyEntries"
          :key="entry.key"
          type="button"
          class="ripple-history-entry"
          :class="{ active: entry.event.event_id === selectedEventId && entry.branch.branch_id === selectedBranchId }"
          :data-testid="`ripple-history-entry-${entry.mode}-${entry.event.event_id}`"
          @click="$emit('select-branch', entry.event.event_id, entry.branch.branch_id)"
        >
          <div class="ripple-history-header">
            <small>{{ entry.index }}</small>
            <span>{{ confidenceLabel }} / {{ formatConfidence(entry.confidence) }}</span>
          </div>

          <div class="ripple-history-copy">
            <strong>{{ entry.event.title }}</strong>
            <p>{{ entry.branch.description || entry.event.summary || entry.branch.cost_hint }}</p>
          </div>

          <div class="ripple-history-meta">
            <span class="event-meta-pill">{{ entry.event.stage }}</span>
            <span class="event-meta-pill">{{ entry.branch.label }}</span>
            <span class="event-meta-pill">{{ copy.counterSignalDensity }} / {{ entry.counterSignalCount }}</span>
          </div>

          <div class="ripple-history-sections">
            <div class="ripple-history-section">
              <span class="annotation-label">{{ copy.upstreamTension }}</span>
              <strong>{{ entry.upstream.title }}</strong>
              <p>{{ entry.upstream.summary }}</p>
            </div>

            <div class="ripple-history-section">
              <span class="annotation-label">{{ copy.hingeBranch }}</span>
              <strong>{{ entry.branch.label }}</strong>
              <p>{{ entry.branch.cost_hint || entry.branch.description }}</p>
            </div>

            <div class="ripple-history-section">
              <span class="annotation-label">{{ copy.downstreamDrift }}</span>
              <strong>{{ entry.downstream.title }}</strong>
              <p>{{ entry.downstream.summary }}</p>
            </div>
          </div>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

import type { KeyEvent } from '@/lib/types'

interface WorldlineTrackNode {
  event_id: string
  title: string
  stage: string
  primary_branch_id: string
  primary_branch_label: string
  confidence: number
}

type HistoryMode = 'active' | 'primary' | 'alternate'
type ReplaySetKey = 'current' | 'stabilizing' | 'pressure'

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
    pathArchive: string
    pathArchiveNote: string
    activePath: string
    primaryPath: string
    alternateDrift: string
    replayHistory: string
    replayHistoryNote: string
    upstreamTension: string
    hingeBranch: string
    downstreamDrift: string
    archiveOrigin: string
    archiveOriginNote: string
    archiveOpenEnd: string
    archiveOpenEndNote: string
    counterSignalDensity: string
    replaySetLibrary: string
    replaySetLibraryNote: string
    currentSet: string
    currentSetNote: string
    stabilizingSet: string
    stabilizingSetNote: string
    pressureSet: string
    pressureSetNote: string
    eventCount: string
    setConfidence: string
    setPressure: string
    setAlternateCount: string
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

const pathVariants = computed<Array<{
  key: HistoryMode
  label: string
  nodes: Array<{
    event: KeyEvent
    branch: KeyEvent['branches'][number]
  }>
}>>(() => {
  const selectedEventBranch = props.events
    .find((event) => event.event_id === props.selectedEventId)
    ?.branches.find((branch) => branch.branch_id === props.selectedBranchId)

  return [
    {
      key: 'active',
      label: props.copy.activePath,
      nodes: props.events.map((event) => ({
        event,
        branch: event.event_id === props.selectedEventId
          ? selectedEventBranch ?? pickPrimaryBranch(event)
          : pickPrimaryBranch(event),
      })),
    },
    {
      key: 'primary',
      label: props.copy.primaryPath,
      nodes: props.events.map((event) => ({
        event,
        branch: pickPrimaryBranch(event),
      })),
    },
    {
      key: 'alternate',
      label: props.copy.alternateDrift,
      nodes: props.events.map((event) => ({
        event,
        branch: pickAlternateBranch(event),
      })),
    },
  ]
})

const selectedReplaySetKey = ref<ReplaySetKey>('current')

const replaySets = computed<Array<{
  key: ReplaySetKey
  label: string
  note: string
  eventCount: number
  averageConfidence: number
  averagePressure: number
  alternateCount: number
  nodes: Array<{
    event: KeyEvent
    branch: KeyEvent['branches'][number]
  }>
}>>(() => {
  const currentPath = pathVariants.value.find((path) => path.key === 'active')?.nodes ?? []
  const stabilizingNodes = props.events.map((event) => ({
    event,
    branch: pickStabilizingBranch(event),
  }))
  const pressureNodes = props.events.map((event) => ({
    event,
    branch: pickPressureBranch(event),
  }))

  return [
    buildReplaySet(
      'current',
      props.copy.currentSet,
      props.copy.currentSetNote,
      currentPath,
    ),
    buildReplaySet(
      'stabilizing',
      props.copy.stabilizingSet,
      props.copy.stabilizingSetNote,
      stabilizingNodes,
    ),
    buildReplaySet(
      'pressure',
      props.copy.pressureSet,
      props.copy.pressureSetNote,
      pressureNodes,
    ),
  ]
})

const historyEntries = computed(() => {
  const activePath = replaySets.value.find((set) => set.key === selectedReplaySetKey.value)
    ?? replaySets.value[0]

  return activePath.nodes.map((node, index) => {
    const upstreamNode = activePath.nodes[index - 1]
    const downstreamNode = activePath.nodes[index + 1]
    const confidence = node.branch.effective_confidence ?? node.branch.confidence

    return {
      key: `${activePath.key}-${node.event.event_id}`,
      mode: activePath.key,
      index: `ARCHIVE ${String(index + 1).padStart(2, '0')}`,
      event: node.event,
      branch: node.branch,
      confidence,
      counterSignalCount: node.branch.signals_against.length,
      upstream: upstreamNode
        ? {
            title: `${upstreamNode.event.title} / ${upstreamNode.branch.label}`,
            summary: upstreamNode.branch.cost_hint || upstreamNode.event.summary || upstreamNode.branch.description,
          }
        : {
            title: props.copy.archiveOrigin,
            summary: props.copy.archiveOriginNote,
          },
      downstream: downstreamNode
        ? {
            title: `${downstreamNode.event.title} / ${downstreamNode.branch.label}`,
            summary: downstreamNode.branch.cost_hint || downstreamNode.event.summary || downstreamNode.branch.description,
          }
        : {
            title: props.copy.archiveOpenEnd,
            summary: props.copy.archiveOpenEndNote,
          },
    }
  })
})

watch(
  () => [props.selectedEventId, props.selectedBranchId],
  () => {
    selectedReplaySetKey.value = replaySets.value.some((set) => set.key === selectedReplaySetKey.value)
      ? selectedReplaySetKey.value
      : 'current'
  },
)

function formatConfidence(value: number) {
  return `${Math.round(value * 100)}%`
}

function pickPrimaryBranch(event: KeyEvent) {
  return event.branches.find((branch) => branch.visibility === 'primary')
    ?? event.branches[0]
}

function pickAlternateBranch(event: KeyEvent) {
  return event.branches.find((branch) => branch.visibility === 'alternate')
    ?? pickPrimaryBranch(event)
}

function pickStabilizingBranch(event: KeyEvent) {
  return [...event.branches].sort((left, right) => (
    (right.effective_confidence ?? right.confidence) - (left.effective_confidence ?? left.confidence)
  ))[0] ?? pickPrimaryBranch(event)
}

function pickPressureBranch(event: KeyEvent) {
  return [...event.branches].sort((left, right) => (
    branchPressure(right) - branchPressure(left)
  ))[0] ?? pickAlternateBranch(event)
}

function branchPressure(branch: KeyEvent['branches'][number]) {
  const confidence = branch.effective_confidence ?? branch.confidence
  return branch.signals_against.length * 2
    + (branch.cost_hint ? 1 : 0)
    + (branch.visibility === 'alternate' ? 0.5 : 0)
    + (1 - confidence)
}

function buildReplaySet(
  key: ReplaySetKey,
  label: string,
  note: string,
  nodes: Array<{ event: KeyEvent, branch: KeyEvent['branches'][number] }>,
) {
  const eventCount = nodes.length
  const totalConfidence = nodes.reduce((sum, node) => (
    sum + (node.branch.effective_confidence ?? node.branch.confidence)
  ), 0)
  const totalPressure = nodes.reduce((sum, node) => sum + branchPressure(node.branch), 0)
  const alternateCount = nodes.filter((node) => node.branch.visibility === 'alternate').length

  return {
    key,
    label,
    note,
    eventCount,
    averageConfidence: eventCount ? totalConfidence / eventCount : 0,
    averagePressure: Math.round(eventCount ? (totalPressure / eventCount) * 10 : 0) / 10,
    alternateCount,
    nodes,
  }
}
</script>
