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

        <div class="event-meta-list">
          <span
            v-for="entity in event.affected_entities.slice(0, 3)"
            :key="`${event.event_id}-${entity}`"
            class="event-meta-pill"
          >
            {{ labels.affected }} · {{ entity }}
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
  </section>
</template>

<script setup lang="ts">
import type { KeyEvent } from '@/lib/types'

defineProps<{
  events: KeyEvent[]
  selectedEventId: string
  selectedBranchId: string
  labels: {
    primary: string
    alternate: string
    affected: string
  }
}>()

defineEmits<{
  'select-event': [eventId: string]
  'select-branch': [eventId: string, branchId: string]
}>()
</script>
