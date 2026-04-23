<template>
  <main class="entry-page">
    <WorldlineCanvas active-surface="observatory" :events="[]" />
    <div class="entry-shell">
      <header class="entry-header">
        <div>
          <p class="eyebrow">MIROWORLD / PUBLIC SHELL</p>
          <h1>Line-first futures for public audiences.</h1>
        </div>
        <LanguageToggle v-model="language" />
      </header>

      <section class="entry-copy">
        <p>
          {{ language === 'zh'
            ? '这里不是答案机器，而是一条可以被观察、纠正、介入和校准的世界线。'
            : 'This is not an answer machine. It is a worldline that can be observed, corrected, intervened in, and calibrated.' }}
        </p>
      </section>

      <FixtureGrid :fixtures="fixtures" :selected-fixture-id="selectedFixtureId" @select="selectedFixtureId = $event" />

      <section class="prompt-station">
        <label class="prompt-label" for="seedPrompt">
          {{ language === 'zh' ? '或者写下一条新的世界线入口' : 'Or write a new worldline entry prompt' }}
        </label>
        <textarea id="seedPrompt" v-model="seedPrompt" class="intervention-input" data-testid="seed-prompt"></textarea>
        <div class="entry-actions">
          <button type="button" class="primary-action" :disabled="creating" @click="launchFixture">
            {{ creating ? 'Opening…' : language === 'zh' ? '从 fixture 进入' : 'Enter via fixture' }}
          </button>
          <button type="button" class="secondary-action" :disabled="creating || !seedPrompt.trim()" @click="launchPrompt">
            {{ language === 'zh' ? '从 prompt 生成' : 'Generate from prompt' }}
          </button>
        </div>
        <p v-if="errorMessage" class="error-copy">{{ errorMessage }}</p>
      </section>
    </div>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import FixtureGrid from '@/components/FixtureGrid.vue'
import LanguageToggle from '@/components/LanguageToggle.vue'
import WorldlineCanvas from '@/components/WorldlineCanvas.vue'
import { createProject, listFixtures } from '@/lib/api'
import type { DisplayLanguage, FixtureDescriptor } from '@/lib/types'

const router = useRouter()
const fixtures = ref<FixtureDescriptor[]>([])
const selectedFixtureId = ref('literary-branching-world')
const seedPrompt = ref('')
const language = ref<DisplayLanguage>('zh')
const creating = ref(false)
const errorMessage = ref('')

onMounted(async () => {
  const manifest = await listFixtures()
  fixtures.value = manifest.fixtures
  if (manifest.fixtures.length > 0) {
    selectedFixtureId.value = manifest.fixtures[0].fixture_id
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
