<template>
  <section class="scene-section" data-testid="cost-section">
    <div class="cost-grid">
      <article v-for="lens in visibleLenses" :key="lens.cost_lens_id" class="cost-card">
        <span class="annotation-label">{{ labels.affectedGroups }}</span>
        <strong>{{ lens.affected_groups.join(' / ') }}</strong>
        <p>{{ lens.first_order_costs.join(' · ') }}</p>
        <small>{{ lens.second_order_costs.join(' · ') }}</small>
        <ul class="cost-note-list">
          <li v-for="note in lens.ethical_notes.slice(0, 2)" :key="note">{{ note }}</li>
        </ul>
      </article>

      <article v-if="visibleLenses.length === 0" class="cost-card muted">
        <p>{{ emptyCopy }}</p>
      </article>

      <article class="cost-card muted passive-floor-card">
        <span class="annotation-label">{{ labels.passiveFloor }}</span>
        <strong>{{ passiveFloor.title }}</strong>
        <p>{{ passiveFloor.summary }}</p>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { CostLens } from '@/lib/types'

const props = defineProps<{
  lenses: CostLens[]
  selectedBranchId: string
  passiveFloor: {
    title: string
    summary: string
  }
  labels: {
    affectedGroups: string
    passiveFloor: string
  }
  emptyCopy: string
}>()

const visibleLenses = computed(() => props.lenses.filter((lens) => lens.target_branch_id === props.selectedBranchId).slice(0, 2))
</script>
