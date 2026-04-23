<template>
  <section class="scene-section" data-testid="ripple-section">
    <p class="surface-callout">{{ latestBend || emptyCopy }}</p>
    <div class="ripple-list">
      <article v-for="card in rippleCards" :key="`${card.title}-${card.branch_label}`" class="ripple-card">
        <strong>{{ card.title }}</strong>
        <p>{{ card.summary }}</p>
        <small>{{ card.branch_label }}</small>
      </article>
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
}>()
</script>
