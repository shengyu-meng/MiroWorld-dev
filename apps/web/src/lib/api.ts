import type {
  CalibrationRecord,
  DisplayLanguage,
  EffectScope,
  FixtureManifest,
  InputType,
  ReplayResult,
  ShareArtifact,
  StageData,
} from '@/lib/types'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

interface ApiEnvelope<T> {
  success: boolean
  data: T
  error?: {
    message: string
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })
  const json = (await response.json()) as ApiEnvelope<T>
  if (!response.ok || !json.success) {
    throw new Error(json.error?.message ?? 'Request failed.')
  }
  return json.data
}

export function listFixtures() {
  return request<FixtureManifest>('/api/fixtures')
}

export function createProject(payload: {
  fixture_id?: string
  seed_prompt?: string
  language: DisplayLanguage
}) {
  return request<{ project_id: string; stage: StageData }>('/api/projects', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function getStage(projectId: string, language: DisplayLanguage) {
  return request<StageData>(`/api/projects/${projectId}/stage?language=${language}`)
}

export function applyInput(
  projectId: string,
  payload: {
    input_type: InputType
    content: string
    target_event_id: string
    target_branch_id: string
    effect_scope: EffectScope
    language: DisplayLanguage
  },
) {
  return request<{ stage: StageData; replay_result: ReplayResult | null }>(
    `/api/projects/${projectId}/inputs`,
    {
      method: 'POST',
      body: JSON.stringify(payload),
    },
  )
}

export function buildShare(
  projectId: string,
  payload: {
    language: DisplayLanguage
    event_id?: string
    branch_id?: string
  },
) {
  return request<ShareArtifact>(`/api/projects/${projectId}/share`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function recordCalibration(
  projectId: string,
  payload: {
    event_id: string
    branch_id: string
    result: CalibrationRecord['result']
    actual_outcome: string
    note: string
    language: DisplayLanguage
  },
) {
  return request<StageData>(`/api/projects/${projectId}/calibration`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
