<template>
  <section class="scene-section ripple-section" data-testid="ripple-section">
    <article class="ripple-callout-card">
      <span class="annotation-label">{{ copy.latestBendLabel }}</span>
      <p class="surface-callout">{{ latestBend || emptyCopy }}</p>
    </article>

    <div class="ripple-track-card">
      <header class="ripple-track-header">
        <span class="annotation-label">{{ copy.rippleTrack }}</span>
      </header>
      <div class="ripple-track-list">
        <article
          v-for="(card, index) in rippleCards"
          :key="`${card.title}-${card.branch_label}`"
          class="ripple-track-node"
        >
          <span class="ripple-track-index">{{ String(index + 1).padStart(2, '0') }}</span>
          <div class="ripple-track-copy">
            <strong>{{ card.title }}</strong>
            <p>{{ card.summary }}</p>
            <small>{{ card.branch_label }}</small>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  latestBend: string
  emptyCopy: string
  rippleCards: Array<{
    title: string
    summary: string
    branch_label: string
  }>
  copy: {
    rippleTrack: string
    latestBendLabel: string
  }
}>()
</script>
