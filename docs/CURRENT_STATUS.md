# Current Status

Updated: 2026-04-23
Status: Active
Phase: `experience-first rebuild / scene-shell slice 3 complete`

## One-line Summary

`MiroWorld-dev` now has a working standalone monorepo, public contracts, fixture-backed API, replay/share/calibration flow, tests, CI, one-click local startup, and a scene-based public shell that has moved into a stronger archive/export presentation layer.

The main product risk is no longer "can it run." It is "how far the public experience has been pushed":

- the shell now reads as a scene-based worldline interface instead of a long panel stack
- the archive/share space now reads more like a curator-facing artifact chamber instead of a utility output list
- but the linefield can still become a stronger event-to-event storytelling actor
- and the calibration / replay archive can still become more comparative and more navigable

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

### Frontend experience rebuild slice 3

- Archive gained a visual poster/export layer rather than relying on text-first share output alone
- share text can now be copied from a clearer export-focused chamber layout
- calibration history gained a first pass pattern view so recent outcomes read at a glance
- Ripple now reads more like a propagation track than a single latest-bend note

### Verification baseline

- `npm run build` passes
- `npm run test` passes
- `npm run smoke` passes

## Still Missing

### Product / experience gaps

- the linefield now acts as a branch field for the current event, but it is not yet a full event-to-event explorer
- the archive now presents a visual artifact, but it does not yet generate downloadable poster/image outputs or saved multi-format share bundles
- calibration history is now patterned, but it is not yet comparative across branch families, time windows, or decision types
- ripple history is now more track-like, but it still centers one replay chain more than a broader event-to-event archive

### Content expression gaps

- the layer lens is now visible, but its depth is still mostly presentation-layer driven rather than fully model-driven
- cost narration can become more comparative across branches, not just branch-local
- archive artifacts can become more authored and less template-like as share formats mature

### Documentation gaps

- canonical docs now exist in-repo
- the next improvement is to keep them moving slice by slice without falling back to chat-only history

## Current Focus

The next active slice is `Experience Rebuild Slice 4`:

- turn the archive poster layer into a stronger exportable artifact path
- make calibration more comparative, not only pattern-readable
- keep extending the linefield / ripple system toward a fuller event-to-event explorer without regressing shell speed
