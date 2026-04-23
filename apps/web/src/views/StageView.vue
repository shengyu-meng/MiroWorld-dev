<template>
  <main class="stage-page">
    <WorldlineCanvas
      :active-surface="activeSurface"
      :events="stage?.observatory.key_events ?? []"
      :selected-event-id="selectedEventId"
      :selected-branch-id="selectedBranchId"
    />

    <div class="stage-shell">
      <header class="stage-header">
        <div>
          <p class="eyebrow">MiroWorld / {{ stage?.project_context.source_label }}</p>
          <h1>{{ stage?.project_context.headline }}</h1>
          <p class="stage-summary">{{ stage?.project_context.summary }}</p>
        </div>
        <LanguageToggle v-model="language" />
      </header>

      <SurfaceRail :surfaces="surfaces" :active-surface="activeSurface" @select="activeSurface = $event" />

      <section v-if="loading" class="status-card" data-testid="loading-state">Loading stage…</section>
      <section v-else-if="errorMessage" class="status-card error" data-testid="error-state">{{ errorMessage }}</section>

      <template v-else-if="stage && selectedEvent && selectedBranch && shareSnapshot">
        <div class="stage-grid">
          <div class="stage-main">
            <ObservatorySection
              :events="stage.observatory.key_events"
              :selected-event-id="selectedEventId"
              :selected-branch-id="selectedBranchId"
              @select-event="handleSelectEvent"
              @select-branch="handleSelectBranch"
            />
            <InterventionSection
              :input-modes="stage.intervention.available_input_types"
              :current-input-type="currentInputType"
              :draft="draft"
              :is-submitting="submitting"
              :placeholder="language === 'zh' ? '写下你的 observation / correction / intervention / preference' : 'Write your observation / correction / intervention / preference'"
              @update:currentInputType="handleModeChange"
              @update:draft="draft = $event"
              @submit="submitInput"
            />
            <CostLensSection
              :lenses="stage.cost_lens.lenses"
              :selected-branch-id="selectedBranchId"
              :passive-floor="stage.cost_lens.passive_floor"
            />
            <RippleSection :latest-bend="latestBend" :ripple-cards="stage.ripple.ripple_cards" />
            <ArchiveSection
              :share-snapshot="shareSnapshot"
              :decision-log="stage.archive.player_decision_log"
              :calibration-summary="stage.archive.calibration_summary"
              :calibration-open="calibrationOpen"
              :calibration-draft="calibrationDraft"
              :calibration-result="calibrationResult"
              @share="generateShare"
              @toggle-calibration="calibrationOpen = !calibrationOpen"
              @update:calibrationDraft="calibrationDraft = $event"
              @update:calibrationResult="handleCalibrationResult"
              @save-calibration="saveCalibration"
            />
          </div>

          <aside class="annotation-rail">
            <div class="annotation-block">
              <span class="annotation-label">Selected Branch</span>
              <strong>{{ selectedBranch.label }}</strong>
              <p>{{ selectedBranch.description }}</p>
            </div>
            <div class="annotation-block">
              <span class="annotation-label">Premises</span>
              <ul>
                <li v-for="premise in selectedBranch.premises" :key="premise">{{ premise }}</li>
              </ul>
            </div>
            <div class="annotation-block">
              <span class="annotation-label">Signals For</span>
              <ul>
                <li v-for="signal in selectedBranch.signals_for" :key="signal">{{ signal }}</li>
              </ul>
            </div>
            <div class="annotation-block">
              <span class="annotation-label">Signals Against</span>
              <ul>
                <li v-for="signal in selectedBranch.signals_against" :key="signal">{{ signal }}</li>
              </ul>
            </div>
            <div class="annotation-block" v-if="replaySummary">
              <span class="annotation-label">Latest Replay</span>
              <p>{{ replaySummary }}</p>
            </div>
          </aside>
        </div>
      </template>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import LanguageToggle from '@/components/LanguageToggle.vue'
import SurfaceRail from '@/components/SurfaceRail.vue'
import WorldlineCanvas from '@/components/WorldlineCanvas.vue'
import ArchiveSection from '@/components/sections/ArchiveSection.vue'
import CostLensSection from '@/components/sections/CostLensSection.vue'
import InterventionSection from '@/components/sections/InterventionSection.vue'
import ObservatorySection from '@/components/sections/ObservatorySection.vue'
import RippleSection from '@/components/sections/RippleSection.vue'
import { applyInput, buildShare, getStage, recordCalibration } from '@/lib/api'
import type { Branch, DisplayLanguage, InputType, StageData, SurfaceKey } from '@/lib/types'

const route = useRoute()
const language = ref<DisplayLanguage>((route.query.lang as DisplayLanguage) || 'zh')
const stage = ref<StageData | null>(null)
const loading = ref(true)
const errorMessage = ref('')
const activeSurface = ref<SurfaceKey>('observatory')
const selectedEventId = ref('')
const selectedBranchId = ref('')
const currentInputType = ref<InputType>('intervention')
const draft = ref('')
const replaySummary = ref('')
const calibrationOpen = ref(false)
const calibrationDraft = ref('')
const calibrationResult = ref<'hit' | 'partial' | 'miss' | 'insufficient_data'>('partial')
const submitting = ref(false)
const shareSnapshot = ref<StageData['archive']['share_snapshot'] | null>(null)

const surfaces: Array<{ key: SurfaceKey; index: string; label: string }> = [
  { key: 'observatory', index: '01', label: 'Observatory' },
  { key: 'intervention', index: '02', label: 'Intervention' },
  { key: 'cost', index: '03', label: 'Cost Lens' },
  { key: 'ripple', index: '04', label: 'Ripple' },
  { key: 'archive', index: '05', label: 'Archive' },
]

const selectedEvent = computed(() => stage.value?.observatory.key_events.find((event) => event.event_id === selectedEventId.value) ?? null)
const selectedBranch = computed<Branch | null>(() => selectedEvent.value?.branches.find((branch) => branch.branch_id === selectedBranchId.value) ?? null)
const latestBend = computed(() => replaySummary.value || stage.value?.ripple.latest_bend || '')

async function loadStage() {
  loading.value = true
  errorMessage.value = ''
  try {
    const projectId = route.params.projectId as string
    stage.value = await getStage(projectId, language.value)
    activeSurface.value = stage.value.surface_defaults.active_surface
    selectedEventId.value = stage.value.surface_defaults.selected_event_id
    selectedBranchId.value = stage.value.surface_defaults.selected_branch_id
    shareSnapshot.value = stage.value.archive.share_snapshot
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  } finally {
    loading.value = false
  }
}

watch(() => language.value, loadStage, { immediate: true })

function handleSelectEvent(eventId: string) {
  selectedEventId.value = eventId
  const event = stage.value?.observatory.key_events.find((item) => item.event_id === eventId)
  if (event) {
    selectedBranchId.value = event.branches[0].branch_id
  }
}

function handleSelectBranch(eventId: string, branchId: string) {
  selectedEventId.value = eventId
  selectedBranchId.value = branchId
}

function handleModeChange(mode: InputType) {
  currentInputType.value = mode
}

function handleCalibrationResult(value: string) {
  if (value === 'hit' || value === 'partial' || value === 'miss' || value === 'insufficient_data') {
    calibrationResult.value = value
  }
}

function effectScopeForMode(mode: InputType) {
  if (mode === 'observation') return 'evidence'
  if (mode === 'correction') return 'world_state'
  if (mode === 'intervention') return 'world_state'
  return 'ranking'
}

async function submitInput() {
  if (!selectedEvent.value || !selectedBranch.value || !draft.value.trim()) return
  submitting.value = true
  try {
    const projectId = route.params.projectId as string
    const response = await applyInput(projectId, {
      input_type: currentInputType.value,
      content: draft.value.trim(),
      target_event_id: selectedEvent.value.event_id,
      target_branch_id: selectedBranch.value.branch_id,
      effect_scope: effectScopeForMode(currentInputType.value),
      language: language.value,
    })
    stage.value = response.stage
    shareSnapshot.value = response.stage.archive.share_snapshot
    replaySummary.value = response.replay_result?.summary ?? ''
    draft.value = ''
    activeSurface.value = response.replay_result ? 'ripple' : 'observatory'
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  } finally {
    submitting.value = false
  }
}

async function generateShare() {
  try {
    const projectId = route.params.projectId as string
    const artifact = await buildShare(projectId, {
      language: language.value,
      event_id: selectedEventId.value,
      branch_id: selectedBranchId.value,
    })
    shareSnapshot.value = artifact
    if (navigator.clipboard) {
      try {
        await navigator.clipboard.writeText(artifact.share_text)
      } catch {
        // Ignore clipboard permission failures; the share artifact is still usable in the UI.
      }
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  }
}

async function saveCalibration() {
  if (!selectedEvent.value || !selectedBranch.value || !calibrationDraft.value.trim()) return
  try {
    const projectId = route.params.projectId as string
    stage.value = await recordCalibration(projectId, {
      event_id: selectedEvent.value.event_id,
      branch_id: selectedBranch.value.branch_id,
      result: calibrationResult.value,
      actual_outcome: calibrationDraft.value.trim(),
      note: '',
      language: language.value,
    })
    shareSnapshot.value = stage.value.archive.share_snapshot
    calibrationDraft.value = ''
    calibrationOpen.value = false
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  }
}
</script>
