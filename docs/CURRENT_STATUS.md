# Current Status

Updated: 2026-04-23
Status: Active
Phase: `experience-first rebuild / scene-shell slice 2 complete`

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

### Frontend experience rebuild slice 2

- Archive expanded from a utility drawer into a richer `Share / Debrief` chamber
- branch-field overlay added so the linefield becomes a selectable branch surface for the current event
- Observatory gained an at-a-glance comparison board for the selected event's branches
- stage copy cleaned up and centralized so the visible shell no longer relies on scattered inline wording

### Verification baseline

- `npm run build` passes
- `npm run test` passes
- `npm run smoke` passes

## Still Missing

### Product / experience gaps

- the linefield now acts as a branch field for the current event, but it is not yet a full event-to-event explorer
- share output is still text-first today and does not yet produce richer visual export artifacts
- calibration history is visible, but its visualization is still list-based rather than patterned or comparative
- ripple history still foregrounds the latest bend more than a multi-step replay trail

### Content expression gaps

- the layer lens is now visible, but its depth is still mostly presentation-layer driven rather than fully model-driven
- cost narration can become more comparative across branches, not just branch-local
- ripple history currently foregrounds the latest bend more than a multi-step replay trail

### Documentation gaps

- canonical docs now exist in-repo
- the next improvement is to keep them moving slice by slice without falling back to chat-only history

## Current Focus

The next active slice is `Experience Rebuild Slice 3`:

- evolve share/export from text-first output toward a more visual artifact layer
- decide whether calibration should become a stronger visual record instead of a list
- deepen ripple history beyond the latest bend without regressing the current shell
