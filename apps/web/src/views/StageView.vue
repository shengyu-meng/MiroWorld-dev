<template>
  <main class="stage-page">
    <WorldlineCanvas
      :active-surface="activeSurface"
      :events="stage?.observatory.key_events ?? []"
      :selected-event-id="selectedEventId"
      :selected-branch-id="selectedBranchId"
      scene="stage"
    />

    <div class="stage-shell stage-shell--immersive">
      <header class="stage-header">
        <div class="stage-heading">
          <p class="eyebrow">{{ copy.stage.sourcePrefix }} / {{ stage?.project_context.source_label ?? 'fixture' }}</p>
          <h1>{{ stage?.project_context.headline ?? copy.stage.loading }}</h1>
          <p class="stage-summary">{{ stage?.project_context.summary ?? copy.stage.actionLine }}</p>
        </div>
        <div class="stage-header-tools">
          <LanguageToggle v-model="language" />
          <p class="stage-action-line">{{ copy.stage.actionLine }}</p>
        </div>
      </header>

      <section v-if="loading" class="status-card" data-testid="loading-state">{{ copy.stage.loading }}</section>
      <section v-else-if="errorMessage" class="status-card error" data-testid="error-state">{{ errorMessage }}</section>

      <template v-else-if="stage && selectedEvent && selectedBranch && shareSnapshot">
        <section class="stage-overview">
          <article class="annotation-block stage-frame-card">
            <span class="annotation-label">{{ copy.currentFrame }}</span>
            <strong>{{ selectedEvent.title }}</strong>
            <p>{{ selectedEvent.summary }}</p>
          </article>

          <article class="annotation-block layer-lens-card">
            <span class="annotation-label">{{ copy.stage.layerLabel }}</span>
            <div class="layer-chip-row">
              <button
                v-for="layer in availableLayers"
                :key="layer"
                type="button"
                class="layer-chip"
                :class="{ active: layer === selectedLayer }"
                @click="selectedLayer = layer"
              >
                {{ layer }}
              </button>
            </div>
            <strong>{{ copy.layers[selectedLayer].title }}</strong>
            <p>{{ copy.layers[selectedLayer].note }}</p>
            <ul class="layer-highlight-list">
              <li v-for="item in layerHighlights" :key="item">{{ item }}</li>
            </ul>
          </article>
        </section>

        <WorldlineOverlay
          :event="selectedEvent"
          :selected-branch-id="selectedBranchId"
          :confidence-label="copy.stage.confidenceLabel"
          :branch-field-label="copy.stage.branchFieldLabel"
          :branch-field-note="copy.stage.branchFieldNote"
          :labels="{
            primary: copy.labels.primary,
            alternate: copy.labels.alternate,
            actionVector: copy.labels.actionVector,
          }"
          @select-branch="handleSelectBranch(selectedEvent.event_id, $event)"
        />

        <SurfaceRail :surfaces="surfaces" :active-surface="activeSurface" @select="activeSurface = $event" />

        <div class="stage-grid">
          <section class="scene-panel" :class="`scene-panel--${activeSurface}`">
            <header class="scene-panel-header">
              <div>
                <span class="surface-kicker">{{ activeSurfaceCopy.index }} / {{ activeSurfaceCopy.label }}</span>
                <h2>{{ activeSurfaceCopy.title }}</h2>
              </div>
              <p class="scene-panel-blurb">{{ activeSurfaceCopy.blurb }}</p>
            </header>

            <ObservatorySection
              v-if="activeSurface === 'observatory'"
              :events="stage.observatory.key_events"
              :selected-event-id="selectedEventId"
              :selected-branch-id="selectedBranchId"
              :labels="{
                primary: copy.labels.primary,
                alternate: copy.labels.alternate,
                affected: copy.labels.affected,
                comparisonBoard: copy.stage.comparisonBoard,
                confidenceLabel: copy.stage.confidenceLabel,
                costHint: copy.labels.costHint,
                actionVector: copy.labels.actionVector,
              }"
              @select-event="handleSelectEvent"
              @select-branch="handleSelectBranch"
            />

            <InterventionSection
              v-else-if="activeSurface === 'intervention'"
              :input-modes="stage.intervention.available_input_types"
              :current-input-type="currentInputType"
              :draft="draft"
              :is-submitting="submitting"
              :placeholder="inputPlaceholder"
              :submit-label="copy.stage.submitAction"
              :loading-label="copy.stage.replaying"
              :input-copy="copy.inputs"
              :branch-cards="stage.intervention.selected_branch_cards"
              :empty-copy="copy.noData"
              @update:currentInputType="handleModeChange"
              @update:draft="draft = $event"
              @submit="submitInput"
            />

            <CostLensSection
              v-else-if="activeSurface === 'cost'"
              :lenses="stage.cost_lens.lenses"
              :selected-branch-id="selectedBranchId"
              :passive-floor="stage.cost_lens.passive_floor"
              :labels="copy.labels"
              :empty-copy="copy.noData"
            />

            <RippleSection
              v-else-if="activeSurface === 'ripple'"
              :project-id="stage.project_context.project_id"
              :latest-bend="latestBend"
              :events="stage.observatory.key_events"
              :worldline-track="stage.observatory.worldline_track"
              :selected-event-id="selectedEventId"
              :selected-branch-id="selectedBranchId"
              :ripple-cards="stage.ripple.ripple_cards"
              :empty-copy="copy.noData"
              :labels="{
                primary: copy.labels.primary,
                alternate: copy.labels.alternate,
                actionVector: copy.labels.actionVector,
              }"
              :confidence-label="copy.stage.confidenceLabel"
              :copy="{
                rippleTrack: copy.archive.rippleTrack,
                latestBendLabel: copy.archive.latestBendLabel,
                continuityAtlas: copy.ripple.continuityAtlas,
                continuityNote: copy.ripple.continuityNote,
                focusEvent: copy.ripple.focusEvent,
                branchSpread: copy.ripple.branchSpread,
                evidenceDensity: copy.ripple.evidenceDensity,
                pathArchive: copy.ripple.pathArchive,
                pathArchiveNote: copy.ripple.pathArchiveNote,
                activePath: copy.ripple.activePath,
                primaryPath: copy.ripple.primaryPath,
                alternateDrift: copy.ripple.alternateDrift,
                replayHistory: copy.ripple.replayHistory,
                replayHistoryNote: copy.ripple.replayHistoryNote,
                upstreamTension: copy.ripple.upstreamTension,
                hingeBranch: copy.ripple.hingeBranch,
                downstreamDrift: copy.ripple.downstreamDrift,
                archiveOrigin: copy.ripple.archiveOrigin,
                archiveOriginNote: copy.ripple.archiveOriginNote,
                archiveOpenEnd: copy.ripple.archiveOpenEnd,
                archiveOpenEndNote: copy.ripple.archiveOpenEndNote,
                counterSignalDensity: copy.ripple.counterSignalDensity,
                replaySetLibrary: copy.ripple.replaySetLibrary,
                replaySetLibraryNote: copy.ripple.replaySetLibraryNote,
                currentSet: copy.ripple.currentSet,
                currentSetNote: copy.ripple.currentSetNote,
                stabilizingSet: copy.ripple.stabilizingSet,
                stabilizingSetNote: copy.ripple.stabilizingSetNote,
                pressureSet: copy.ripple.pressureSet,
                pressureSetNote: copy.ripple.pressureSetNote,
                eventCount: copy.ripple.eventCount,
                setConfidence: copy.ripple.setConfidence,
                setPressure: copy.ripple.setPressure,
                setAlternateCount: copy.ripple.setAlternateCount,
                replayDossier: copy.ripple.replayDossier,
                replayDossierNote: copy.ripple.replayDossierNote,
                replayArtifact: language === 'zh' ? '重演展签' : 'Replay Artifact',
                replayArtifactNote: language === 'zh'
                  ? '把当前重演读成一张可带走的展签，而不是只留在技术 dossier 里。'
                  : 'Read the current replay as an exhibition label instead of leaving it inside a technical dossier only.',
                replayExcerpt: language === 'zh' ? '重演摘录' : 'Replay Excerpt',
                copyReplayExcerpt: language === 'zh' ? '复制重演摘录' : 'Copy Replay Excerpt',
                copyReplayArtifact: language === 'zh' ? '复制重演展签' : 'Copy Replay Artifact',
                downloadReplayDossier: language === 'zh' ? '导出 Replay Dossier' : 'Download Replay Dossier',
                downloadReplayPacket: language === 'zh' ? '导出 Replay Packet' : 'Download Replay Packet',
                downloadReplayExhibit: language === 'zh' ? '导出 Replay Exhibit' : 'Download Replay Exhibit',
                replayDossierSummaryTemplate: language === 'zh'
                  ? '从 {entry} 进入，在 {hinge} 承压，并在 {terminal} 暴露尾迹。'
                  : 'Enters through {entry}, takes pressure at {hinge}, and exposes its tail at {terminal}.',
                replayPacketIntroTemplate: language === 'zh'
                  ? '这份重演案卷以 {setLabel} 为视角，覆盖 {eventCount} 个事件，平均置信 {confidence}，平均压力 {pressure}。'
                  : 'This replay dossier reads through {setLabel}, covering {eventCount} events with {confidence} average confidence and {pressure} average pressure.',
                replayArtifactDeckTemplate: language === 'zh'
                  ? '从 {entry} 倾入，在 {hinge} 拐折，朝 {terminal} 留下余波。'
                  : 'Pours in from {entry}, bends at {hinge}, and leaves its afterimage toward {terminal}.',
                replayArtifactWallTemplate: language === 'zh'
                  ? '这条 {setLabel} 重演跨越 {eventCount} 个事件，维持 {confidence} 有效置信，同时携带 {pressure} 可见压力，并把 {alternateCount} 次替代转向保留在画面里。'
                  : 'This {setLabel} replay spans {eventCount} events, holds {confidence} effective confidence, carries {pressure} visible pressure, and keeps {alternateCount} alternate turns in frame.',
                replayArtifactClosingTemplate: language === 'zh'
                  ? '它在 {terminal} 留下的并不是一个无代价的结尾，因为整条线仍把 {alternateCount} 次替代转向压在背景里。'
                  : 'What remains at {terminal} is not a free ending, because the line still keeps {alternateCount} alternate turns under pressure in the background.',
                replayArtifactPressureHigh: language === 'zh'
                  ? '这是一条高压读法：它主动停留在反证更密、代价更重的支路上。'
                  : 'This is a high-pressure reading: it stays with the branch where counter-signals and costs remain most exposed.',
                replayArtifactPressureMedium: language === 'zh'
                  ? '这条线并未彻底失稳，但它持续把压力集中在转折节点附近。'
                  : 'This line is not fully unstable, but it keeps pressure concentrated near the hinge.',
                replayArtifactPressureLow: language === 'zh'
                  ? '这是一条相对克制的读法：它让压力保持可见，却没有让整条线彻底断裂。'
                  : 'This is a more restrained reading: it keeps pressure visible without letting the line fully tear open.',
                replayShelf: language === 'zh' ? '重演架' : 'Replay Shelf',
                replayShelfNote: language === 'zh'
                  ? '把当前重演包暂存到本地架上，之后可以回看、恢复和再次导出。'
                  : 'Keep authored replay packets on a local shelf so they can be revisited, restored, and exported again.',
                saveReplayShelf: language === 'zh' ? '保存到 Replay Shelf' : 'Save To Replay Shelf',
                restoreReplayShelf: language === 'zh' ? '恢复重演' : 'Restore Replay',
                removeReplayShelf: language === 'zh' ? '移除' : 'Remove',
                emptyReplayShelf: language === 'zh'
                  ? '当前项目还没有保存的 replay packet。'
                  : 'No replay packets have been saved for this project yet.',
                savedAtLabel: language === 'zh' ? '保存时间' : 'Saved At',
                savedFocus: language === 'zh' ? '聚焦锚点' : 'Saved Focus',
                downloadSavedReplayDossier: language === 'zh' ? '导出已存 Dossier' : 'Download Saved Dossier',
                downloadSavedReplayPacket: language === 'zh' ? '导出已存 Packet' : 'Download Saved Packet',
                downloadSavedReplayExhibit: language === 'zh' ? '导出已存 Exhibit' : 'Download Saved Exhibit',
                entryAnchor: copy.ripple.entryAnchor,
                hingePressure: copy.ripple.hingePressure,
                terminalExposure: copy.ripple.terminalExposure,
              }"
              @select-event="handleSelectEvent"
              @select-branch="handleSelectBranch"
            />

            <ArchiveSection
              v-else
              :share-snapshot="shareSnapshot"
              :decision-log="stage.archive.player_decision_log"
              :calibration-summary="stage.archive.calibration_summary"
              :calibration-records="stage.archive.calibration_records"
              :calibration-open="calibrationOpen"
              :calibration-draft="calibrationDraft"
              :calibration-result="calibrationResult"
              :project-id="stage.project_context.project_id"
              :copy="{
                ...copy.archive,
                decisionSlices: language === 'zh' ? '决策切片' : 'Decision Slices',
                longitudinalSlices: language === 'zh' ? '纵深切片' : 'Longitudinal Slices',
                originWindow: language === 'zh' ? '起始窗口' : 'Origin Window',
                hingeWindow: language === 'zh' ? '中段窗口' : 'Hinge Window',
                latestWindow: language === 'zh' ? '最新窗口' : 'Latest Window',
                observationType: copy.inputs.observation.label,
                correctionType: copy.inputs.correction.label,
                interventionType: copy.inputs.intervention.label,
                preferenceType: copy.inputs.preference.label,
                unknownDecisionType: language === 'zh' ? '未映射输入' : 'Unmapped Input',
              }"
              @share="generateShare"
              @toggle-calibration="calibrationOpen = !calibrationOpen"
              @update:calibrationDraft="calibrationDraft = $event"
              @update:calibrationResult="handleCalibrationResult"
              @save-calibration="saveCalibration"
            />
          </section>

          <aside class="annotation-rail">
            <div class="annotation-block">
              <span class="annotation-label">{{ copy.stage.selectedBranch }}</span>
              <strong>{{ selectedBranch.label }}</strong>
              <p>{{ selectedBranch.description }}</p>
              <small>{{ copy.stage.confidenceLabel }} / {{ formatConfidence(selectedBranch.effective_confidence ?? selectedBranch.confidence) }}</small>
            </div>

            <div class="annotation-block">
              <span class="annotation-label">{{ copy.stage.selectedEvent }}</span>
              <strong>{{ selectedEvent.title }}</strong>
              <p>{{ selectedEvent.stage }} / {{ selectedEvent.impact_level }}</p>
              <ul>
                <li v-for="entity in selectedEvent.affected_entities" :key="entity">{{ entity }}</li>
              </ul>
            </div>

            <div class="annotation-block">
              <span class="annotation-label">{{ copy.labels.premises }}</span>
              <ul>
                <li v-for="premise in selectedBranch.premises" :key="premise">{{ premise }}</li>
              </ul>
            </div>

            <div class="annotation-block">
              <span class="annotation-label">{{ copy.labels.signalsFor }}</span>
              <ul>
                <li v-for="signal in selectedBranch.signals_for" :key="signal">{{ signal }}</li>
              </ul>
            </div>

            <div class="annotation-block">
              <span class="annotation-label">{{ copy.labels.signalsAgainst }}</span>
              <ul>
                <li v-for="signal in selectedBranch.signals_against" :key="signal">{{ signal }}</li>
              </ul>
            </div>

            <div class="annotation-block">
              <span class="annotation-label">{{ copy.stage.trackLabel }}</span>
              <div class="track-list">
                <button
                  v-for="track in stage.observatory.worldline_track"
                  :key="track.event_id"
                  type="button"
                  class="track-node"
                  :class="{ active: track.event_id === selectedEventId }"
                  @click="handleSelectEvent(track.event_id)"
                >
                  <span>{{ track.stage }}</span>
                  <strong>{{ track.title }}</strong>
                  <small>{{ formatConfidence(track.confidence) }}</small>
                </button>
              </div>
            </div>

            <div class="annotation-block" v-if="latestBend">
              <span class="annotation-label">{{ copy.stage.replayLabel }}</span>
              <p>{{ latestBend }}</p>
            </div>
          </aside>
        </div>
      </template>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import LanguageToggle from '@/components/LanguageToggle.vue'
import SurfaceRail from '@/components/SurfaceRail.vue'
import WorldlineCanvas from '@/components/WorldlineCanvas.vue'
import WorldlineOverlay from '@/components/WorldlineOverlay.vue'
import ArchiveSection from '@/components/sections/ArchiveSection.vue'
import CostLensSection from '@/components/sections/CostLensSection.vue'
import InterventionSection from '@/components/sections/InterventionSection.vue'
import ObservatorySection from '@/components/sections/ObservatorySection.vue'
import RippleSection from '@/components/sections/RippleSection.vue'
import { applyInput, buildShare, getStage, recordCalibration } from '@/lib/api'
import { getAppCopy } from '@/lib/copy'
import type { Branch, DisplayLanguage, InputType, KnowledgeLayer, StageData, SurfaceKey } from '@/lib/types'

const route = useRoute()
const router = useRouter()
const language = ref<DisplayLanguage>((route.query.lang as DisplayLanguage) || 'zh')
const stage = ref<StageData | null>(null)
const loading = ref(true)
const errorMessage = ref('')
const activeSurface = ref<SurfaceKey>('observatory')
const selectedEventId = ref('')
const selectedBranchId = ref('')
const selectedLayer = ref<KnowledgeLayer>('FACT')
const currentInputType = ref<InputType>('intervention')
const draft = ref('')
const replaySummary = ref('')
const calibrationOpen = ref(false)
const calibrationDraft = ref('')
const calibrationResult = ref<'hit' | 'partial' | 'miss' | 'insufficient_data'>('partial')
const submitting = ref(false)
const shareSnapshot = ref<StageData['archive']['share_snapshot'] | null>(null)

const copy = computed(() => getAppCopy(language.value))
const surfaceKeys: SurfaceKey[] = ['observatory', 'intervention', 'cost', 'ripple', 'archive']

const surfaces = computed(() => surfaceKeys.map((key) => ({
  key,
  index: copy.value.surfaces[key].index,
  label: copy.value.surfaces[key].label,
  title: copy.value.surfaces[key].title,
})))

const selectedEvent = computed(() => stage.value?.observatory.key_events.find((event) => event.event_id === selectedEventId.value) ?? null)
const selectedBranch = computed<Branch | null>(() => selectedEvent.value?.branches.find((branch) => branch.branch_id === selectedBranchId.value) ?? null)
const latestBend = computed(() => replaySummary.value || stage.value?.ripple.latest_bend || '')
const activeSurfaceCopy = computed(() => copy.value.surfaces[activeSurface.value])
const selectedLenses = computed(() => stage.value?.cost_lens.lenses.filter((lens) => lens.target_branch_id === selectedBranchId.value) ?? [])

const availableLayers = computed<KnowledgeLayer[]>(() => {
  const layers = stage.value?.observatory.knowledge_layers ?? []
  return layers.filter((layer): layer is KnowledgeLayer => layer in copy.value.layers)
})

const inputPlaceholder = computed(() => (
  language.value === 'zh'
    ? '写下你的 observation / correction / intervention / preference'
    : 'Write your observation / correction / intervention / preference'
))

const layerHighlights = computed(() => {
  if (!selectedEvent.value || !selectedBranch.value) return []

  if (selectedLayer.value === 'FACT') {
    return [...selectedEvent.value.affected_entities, ...selectedEvent.value.evidence_notes].slice(0, 4)
  }

  if (selectedLayer.value === 'INFERENCE') {
    return [...selectedBranch.value.premises, ...selectedBranch.value.signals_for].slice(0, 4)
  }

  if (selectedLayer.value === 'VALUE') {
    return [
      ...selectedLenses.value.flatMap((lens) => lens.affected_groups),
      ...selectedLenses.value.flatMap((lens) => lens.ethical_notes),
      stage.value?.cost_lens.passive_floor.summary ?? '',
    ].filter(Boolean).slice(0, 4)
  }

  return [
    copy.value.inputs[currentInputType.value].note,
    selectedBranch.value.player_influence,
    latestBend.value || copy.value.stage.archivePrompt,
  ].filter(Boolean).slice(0, 4)
})

watch(
  () => language.value,
  async () => {
    if (route.query.lang !== language.value) {
      await router.replace({
        query: {
          ...route.query,
          lang: language.value,
        },
      })
    }
    await loadStage()
  },
  { immediate: true },
)

async function loadStage() {
  loading.value = true
  errorMessage.value = ''
  try {
    const projectId = route.params.projectId as string
    const nextStage = await getStage(projectId, language.value)
    syncSelection(nextStage, nextStage.surface_defaults.active_surface)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  } finally {
    loading.value = false
  }
}

function syncSelection(nextStage: StageData, nextSurface = activeSurface.value) {
  stage.value = nextStage
  activeSurface.value = nextSurface
  shareSnapshot.value = nextStage.archive.share_snapshot

  const events = nextStage.observatory.key_events
  const nextEvent = events.find((event) => event.event_id === selectedEventId.value)
    ?? events.find((event) => event.event_id === nextStage.surface_defaults.selected_event_id)
    ?? events[0]

  selectedEventId.value = nextEvent?.event_id ?? ''

  const nextBranch = nextEvent?.branches.find((branch) => branch.branch_id === selectedBranchId.value)
    ?? nextEvent?.branches.find((branch) => branch.branch_id === nextStage.surface_defaults.selected_branch_id)
    ?? nextEvent?.branches[0]

  selectedBranchId.value = nextBranch?.branch_id ?? ''

  if (!availableLayers.value.includes(selectedLayer.value)) {
    selectedLayer.value = availableLayers.value[0] ?? 'FACT'
  }

  if (!nextStage.intervention.available_input_types.includes(currentInputType.value)) {
    currentInputType.value = nextStage.intervention.available_input_types[0] ?? 'intervention'
  }
}

function formatConfidence(value: number) {
  return `${Math.round(value * 100)}%`
}

function handleSelectEvent(eventId: string) {
  selectedEventId.value = eventId
  const event = stage.value?.observatory.key_events.find((item) => item.event_id === eventId)
  if (event) {
    selectedBranchId.value = event.branches.find((branch) => branch.branch_id === selectedBranchId.value)?.branch_id
      ?? event.branches[0]?.branch_id
      ?? ''
  }
}

function handleSelectBranch(eventId: string, branchId: string) {
  selectedEventId.value = eventId
  selectedBranchId.value = branchId
}

function handleModeChange(mode: InputType) {
  currentInputType.value = mode
  selectedLayer.value = 'ACTION'
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
  errorMessage.value = ''
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
    syncSelection(response.stage, response.replay_result ? 'ripple' : 'observatory')
    replaySummary.value = response.replay_result?.summary ?? ''
    draft.value = ''
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
    activeSurface.value = 'archive'
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
    const nextStage = await recordCalibration(projectId, {
      event_id: selectedEvent.value.event_id,
      branch_id: selectedBranch.value.branch_id,
      result: calibrationResult.value,
      actual_outcome: calibrationDraft.value.trim(),
      note: '',
      language: language.value,
    })
    syncSelection(nextStage, 'archive')
    calibrationDraft.value = ''
    calibrationOpen.value = false
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  }
}
</script>
