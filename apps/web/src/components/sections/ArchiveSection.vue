<template>
  <section class="scene-section archive-section" data-testid="archive-section">
    <div class="archive-actions">
      <div class="archive-action-group">
        <button type="button" class="primary-action" @click="$emit('share')">{{ copy.share }}</button>
        <button type="button" class="secondary-action" @click="$emit('toggle-calibration')">
          {{ calibrationOpen ? copy.hideCalibration : copy.openCalibration }}
        </button>
      </div>
      <div class="archive-action-group">
        <button type="button" class="ghost-action" data-testid="download-poster" @click="downloadPoster">
          {{ copy.downloadPoster }}
        </button>
        <button type="button" class="ghost-action" data-testid="download-poster-png" @click="downloadPosterPng">
          {{ copy.downloadPosterPng }}
        </button>
        <button type="button" class="ghost-action" data-testid="download-bundle" @click="downloadBundle">
          {{ copy.downloadBundle }}
        </button>
        <button type="button" class="ghost-action" data-testid="download-exhibit" @click="downloadExhibitHtml">
          {{ copy.downloadExhibitHtml }}
        </button>
        <button type="button" class="ghost-action" data-testid="download-artifact-bundle" @click="downloadArtifactBundle">
          {{ copy.downloadArtifactBundle }}
        </button>
      </div>
    </div>
    <small v-if="archiveFeedback" class="archive-status">{{ archiveFeedback }}</small>

    <div class="archive-grid">
      <div class="archive-main">
        <article class="poster-artifact-card">
          <span class="annotation-label">{{ copy.posterArtifact }}</span>
          <div class="poster-artifact-shell">
            <div class="poster-artifact-body">
              <p class="poster-artifact-brand">MIROWORLD</p>
              <h3>{{ shareSnapshot.title }}</h3>
              <p class="poster-artifact-summary">{{ shareSnapshot.summary }}</p>
              <p class="poster-artifact-caption">{{ shareSnapshot.poster_caption }}</p>

              <div class="share-tag-row">
                <span v-for="tag in shareSnapshot.tags" :key="tag" class="share-tag">{{ tag }}</span>
              </div>
            </div>

            <aside class="poster-artifact-side">
              <span class="annotation-label">{{ copy.wallLabel }}</span>
              <p>{{ shareSnapshot.wall_label }}</p>
              <span class="annotation-label">{{ copy.curatorNote }}</span>
              <p>{{ shareSnapshot.curator_note || shareSnapshot.short_excerpt }}</p>
            </aside>
          </div>
        </article>

        <div class="share-detail-grid">
          <article class="share-card export-card">
            <span class="annotation-label">{{ copy.posterCaption }}</span>
            <p>{{ shareSnapshot.poster_caption }}</p>
            <button type="button" class="ghost-action" @click="copyText(copy.copyPosterCaption, shareSnapshot.poster_caption)">
              {{ copy.copyPosterCaption }}
            </button>
          </article>

          <article class="share-card export-card">
            <span class="annotation-label">{{ copy.shortExcerpt }}</span>
            <p>{{ shareSnapshot.short_excerpt }}</p>
            <button type="button" class="ghost-action" @click="copyText(copy.copyWallLabel, shareSnapshot.wall_label)">
              {{ copy.copyWallLabel }}
            </button>
          </article>

          <article class="share-card export-card">
            <span class="annotation-label">{{ copy.archiveSummary }}</span>
            <p>{{ shareSnapshot.archive_summary }}</p>
          </article>
        </div>

        <article class="share-card share-text-card">
          <div class="share-card-header">
            <span class="annotation-label">{{ copy.shareText }}</span>
            <button type="button" class="ghost-action" @click="copyText(copy.copyShareText, shareSnapshot.share_text)">
              {{ copy.copyShareText }}
            </button>
          </div>
          <p class="share-text-body">{{ shareSnapshot.share_text }}</p>
          <small v-if="copyFeedback" class="copy-feedback">{{ copyFeedback }}</small>
        </article>
      </div>

      <aside class="archive-side">
        <article class="annotation-block archive-panel">
          <span class="annotation-label">{{ copy.decisionLog }}</span>
          <div class="archive-log">
            <article v-for="entry in decisionLog" :key="entry.entry_id" class="archive-entry">
              <span>{{ entry.input_type }}</span>
              <strong>{{ entry.event_title }}</strong>
              <small>{{ formatTimestamp(entry.created_at) }}</small>
              <p>{{ entry.content }}</p>
              <small>{{ entry.replay_summary }}</small>
              <small v-if="entry.cost_changes.length">{{ entry.cost_changes.join(' / ') }}</small>
            </article>
          </div>
        </article>

        <article class="annotation-block archive-panel">
          <span class="annotation-label">{{ copy.calibrationPattern }}</span>
          <span class="annotation-label">{{ copy.calibrationAtlas }}</span>
          <div class="calibration-atlas-grid" data-testid="calibration-atlas">
            <article v-for="item in calibrationAtlasCards" :key="item.label" class="calibration-atlas-card">
              <span class="annotation-label">{{ item.label }}</span>
              <strong>{{ item.value }}</strong>
              <p>{{ item.note }}</p>
            </article>
          </div>
          <div class="calibration-meter">
            <div
              v-for="segment in calibrationSegments"
              :key="segment.key"
              class="calibration-meter-segment"
              :class="`result-${segment.key}`"
              :style="{ flexGrow: segment.count || 1 }"
            >
              <span>{{ segment.label }}</span>
              <strong>{{ segment.count }}</strong>
            </div>
          </div>
          <div class="calibration-pattern-row">
            <span
              v-for="record in sortedCalibrationRecords.slice(0, 12)"
              :key="record.calibration_id"
              class="calibration-pattern-dot"
              :class="`result-${record.result}`"
              :title="`${mapResultLabel(record.result)} / ${record.actual_outcome}`"
            ></span>
          </div>
          <div class="calibration-comparison-stack">
            <div class="calibration-comparison-row">
              <span>{{ copy.recentWindow }}</span>
              <div class="calibration-comparison-bar">
                <span
                  v-for="segment in recentCalibrationSegments"
                  :key="`recent-${segment.key}`"
                  class="calibration-comparison-segment"
                  :class="`result-${segment.key}`"
                  :style="{ flexGrow: segment.count || 1 }"
                >
                  <small>{{ segment.count }}</small>
                </span>
              </div>
            </div>
            <div class="calibration-comparison-row">
              <span>{{ copy.fullArchive }}</span>
              <div class="calibration-comparison-bar">
                <span
                  v-for="segment in calibrationSegments"
                  :key="`full-${segment.key}`"
                  class="calibration-comparison-segment"
                  :class="`result-${segment.key}`"
                  :style="{ flexGrow: segment.count || 1 }"
                >
                  <small>{{ segment.count }}</small>
                </span>
              </div>
            </div>
          </div>
          <p>{{ calibrationSummary.summary }}</p>
        </article>

        <article class="annotation-block archive-panel">
          <span class="annotation-label">{{ copy.calibrationHistory }}</span>
          <div class="calibration-record-list">
            <article v-for="record in sortedCalibrationRecords.slice(0, 4)" :key="record.calibration_id" class="calibration-record">
              <strong>{{ mapResultLabel(record.result) }}</strong>
              <small>{{ formatTimestamp(record.created_at) }}</small>
              <p>{{ record.actual_outcome }}</p>
            </article>
            <p v-if="calibrationRecords.length === 0" class="archive-empty">{{ copy.actualOutcomePlaceholder }}</p>
          </div>
        </article>
      </aside>
    </div>

    <div v-if="calibrationOpen" class="calibration-drawer" data-testid="calibration-drawer">
      <p>{{ calibrationSummary.summary }}</p>
      <select :value="calibrationResult" class="calibration-field" @change="$emit('update:calibrationResult', ($event.target as HTMLSelectElement).value)">
        <option value="hit">hit</option>
        <option value="partial">partial</option>
        <option value="miss">miss</option>
        <option value="insufficient_data">insufficient_data</option>
      </select>
      <textarea
        :value="calibrationDraft"
        class="intervention-input"
        :placeholder="copy.actualOutcomePlaceholder"
        @input="$emit('update:calibrationDraft', ($event.target as HTMLTextAreaElement).value)"
      ></textarea>
      <button type="button" class="primary-action" @click="$emit('save-calibration')">{{ copy.saveCalibration }}</button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

import type { CalibrationRecord, ShareArtifact } from '@/lib/types'

const props = defineProps<{
  shareSnapshot: ShareArtifact
  decisionLog: Array<{
    entry_id: string
    created_at: string
    input_type: string
    event_id: string
    event_title: string
    branch_id: string
    branch_label: string
    content: string
    replay_summary: string
    cost_changes: string[]
  }>
  calibrationSummary: {
    summary: string
  }
  calibrationRecords: CalibrationRecord[]
  calibrationOpen: boolean
  calibrationDraft: string
  calibrationResult: string
  projectId: string
  copy: {
    share: string
    openCalibration: string
    hideCalibration: string
    saveCalibration: string
    actualOutcomePlaceholder: string
    decisionLog: string
    curatorNote: string
    shareText: string
    wallLabel: string
    archiveSummary: string
    calibrationHistory: string
    posterArtifact: string
    posterCaption: string
    shortExcerpt: string
    copyWallLabel: string
    copyPosterCaption: string
    copyShareText: string
    calibrationPattern: string
    downloadPoster: string
    downloadPosterPng: string
    downloadBundle: string
    downloadExhibitHtml: string
    downloadArtifactBundle: string
    calibrationAtlas: string
    dominantOutcome: string
    recentTendency: string
    mostTestedBranch: string
    recentWindow: string
    fullArchive: string
    tendencyStrengthening: string
    tendencySlipping: string
    tendencyHolding: string
    thinArchive: string
    noBranchFocus: string
    hit: string
    partial: string
    miss: string
    insufficient_data: string
  }
}>()

defineEmits<{
  share: []
  'toggle-calibration': []
  'update:calibrationDraft': [value: string]
  'update:calibrationResult': [value: string]
  'save-calibration': []
}>()

const copyFeedback = ref('')
const archiveFeedback = ref('')

const sortedCalibrationRecords = computed(() => [...props.calibrationRecords].sort((left, right) => (
  new Date(right.created_at).getTime() - new Date(left.created_at).getTime()
)))

const recentCalibrationRecords = computed(() => sortedCalibrationRecords.value.slice(0, 4))

const calibrationSegments = computed(() => {
  return buildResultSegments(sortedCalibrationRecords.value)
})

const recentCalibrationSegments = computed(() => {
  return buildResultSegments(recentCalibrationRecords.value)
})

const calibrationAtlasCards = computed(() => {
  const total = sortedCalibrationRecords.value.length
  const dominant = calibrationSegments.value.reduce((best, segment) => (
    segment.count > best.count ? segment : best
  ), calibrationSegments.value[0])
  const branchCounts = new Map<string, { count: number, label: string }>()
  const branchLabels = new Map(props.decisionLog.map((entry) => [entry.branch_id, entry.branch_label]))
  const recentScore = scoreWindow(recentCalibrationRecords.value)
  const priorWindow = sortedCalibrationRecords.value.slice(4, 8)
  const priorScore = priorWindow.length ? scoreWindow(priorWindow) : recentScore
  const delta = recentScore - priorScore

  for (const record of sortedCalibrationRecords.value) {
    const label = branchLabels.get(record.branch_id) ?? record.branch_id
    const current = branchCounts.get(record.branch_id) ?? { count: 0, label }
    current.count += 1
    branchCounts.set(record.branch_id, current)
  }

  const mostTestedBranch = [...branchCounts.values()].sort((left, right) => right.count - left.count)[0]

  return [
    {
      label: props.copy.dominantOutcome,
      value: total ? dominant.label : props.copy.thinArchive,
      note: total ? `${dominant.count} / ${total}` : props.calibrationSummary.summary,
    },
    {
      label: props.copy.recentTendency,
      value: describeTendency(delta, total),
      note: total
        ? `${props.copy.recentWindow}: ${recentCalibrationRecords.value.length} / ${props.copy.fullArchive}: ${total}`
        : props.calibrationSummary.summary,
    },
    {
      label: props.copy.mostTestedBranch,
      value: mostTestedBranch?.label ?? props.copy.noBranchFocus,
      note: mostTestedBranch ? `${mostTestedBranch.count} / ${total}` : props.calibrationSummary.summary,
    },
  ]
})

function buildResultSegments(records: CalibrationRecord[]) {
  const counts = {
    hit: 0,
    partial: 0,
    miss: 0,
    insufficient_data: 0,
  }

  for (const record of records) {
    counts[record.result] += 1
  }

  return [
    { key: 'hit', count: counts.hit, label: props.copy.hit },
    { key: 'partial', count: counts.partial, label: props.copy.partial },
    { key: 'miss', count: counts.miss, label: props.copy.miss },
    { key: 'insufficient_data', count: counts.insufficient_data, label: props.copy.insufficient_data },
  ] as const
}

async function copyText(label: string, text: string) {
  copyFeedback.value = ''
  if (!navigator.clipboard) return
  try {
    await navigator.clipboard.writeText(text)
    copyFeedback.value = label
  } catch {
    copyFeedback.value = ''
  }
}

function downloadPoster() {
  archiveFeedback.value = ''
  downloadFile(`${safeFileStem(props.projectId)}-poster.svg`, buildPosterSvg(), 'image/svg+xml;charset=utf-8')
  archiveFeedback.value = props.copy.downloadPoster
}

async function downloadPosterPng() {
  archiveFeedback.value = ''
  try {
    const pngDataUrl = await buildPosterPngDataUrl()
    downloadDataUrl(`${safeFileStem(props.projectId)}-poster.png`, pngDataUrl)
    archiveFeedback.value = props.copy.downloadPosterPng
  } catch {
    downloadPoster()
  }
}

function downloadBundle() {
  archiveFeedback.value = ''
  downloadFile(`${safeFileStem(props.projectId)}-share.txt`, buildShareBundle(), 'text/plain;charset=utf-8')
  archiveFeedback.value = props.copy.downloadBundle
}

function downloadExhibitHtml() {
  archiveFeedback.value = ''
  downloadFile(`${safeFileStem(props.projectId)}-exhibit.html`, buildExhibitHtml(), 'text/html;charset=utf-8')
  archiveFeedback.value = props.copy.downloadExhibitHtml
}

function downloadArtifactBundle() {
  archiveFeedback.value = ''
  downloadFile(
    `${safeFileStem(props.projectId)}-artifact-bundle.json`,
    buildArtifactBundle(),
    'application/json;charset=utf-8',
  )
  archiveFeedback.value = props.copy.downloadArtifactBundle
}

function formatTimestamp(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}

function mapResultLabel(result: CalibrationRecord['result']) {
  return props.copy[result]
}

function scoreWindow(records: CalibrationRecord[]) {
  if (!records.length) return 0
  const scoreMap: Record<CalibrationRecord['result'], number> = {
    hit: 1,
    partial: 0.35,
    miss: -1,
    insufficient_data: 0.1,
  }
  const total = records.reduce((sum, record) => sum + scoreMap[record.result], 0)
  return total / records.length
}

function describeTendency(delta: number, total: number) {
  if (total < 2) return props.copy.thinArchive
  if (delta > 0.22) return props.copy.tendencyStrengthening
  if (delta < -0.22) return props.copy.tendencySlipping
  return props.copy.tendencyHolding
}

function buildPosterSvg() {
  const titleLines = wrapLines(props.shareSnapshot.title, 16)
  const summaryLines = wrapLines(props.shareSnapshot.summary, 34)
  const captionLines = wrapLines(props.shareSnapshot.poster_caption, 28)
  const noteLines = wrapLines(props.shareSnapshot.curator_note || props.shareSnapshot.short_excerpt, 28)
  const tagLine = props.shareSnapshot.tags.join(' / ')

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc">
  <title id="title">${escapeXml(props.shareSnapshot.title)}</title>
  <desc id="desc">${escapeXml(props.shareSnapshot.summary)}</desc>
  <rect width="1280" height="720" fill="#071117" />
  <circle cx="200" cy="140" r="220" fill="#ffb979" fill-opacity="0.09" />
  <circle cx="1110" cy="130" r="180" fill="#8be2f8" fill-opacity="0.08" />
  <path d="M118 566C256 500 356 468 485 432C628 394 726 332 920 270C1044 230 1122 199 1216 148" fill="none" stroke="#8be2f8" stroke-opacity="0.42" stroke-width="2" stroke-linecap="round" />
  <circle cx="192" cy="531" r="12" fill="#ffb979" fill-opacity="0.92" />
  <circle cx="192" cy="531" r="36" fill="#ffb979" fill-opacity="0.08" />
  <text x="72" y="86" fill="#8be2f8" font-size="18" font-family="Aptos, Segoe UI, sans-serif" letter-spacing="6">MIROWORLD</text>
  <text x="72" y="124" fill="#8fa7b0" font-size="14" font-family="Aptos, Segoe UI, sans-serif" letter-spacing="4">${escapeXml(props.copy.posterArtifact.toUpperCase())}</text>
  ${renderTextLines(titleLines, 72, 232, 68, 66, '#e8efe9', `'Iowan Old Style', 'Palatino Linotype', serif`, '600')}
  ${renderTextLines(summaryLines, 76, 338, 28, 38, '#e8efe9', `'Aptos', 'Segoe UI', sans-serif`, '400')}
  ${renderTextLines(captionLines, 76, 512, 24, 34, '#ffb979', `'Aptos', 'Segoe UI', sans-serif`, '400')}
  <rect x="906" y="92" width="292" height="404" rx="28" fill="#ffffff" fill-opacity="0.03" stroke="#ffffff" stroke-opacity="0.08" />
  <text x="942" y="140" fill="#8fa7b0" font-size="13" font-family="Aptos, Segoe UI, sans-serif" letter-spacing="3">${escapeXml(props.copy.wallLabel.toUpperCase())}</text>
  ${renderTextLines(wrapLines(props.shareSnapshot.wall_label, 24), 942, 180, 18, 28, '#e8efe9', `'Aptos', 'Segoe UI', sans-serif`, '400')}
  <text x="942" y="294" fill="#8fa7b0" font-size="13" font-family="Aptos, Segoe UI, sans-serif" letter-spacing="3">${escapeXml(props.copy.curatorNote.toUpperCase())}</text>
  ${renderTextLines(noteLines, 942, 334, 18, 28, '#e8efe9', `'Aptos', 'Segoe UI', sans-serif`, '400')}
  <text x="76" y="646" fill="#8fa7b0" font-size="15" font-family="Aptos, Segoe UI, sans-serif">${escapeXml(tagLine)}</text>
  <text x="76" y="680" fill="#8fa7b0" font-size="13" font-family="Aptos, Segoe UI, sans-serif">${escapeXml(props.shareSnapshot.archive_summary)}</text>
</svg>`
}

function buildShareBundle() {
  const decisions = props.decisionLog.length
    ? props.decisionLog.map((entry, index) => (
      `${index + 1}. ${entry.event_title}\n` +
      `   ${entry.input_type}: ${entry.content}\n` +
      `   ${entry.replay_summary}\n` +
      (entry.cost_changes.length ? `   ${entry.cost_changes.join(' / ')}\n` : '')
    )).join('\n')
    : 'No recorded decisions yet.\n'

  const calibrations = props.calibrationRecords.length
    ? props.calibrationRecords.slice(0, 6).map((record, index) => (
      `${index + 1}. ${mapResultLabel(record.result)}\n` +
      `   ${record.actual_outcome}\n` +
      `   ${formatTimestamp(record.created_at)}\n`
    )).join('\n')
    : `${props.copy.actualOutcomePlaceholder}\n`

  return [
    props.shareSnapshot.title,
    '',
    props.shareSnapshot.summary,
    '',
    `${props.copy.posterCaption}: ${props.shareSnapshot.poster_caption}`,
    `${props.copy.wallLabel}: ${props.shareSnapshot.wall_label}`,
    `${props.copy.curatorNote}: ${props.shareSnapshot.curator_note || props.shareSnapshot.short_excerpt}`,
    `${props.copy.archiveSummary}: ${props.shareSnapshot.archive_summary}`,
    '',
    `${props.copy.shareText}:`,
    props.shareSnapshot.share_text,
    '',
    `${props.copy.decisionLog}:`,
    decisions.trimEnd(),
    '',
    `${props.copy.calibrationHistory}:`,
    calibrations.trimEnd(),
  ].join('\n')
}

function buildArtifactBundle() {
  return JSON.stringify({
    schema_version: 1,
    project_id: props.projectId,
    exported_at: new Date().toISOString(),
    manifest: {
      artifact_count: 4,
      includes: ['poster_svg', 'poster_png', 'share_bundle_text', 'exhibit_html'],
      decision_log_count: props.decisionLog.length,
      calibration_record_count: sortedCalibrationRecords.value.length,
    },
    share_snapshot: props.shareSnapshot,
    decision_log: props.decisionLog,
    calibration_summary: props.calibrationSummary,
    calibration_records: sortedCalibrationRecords.value,
    artifacts: {
      poster_svg: buildPosterSvg(),
      share_bundle_text: buildShareBundle(),
      exhibit_html: buildExhibitHtml(),
      suggested_png_filename: `${safeFileStem(props.projectId)}-poster.png`,
    },
  }, null, 2)
}

function buildExhibitHtml() {
  const decisionMarkup = props.decisionLog.length
    ? props.decisionLog.map((entry) => `
        <article class="log-entry">
          <span class="meta">${escapeXml(entry.input_type)} / ${escapeXml(formatTimestamp(entry.created_at))}</span>
          <h3>${escapeXml(entry.event_title)}</h3>
          <p>${escapeXml(entry.content)}</p>
          <small>${escapeXml(entry.replay_summary)}</small>
        </article>
      `).join('')
    : `<p class="empty">${escapeXml(props.copy.actualOutcomePlaceholder)}</p>`

  const calibrationMarkup = sortedCalibrationRecords.value.length
    ? sortedCalibrationRecords.value.slice(0, 6).map((record) => `
        <article class="calibration-entry ${record.result}">
          <span class="meta">${escapeXml(mapResultLabel(record.result))}</span>
          <p>${escapeXml(record.actual_outcome)}</p>
          <small>${escapeXml(formatTimestamp(record.created_at))}</small>
        </article>
      `).join('')
    : `<p class="empty">${escapeXml(props.copy.actualOutcomePlaceholder)}</p>`

  const atlasMarkup = calibrationAtlasCards.value.map((card) => `
      <article class="atlas-card">
        <span class="meta">${escapeXml(card.label)}</span>
        <strong>${escapeXml(card.value)}</strong>
        <p>${escapeXml(card.note)}</p>
      </article>
    `).join('')

  const shareTextMarkup = escapeXml(props.shareSnapshot.share_text).replaceAll('\n', '<br />')

  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${escapeXml(props.shareSnapshot.title)} / MIROWORLD</title>
    <style>
      :root {
        color-scheme: dark;
        --bg: #071117;
        --panel: rgba(12, 24, 31, 0.92);
        --line: rgba(139, 226, 248, 0.16);
        --text: #e8efe9;
        --muted: #8fa7b0;
        --warm: #ffb979;
        --cool: #8be2f8;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Aptos, "Segoe UI", sans-serif;
        background:
          radial-gradient(circle at top left, rgba(38, 76, 83, 0.34), transparent 26%),
          radial-gradient(circle at 78% 18%, rgba(122, 84, 45, 0.18), transparent 22%),
          var(--bg);
        color: var(--text);
      }
      main {
        width: min(1180px, calc(100% - 2rem));
        margin: 0 auto;
        padding: 2rem 0 3rem;
        display: grid;
        gap: 1.25rem;
      }
      .hero, .card, .log-entry, .calibration-entry, .atlas-card {
        border: 1px solid var(--line);
        border-radius: 24px;
        background: var(--panel);
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
      }
      .hero {
        display: grid;
        gap: 1rem;
        grid-template-columns: minmax(0, 1.4fr) minmax(240px, 0.8fr);
        padding: 1.2rem;
      }
      .poster {
        padding: 1.3rem;
        border-radius: 22px;
        background:
          radial-gradient(circle at 15% 18%, rgba(255, 185, 121, 0.16), transparent 24%),
          radial-gradient(circle at 88% 14%, rgba(139, 226, 248, 0.15), transparent 22%),
          linear-gradient(180deg, rgba(16, 28, 36, 0.94), rgba(9, 13, 18, 0.88));
      }
      .brand, .meta {
        color: var(--muted);
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-size: 0.75rem;
      }
      h1, h2, h3 {
        margin: 0;
        font-family: "Iowan Old Style", "Palatino Linotype", serif;
        line-height: 0.96;
      }
      h1 { font-size: clamp(2.4rem, 5vw, 4rem); max-width: 10ch; }
      h2 { font-size: 1.35rem; margin-bottom: 0.65rem; }
      h3 { font-size: 1.05rem; margin-bottom: 0.45rem; }
      .caption { color: var(--warm); font-size: 1.05rem; }
      .side {
        display: grid;
        gap: 0.9rem;
        align-content: start;
        padding: 0.5rem 0.25rem;
      }
      .grid {
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
      .grid.two {
        grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
      }
      .card {
        padding: 1rem;
        display: grid;
        gap: 0.7rem;
      }
      .share {
        white-space: pre-wrap;
        line-height: 1.6;
      }
      .atlas-grid, .log-stack, .calibration-stack {
        display: grid;
        gap: 0.75rem;
      }
      .atlas-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
      .atlas-card, .log-entry, .calibration-entry {
        padding: 0.85rem;
      }
      .hit { border-color: rgba(142, 240, 206, 0.28); }
      .partial { border-color: rgba(255, 185, 121, 0.28); }
      .miss { border-color: rgba(245, 135, 135, 0.28); }
      .insufficient_data { border-color: rgba(139, 226, 248, 0.24); }
      .tag-row { display: flex; flex-wrap: wrap; gap: 0.5rem; }
      .tag {
        padding: 0.28rem 0.55rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        color: var(--muted);
      }
      .empty { color: var(--muted); }
      @media (max-width: 920px) {
        .hero, .grid, .grid.two, .atlas-grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
  </head>
  <body>
    <main>
      <section class="hero">
        <article class="poster">
          <p class="brand">MIROWORLD</p>
          <h1>${escapeXml(props.shareSnapshot.title)}</h1>
          <p>${escapeXml(props.shareSnapshot.summary)}</p>
          <p class="caption">${escapeXml(props.shareSnapshot.poster_caption)}</p>
          <div class="tag-row">${props.shareSnapshot.tags.map((tag) => `<span class="tag">${escapeXml(tag)}</span>`).join('')}</div>
        </article>
        <aside class="side">
          <div>
            <span class="meta">${escapeXml(props.copy.wallLabel)}</span>
            <p>${escapeXml(props.shareSnapshot.wall_label)}</p>
          </div>
          <div>
            <span class="meta">${escapeXml(props.copy.curatorNote)}</span>
            <p>${escapeXml(props.shareSnapshot.curator_note || props.shareSnapshot.short_excerpt)}</p>
          </div>
          <div>
            <span class="meta">${escapeXml(props.copy.archiveSummary)}</span>
            <p>${escapeXml(props.shareSnapshot.archive_summary)}</p>
          </div>
        </aside>
      </section>

      <section class="grid">
        <article class="card">
          <span class="meta">${escapeXml(props.copy.posterCaption)}</span>
          <p>${escapeXml(props.shareSnapshot.poster_caption)}</p>
        </article>
        <article class="card">
          <span class="meta">${escapeXml(props.copy.shortExcerpt)}</span>
          <p>${escapeXml(props.shareSnapshot.short_excerpt)}</p>
        </article>
        <article class="card">
          <span class="meta">${escapeXml(props.copy.shareText)}</span>
          <p class="share">${shareTextMarkup}</p>
        </article>
      </section>

      <section class="grid two">
        <article class="card">
          <h2>${escapeXml(props.copy.decisionLog)}</h2>
          <div class="log-stack">${decisionMarkup}</div>
        </article>
        <article class="card">
          <h2>${escapeXml(props.copy.calibrationAtlas)}</h2>
          <div class="atlas-grid">${atlasMarkup}</div>
          <h2>${escapeXml(props.copy.calibrationHistory)}</h2>
          <div class="calibration-stack">${calibrationMarkup}</div>
        </article>
      </section>
    </main>
  </body>
</html>`
}

function downloadFile(filename: string, content: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}

async function buildPosterPngDataUrl() {
  const svgBlob = new Blob([buildPosterSvg()], { type: 'image/svg+xml;charset=utf-8' })
  const svgUrl = URL.createObjectURL(svgBlob)

  try {
    const image = await loadImage(svgUrl)
    const scale = 2
    const canvas = document.createElement('canvas')
    canvas.width = 1280 * scale
    canvas.height = 720 * scale

    const context = canvas.getContext('2d')
    if (!context) {
      throw new Error('Canvas context unavailable')
    }

    context.fillStyle = '#071117'
    context.fillRect(0, 0, canvas.width, canvas.height)
    context.drawImage(image, 0, 0, canvas.width, canvas.height)

    if (typeof canvas.toDataURL !== 'function') {
      throw new Error('Canvas export unavailable')
    }

    return canvas.toDataURL('image/png')
  } finally {
    URL.revokeObjectURL(svgUrl)
  }
}

function loadImage(src: string) {
  return new Promise<HTMLImageElement>((resolve, reject) => {
    const image = new Image()
    image.onload = () => resolve(image)
    image.onerror = () => reject(new Error('Image export unavailable'))
    image.src = src
  })
}

function downloadDataUrl(filename: string, dataUrl: string) {
  const link = document.createElement('a')
  link.href = dataUrl
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
}

function wrapLines(value: string, lineLength: number) {
  const trimmed = value.trim()
  if (!trimmed) return []

  const words = trimmed.split(/\s+/).filter(Boolean)
  if (words.length <= 1 && trimmed.length > lineLength) {
    const chunks: string[] = []
    for (let index = 0; index < trimmed.length; index += lineLength) {
      chunks.push(trimmed.slice(index, index + lineLength))
    }
    return chunks.slice(0, 4)
  }

  const lines: string[] = []
  let current = ''

  for (const word of words) {
    const next = current ? `${current} ${word}` : word
    if (next.length > lineLength && current) {
      lines.push(current)
      current = word
    } else {
      current = next
    }
  }

  if (current) lines.push(current)
  return lines.slice(0, 4)
}

function renderTextLines(
  lines: string[],
  x: number,
  startY: number,
  fontSize: number,
  lineHeight: number,
  fill: string,
  fontFamily: string,
  fontWeight: string,
) {
  return lines.map((line, index) => (
    `<text x="${x}" y="${startY + lineHeight * index}" fill="${fill}" font-size="${fontSize}" font-family="${fontFamily}" font-weight="${fontWeight}">${escapeXml(line)}</text>`
  )).join('')
}

function escapeXml(value: string) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;')
}

function safeFileStem(value: string) {
  const stem = value.toLowerCase().replace(/[^a-z0-9-_]+/g, '-').replace(/^-+|-+$/g, '')
  return stem || 'miroworld-artifact'
}
</script>
