<template>
  <nav class="surface-rail" aria-label="worldline surfaces">
    <button
      v-for="surface in surfaces"
      :key="surface.key"
      type="button"
      class="surface-chip"
      :class="{ active: surface.key === activeSurface }"
      @click="$emit('select', surface.key)"
    >
      <span class="surface-index">{{ surface.index }}</span>
      <span>{{ surface.label }}</span>
    </button>
  </nav>
</template>

<script setup lang="ts">
import type { SurfaceKey } from '@/lib/types'

defineProps<{
  surfaces: Array<{ key: SurfaceKey; index: string; label: string }>
  activeSurface: SurfaceKey
}>()

defineEmits<{
  select: [value: SurfaceKey]
}>()
</script>
