import { flushPromises, mount } from '@vue/test-utils'
import { createMemoryHistory, createRouter } from 'vue-router'
import { afterEach, describe, expect, it, vi } from 'vitest'

import type { Branch, StageData } from '@/lib/types'
import StageView from '@/views/StageView.vue'

function branch(eventId: string, id: string, label: string, confidence: number, visibility: Branch['visibility']): Branch {
  return {
    branch_id: id,
    event_id: eventId,
    label,
    description: `${label} keeps the worldline moving through a rule and material constraint.`,
    confidence,
    premises: ['The rule layer is pulling on the material layer.'],
    signals_for: ['Field signals are becoming denser.'],
    signals_against: ['A local correction could bend the node.'],
    visibility,
    state: visibility === 'primary' ? 'selected' : 'candidate',
    cost_hint: `${label} shifts cost across actants and constraints.`,
    player_memory_count: 0,
    player_memory_note: '',
    memory_confidence_delta: 0,
    effective_confidence: confidence,
    player_influence: 'observer disturbance',
  }
}

const sampleStage: StageData = {
  project_context: {
    project_id: 'proj_test',
    headline: 'Campus public opinion spiral',
    summary: 'A platform-shaped public opinion fixture that should be rewritten at display time.',
    status: 'active',
    source_label: 'campus-public-opinion',
    display_language: 'zh',
  },
  surface_defaults: {
    selected_event_id: 'evt_1',
    selected_branch_id: 'br_1',
    active_surface: 'observatory',
  },
  observatory: {
    knowledge_layers: ['FACT', 'INFERENCE', 'VALUE', 'ACTION'],
    key_events: [
      {
        event_id: 'evt_1',
        title: '触发材料进入公共视野',
        summary: '第一波传播开始塑造入口温度。',
        stage: '入口',
        impact_level: 'high',
        affected_entities: ['发起者', '公众气候'],
        evidence_notes: ['事实层与价值层正在彼此牵引。'],
        branches: [
          branch('evt_1', 'br_1', '主分支', 0.66, 'primary'),
          branch('evt_1', 'br_2', '替代分支', 0.22, 'alternate'),
        ],
      },
      {
        event_id: 'evt_2',
        title: '机构与平台开始重新分配位置',
        summary: '规则与材料开始决定谁承担代价。',
        stage: '扭转',
        impact_level: 'medium',
        affected_entities: ['规则层', '材料供应'],
        evidence_notes: ['新的约束开始显影。'],
        branches: [
          branch('evt_2', 'br_3', '延续', 0.58, 'primary'),
          branch('evt_2', 'br_4', '回折', 0.31, 'alternate'),
        ],
      },
      {
        event_id: 'evt_3',
        title: '后果沉淀为新的公众记忆',
        summary: '系统留下新的世界残影。',
        stage: '回响',
        impact_level: 'medium',
        affected_entities: ['制度', '环境'],
        evidence_notes: ['回响继续传导。'],
        branches: [
          branch('evt_3', 'br_5', '沉淀', 0.52, 'primary'),
          branch('evt_3', 'br_6', '再分叉', 0.28, 'alternate'),
        ],
      },
    ],
    worldline_track: [
      {
        event_id: 'evt_1',
        title: '触发材料进入公共视野',
        stage: '入口',
        primary_branch_id: 'br_1',
        primary_branch_label: '主分支',
        confidence: 0.66,
      },
      {
        event_id: 'evt_2',
        title: '机构与平台开始重新分配位置',
        stage: '扭转',
        primary_branch_id: 'br_3',
        primary_branch_label: '延续',
        confidence: 0.58,
      },
      {
        event_id: 'evt_3',
        title: '后果沉淀为新的公众记忆',
        stage: '回响',
        primary_branch_id: 'br_5',
        primary_branch_label: '沉淀',
        confidence: 0.52,
      },
    ],
  },
  intervention: {
    available_input_types: ['observation', 'correction', 'intervention', 'preference'],
    selected_branch_cards: [],
  },
  cost_lens: {
    lenses: [
      {
        cost_lens_id: 'cl_1',
        target_branch_id: 'br_1',
        first_order_costs: ['规则层吸收第一轮压力。'],
        second_order_costs: ['材料供应承担后续约束。'],
        affected_groups: ['规则层', '自然物'],
        ethical_notes: ['不要把清晰误认为正当。'],
      },
    ],
    passive_floor: {
      title: '被动代价',
      summary: '不触碰世界线，也仍然有代价沉积。',
    },
  },
  ripple: {
    latest_bend: '主分支获得第一轮可见优势。',
    ripple_cards: [
      { title: '入口回响', summary: '第一节点开始传导。', branch_label: '主分支' },
      { title: '扭转回响', summary: '第二节点继续弯折。', branch_label: '延续' },
      { title: '档案回响', summary: '第三节点进入残影。', branch_label: '沉淀' },
    ],
    saved_replay_sets: [],
  },
  archive: {
    share_snapshot: {
      title: 'Campus public opinion spiral',
      subtitle: 'Subtitle',
      summary: 'Share summary',
      disclaimer: 'Disclaimer',
      share_text: 'Share text',
      tags: ['miroworld'],
      short_excerpt: 'Short excerpt',
      poster_caption: 'Poster',
      curator_note: 'Curator',
      wall_label: 'Wall',
      archive_summary: 'Archive summary',
    },
    player_decision_log: [],
    calibration_records: [],
    calibration_summary: {
      count: 0,
      summary: 'No calibration yet.',
    },
  },
  version: 1,
}

function apiResponse<T>(data: T, status = 200) {
  return Promise.resolve(new Response(JSON.stringify({ success: status < 400, data }), { status }))
}

async function mountStage(stage: StageData = sampleStage) {
  const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input)
    if (url.includes('/stage')) return apiResponse(stage)
    if (url.includes('/share')) return apiResponse(stage.archive.share_snapshot)
    if (url.includes('/calibration')) return apiResponse(stage)
    if (url.includes('/inputs')) {
      return apiResponse({
        stage,
        replay_result: {
          replay_id: 'rp_1',
          checkpoint_id: 'evt_1',
          before_branch_id: 'br_1',
          after_branch_id: 'br_1',
          input_style: 'intervention',
          impact_mode: 'world_state',
          changed_events: ['evt_2'],
          changed_branches: ['br_3'],
          cost_changes: ['field pressure redistributed'],
          summary: 'The intervention bent the downstream line.',
        },
      })
    }
    return apiResponse({}, 404)
  })
  vi.stubGlobal('fetch', fetchMock)

  const router = createRouter({
    history: createMemoryHistory(),
    routes: [{ path: '/world/:projectId', component: StageView }],
  })
  router.push('/world/proj_test?lang=zh')
  await router.isReady()

  const wrapper = mount(StageView, {
    global: {
      plugins: [router],
    },
  })
  await flushPromises()
  return { wrapper, fetchMock }
}

afterEach(() => {
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

describe('worldline theatre stage', () => {
  it('progressively reveals the worldline when the viewer only presses next', async () => {
    const { wrapper } = await mountStage()

    expect(wrapper.get('[data-testid="revealed-event-count"]').text()).toContain('1 / 3')
    expect(wrapper.find('[data-testid="worldline-event-evt_1"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="worldline-event-evt_2"]').exists()).toBe(false)

    await wrapper.get('[data-testid="worldline-next"]').trigger('click')
    expect(wrapper.get('[data-testid="revealed-event-count"]').text()).toContain('2 / 3')
    expect(wrapper.find('[data-testid="worldline-event-evt_2"]').exists()).toBe(true)

    await wrapper.get('[data-testid="worldline-next"]').trigger('click')
    expect(wrapper.get('[data-testid="revealed-event-count"]').text()).toContain('3 / 3')
    expect(wrapper.find('[data-testid="worldline-event-evt_3"]').exists()).toBe(true)

    await wrapper.get('[data-testid="worldline-next"]').trigger('click')
    expect(wrapper.find('[data-testid="archive-section"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="archive-terminal"]').exists()).toBe(true)
  })

  it('removes legacy public-opinion wording from the rendered core UI', async () => {
    const { wrapper } = await mountStage()
    const text = wrapper.text()

    expect(text).toContain('触发源')
    expect(text).toContain('场域气候')
    expect(text).toContain('可观测层')
    expect(text).not.toContain('发起者')
    expect(text).not.toContain('公众气候')
    expect(text).not.toContain('公共视野')
    expect(text).not.toContain('舆论')
  })

  it('keeps branch selection and intervention flow available inside the theatre', async () => {
    const { wrapper, fetchMock } = await mountStage()

    const branches = wrapper.findAll('.branch-chip')
    await branches[1].trigger('click')
    expect(branches[1].classes()).toContain('active')

    await wrapper.findAll('.surface-chip')[1].trigger('click')
    expect(wrapper.find('[data-testid="intervention-section"]').exists()).toBe(true)
    await wrapper.find('[data-testid="intervention-section"] textarea').setValue('Let the material constraint become visible.')
    await wrapper.find('[data-testid="intervention-section"] form').trigger('submit.prevent')
    await flushPromises()

    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining('/inputs'),
      expect.objectContaining({ method: 'POST' }),
    )
    expect(wrapper.find('[data-testid="ripple-section"]').exists()).toBe(true)
  })
})
