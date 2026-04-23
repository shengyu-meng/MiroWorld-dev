# Next Work Plan

Updated: 2026-04-23
Status: Active
Current slice: `Experience Rebuild Slice 2`

## Goal

Continue moving `MiroWorld-dev` from a working scene-shell MVP toward a stronger public-facing worldline artwork that better matches:

- the legacy Mirror World product principles
- the rebuild direction documented in the old repo
- the reference `miroworld_abstract_worldline_ui_v3` visual language

## Scope

This slice intentionally stays inside the existing MVP boundary:

- no contract rewrite
- no major backend architecture rewrite
- no PDF ingestion
- no legacy feature parity chase

This slice does include:

- deeper archive and share chamber
- stronger branch comparison in Observatory
- selective linefield overlay upgrades where they materially improve reading
- further documentation sync after each iteration

## Slice 1 Completed

- [x] the repo has canonical `CURRENT_STATUS / NEXT_WORK_PLAN / DEVELOPMENT_LOG / BLOCKERS` docs
- [x] `/` reads as a public entry scene, not just a fixture picker page
- [x] `/world/:projectId` shows one active scene at a time instead of a long vertical stack of all five surfaces
- [x] the linefield remains lightweight and does not block route startup
- [x] `FACT / INFERENCE / VALUE / ACTION` is visible as an interaction lens in the stage shell
- [x] existing replay/share/calibration flow still works
- [x] build, tests, and smoke pass after the redesign

## Slice 2 Acceptance Criteria

- Observatory makes branch differences easier to read without opening every branch manually
- Archive feels closer to a `Debrief / Share / Export` destination than a utility drawer
- share output presentation becomes richer without introducing frontend-side secret risk
- linefield upgrades do not regress startup, replay flow, or local FPS expectations
- docs are updated again when the slice lands

## Checklist

### Completed before this slice

- [x] bootstrap monorepo
- [x] import safe contracts and fixtures
- [x] implement API core
- [x] wire basic web shell
- [x] add CI baseline
- [x] add one-click start / stop scripts

### In progress now

- [x] redesign Archive into a fuller `Debrief / Share / Export` chamber
- [x] improve Observatory branch comparison density
- [ ] decide whether to add a dedicated branch-explorer scene or richer scene overlays
- [ ] keep docs, tests, and smoke aligned with each iteration

### Deferred after this slice

- [ ] improve share artifact presentation beyond text-first copy
- [ ] explore poster/export image generation
- [ ] continue polishing Observatory density and wording
- [ ] revisit calibration visualization once archive structure is stronger

## Verification Plan

- `npm run build`
- `npm run test`
- `npm run smoke`
- one local visual pass for `/`
- one local visual pass for `/world/:projectId`

## Blocker Record

Write real blockers to `BLOCKERS.md` only if they stop autonomous progress.
