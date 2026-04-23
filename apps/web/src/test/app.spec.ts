import { flushPromises, mount } from '@vue/test-utils'
import { createMemoryHistory, createRouter } from 'vue-router'

import App from '@/App.vue'
import type { StageData } from '@/lib/types'
import EntryView from '@/views/EntryView.vue'
import StageView from '@/views/StageView.vue'

const sampleStage: StageData = {
  project_context: {
    project_id: 'proj_test',
    headline: 'Test Worldline',
    summary: 'A stage for test coverage.',
    status: 'active',
    source_label: 'literary-branching-world',
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
        title: 'Event One',
        summary: 'Summary one',
        stage: 'Entry',
        impact_level: 'high',
        affected_entities: ['Public'],
        evidence_notes: ['Evidence'],
        branches: [
          {
            branch_id: 'br_1',
            event_id: 'evt_1',
            label: 'Primary',
            description: 'Primary branch',
            confidence: 0.66,
            premises: ['Premise A'],
            signals_for: ['Signal A'],
            signals_against: ['Signal B'],
            visibility: 'primary',
            state: 'selected',
            cost_hint: 'Cost A',
            player_memory_count: 0,
            player_memory_note: '',
            memory_confidence_delta: 0,
            effective_confidence: 0.66,
            player_influence: 'neutral',
          },
          {
            branch_id: 'br_2',
            event_id: 'evt_1',
            label: 'Alternate',
            description: 'Alternate branch',
            confidence: 0.22,
            premises: ['Premise B'],
            signals_for: ['Signal C'],
            signals_against: ['Signal D'],
            visibility: 'alternate',
            state: 'candidate',
            cost_hint: 'Cost B',
            player_memory_count: 0,
            player_memory_note: '',
            memory_confidence_delta: 0,
            effective_confidence: 0.22,
            player_influence: 'neutral',
          },
        ],
      },
      {
        event_id: 'evt_2',
        title: 'Event Two',
        summary: 'Summary two',
        stage: 'Aftermath',
        impact_level: 'medium',
        affected_entities: ['Students', 'Media'],
        evidence_notes: ['Evidence two'],
        branches: [
          {
            branch_id: 'br_3',
            event_id: 'evt_2',
            label: 'Continuation',
            description: 'Continuation branch',
            confidence: 0.58,
            premises: ['Premise C'],
            signals_for: ['Signal E'],
            signals_against: ['Signal F'],
            visibility: 'primary',
            state: 'selected',
            cost_hint: 'Cost C',
            player_memory_count: 0,
            player_memory_note: '',
            memory_confidence_delta: 0,
            effective_confidence: 0.58,
            player_influence: 'tilting',
          },
          {
            branch_id: 'br_4',
            event_id: 'evt_2',
            label: 'Backlash',
            description: 'Backlash branch',
            confidence: 0.31,
            premises: ['Premise D'],
            signals_for: ['Signal G'],
            signals_against: ['Signal H'],
            visibility: 'alternate',
            state: 'candidate',
            cost_hint: 'Cost D',
            player_memory_count: 0,
            player_memory_note: '',
            memory_confidence_delta: 0,
            effective_confidence: 0.31,
            player_influence: 'volatile',
          },
        ],
      },
    ],
    worldline_track: [
      {
        event_id: 'evt_1',
        title: 'Event One',
        stage: 'Entry',
        primary_branch_id: 'br_1',
        primary_branch_label: 'Primary',
        confidence: 0.66,
      },
      {
        event_id: 'evt_2',
        title: 'Event Two',
        stage: 'Aftermath',
        primary_branch_id: 'br_3',
        primary_branch_label: 'Continuation',
        confidence: 0.58,
      },
    ],
  },
  intervention: {
    available_input_types: ['observation', 'correction', 'intervention', 'preference'],
    selected_branch_cards: [
      {
        label: 'Primary',
        description: 'Primary branch',
        premises: ['Premise A'],
        signals_for: ['Signal A'],
        signals_against: ['Signal B'],
      },
    ],
  },
  cost_lens: {
    lenses: [
      {
        cost_lens_id: 'cl_1',
        target_branch_id: 'br_1',
        first_order_costs: ['Cost 1'],
        second_order_costs: ['Cost 2'],
        affected_groups: ['Group 1'],
        ethical_notes: ['Note'],
      },
    ],
    passive_floor: {
      title: 'passive floor',
      summary: 'Cost exists even when nobody touches the branch.',
    },
  },
  ripple: {
    latest_bend: 'The branch has bent.',
    ripple_cards: [
      {
        title: 'Ripple',
        summary: 'Ripple summary',
        branch_label: 'Primary',
      },
      {
        title: 'Aftershock',
        summary: 'Aftershock summary',
        branch_label: 'Continuation',
      },
    ],
  },
  archive: {
    share_snapshot: {
      title: 'Test Worldline',
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
    player_decision_log: [
      {
        entry_id: 'log_1',
        created_at: '2026-01-01T00:00:00Z',
        input_type: 'intervention',
        event_id: 'evt_1',
        event_title: 'Event One',
        branch_id: 'br_1',
        branch_label: 'Primary',
        content: 'Intervene',
        replay_summary: 'Replay summary',
        cost_changes: ['Cost 1'],
      },
    ],
    calibration_records: [
      {
        calibration_id: 'cal_1',
        event_id: 'evt_1',
        branch_id: 'br_1',
        result: 'hit',
        actual_outcome: 'Outcome one aligned with the selected branch.',
        note: '',
        created_at: '2026-01-05T00:00:00Z',
      },
      {
        calibration_id: 'cal_2',
        event_id: 'evt_1',
        branch_id: 'br_1',
        result: 'partial',
        actual_outcome: 'Outcome two only partially aligned.',
        note: '',
        created_at: '2026-01-04T00:00:00Z',
      },
      {
        calibration_id: 'cal_3',
        event_id: 'evt_1',
        branch_id: 'br_2',
        result: 'miss',
        actual_outcome: 'Outcome three broke away from the branch.',
        note: '',
        created_at: '2026-01-03T00:00:00Z',
      },
      {
        calibration_id: 'cal_4',
        event_id: 'evt_1',
        branch_id: 'br_1',
        result: 'partial',
        actual_outcome: 'Outcome four stayed contested.',
        note: '',
        created_at: '2026-01-02T00:00:00Z',
      },
    ],
    calibration_summary: {
      count: 4,
      summary: 'The archive now shows a split but partially stabilizing calibration pattern.',
    },
  },
  version: 1,
}

function makeRouter(initialPath: string) {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: EntryView },
      { path: '/world/:projectId', component: StageView },
    ],
  })
}

describe('app routes', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('loads the entry route and renders fixtures', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValueOnce(new Response(JSON.stringify({
      success: true,
      data: {
        version: 1,
        fixtures: [
          {
            fixture_id: 'literary-branching-world',
            file: 'literary-branching-world.json',
            purpose: 'Literary branch baseline',
            must_produce: ['share_artifact'],
          },
        ],
      },
    })))

    const router = makeRouter('/')
    router.push('/')
    await router.isReady()

    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    })
    await flushPromises()

    expect(wrapper.find('[data-testid="fixture-grid"]').exists()).toBe(true)
    expect(wrapper.text()).toContain('literary-branching-world')
    expect(wrapper.text()).toContain('MIROWORLD')
  })

  it('loads the stage route, allows branch selection, language switching, and archive drawer toggle', async () => {
    const fetchMock = vi.spyOn(global, 'fetch')
    const createObjectURLMock = vi.fn(() => 'blob:miroworld')
    const revokeObjectURLMock = vi.fn()
    const anchorClickMock = vi.fn()
    Object.defineProperty(global.URL, 'createObjectURL', {
      writable: true,
      value: createObjectURLMock,
    })
    Object.defineProperty(global.URL, 'revokeObjectURL', {
      writable: true,
      value: revokeObjectURLMock,
    })
    vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(anchorClickMock)
    fetchMock
      .mockResolvedValueOnce(new Response(JSON.stringify({ success: true, data: sampleStage })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ success: true, data: sampleStage })))

    const router = makeRouter('/world/proj_test')
    router.push('/world/proj_test?lang=zh')
    await router.isReady()

    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    })
    await flushPromises()

    expect(wrapper.find('[data-testid="observatory-section"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="worldline-overlay"]').exists()).toBe(true)
    await wrapper.findAll('.branch-chip')[1]?.trigger('click')
    expect(wrapper.text()).toContain('Alternate branch')

    await wrapper.findAll('.language-button')[1]?.trigger('click')
    await flushPromises()
    expect(fetchMock).toHaveBeenCalledTimes(2)

    await wrapper.findAll('.surface-chip')[3]?.trigger('click')
    await flushPromises()
    expect(wrapper.find('[data-testid="ripple-continuity-explorer"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="ripple-path-archive"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="ripple-replay-history"]').exists()).toBe(true)
    await wrapper.find('[data-testid="ripple-event-node-evt_2"]').trigger('click')
    expect(wrapper.find('[data-testid="ripple-focus-card"]').text()).toContain('Event Two')
    await wrapper.find('[data-testid="ripple-path-node-alternate-evt_2"]').trigger('click')
    expect(wrapper.find('[data-testid="ripple-focus-card"]').text()).toContain('Event Two')
    expect(wrapper.text()).toContain('Backlash branch')
    await wrapper.find('[data-testid="ripple-history-mode-alternate"]').trigger('click')
    await wrapper.find('[data-testid="ripple-history-entry-alternate-evt_2"]').trigger('click')
    expect(wrapper.text()).toContain('Counter-Signal Density')
    expect(wrapper.text()).toContain('Backlash')

    await wrapper.findAll('.surface-chip')[4]?.trigger('click')
    await flushPromises()
    expect(wrapper.find('[data-testid="archive-section"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="calibration-atlas"]').exists()).toBe(true)
    await wrapper.find('[data-testid="download-poster"]').trigger('click')
    expect(createObjectURLMock).toHaveBeenCalledTimes(1)
    await wrapper.find('[data-testid="download-bundle"]').trigger('click')
    expect(createObjectURLMock).toHaveBeenCalledTimes(2)
    await wrapper.find('[data-testid="download-exhibit"]').trigger('click')
    expect(createObjectURLMock).toHaveBeenCalledTimes(3)
    expect(anchorClickMock).toHaveBeenCalledTimes(3)
    expect(revokeObjectURLMock).toHaveBeenCalledTimes(3)
    await wrapper.find('[data-testid="archive-section"] .secondary-action').trigger('click')
    expect(wrapper.find('[data-testid="calibration-drawer"]').exists()).toBe(true)
  })

  it('renders an error state when stage loading fails', async () => {
    vi.spyOn(global, 'fetch').mockRejectedValueOnce(new Error('boom'))

    const router = makeRouter('/world/proj_test')
    router.push('/world/proj_test?lang=zh')
    await router.isReady()

    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    })
    await flushPromises()

    expect(wrapper.find('[data-testid="error-state"]').exists()).toBe(true)
    expect(wrapper.text()).toContain('boom')
  })
})
