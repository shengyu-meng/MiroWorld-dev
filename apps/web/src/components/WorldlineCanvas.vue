<template>
  <div ref="containerRef" class="worldline-canvas-shell" aria-hidden="true">
    <canvas ref="canvasRef" class="worldline-canvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'

import type { KeyEvent, SurfaceKey } from '@/lib/types'

interface LineModel {
  points: Array<[number, number]>
  color: string
  width: number
  opacity: number
}

const props = defineProps<{
  activeSurface: SurfaceKey
  events: KeyEvent[]
  selectedEventId?: string
  selectedBranchId?: string
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
const containerRef = ref<HTMLDivElement | null>(null)
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
const visible = ref(true)
const pointer = ref({ x: 0.4, y: 0.45 })
let frameId = 0
let resizeObserver: ResizeObserver | null = null
let precomputedLines: LineModel[] = []
let dpr = Math.min(window.devicePixelRatio || 1, 2)

const accent = computed(() => ({
  observatory: 'rgba(123, 182, 181, 0.85)',
  intervention: 'rgba(215, 177, 126, 0.92)',
  cost: 'rgba(167, 93, 63, 0.9)',
  ripple: 'rgba(173, 208, 225, 0.88)',
  archive: 'rgba(196, 190, 165, 0.86)',
}[props.activeSurface]))

const windowedEvents = computed(() => {
  if (props.events.length <= 3) return props.events
  const index = props.events.findIndex((event) => event.event_id === props.selectedEventId)
  if (index < 0) return props.events.slice(0, 3)
  const start = Math.max(0, index - 1)
  return props.events.slice(start, start + 3)
})

function buildLines(width: number, height: number) {
  const eventCount = Math.max(windowedEvents.value.length, 1)
  const density = reducedMotion.matches ? 16 : width < 720 ? 24 : 42
  const lines: LineModel[] = []
  for (let eventIndex = 0; eventIndex < eventCount; eventIndex += 1) {
    const event = windowedEvents.value[eventIndex]
    const branchCount = Math.min(event?.branches.length ?? 1, 3)
    for (let branchIndex = 0; branchIndex < branchCount; branchIndex += 1) {
      const branch = event?.branches[branchIndex]
      for (let thread = 0; thread < Math.max(1, Math.floor(density / eventCount)); thread += 1) {
        const baseY = ((eventIndex + 1) / (eventCount + 1)) * height
        const drift = ((thread + 1) / density) * height * 0.45
        const focusBoost = branch?.branch_id === props.selectedBranchId ? 1.35 : 1
        lines.push({
          points: [
            [width * -0.05, baseY - drift * 0.5],
            [width * 0.24, baseY + drift * 0.2],
            [width * 0.58, baseY - drift * 0.16],
            [width * 1.04, baseY + drift * 0.08],
          ],
          color: branch?.visibility === 'primary' ? accent.value : 'rgba(152, 163, 160, 0.75)',
          width: branch?.visibility === 'primary' ? 1.6 * focusBoost : 0.8,
          opacity: branch?.branch_id === props.selectedBranchId ? 0.96 : branch?.visibility === 'primary' ? 0.54 : 0.22,
        })
      }
    }
  }
  precomputedLines = lines
}

function resizeCanvas() {
  if (!canvasRef.value || !containerRef.value) return
  const rect = containerRef.value.getBoundingClientRect()
  dpr = Math.min(window.devicePixelRatio || 1, 2)
  canvasRef.value.width = rect.width * dpr
  canvasRef.value.height = rect.height * dpr
  canvasRef.value.style.width = `${rect.width}px`
  canvasRef.value.style.height = `${rect.height}px`
  buildLines(rect.width, rect.height)
}

function draw() {
  if (!canvasRef.value || !containerRef.value) return
  const ctx = canvasRef.value.getContext('2d')
  if (!ctx) return
  const width = containerRef.value.clientWidth
  const height = containerRef.value.clientHeight
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, width, height)

  const gradient = ctx.createRadialGradient(
    width * (0.24 + pointer.value.x * 0.14),
    height * (0.2 + pointer.value.y * 0.14),
    0,
    width * 0.28,
    height * 0.28,
    width * 0.8,
  )
  gradient.addColorStop(0, 'rgba(33, 72, 73, 0.25)')
  gradient.addColorStop(1, 'rgba(5, 9, 13, 0)')
  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, width, height)

  for (const line of precomputedLines) {
    ctx.beginPath()
    const [p0, p1, p2, p3] = line.points
    ctx.moveTo(p0[0], p0[1])
    ctx.bezierCurveTo(
      p1[0] + pointer.value.x * 16,
      p1[1] + pointer.value.y * 12,
      p2[0] - pointer.value.x * 12,
      p2[1] - pointer.value.y * 10,
      p3[0],
      p3[1],
    )
    ctx.strokeStyle = line.color.replace(/0\.\d+\)$/, `${line.opacity})`)
    ctx.lineWidth = line.width
    ctx.stroke()
  }

  ctx.beginPath()
  ctx.arc(width * 0.37, height * 0.52, 14, 0, Math.PI * 2)
  ctx.fillStyle = 'rgba(9, 12, 14, 0.94)'
  ctx.fill()
  ctx.strokeStyle = accent.value
  ctx.lineWidth = 1.2
  ctx.stroke()

  if (visible.value && !reducedMotion.matches) {
    frameId = requestAnimationFrame(draw)
  }
}

function handleVisibility() {
  visible.value = !document.hidden
  cancelAnimationFrame(frameId)
  draw()
}

function handlePointerMove(event: PointerEvent) {
  if (!containerRef.value) return
  const rect = containerRef.value.getBoundingClientRect()
  pointer.value = {
    x: (event.clientX - rect.left) / rect.width,
    y: (event.clientY - rect.top) / rect.height,
  }
}

onMounted(() => {
  if (!containerRef.value) return
  resizeObserver = new ResizeObserver(() => {
    resizeCanvas()
    cancelAnimationFrame(frameId)
    draw()
  })
  resizeObserver.observe(containerRef.value)
  containerRef.value.addEventListener('pointermove', handlePointerMove)
  document.addEventListener('visibilitychange', handleVisibility)
  reducedMotion.addEventListener('change', handleVisibility)
  resizeCanvas()
  draw()
})

watch(
  () => [props.activeSurface, props.selectedEventId, props.selectedBranchId, props.events],
  () => {
    resizeCanvas()
    cancelAnimationFrame(frameId)
    draw()
  },
  { deep: true },
)

onUnmounted(() => {
  cancelAnimationFrame(frameId)
  resizeObserver?.disconnect()
  containerRef.value?.removeEventListener('pointermove', handlePointerMove)
  document.removeEventListener('visibilitychange', handleVisibility)
  reducedMotion.removeEventListener('change', handleVisibility)
})
</script>
