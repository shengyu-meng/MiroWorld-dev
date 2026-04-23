<template>
  <div class="fixture-grid" data-testid="fixture-grid">
    <button
      v-for="fixture in fixtures"
      :key="fixture.fixture_id"
      type="button"
      class="fixture-card"
      :class="{ active: fixture.fixture_id === selectedFixtureId }"
      @click="$emit('select', fixture.fixture_id)"
    >
      <span class="fixture-id">{{ fixture.fixture_id }}</span>
      <strong>{{ fixture.purpose }}</strong>
      <span class="fixture-caption">{{ language === 'zh' ? '策展基线' : 'Curated baseline' }}</span>
      <span class="fixture-metrics">{{ fixture.must_produce.join(' / ') }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import type { DisplayLanguage, FixtureDescriptor } from '@/lib/types'

defineProps<{
  fixtures: FixtureDescriptor[]
  selectedFixtureId: string
  language: DisplayLanguage
}>()

defineEmits<{
  select: [fixtureId: string]
}>()
</script>
