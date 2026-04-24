<template>
  <main class="entry-page">
    <WorldlineCanvas active-surface="observatory" :events="[]" scene="entry" />
    <div class="entry-shell entry-shell--immersive">
      <header class="entry-topbar">
        <div class="entry-brand-block">
          <p class="eyebrow">{{ copy.entry.title }}</p>
          <span class="entry-brand-mark">{{ copy.brand }}</span>
        </div>
        <LanguageToggle v-model="language" />
      </header>

      <section class="entry-hero">
        <div class="entry-hero-copy">
          <h1>{{ copy.entry.headline }}</h1>
          <p class="entry-dek">{{ copy.entry.subtitle }}</p>
          <p class="entry-summary">{{ copy.entry.summary }}</p>

          <div class="entry-stats">
            <article v-for="stat in copy.entry.frameStats" :key="stat.label" class="entry-stat-card">
              <span class="annotation-label">{{ stat.label }}</span>
              <strong>{{ stat.value }}</strong>
            </article>
          </div>
        </div>

        <aside class="entry-hero-side">
          <article class="annotation-block entry-note-card">
            <span class="annotation-label">{{ copy.worldlineLens }}</span>
            <p>{{ copy.entry.surfaceNote }}</p>
          </article>
          <article v-if="selectedFixture" class="annotation-block entry-note-card">
            <span class="annotation-label">{{ copy.currentFrame }}</span>
            <strong>{{ selectedFixture.fixture_id }}</strong>
            <p>{{ selectedFixture.purpose }}</p>
            <small>{{ selectedFixture.must_produce.join(' / ') }}</small>
          </article>
        </aside>
      </section>

      <section class="entry-launch-grid">
        <article class="entry-panel">
          <div class="panel-heading">
            <p class="eyebrow">{{ copy.entry.primaryAction }}</p>
            <h2>{{ copy.entry.fixtureLabel }}</h2>
          </div>

          <FixtureGrid
            :fixtures="fixtures"
            :selected-fixture-id="selectedFixtureId"
            :language="language"
            @select="selectedFixtureId = $event"
          />

          <div class="entry-actions">
            <button type="button" class="primary-action" :disabled="creating" @click="launchFixture">
              {{ creating ? copy.entry.opening : copy.entry.primaryAction }}
            </button>
          </div>
        </article>

        <article class="entry-panel">
          <div class="panel-heading">
            <p class="eyebrow">{{ copy.entry.secondaryAction }}</p>
            <h2>{{ copy.entry.promptLabel }}</h2>
          </div>

          <label class="prompt-label" for="seedPrompt">{{ copy.entry.promptLabel }}</label>
          <textarea
            id="seedPrompt"
            v-model="seedPrompt"
            class="intervention-input"
            data-testid="seed-prompt"
            :placeholder="copy.entry.promptPlaceholder"
          ></textarea>

          <div class="entry-actions">
            <button
              type="button"
              class="secondary-action"
              data-testid="prompt-launch"
              :disabled="creating || !seedPrompt.trim()"
              @click="launchPrompt"
            >
              {{ creating ? copy.entry.opening : copy.entry.secondaryAction }}
            </button>
          </div>
        </article>
      </section>

      <p v-if="errorMessage" class="error-copy entry-error">{{ errorMessage }}</p>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import FixtureGrid from '@/components/FixtureGrid.vue'
import LanguageToggle from '@/components/LanguageToggle.vue'
import WorldlineCanvas from '@/components/WorldlineCanvas.vue'
import { createProject, listFixtures } from '@/lib/api'
import { getAppCopy } from '@/lib/copy'
import type { DisplayLanguage, FixtureDescriptor } from '@/lib/types'

const router = useRouter()
const fixtures = ref<FixtureDescriptor[]>([])
const selectedFixtureId = ref('literary-branching-world')
const seedPrompt = ref('')
const language = ref<DisplayLanguage>('zh')
const creating = ref(false)
const errorMessage = ref('')

const copy = computed(() => getAppCopy(language.value))
const selectedFixture = computed(() => fixtures.value.find((fixture) => fixture.fixture_id === selectedFixtureId.value) ?? null)

onMounted(async () => {
  errorMessage.value = ''
  try {
    const manifest = await listFixtures()
    fixtures.value = manifest.fixtures
    if (manifest.fixtures.length > 0) {
      selectedFixtureId.value = manifest.fixtures[0].fixture_id
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  }
})

async function launchFixture() {
  creating.value = true
  errorMessage.value = ''
  try {
    const payload = await createProject({
      fixture_id: selectedFixtureId.value,
      language: language.value,
    })
    await router.push(`/world/${payload.project_id}?lang=${language.value}`)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  } finally {
    creating.value = false
  }
}

async function launchPrompt() {
  creating.value = true
  errorMessage.value = ''
  try {
    const payload = await createProject({
      seed_prompt: seedPrompt.value,
      language: language.value,
    })
    await router.push(`/world/${payload.project_id}?lang=${language.value}`)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  } finally {
    creating.value = false
  }
}
</script>
