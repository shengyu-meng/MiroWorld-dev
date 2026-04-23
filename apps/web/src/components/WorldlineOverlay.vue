<template>
  <section class="worldline-overlay" data-testid="worldline-overlay">
    <header class="worldline-overlay-header">
      <div>
        <span class="annotation-label">{{ branchFieldLabel }}</span>
        <strong>{{ event.title }}</strong>
      </div>
      <p>{{ branchFieldNote }}</p>
    </header>

    <div class="worldline-overlay-field">
      <div class="worldline-knot"></div>

      <div
        v-for="node in branchNodes"
        :key="`${node.branch.branch_id}-connector`"
        class="worldline-connector"
        :style="node.connectorStyle"
      ></div>

      <button
        v-for="node in branchNodes"
        :key="node.branch.branch_id"
        type="button"
        class="overlay-branch-card"
        :class="{ active: node.branch.branch_id === selectedBranchId }"
        :style="node.positionStyle"
        @click="$emit('select-branch', node.branch.branch_id)"
      >
        <span class="annotation-label">{{ node.branch.visibility === 'primary' ? labels.primary : labels.alternate }}</span>
        <strong>{{ node.branch.label }}</strong>
        <small>{{ confidenceLabel }} / {{ formatConfidence(node.branch.effective_confidence ?? node.branch.confidence) }}</small>
        <p>{{ node.branch.cost_hint }}</p>
        <small>{{ labels.actionVector }} / {{ node.branch.player_influence }}</small>
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { KeyEvent } from '@/lib/types'

const props = defineProps<{
  event: KeyEvent
  selectedBranchId: string
  confidenceLabel: string
  branchFieldLabel: string
  branchFieldNote: string
  labels: {
    primary: string
    alternate: string
    actionVector: string
  }
}>()

defineEmits<{
  'select-branch': [branchId: string]
}>()

const knot = {
  x: 14,
  y: 52,
}

const branchNodes = computed(() => {
  const visibleBranches = props.event.branches.slice(0, 4)

  return visibleBranches.map((branch, index) => {
    const count = visibleBranches.length
    const x = count === 1 ? 68 : 40 + (index * 42) / Math.max(count - 1, 1)
    const confidence = branch.effective_confidence ?? branch.confidence
    const visibilityOffset = branch.visibility === 'primary' ? -4 : 4
    const y = Math.max(18, Math.min(78, 72 - confidence * 42 + visibilityOffset))
    const dx = x - knot.x
    const dy = y - knot.y
    const distance = Math.sqrt((dx ** 2) + (dy ** 2))
    const angle = Math.atan2(dy, dx)

    return {
      branch,
      positionStyle: {
        left: `${x}%`,
        top: `${y}%`,
      },
      connectorStyle: {
        left: `${knot.x}%`,
        top: `${knot.y}%`,
        width: `${distance}%`,
        transform: `rotate(${angle}rad)`,
      },
    }
  })
})

function formatConfidence(value: number) {
  return `${Math.round(value * 100)}%`
}
</script>
