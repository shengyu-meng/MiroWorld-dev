<template>
  <section class="stage-surface" data-testid="cost-section">
    <div class="surface-heading">
      <span class="surface-kicker">03 / Cost Lens</span>
      <h2>See who absorbs the pressure.</h2>
    </div>
    <div class="cost-grid">
      <article v-for="lens in visibleLenses" :key="lens.cost_lens_id" class="cost-card">
        <strong>{{ lens.affected_groups.join(' / ') }}</strong>
        <p>{{ lens.first_order_costs[0] }}</p>
        <small>{{ lens.second_order_costs[0] }}</small>
      </article>
      <article class="cost-card muted">
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
}>()

const visibleLenses = computed(() => props.lenses.filter((lens) => lens.target_branch_id === props.selectedBranchId).slice(0, 2))
</script>
