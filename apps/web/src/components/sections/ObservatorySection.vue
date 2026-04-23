<template>
  <section class="stage-surface" data-testid="observatory-section">
    <div class="surface-heading">
      <span class="surface-kicker">01 / Observatory</span>
      <h2>Read the knot before you touch it.</h2>
    </div>
    <div class="event-list">
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
}>()

defineEmits<{
  'select-event': [eventId: string]
  'select-branch': [eventId: string, branchId: string]
}>()
</script>
