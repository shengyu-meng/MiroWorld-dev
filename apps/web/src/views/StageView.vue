<template>
  <main class="theatre-page stage-page" :data-surface="activeSurface">
    <WorldlineCanvas
      :active-surface="activeSurface"
      :events="revealedEvents"
      :selected-event-id="selectedEventId"
      :selected-branch-id="selectedBranchId"
      :revealed-event-count="revealedCount"
      :pulse-key="pulseKey"
      scene="stage"
    />

    <div class="theatre-shell">
      <header class="theatre-topbar">
        <div class="theatre-title-block">
          <p class="eyebrow">{{ t.kicker }} / {{ cleanText(stage?.project_context.source_label ?? 'fixture') }}</p>
          <h1>{{ cleanText(stage?.project_context.headline ?? t.loading) }}</h1>
          <p>{{ cleanText(stage?.project_context.summary ?? t.summaryFallback) }}</p>
        </div>
        <div class="theatre-tools">
          <LanguageToggle v-model="language" />
          <span class="theatre-readout" data-testid="theatre-readout">
            <span>{{ t.readout }}</span>
            <strong>{{ revealedCount }} / {{ events.length || '-' }}</strong>
          </span>
          <span class="theatre-live-dot">{{ t.live }}</span>
        </div>
      </header>

      <section v-if="loading" class="theatre-status" data-testid="loading-state">{{ t.loading }}</section>
      <section v-else-if="errorMessage" class="theatre-status theatre-status--error" data-testid="error-state">
        {{ errorMessage }}
      </section>

      <template v-else-if="stage && selectedEvent && selectedBranch && shareSnapshot">
        <section class="worldline-theatre" data-testid="worldline-theatre">
          <aside class="theatre-left-rail">
            <article class="theatre-panel theatre-panel--quiet">
              <span class="annotation-label">{{ t.progressLabel }}</span>
              <strong data-testid="revealed-event-count">{{ revealedCount }} / {{ events.length }}</strong>
              <div class="theatre-progress-track" aria-hidden="true">
                <i :style="{ width: `${stageProgress * 100}%` }"></i>
              </div>
              <p>{{ progressComplete ? t.progressComplete : t.progressHint }}</p>
              <small
                class="progress-save-state"
                :class="`progress-save-state--${progressSaveState}`"
                data-testid="progress-save-state"
              >
                {{ progressSaveLabel }}
              </small>
            </article>

            <article class="theatre-panel">
              <span class="annotation-label">{{ t.layerLabel }}</span>
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
              <strong>{{ t.layers[selectedLayer].title }}</strong>
              <p>{{ t.layers[selectedLayer].note }}</p>
              <ul class="theatre-mini-list">
                <li v-for="item in layerHighlights" :key="item">{{ item }}</li>
              </ul>
            </article>

            <nav class="surface-orbit" aria-label="Worldline lenses">
              <button
                v-for="surface in surfaces"
                :key="surface.key"
                type="button"
                class="surface-chip"
                :class="{ active: surface.key === activeSurface }"
                @click="handleSurfaceChange(surface.key)"
              >
                <span>{{ surface.index }}</span>
                {{ surface.label }}
              </button>
            </nav>
          </aside>

          <section class="theatre-center-field">
            <div class="stage-orbit-map" data-testid="stage-orbit-map" aria-hidden="true">
              <i
                v-for="(event, index) in events"
                :key="`orbit-${event.event_id}`"
                :class="{
                  revealed: revealedIds.has(event.event_id),
                  active: event.event_id === selectedEventId,
                }"
                :style="orbitNodeStyle(index, events.length)"
              ></i>
            </div>

            <div class="singularity-caption">
              <span>{{ t.singularityLabel }}</span>
              <strong>{{ t.singularityNote }}</strong>
            </div>

            <article v-if="currentProcessStep" class="process-trace-card" data-testid="process-trace-panel">
              <div class="process-trace-head">
                <div>
                  <span class="annotation-label">{{ processText.processLabel }}</span>
                  <strong>{{ processText.stepLabel }} {{ processStepIndex }} / {{ processSteps.length }}</strong>
                </div>
                <small>{{ currentProcessStep.status }} / {{ currentProcessStep.artifact_kind }}</small>
              </div>

              <div class="process-orbit" aria-hidden="true">
                <i
                  v-for="(step, index) in processSteps"
                  :key="step.step_id"
                  :class="{
                    active: step.event_id === currentProcessStep.event_id,
                    revealed: revealedIds.has(step.event_id),
                  }"
                  :style="{ '--orbit-delay': `${index * 70}ms` }"
                ></i>
              </div>

              <strong>{{ cleanText(currentProcessStep.event_title) }}</strong>
              <p>{{ cleanText(currentProcessStep.summary) }}</p>

              <div class="process-file-strip">
                <span>{{ processText.fileLabel }}</span>
                <code data-testid="process-file-path">{{ currentProcessStep.artifact_path }}</code>
              </div>

              <div class="process-metric-row">
                <span data-testid="process-metric-confidence">
                  {{ processText.confidenceLabel }} {{ formatConfidence(currentProcessStep.artifact_preview.primary_confidence) }}
                </span>
                <span data-testid="process-metric-cost-mass">
                  {{ processText.costMassLabel }} {{ currentProcessStep.artifact_preview.cost_mass }}
                </span>
                <span>
                  {{ processText.counterSignalLabel }} {{ currentProcessStep.artifact_preview.counter_signal_count }}
                </span>
              </div>

              <div class="process-layer-grid">
                <button
                  v-for="layerResult in currentProcessStep.layer_results"
                  :key="layerResult.layer"
                  type="button"
                  class="process-layer-card"
                  :class="{ active: layerResult.layer === selectedLayer }"
                  :data-testid="`process-layer-${layerResult.layer}`"
                  @click="selectedLayer = layerResult.layer"
                >
                  <span>{{ layerResult.layer }}</span>
                  <strong>{{ cleanText(layerResult.title) }}</strong>
                  <small>{{ cleanText(layerResult.outputs[0] ?? layerResult.confidence_note) }}</small>
                </button>
              </div>

              <section v-if="selectedProcessLayer" class="process-layer-inspector" data-testid="process-layer-inspector">
                <header>
                  <span>{{ selectedProcessLayer.layer }}</span>
                  <strong>{{ cleanText(selectedProcessLayer.title) }}</strong>
                </header>
                <div class="process-io-grid">
                  <div>
                    <span>{{ processText.inputsLabel }}</span>
                    <ul>
                      <li v-for="item in selectedProcessLayer.inputs" :key="item">{{ cleanText(item) }}</li>
                    </ul>
                  </div>
                  <div>
                    <span>{{ processText.outputsLabel }}</span>
                    <ul>
                      <li v-for="item in selectedProcessLayer.outputs" :key="item">{{ cleanText(item) }}</li>
                    </ul>
                  </div>
                </div>
                <p>{{ cleanText(selectedProcessLayer.confidence_note) }}</p>
              </section>

              <div
                v-if="currentProcessStep.intervention_window.is_open"
                class="intervention-window"
                data-testid="process-intervention-window"
              >
                <span class="annotation-label">{{ processText.interventionWindow }}</span>
                <p>{{ cleanText(currentProcessStep.intervention_window.reason) }}</p>
                <button
                  type="button"
                  class="theatre-secondary-action"
                  data-testid="process-intervene"
                  @click="openProcessIntervention(currentProcessStep)"
                >
                  {{ processText.openInterventionWindow }}
                </button>
              </div>
            </article>

            <ol class="progressive-worldline" data-testid="progressive-worldline">
              <li
                v-for="(event, index) in revealedEvents"
                :key="event.event_id"
                :data-testid="`worldline-event-${event.event_id}`"
                :class="{ active: event.event_id === selectedEventId }"
              >
                <button type="button" @click="handleSelectEvent(event.event_id)">
                  <span>{{ String(index + 1).padStart(2, '0') }}</span>
                  <strong>{{ cleanText(event.title) }}</strong>
                  <small>{{ cleanText(event.stage) }} / {{ event.impact_level }}</small>
                </button>
              </li>
              <li v-if="!progressComplete" class="ghost-node">
                <span>{{ t.nextGhost }}</span>
              </li>
            </ol>
          </section>

          <aside class="theatre-right-rail" data-testid="observatory-section">
            <article class="theatre-panel selected-event-card">
              <span class="annotation-label">{{ t.selectedEvent }}</span>
              <h2>{{ cleanText(selectedEvent.title) }}</h2>
              <p>{{ cleanText(selectedEvent.summary) }}</p>
              <div class="theatre-tag-row">
                <span v-for="entity in focusTags" :key="entity">{{ t.actantLabel }} / {{ entity }}</span>
              </div>
            </article>

            <article class="theatre-panel worldline-overlay" data-testid="worldline-overlay">
              <span class="annotation-label">{{ t.branchField }}</span>
              <div class="branch-constellation">
                <button
                  v-for="branch in selectedEvent.branches"
                  :key="branch.branch_id"
                  type="button"
                  class="branch-chip"
                  :class="{ active: branch.branch_id === selectedBranchId }"
                  @click="handleSelectBranch(selectedEvent.event_id, branch.branch_id)"
                >
                  <span>{{ branch.visibility === 'primary' ? t.primary : t.alternate }}</span>
                  <strong>{{ cleanText(branch.label) }}</strong>
                  <small>{{ formatConfidence(branch.effective_confidence ?? branch.confidence) }}</small>
                </button>
              </div>
              <p class="branch-description">{{ cleanText(selectedBranch.description) }}</p>
            </article>

            <article class="theatre-panel">
              <span class="annotation-label">{{ t.premises }}</span>
              <ul class="theatre-mini-list">
                <li v-for="item in selectedBranch.premises" :key="item">{{ cleanText(item) }}</li>
              </ul>
            </article>

            <article class="theatre-panel">
              <span class="annotation-label">{{ t.costLabel }}</span>
              <p>{{ cleanText(selectedBranch.cost_hint) }}</p>
              <ul class="theatre-mini-list">
                <li v-for="item in currentCosts" :key="item">{{ item }}</li>
              </ul>
            </article>

            <article class="theatre-panel">
              <span class="annotation-label">{{ t.rippleLabel }}</span>
              <p>{{ latestBend }}</p>
            </article>
          </aside>
        </section>

        <section class="theatre-drawer" :class="`theatre-drawer--${activeSurface}`">
          <header>
            <span class="surface-kicker">{{ activeSurfaceCopy.index }} / {{ activeSurfaceCopy.label }}</span>
            <h2>{{ activeSurfaceCopy.title }}</h2>
            <p>{{ activeSurfaceCopy.blurb }}</p>
          </header>

          <div v-if="activeSurface === 'intervention'" class="drawer-grid" data-testid="intervention-section">
            <div>
              <div class="input-mode-row">
                <button
                  v-for="mode in stage.intervention.available_input_types"
                  :key="mode"
                  type="button"
                  class="input-mode-chip"
                  :class="{ active: mode === currentInputType }"
                  @click="handleModeChange(mode)"
                >
                  {{ t.inputs[mode].label }}
                </button>
              </div>
              <p>{{ t.inputs[currentInputType].note }}</p>
            </div>
            <form class="theatre-input-form" @submit.prevent="submitInput">
              <textarea v-model="draft" :placeholder="interventionPlaceholder"></textarea>
              <button type="submit" class="theatre-primary-action" :disabled="submitting || !draft.trim()">
                {{ submitting ? t.replaying : t.submitAction }}
              </button>
            </form>
          </div>

          <div v-else-if="activeSurface === 'cost'" class="drawer-grid" data-testid="cost-lens-section">
            <article v-for="lens in selectedLenses" :key="lens.cost_lens_id" class="drawer-card">
              <span class="annotation-label">{{ t.costLabel }}</span>
              <ul class="theatre-mini-list">
                <li v-for="item in lens.first_order_costs" :key="item">{{ cleanText(item) }}</li>
                <li v-for="item in lens.second_order_costs" :key="item">{{ cleanText(item) }}</li>
              </ul>
            </article>
            <article class="drawer-card">
              <span class="annotation-label">{{ t.passiveFloor }}</span>
              <strong>{{ cleanText(stage.cost_lens.passive_floor.title) }}</strong>
              <p>{{ cleanText(stage.cost_lens.passive_floor.summary) }}</p>
            </article>
          </div>

          <div v-else-if="activeSurface === 'ripple'" class="drawer-grid drawer-grid--instrument" data-testid="ripple-section">
            <article class="drawer-card theatre-instrument ripple-console" data-testid="ripple-console">
              <span class="annotation-label">{{ instrumentText.rippleConsole }}</span>
              <div class="instrument-hero">
                <strong>{{ latestBend }}</strong>
                <p>{{ instrumentText.rippleConsoleHint }}</p>
              </div>
              <div class="instrument-metrics" data-testid="ripple-instrument-metrics">
                <span v-for="metric in rippleMetrics" :key="metric.label">
                  <b>{{ metric.value }}</b>
                  <small>{{ metric.label }}</small>
                </span>
              </div>
              <div class="instrument-actions">
                <button type="button" class="instrument-action" data-testid="ripple-trace-export" @click="exportRippleTrace">
                  {{ instrumentText.exportRipple }}
                </button>
                <small aria-live="polite">{{ exportFeedback }}</small>
              </div>
            </article>
            <article class="drawer-card theatre-track-card">
              <span class="annotation-label">{{ t.worldlineTrack }}</span>
              <ol class="instrument-track">
                <li v-for="(track, index) in revealedTrack" :key="track.event_id">
                  <span>{{ String(index + 1).padStart(2, '0') }}</span>
                  <strong>{{ cleanText(track.title) }}</strong>
                  <em>{{ cleanText(track.primary_branch_label) }} / {{ formatConfidence(track.confidence) }}</em>
                </li>
              </ol>
            </article>
            <article class="drawer-card theatre-ripple-card">
              <span class="annotation-label">{{ instrumentText.rippleAfterimage }}</span>
              <ul class="ripple-signal-stack">
                <li v-for="card in visibleRippleCards" :key="`${card.title}-${card.branch_label}`">
                  <strong>{{ cleanText(card.title) }}</strong>
                  <span>{{ cleanText(card.branch_label) }}</span>
                  <p>{{ cleanText(card.summary) }}</p>
                </li>
              </ul>
            </article>
          </div>

          <div v-else-if="activeSurface === 'archive'" class="drawer-grid drawer-grid--instrument" data-testid="archive-section">
            <article class="drawer-card archive-capsule-card" :data-testid="progressComplete ? 'archive-terminal' : 'archive-preview'">
              <div class="archive-capsule" data-testid="archive-capsule">
                <span class="annotation-label">{{ instrumentText.archiveCapsule }}</span>
                <div class="instrument-hero">
                  <strong>{{ cleanText(shareSnapshot.title) }}</strong>
                  <p>{{ cleanText(shareSnapshot.summary) }}</p>
                </div>
                <div class="instrument-metrics" data-testid="archive-capsule-metrics">
                  <span v-for="metric in archiveMetrics" :key="metric.label">
                    <b>{{ metric.value }}</b>
                    <small>{{ metric.label }}</small>
                  </span>
                </div>
                <div class="instrument-actions">
                  <button type="button" class="instrument-action" @click="generateShare">
                    {{ t.shareAction }}
                  </button>
                  <button type="button" class="instrument-action" data-testid="archive-capsule-copy" @click="copyArchiveCapsule">
                    {{ instrumentText.copyCapsule }}
                  </button>
                  <button type="button" class="instrument-action" data-testid="archive-capsule-export" @click="exportArchiveCapsule">
                    {{ instrumentText.exportCapsule }}
                  </button>
                </div>
                <small class="instrument-feedback" aria-live="polite">{{ exportFeedback }}</small>
              </div>
            </article>
            <article class="drawer-card">
              <span class="annotation-label">{{ t.calibrationLabel }}</span>
              <button type="button" class="theatre-secondary-action" @click="calibrationOpen = !calibrationOpen">
                {{ calibrationOpen ? t.hideCalibration : t.openCalibration }}
              </button>
              <div v-if="calibrationOpen" class="calibration-drawer" data-testid="calibration-drawer">
                <div class="input-mode-row">
                  <button
                    v-for="result in calibrationResults"
                    :key="result"
                    type="button"
                    class="input-mode-chip"
                    :class="{ active: result === calibrationResult }"
                    @click="handleCalibrationResult(result)"
                  >
                    {{ t.calibrationResults[result] }}
                  </button>
                </div>
                <textarea v-model="calibrationDraft" :placeholder="t.calibrationPlaceholder"></textarea>
                <button type="button" class="theatre-primary-action" @click="saveCalibration">
                  {{ t.saveCalibration }}
                </button>
              </div>
            </article>
            <article class="drawer-card">
              <span class="annotation-label">{{ t.decisionLog }}</span>
              <ul class="theatre-mini-list">
                <li v-for="entry in stage.archive.player_decision_log.slice(0, 4)" :key="entry.entry_id">
                  {{ cleanText(entry.event_title) }} / {{ cleanText(entry.branch_label) }}
                </li>
              </ul>
            </article>
          </div>

          <div v-else class="drawer-grid">
            <article class="drawer-card">
              <span class="annotation-label">{{ t.selectedEvent }}</span>
              <p>{{ t.observatoryNote }}</p>
            </article>
          </div>
        </section>

        <footer class="theatre-bottombar">
          <div>
            <span class="annotation-label">{{ t.currentLens }}</span>
            <strong>{{ activeSurfaceCopy.label }} / {{ cleanText(selectedBranch.label) }}</strong>
          </div>
          <div class="theatre-bottom-actions">
            <button type="button" class="theatre-secondary-action" @click="handleSurfaceChange('intervention')">
              {{ t.interveneShortcut }}
            </button>
            <button type="button" class="theatre-primary-action" data-testid="worldline-next" @click="advanceWorldline">
              {{ nextActionLabel }}
            </button>
          </div>
        </footer>
      </template>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import LanguageToggle from '@/components/LanguageToggle.vue'
import WorldlineCanvas from '@/components/WorldlineCanvas.vue'
import {
  applyInput,
  buildShare,
  getStage,
  recordCalibration,
  saveTheatreProgress,
} from '@/lib/api'
import type {
  Branch,
  CalibrationRecord,
  CostLens,
  DisplayLanguage,
  InputType,
  KnowledgeLayer,
  StageData,
  SurfaceKey,
  TheatreProgress,
} from '@/lib/types'

const route = useRoute()
const router = useRouter()

const stage = ref<StageData | null>(null)
const language = ref<DisplayLanguage>(route.query.lang === 'en' ? 'en' : 'zh')
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
const calibrationResult = ref<CalibrationRecord['result']>('partial')
const submitting = ref(false)
const shareSnapshot = ref<StageData['archive']['share_snapshot'] | null>(null)
const revealedCount = ref(1)
const pulseKey = ref(0)
const branchMemory = ref<Record<string, string>>({})
const progressSaveState = ref<'idle' | 'saving' | 'saved' | 'failed'>('idle')
const exportFeedback = ref('')
let progressSaveRevision = 0

const surfaceKeys: SurfaceKey[] = ['observatory', 'intervention', 'cost', 'ripple', 'archive']
const calibrationResults: CalibrationRecord['result'][] = ['hit', 'partial', 'miss', 'insufficient_data']

const textReplacements: Array<[RegExp, string]> = [
  [/public opinion/gi, 'world-field'],
  [/public memory/gi, 'world afterimage'],
  [/public view/gi, 'observable layer'],
  [/public climate/gi, 'field climate'],
  [/platforms?/gi, 'rule layers'],
  [/media/gi, 'signal layer'],
  [/audience/gi, 'observer field'],
  [/public/gi, 'open'],
  [/opinion/gi, 'field reading'],
  [/viral/gi, 'high-transmission'],
  [/舆论/g, '观测场'],
  [/公众记忆/g, '世界残影'],
  [/公共视野/g, '可观测层'],
  [/公众气候/g, '场域气候'],
  [/受影响对象/g, '作用体'],
  [/发起者/g, '触发源'],
  [/传播/g, '传导'],
  [/平台/g, '规则层'],
  [/观众/g, '观测者'],
  [/公众/g, '场域'],
]

const theatreCopy = {
  zh: {
    kicker: 'MIROWORLD THEATRE',
    live: '世界线在线',
    readout: '轨道读数',
    loading: '正在装配世界线剧场...',
    summaryFallback: '世界线先显影，解释稍后抵达。',
    progressLabel: '显影进度',
    progressHint: '只点下一步，也会逐段打开事件、分支、代价与回响。',
    progressComplete: '当前世界线已经显影到档案端。',
    layerLabel: '知识层',
    singularityLabel: '小型奇点',
    singularityNote: '黑洞只是引力锚点，真正的主角是正在弯折的线。',
    nextGhost: '下一节点尚未显影',
    selectedEvent: '当前节点',
    actantLabel: '作用体',
    branchField: '分支场',
    primary: '主分支',
    alternate: '替代分支',
    premises: '成立条件',
    costLabel: '代价质量',
    rippleLabel: '最新回响',
    passiveFloor: '被动代价底线',
    worldlineTrack: '世界线轨道',
    archiveLabel: '档案残影',
    shareAction: '生成分享文本',
    calibrationLabel: '校准',
    openCalibration: '打开校准',
    hideCalibration: '收起校准',
    calibrationPlaceholder: '写下后来真实发生的结果，用它校准这条分支。',
    saveCalibration: '保存校准',
    decisionLog: '介入记录',
    currentLens: '当前镜头',
    interveneShortcut: '写入扰动',
    next: '下一步：显影下一个节点',
    finish: '进入档案残影',
    submitAction: '运行重演',
    replaying: '正在折弯世界线...',
    inputPlaceholder: '写下观测、修正、介入或偏好约束，它会成为世界线的扰动。',
    observatoryNote: '先看节点如何成立，再决定是否触碰它。',
    surfaces: {
      observatory: { index: '01', label: '观测台', title: '先看线如何成立。', blurb: '分支不是结论，而是条件、约束和材料共同推演出的轨道。' },
      intervention: { index: '02', label: '介入', title: '声明你的扰动。', blurb: '介入会改变后续轨道，观测和修正只改变对应层。' },
      cost: { index: '03', label: '代价镜', title: '看压力被谁吸收。', blurb: '规则、材料、环境与行动者都会承担代价。' },
      ripple: { index: '04', label: '回响', title: '看偏折如何向后传导。', blurb: '回响不是报告摘要，而是节点之间的连续弯曲。' },
      archive: { index: '05', label: '档案', title: '留下这次观测的残影。', blurb: '分享、介入记录与真实结果在这里汇合。' },
    },
    layers: {
      FACT: { title: '事实层', note: '只处理已经可观测的事件、材料、对象与痕迹。' },
      INFERENCE: { title: '推断层', note: '解释分支为什么能成立，以及哪些信号在反向牵引。' },
      VALUE: { title: '价值层', note: '观察谁承担代价，谁获得余量，规则如何分配压力。' },
      ACTION: { title: '行动层', note: '决定观测者以何种方式扰动世界线，以及从哪里开始重演。' },
    },
    inputs: {
      observation: { label: '观测', note: '增加证据和材料，不直接改写世界状态。' },
      correction: { label: '修正', note: '修正事实层，让原有分支重新稳定或失衡。' },
      intervention: { label: '介入', note: '改变世界线本身，从当前节点之后重新展开。' },
      preference: { label: '偏好约束', note: '表达价值排序，改变建议权重而不是伪造事实。' },
    },
    calibrationResults: {
      hit: '命中',
      partial: '部分命中',
      miss: '偏离',
      insufficient_data: '数据不足',
    },
  },
  en: {
    kicker: 'MIROWORLD THEATRE',
    live: 'worldline live',
    readout: 'Orbit Readout',
    loading: 'Assembling the worldline theatre...',
    summaryFallback: 'The line appears first. Explanation arrives later.',
    progressLabel: 'Reveal Progress',
    progressHint: 'Press Next to open events, branches, costs, and ripples without writing anything.',
    progressComplete: 'This worldline has reached its archive edge.',
    layerLabel: 'Knowledge Layer',
    singularityLabel: 'Small Singularity',
    singularityNote: 'The black hole is only an anchor. The bending line is the subject.',
    nextGhost: 'Next node is still latent',
    selectedEvent: 'Current Node',
    actantLabel: 'Actant',
    branchField: 'Branch Field',
    primary: 'Primary',
    alternate: 'Alternate',
    premises: 'Premises',
    costLabel: 'Cost Mass',
    rippleLabel: 'Latest Ripple',
    passiveFloor: 'Passive Cost Floor',
    worldlineTrack: 'Worldline Track',
    archiveLabel: 'Archive Afterimage',
    shareAction: 'Generate Share Text',
    calibrationLabel: 'Calibration',
    openCalibration: 'Open Calibration',
    hideCalibration: 'Hide Calibration',
    calibrationPlaceholder: 'Write what actually happened so this branch can be calibrated.',
    saveCalibration: 'Save Calibration',
    decisionLog: 'Intervention Log',
    currentLens: 'Current Lens',
    interveneShortcut: 'Write Disturbance',
    next: 'Next: reveal the next node',
    finish: 'Enter Archive Afterimage',
    submitAction: 'Run Replay',
    replaying: 'Bending worldline...',
    inputPlaceholder: 'Write an observation, correction, intervention, or preference constraint.',
    observatoryNote: 'Read how the node holds before deciding whether to touch it.',
    surfaces: {
      observatory: { index: '01', label: 'Observatory', title: 'Read how the line holds.', blurb: 'Branches are not conclusions. They are tracks produced by conditions, rules, materials, and constraints.' },
      intervention: { index: '02', label: 'Intervention', title: 'Declare your disturbance.', blurb: 'Intervention changes later tracks; observation and correction only touch their declared layers.' },
      cost: { index: '03', label: 'Cost Lens', title: 'See where pressure lands.', blurb: 'Rules, materials, environments, and actors can all carry cost.' },
      ripple: { index: '04', label: 'Ripple', title: 'Watch the bend travel downstream.', blurb: 'Ripple is not a report summary. It is continuity between nodes.' },
      archive: { index: '05', label: 'Archive', title: 'Keep the afterimage.', blurb: 'Share text, interventions, and actual outcomes meet here.' },
    },
    layers: {
      FACT: { title: 'Fact Layer', note: 'Visible events, materials, objects, and traces only.' },
      INFERENCE: { title: 'Inference Layer', note: 'Why a branch holds, and which signals pull against it.' },
      VALUE: { title: 'Value Layer', note: 'Who carries cost, who gains slack, and how rules distribute pressure.' },
      ACTION: { title: 'Action Layer', note: 'How the observer disturbs the line and where replay begins.' },
    },
    inputs: {
      observation: { label: 'Observation', note: 'Adds evidence and material without directly mutating the world state.' },
      correction: { label: 'Correction', note: 'Corrects the fact layer and forces branches to restabilize.' },
      intervention: { label: 'Intervention', note: 'Changes the worldline itself and unfolds again from this node.' },
      preference: { label: 'Preference Constraint', note: 'Changes value ranking without pretending to rewrite facts.' },
    },
    calibrationResults: {
      hit: 'Hit',
      partial: 'Partial',
      miss: 'Miss',
      insufficient_data: 'Insufficient Data',
    },
  },
} satisfies Record<DisplayLanguage, {
  kicker: string
  live: string
  readout: string
  loading: string
  summaryFallback: string
  progressLabel: string
  progressHint: string
  progressComplete: string
  layerLabel: string
  singularityLabel: string
  singularityNote: string
  nextGhost: string
  selectedEvent: string
  actantLabel: string
  branchField: string
  primary: string
  alternate: string
  premises: string
  costLabel: string
  rippleLabel: string
  passiveFloor: string
  worldlineTrack: string
  archiveLabel: string
  shareAction: string
  calibrationLabel: string
  openCalibration: string
  hideCalibration: string
  calibrationPlaceholder: string
  saveCalibration: string
  decisionLog: string
  currentLens: string
  interveneShortcut: string
  next: string
  finish: string
  submitAction: string
  replaying: string
  inputPlaceholder: string
  observatoryNote: string
  surfaces: Record<SurfaceKey, { index: string; label: string; title: string; blurb: string }>
  layers: Record<KnowledgeLayer, { title: string; note: string }>
  inputs: Record<InputType, { label: string; note: string }>
  calibrationResults: Record<CalibrationRecord['result'], string>
}>

const processCopy = {
  zh: {
    processLabel: '后台过程文件',
    stepLabel: '显影层',
    fileLabel: 'runtime artifact',
    confidenceLabel: '置信',
    costMassLabel: '代价质量',
    counterSignalLabel: '反向信号',
    inputsLabel: '输入材料',
    outputsLabel: '输出结果',
    interventionWindow: '可介入窗口',
    openInterventionWindow: '从这里介入',
  },
  en: {
    processLabel: 'Process File',
    stepLabel: 'Exposure',
    fileLabel: 'runtime artifact',
    confidenceLabel: 'confidence',
    costMassLabel: 'cost mass',
    counterSignalLabel: 'counter-signals',
    inputsLabel: 'inputs',
    outputsLabel: 'outputs',
    interventionWindow: 'Intervention Window',
    openInterventionWindow: 'Intervene Here',
  },
} satisfies Record<DisplayLanguage, {
  processLabel: string
  stepLabel: string
  fileLabel: string
  confidenceLabel: string
  costMassLabel: string
  counterSignalLabel: string
  inputsLabel: string
  outputsLabel: string
  interventionWindow: string
  openInterventionWindow: string
}>

const progressSaveCopy = {
  zh: {
    idle: '阅读书签待同步',
    saving: '正在保存阅读书签',
    saved: '阅读书签已保存',
    failed: '书签暂存本地',
  },
  en: {
    idle: 'bookmark pending',
    saving: 'saving bookmark',
    saved: 'bookmark saved',
    failed: 'bookmark local only',
  },
} satisfies Record<DisplayLanguage, Record<'idle' | 'saving' | 'saved' | 'failed', string>>

const instrumentCopy = {
  zh: {
    rippleConsole: '回响控制台',
    rippleConsoleHint: '这一组读数来自当前已经显影的轨道，不需要等待新的模型调用。',
    rippleAfterimage: '回响残影',
    archiveCapsule: '残影胶囊',
    revealedNodes: '已显影节点',
    alternatePressure: '替代压力',
    savedSets: '已存重演',
    meanConfidence: '平均置信',
    decisions: '干涉记录',
    calibrations: '校准记录',
    rippleCards: '回响片段',
    exportRipple: '导出回响轨迹包',
    copyCapsule: '复制胶囊文本',
    exportCapsule: '导出残影胶囊',
    exportReady: '本地文件已生成',
    copyReady: '胶囊文本已复制',
    copyUnavailable: '剪贴板不可用，可改用导出',
  },
  en: {
    rippleConsole: 'Ripple Console',
    rippleConsoleHint: 'These readings come from the revealed track; no fresh model call is needed.',
    rippleAfterimage: 'Ripple Afterimage',
    archiveCapsule: 'Afterimage Capsule',
    revealedNodes: 'revealed nodes',
    alternatePressure: 'alternate pressure',
    savedSets: 'saved replays',
    meanConfidence: 'mean confidence',
    decisions: 'decision marks',
    calibrations: 'calibrations',
    rippleCards: 'ripple cards',
    exportRipple: 'Export Ripple Trace',
    copyCapsule: 'Copy Capsule Text',
    exportCapsule: 'Export Afterimage Capsule',
    exportReady: 'local file generated',
    copyReady: 'capsule text copied',
    copyUnavailable: 'clipboard unavailable; export instead',
  },
} satisfies Record<DisplayLanguage, {
  rippleConsole: string
  rippleConsoleHint: string
  rippleAfterimage: string
  archiveCapsule: string
  revealedNodes: string
  alternatePressure: string
  savedSets: string
  meanConfidence: string
  decisions: string
  calibrations: string
  rippleCards: string
  exportRipple: string
  copyCapsule: string
  exportCapsule: string
  exportReady: string
  copyReady: string
  copyUnavailable: string
}>

const t = computed(() => theatreCopy[language.value])
const processText = computed(() => processCopy[language.value])
const instrumentText = computed(() => instrumentCopy[language.value])
const progressSaveLabel = computed(() => progressSaveCopy[language.value][progressSaveState.value])
const events = computed(() => stage.value?.observatory.key_events ?? [])
const revealedEvents = computed(() => events.value.slice(0, Math.min(revealedCount.value, events.value.length)))
const revealedIds = computed(() => new Set(revealedEvents.value.map((event) => event.event_id)))
const progressComplete = computed(() => events.value.length > 0 && revealedCount.value >= events.value.length)
const stageProgress = computed(() => (events.value.length === 0 ? 0 : Math.min(1, revealedCount.value / events.value.length)))

const selectedEvent = computed(() => (
  revealedEvents.value.find((event) => event.event_id === selectedEventId.value)
  ?? revealedEvents.value.at(-1)
  ?? null
))
const selectedBranch = computed<Branch | null>(() => selectedEvent.value?.branches.find((branch) => branch.branch_id === selectedBranchId.value) ?? selectedEvent.value?.branches[0] ?? null)
const selectedLenses = computed<CostLens[]>(() => stage.value?.cost_lens.lenses.filter((lens) => lens.target_branch_id === selectedBranchId.value) ?? [])
const latestBend = computed(() => cleanText(replaySummary.value || stage.value?.ripple.latest_bend || t.value.progressHint))
const currentCosts = computed(() => selectedLenses.value.flatMap((lens) => [...lens.first_order_costs, ...lens.second_order_costs]).map(cleanText).slice(0, 4))
const visibleRippleCards = computed(() => stage.value?.ripple.ripple_cards.slice(0, revealedCount.value) ?? [])
const revealedTrack = computed(() => stage.value?.observatory.worldline_track.filter((track) => revealedIds.value.has(track.event_id)) ?? [])
const savedReplayCount = computed(() => stage.value?.ripple.saved_replay_sets.length ?? 0)
const averageRevealedConfidence = computed(() => {
  if (revealedTrack.value.length === 0) return 0
  return revealedTrack.value.reduce((total, track) => total + track.confidence, 0) / revealedTrack.value.length
})
const alternatePressure = computed(() => revealedEvents.value.reduce((total, event) => (
  total + event.branches.filter((branch) => branch.visibility === 'alternate').length
), 0))
const rippleMetrics = computed(() => [
  { value: `${revealedTrack.value.length}/${events.value.length || 0}`, label: instrumentText.value.revealedNodes },
  { value: String(alternatePressure.value), label: instrumentText.value.alternatePressure },
  { value: String(savedReplayCount.value), label: instrumentText.value.savedSets },
  { value: formatConfidence(averageRevealedConfidence.value), label: instrumentText.value.meanConfidence },
])
const archiveMetrics = computed(() => [
  { value: `${revealedTrack.value.length}/${events.value.length || 0}`, label: instrumentText.value.revealedNodes },
  { value: String(stage.value?.archive.player_decision_log.length ?? 0), label: instrumentText.value.decisions },
  { value: String(stage.value?.archive.calibration_summary.count ?? stage.value?.archive.calibration_records.length ?? 0), label: instrumentText.value.calibrations },
  { value: String(visibleRippleCards.value.length), label: instrumentText.value.rippleCards },
])
const processSteps = computed(() => stage.value?.process_trace.steps ?? [])
const currentProcessStep = computed(() => processSteps.value.find((step) => step.event_id === selectedEventId.value) ?? null)
const processStepIndex = computed(() => Math.max(1, processSteps.value.findIndex((step) => step.event_id === currentProcessStep.value?.event_id) + 1))
const selectedProcessLayer = computed(() => (
  currentProcessStep.value?.layer_results.find((layer) => layer.layer === selectedLayer.value)
  ?? currentProcessStep.value?.layer_results[0]
  ?? null
))
const activeSurfaceCopy = computed(() => t.value.surfaces[activeSurface.value])
const nextActionLabel = computed(() => (progressComplete.value ? t.value.finish : t.value.next))
const interventionPlaceholder = computed(() => cleanText(currentProcessStep.value?.intervention_window.prompt ?? t.value.inputPlaceholder))

const availableLayers = computed<KnowledgeLayer[]>(() => {
  const layers = stage.value?.observatory.knowledge_layers ?? []
  return layers.filter((layer): layer is KnowledgeLayer => layer === 'FACT' || layer === 'INFERENCE' || layer === 'VALUE' || layer === 'ACTION')
})

const surfaces = computed(() => surfaceKeys.map((key) => ({
  key,
  index: t.value.surfaces[key].index,
  label: t.value.surfaces[key].label,
})))

const focusTags = computed(() => (selectedEvent.value?.affected_entities ?? []).map(cleanText).slice(0, 5))

const layerHighlights = computed(() => {
  if (!selectedEvent.value || !selectedBranch.value) return []

  if (selectedLayer.value === 'FACT') {
    return [...selectedEvent.value.affected_entities, ...selectedEvent.value.evidence_notes].map(cleanText).slice(0, 4)
  }

  if (selectedLayer.value === 'INFERENCE') {
    return [...selectedBranch.value.premises, ...selectedBranch.value.signals_for].map(cleanText).slice(0, 4)
  }

  if (selectedLayer.value === 'VALUE') {
    return [
      ...selectedLenses.value.flatMap((lens) => lens.affected_groups),
      ...selectedLenses.value.flatMap((lens) => lens.ethical_notes),
      stage.value?.cost_lens.passive_floor.summary ?? '',
    ].filter(Boolean).map(cleanText).slice(0, 4)
  }

  return [
    t.value.inputs[currentInputType.value].note,
    selectedBranch.value.player_influence,
    latestBend.value,
  ].filter(Boolean).map(cleanText).slice(0, 4)
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
    syncSelection(nextStage, activeSurface.value, true)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  } finally {
    loading.value = false
  }
}

function syncSelection(nextStage: StageData, nextSurface = activeSurface.value, restoreProgress = false) {
  stage.value = nextStage
  activeSurface.value = restoreProgress ? nextStage.surface_defaults.active_surface : nextSurface
  shareSnapshot.value = nextStage.archive.share_snapshot

  const nextEvents = nextStage.observatory.key_events
  const preferredRevealCount = restoreProgress
    ? nextStage.surface_defaults.revealed_event_count
    : revealedCount.value
  revealedCount.value = Math.max(1, Math.min(preferredRevealCount, nextEvents.length || 1))

  const visibleEvents = nextEvents.slice(0, revealedCount.value)
  const preferredEventId = restoreProgress ? nextStage.surface_defaults.selected_event_id : selectedEventId.value
  const nextEvent = visibleEvents.find((event) => event.event_id === preferredEventId)
    ?? visibleEvents.find((event) => event.event_id === nextStage.surface_defaults.selected_event_id)
    ?? visibleEvents[visibleEvents.length - 1]
    ?? nextEvents[0]

  selectEvent(nextEvent, restoreProgress ? nextStage.surface_defaults.selected_branch_id : undefined)
  progressSaveState.value = nextStage.surface_defaults.progress_saved_at ? 'saved' : progressSaveState.value

  if (!availableLayers.value.includes(selectedLayer.value)) {
    selectedLayer.value = availableLayers.value[0] ?? 'FACT'
  }

  if (!nextStage.intervention.available_input_types.includes(currentInputType.value)) {
    currentInputType.value = nextStage.intervention.available_input_types[0] ?? 'intervention'
  }
}

function selectEvent(event?: StageData['observatory']['key_events'][number], preferredBranchId?: string) {
  if (!event) return
  selectedEventId.value = event.event_id
  const rememberedBranchId = branchMemory.value[event.event_id]
  const nextBranch = event.branches.find((branch) => branch.branch_id === preferredBranchId)
    ?? event.branches.find((branch) => branch.branch_id === rememberedBranchId)
    ?? event.branches.find((branch) => branch.visibility === 'primary')
    ?? event.branches[0]
  selectedBranchId.value = nextBranch?.branch_id ?? ''
}

function advanceWorldline() {
  if (!stage.value || events.value.length === 0) return

  if (revealedCount.value < events.value.length) {
    const nextEvent = events.value[revealedCount.value]
    revealedCount.value += 1
    selectEvent(nextEvent)
    activeSurface.value = revealedCount.value === events.value.length ? 'ripple' : 'observatory'
  } else {
    activeSurface.value = 'archive'
  }

  pulseKey.value += 1
  void persistTheatreProgress()
}

function handleSelectEvent(eventId: string, persist = true) {
  const index = events.value.findIndex((event) => event.event_id === eventId)
  if (index < 0) return
  if (index + 1 > revealedCount.value) revealedCount.value = index + 1
  selectEvent(events.value[index])
  if (persist) void persistTheatreProgress()
}

function handleSelectBranch(eventId: string, branchId: string, persist = true) {
  selectedEventId.value = eventId
  selectedBranchId.value = branchId
  branchMemory.value = {
    ...branchMemory.value,
    [eventId]: branchId,
  }
  if (persist) void persistTheatreProgress()
}

function handleModeChange(mode: InputType) {
  currentInputType.value = mode
  selectedLayer.value = 'ACTION'
}

function handleSurfaceChange(surface: SurfaceKey) {
  activeSurface.value = surface
  exportFeedback.value = ''
  void persistTheatreProgress({ active_surface: surface })
}

function openProcessIntervention(step: StageData['process_trace']['steps'][number]) {
  handleSelectEvent(step.intervention_window.target_event_id, false)
  handleSelectBranch(step.intervention_window.target_event_id, step.intervention_window.target_branch_id, false)
  currentInputType.value = step.intervention_window.recommended_input_type
  selectedLayer.value = 'ACTION'
  activeSurface.value = 'intervention'
  void persistTheatreProgress()
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
    void persistTheatreProgress({ active_surface: response.replay_result ? 'ripple' : 'observatory' })
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
    handleSurfaceChange('archive')
    if (navigator.clipboard) {
      try {
        await navigator.clipboard.writeText(cleanText(artifact.share_text))
      } catch {
        // Clipboard permission can fail; the artifact still remains visible in the drawer.
      }
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  }
}

function exportRippleTrace() {
  downloadTextFile(
    `${safeFileStem(stage.value?.project_context.project_id ?? 'miroworld')}-ripple-trace.json`,
    JSON.stringify(buildRippleTracePacket(), null, 2),
    'application/json;charset=utf-8',
  )
  exportFeedback.value = instrumentText.value.exportReady
}

async function copyArchiveCapsule() {
  if (!navigator.clipboard) {
    exportFeedback.value = instrumentText.value.copyUnavailable
    return
  }

  try {
    await navigator.clipboard.writeText(buildArchiveCapsuleText())
    exportFeedback.value = instrumentText.value.copyReady
  } catch {
    exportFeedback.value = instrumentText.value.copyUnavailable
  }
}

function exportArchiveCapsule() {
  downloadTextFile(
    `${safeFileStem(stage.value?.project_context.project_id ?? 'miroworld')}-afterimage-capsule.json`,
    JSON.stringify(buildArchiveCapsulePacket(), null, 2),
    'application/json;charset=utf-8',
  )
  exportFeedback.value = instrumentText.value.exportReady
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
    void persistTheatreProgress({ active_surface: 'archive' })
    calibrationDraft.value = ''
    calibrationOpen.value = false
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : String(error)
  }
}

async function persistTheatreProgress(overrides: Partial<Pick<TheatreProgress, 'revealed_event_count' | 'selected_event_id' | 'selected_branch_id' | 'active_surface'>> = {}) {
  if (!stage.value || !selectedEvent.value || !selectedBranch.value) return

  const payload = {
    revealed_event_count: overrides.revealed_event_count ?? revealedCount.value,
    selected_event_id: overrides.selected_event_id ?? selectedEvent.value.event_id,
    selected_branch_id: overrides.selected_branch_id ?? selectedBranch.value.branch_id,
    active_surface: overrides.active_surface ?? activeSurface.value,
    language: language.value,
  }
  const revision = ++progressSaveRevision
  progressSaveState.value = 'saving'

  try {
    const projectId = route.params.projectId as string
    const saved = await saveTheatreProgress(projectId, payload)
    if (revision !== progressSaveRevision) return
    progressSaveState.value = 'saved'
    if (stage.value) {
      stage.value.surface_defaults = {
        selected_event_id: saved.selected_event_id,
        selected_branch_id: saved.selected_branch_id,
        active_surface: saved.active_surface,
        revealed_event_count: saved.revealed_event_count,
        progress_saved_at: saved.updated_at,
      }
    }
  } catch {
    if (revision === progressSaveRevision) {
      progressSaveState.value = 'failed'
    }
  }
}

function cleanText(value?: string | null) {
  if (!value) return ''
  return textReplacements.reduce((next, [pattern, replacement]) => next.replace(pattern, replacement), value)
}

function buildRippleTracePacket() {
  return {
    kind: 'miroworld.ripple_trace',
    version: 1,
    generated_at: new Date().toISOString(),
    language: language.value,
    project: stage.value?.project_context ?? null,
    selected_event: selectedEvent.value
      ? {
          event_id: selectedEvent.value.event_id,
          title: cleanText(selectedEvent.value.title),
          stage: cleanText(selectedEvent.value.stage),
        }
      : null,
    selected_branch: selectedBranch.value
      ? {
          branch_id: selectedBranch.value.branch_id,
          label: cleanText(selectedBranch.value.label),
          confidence: selectedBranch.value.effective_confidence ?? selectedBranch.value.confidence,
          cost_hint: cleanText(selectedBranch.value.cost_hint),
        }
      : null,
    metrics: rippleMetrics.value,
    latest_bend: latestBend.value,
    revealed_track: revealedTrack.value.map((track) => ({
      event_id: track.event_id,
      title: cleanText(track.title),
      stage: cleanText(track.stage),
      branch_id: track.primary_branch_id,
      branch_label: cleanText(track.primary_branch_label),
      confidence: track.confidence,
    })),
    ripple_cards: visibleRippleCards.value.map((card) => ({
      title: cleanText(card.title),
      branch_label: cleanText(card.branch_label),
      summary: cleanText(card.summary),
    })),
    saved_replay_sets: stage.value?.ripple.saved_replay_sets.map((set) => ({
      replay_set_id: set.replay_set_id,
      replay_set_label: cleanText(set.replay_set_label),
      focus: set.focus,
      metrics: set.metrics,
      saved_at: set.saved_at,
    })) ?? [],
  }
}

function buildArchiveCapsulePacket() {
  const snapshot = shareSnapshot.value
  return {
    kind: 'miroworld.afterimage_capsule',
    version: 1,
    generated_at: new Date().toISOString(),
    language: language.value,
    project: stage.value?.project_context ?? null,
    share_snapshot: snapshot
      ? {
          title: cleanText(snapshot.title),
          subtitle: cleanText(snapshot.subtitle),
          summary: cleanText(snapshot.summary),
          short_excerpt: cleanText(snapshot.short_excerpt),
          curator_note: cleanText(snapshot.curator_note),
          wall_label: cleanText(snapshot.wall_label),
          archive_summary: cleanText(snapshot.archive_summary),
          disclaimer: cleanText(snapshot.disclaimer),
          tags: snapshot.tags.map(cleanText),
        }
      : null,
    selected_event: selectedEvent.value
      ? {
          event_id: selectedEvent.value.event_id,
          title: cleanText(selectedEvent.value.title),
          impact_level: selectedEvent.value.impact_level,
        }
      : null,
    selected_branch: selectedBranch.value
      ? {
          branch_id: selectedBranch.value.branch_id,
          label: cleanText(selectedBranch.value.label),
          confidence: selectedBranch.value.effective_confidence ?? selectedBranch.value.confidence,
          cost_hint: cleanText(selectedBranch.value.cost_hint),
        }
      : null,
    metrics: archiveMetrics.value,
    revealed_track: revealedTrack.value.map((track) => ({
      event_id: track.event_id,
      title: cleanText(track.title),
      branch_label: cleanText(track.primary_branch_label),
      confidence: track.confidence,
    })),
    decision_log: stage.value?.archive.player_decision_log.map((entry) => ({
      entry_id: entry.entry_id,
      created_at: entry.created_at,
      input_type: entry.input_type,
      event_title: cleanText(entry.event_title),
      branch_label: cleanText(entry.branch_label),
      content: cleanText(entry.content),
      replay_summary: cleanText(entry.replay_summary),
      cost_changes: entry.cost_changes.map(cleanText),
    })) ?? [],
    calibration_summary: stage.value?.archive.calibration_summary ?? null,
    calibration_records: stage.value?.archive.calibration_records ?? [],
  }
}

function buildArchiveCapsuleText() {
  const packet = buildArchiveCapsulePacket()
  const snapshot = packet.share_snapshot
  const lines = [
    snapshot?.title ?? 'MiroWorld afterimage',
    snapshot?.summary ?? '',
    '',
    `${instrumentText.value.revealedNodes}: ${archiveMetrics.value[0]?.value ?? '0'}`,
    `${instrumentText.value.decisions}: ${archiveMetrics.value[1]?.value ?? '0'}`,
    `${instrumentText.value.calibrations}: ${archiveMetrics.value[2]?.value ?? '0'}`,
    '',
    packet.revealed_track.map((track) => `${track.title} / ${track.branch_label} / ${formatConfidence(track.confidence)}`).join('\n'),
    '',
    snapshot?.disclaimer ?? '',
  ]
  return lines.filter((line) => line !== '').join('\n')
}

function downloadTextFile(filename: string, content: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType })
  const href = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = href
  link.download = filename
  link.rel = 'noopener'
  link.click()
  URL.revokeObjectURL(href)
}

function safeFileStem(value: string) {
  return cleanText(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48) || 'miroworld'
}

function formatConfidence(value: number) {
  return `${Math.round(value * 100)}%`
}

function orbitNodeStyle(index: number, total: number) {
  const denominator = Math.max(total - 1, 1)
  const angle = -126 + (252 * index) / denominator
  const distance = 34 + (index % 3) * 6
  return {
    '--orbit-angle': `${angle}deg`,
    '--orbit-counter-angle': `${-angle}deg`,
    '--orbit-distance': `${distance}%`,
    '--orbit-delay': `${index * 80}ms`,
  } as Record<string, string>
}
</script>
