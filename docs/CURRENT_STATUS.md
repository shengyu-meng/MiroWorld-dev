# Current Status

Updated: 2026-04-23
Status: Active
Phase: `experience-first rebuild / scene-shell slice 2 in progress`

## One-line Summary

`MiroWorld-dev` now has a working standalone monorepo, public contracts, fixture-backed API, replay/share/calibration flow, tests, CI, one-click local startup, and a first scene-based public shell rebuild.

The main product risk is no longer "can it run." It is "how far the public experience has been pushed":

- the shell now reads as a scene-based worldline interface instead of a long panel stack
- but the linefield can still become a stronger storytelling actor
- and the archive/share space still needs a deeper curator-facing presentation

## Completed

### Repository and delivery baseline

- standalone repo initialized and connected to `origin/main`
- strict `.gitignore` created before importing assets or fixtures
- CI baseline added for secret scan, build, API tests, and smoke flow
- one-click local start and stop scripts added

### Public domain model and backend

- public contracts established in `contracts/`
- curated public fixtures copied into `fixtures/`
- FastAPI app created under `apps/api`
- project creation, stage loading, structured inputs, share generation, and calibration recording implemented
- MiniMax server-side adapter wired through local env vars only
- runtime snapshots and cache kept in ignored local data storage

### Frontend MVP shell

- Vue 3 + TypeScript + Vite app created under `apps/web`
- public entry route `/`
- stage route `/world/:projectId`
- five public surfaces wired:
  - `Observatory`
  - `Intervention`
  - `Cost Lens`
  - `Ripple`
  - `Archive`
- isolated canvas linefield component in place

### Frontend experience rebuild slice 1

- entry route rebuilt into a line-first public entry scene
- stage route rebuilt into a single-active-scene workbench instead of a long stacked dashboard
- Chinese and English UI copy centralized in `apps/web/src/lib/copy.ts`
- `FACT / INFERENCE / VALUE / ACTION` exposed as a visible stage lens
- archive, replay, and branch annotations reorganized into a stronger right-rail and scene layout
- frontend tests and smoke flow updated to the new shell

### Verification baseline

- `npm run build` passes
- `npm run test` passes
- `npm run smoke` passes

## Still Missing

### Product / experience gaps

- the linefield is stronger now, but it still behaves more like a live atmosphere than a true branch-explorer surface
- Observatory can still become denser and more legible for branch comparison at a glance
- Archive is still a compact utility space; it is not yet a full `Debrief / Share / Export` chamber
- share output is text-first today and does not yet produce richer visual export artifacts

### Content expression gaps

- the layer lens is now visible, but its depth is still mostly presentation-layer driven rather than fully model-driven
- cost narration can become more comparative across branches, not just branch-local
- ripple history currently foregrounds the latest bend more than a multi-step replay trail

### Documentation gaps

- canonical docs now exist in-repo
- the next improvement is to keep them moving slice by slice without falling back to chat-only history

## Current Focus

The current active slice is `Experience Rebuild Slice 2`:

- Archive has now moved toward a fuller `Share / Debrief` chamber with richer share text, wall label, archive summary, and calibration history
- Observatory now exposes evidence notes earlier in the reading flow
- the next highest-value remaining step is still deciding how far to push branch comparison and linefield overlays
- performance and contract stability remain intact after the second frontend pass
