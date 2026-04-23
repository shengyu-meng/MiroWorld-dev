export type DisplayLanguage = 'zh' | 'en'
export type InputType = 'observation' | 'correction' | 'intervention' | 'preference'
export type EffectScope = 'evidence' | 'world_state' | 'ranking'
export type SurfaceKey = 'observatory' | 'intervention' | 'cost' | 'ripple' | 'archive'

export interface FixtureDescriptor {
  fixture_id: string
  file: string
  purpose: string
  must_produce: string[]
}

export interface FixtureManifest {
  version: number
  fixtures: FixtureDescriptor[]
}

export interface Branch {
  branch_id: string
  event_id: string
  label: string
  description: string
  confidence: number
  premises: string[]
  signals_for: string[]
  signals_against: string[]
  visibility: 'primary' | 'alternate'
  state: string
  cost_hint: string
  player_memory_count: number
  player_memory_note: string
  memory_confidence_delta: number
  effective_confidence: number | null
  player_influence: string
}

export interface KeyEvent {
  event_id: string
  title: string
  summary: string
  stage: string
  impact_level: 'low' | 'medium' | 'high'
  affected_entities: string[]
  evidence_notes: string[]
  branches: Branch[]
}

export interface CostLens {
  cost_lens_id: string
  target_branch_id: string
  first_order_costs: string[]
  second_order_costs: string[]
  affected_groups: string[]
  ethical_notes: string[]
}

export interface ReplayResult {
  replay_id: string
  checkpoint_id: string
  before_branch_id: string
  after_branch_id: string
  input_style: InputType
  impact_mode: string
  changed_events: string[]
  changed_branches: string[]
  cost_changes: string[]
  summary: string
}

export interface ShareArtifact {
  title: string
  subtitle: string
  summary: string
  disclaimer: string
  share_text: string
  tags: string[]
  short_excerpt: string
  poster_caption: string
  curator_note: string
  wall_label: string
  archive_summary: string
}

export interface CalibrationRecord {
  calibration_id: string
  event_id: string
  branch_id: string
  result: 'hit' | 'partial' | 'miss' | 'insufficient_data'
  actual_outcome: string
  note: string
  created_at: string
}

export interface StageData {
  project_context: {
    project_id: string
    headline: string
    summary: string
    status: string
    source_label: string
    display_language: DisplayLanguage
  }
  surface_defaults: {
    selected_event_id: string
    selected_branch_id: string
    active_surface: SurfaceKey
  }
  observatory: {
    knowledge_layers: string[]
    key_events: KeyEvent[]
    worldline_track: Array<{
      event_id: string
      title: string
      stage: string
      primary_branch_id: string
      primary_branch_label: string
      confidence: number
    }>
  }
  intervention: {
    available_input_types: InputType[]
    selected_branch_cards: Array<{
      label: string
      description: string
      premises: string[]
      signals_for: string[]
      signals_against: string[]
    }>
  }
  cost_lens: {
    lenses: CostLens[]
    passive_floor: {
      title: string
      summary: string
    }
  }
  ripple: {
    latest_bend: string
    ripple_cards: Array<{
      title: string
      summary: string
      branch_label: string
    }>
  }
  archive: {
    share_snapshot: ShareArtifact
    player_decision_log: Array<{
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
    calibration_records: CalibrationRecord[]
    calibration_summary: {
      count: number
      summary: string
    }
  }
  version: number
}
