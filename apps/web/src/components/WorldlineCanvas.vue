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
  scene?: 'entry' | 'stage'
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
  observatory: 'rgba(149, 224, 255, 0.92)',
  intervention: 'rgba(255, 198, 103, 0.94)',
  cost: 'rgba(255, 145, 109, 0.9)',
  ripple: 'rgba(188, 180, 255, 0.9)',
  archive: 'rgba(166, 255, 220, 0.88)',
}[props.activeSurface]))

const scene = computed(() => props.scene ?? 'stage')

const windowedEvents = computed(() => {
  if (props.events.length <= 3) return props.events
  const index = props.events.findIndex((event) => event.event_id === props.selectedEventId)
  if (index < 0) return props.events.slice(0, 3)
  const start = Math.max(0, index - 1)
  return props.events.slice(start, start + 3)
})

const nodePosition = computed(() => {
  if (scene.value === 'entry') {
    return { x: 0.63, y: 0.58, radius: 16 }
  }

  return {
    observatory: { x: 0.68, y: 0.56, radius: 13 },
    intervention: { x: 0.61, y: 0.59, radius: 14 },
    cost: { x: 0.72, y: 0.63, radius: 13 },
    ripple: { x: 0.56, y: 0.52, radius: 14 },
    archive: { x: 0.73, y: 0.5, radius: 12 },
  }[props.activeSurface]
})

function buildLines(width: number, height: number) {
  const eventCount = Math.max(windowedEvents.value.length, 1)
  const density = reducedMotion.matches ? 14 : scene.value === 'entry' ? (width < 720 ? 26 : 54) : width < 720 ? 22 : 40
  const lines: LineModel[] = []

  for (let eventIndex = 0; eventIndex < eventCount; eventIndex += 1) {
    const event = windowedEvents.value[eventIndex]
    const branchCount = Math.min(event?.branches.length ?? 1, 3)
    for (let branchIndex = 0; branchIndex < branchCount; branchIndex += 1) {
      const branch = event?.branches[branchIndex]
      for (let thread = 0; thread < Math.max(1, Math.floor(density / eventCount)); thread += 1) {
        const baseY = scene.value === 'entry'
          ? height * (0.22 + (thread / density) * 0.62)
          : ((eventIndex + 1) / (eventCount + 1)) * height
        const drift = ((thread + 1) / density) * height * (scene.value === 'entry' ? 0.62 : 0.45)
        const focusBoost = branch?.branch_id === props.selectedBranchId ? 1.35 : 1

        lines.push({
          points: [
            [width * -0.06, baseY - drift * (scene.value === 'entry' ? 0.18 : 0.5)],
            [width * 0.24, baseY + drift * 0.16],
            [width * (scene.value === 'entry' ? 0.58 : 0.54), baseY - drift * 0.14],
            [width * 1.06, baseY + drift * 0.08],
          ],
          color: branch?.visibility === 'primary' ? accent.value : 'rgba(145, 176, 200, 0.72)',
          width: branch?.visibility === 'primary' ? 1.55 * focusBoost : 0.78,
          opacity: branch?.branch_id === props.selectedBranchId ? 0.98 : branch?.visibility === 'primary' ? 0.58 : 0.18,
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
  const node = nodePosition.value

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, width, height)

  const gradient = ctx.createRadialGradient(
    width * (scene.value === 'entry' ? 0.52 : 0.28 + pointer.value.x * 0.14),
    height * (scene.value === 'entry' ? 0.48 : 0.2 + pointer.value.y * 0.14),
    0,
    width * (scene.value === 'entry' ? 0.58 : 0.28),
    height * (scene.value === 'entry' ? 0.52 : 0.28),
    width * 0.8,
  )
  gradient.addColorStop(0, scene.value === 'entry' ? 'rgba(34, 66, 82, 0.26)' : 'rgba(33, 72, 73, 0.25)')
  gradient.addColorStop(1, 'rgba(5, 9, 13, 0)')
  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, width, height)

  for (let i = 0; i < 7; i += 1) {
    const y = height * (0.08 + i * 0.12 + pointer.value.y * 0.01)
    const x = width * (0.08 + (i % 4) * 0.17)
    ctx.beginPath()
    ctx.moveTo(x, y)
    ctx.lineTo(x + width * 0.09, y - (i % 2 === 0 ? 1 : -1))
    ctx.strokeStyle = 'rgba(140, 220, 255, 0.32)'
    ctx.lineWidth = 1
    ctx.stroke()
  }

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

  const ringBase = node.radius

  ctx.beginPath()
  ctx.arc(width * node.x, height * node.y, ringBase, 0, Math.PI * 2)
  ctx.fillStyle = 'rgba(9, 12, 14, 0.94)'
  ctx.fill()
  ctx.strokeStyle = accent.value
  ctx.lineWidth = 1.2
  ctx.stroke()

  for (let ring = 1; ring <= 3; ring += 1) {
    ctx.beginPath()
    ctx.arc(width * node.x, height * node.y, ringBase + ring * 8 + pointer.value.x * 2, 0, Math.PI * 2)
    ctx.strokeStyle = `rgba(144, 222, 255, ${0.14 / ring})`
    ctx.lineWidth = 1
    ctx.stroke()
  }

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
  reducedMotion.addEventListener?.('change', handleVisibility)
  resizeCanvas()
  draw()
})

watch(
  () => [props.activeSurface, props.selectedEventId, props.selectedBranchId, props.events, props.scene],
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
  reducedMotion.removeEventListener?.('change', handleVisibility)
})
</script>
