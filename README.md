# MiroWorld-dev

Standalone experience-first rebuild of MiroWorld.

## Product Direction

MiroWorld-dev is a public-facing branching world experience built around:

- worldline observation
- explicit branching and tradeoffs
- structured user intervention
- replay and ripple comparison
- shareable and calibratable world states

## Monorepo Layout

- `apps/web`: Vue 3 + TypeScript + Vite public shell
- `apps/api`: FastAPI backend, domain services, and MiniMax adapter
- `contracts`: JSON Schemas and public payload contracts
- `fixtures`: curated public scenarios and regression inputs
- `data`: local runtime state, cache, and generated artifacts (gitignored)

## Architecture Decisions

- Backend is feature-first: fixtures, projects, and system routes live beside their service logic.
- Public contracts are kept in `contracts/` and validated in tests against real API payloads.
- Prompt generation is server-side only and uses an OpenAI-compatible MiniMax adapter with cache fallback.
- The web shell is built around a single `/world/:projectId` stage route with fixed surfaces:
  - `Observatory`
  - `Intervention`
  - `Cost Lens`
  - `Ripple`
  - `Archive`
- The worldline background is a single isolated canvas component with:
  - precomputed line geometry
  - scoped pointer listeners
  - visibility pause
  - reduced-motion fallback
  - event windowing around the current focus

## Local Setup

1. Create a local `.env` from `.env.example`
2. Install JavaScript dependencies:

```bash
npm install
```

3. Install Python dependencies:

```bash
cd apps/api
python -m pip install -e .[dev]
```

## Run

Start both apps from the repo root:

```bash
npm run dev
```

Or separately:

```bash
npm run dev:web
npm run dev:api
```

## Verification

```bash
npm run build
npm run test:web
npm run test:api
npm run smoke
```

## Safety

- Real secrets belong only in local `.env`
- The MiniMax API key must never be committed
- Runtime logs, caches, screenshots, and generated artifacts stay out of git
- `fixtures/` and `contracts/` are treated as safe, reviewable inputs

## Current MVP Scope

- Fixture-based project creation
- Prompt-based seed creation with deterministic fallback and optional MiniMax enrichment
- Stage read model for five-surface public experience
- Structured observation / correction / intervention / preference inputs
- Replay results, share generation, and lightweight calibration archive
- Contract tests, frontend interaction tests, Playwright smoke flow, and CI
