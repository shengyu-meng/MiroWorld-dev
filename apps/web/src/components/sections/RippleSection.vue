<template>
  <section class="stage-surface" data-testid="ripple-section">
    <div class="surface-heading">
      <span class="surface-kicker">04 / Ripple</span>
      <h2>Watch the bend travel downstream.</h2>
    </div>
    <p class="surface-callout">{{ latestBend }}</p>
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
  rippleCards: Array<{
    title: string
    summary: string
    branch_label: string
  }>
}>()
</script>
