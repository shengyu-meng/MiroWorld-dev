# Next Work Plan

Updated: 2026-04-23
Status: Active
Current slice: `Experience Rebuild Slice 4`

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

- stronger exportable artifact output
- more comparative calibration reading
- deeper event-to-event ripple and branch exploration
- further documentation sync after each iteration

## Slice 1 Completed

- [x] the repo has canonical `CURRENT_STATUS / NEXT_WORK_PLAN / DEVELOPMENT_LOG / BLOCKERS` docs
- [x] `/` reads as a public entry scene, not just a fixture picker page
- [x] `/world/:projectId` shows one active scene at a time instead of a long vertical stack of all five surfaces
- [x] the linefield remains lightweight and does not block route startup
- [x] `FACT / INFERENCE / VALUE / ACTION` is visible as an interaction lens in the stage shell
- [x] existing replay/share/calibration flow still works
- [x] build, tests, and smoke pass after the redesign

## Slice 2 Completed

- [x] Observatory makes branch differences easier to read without opening every branch manually
- [x] Archive feels closer to a `Debrief / Share / Export` destination than a utility drawer
- [x] linefield upgrades remain lightweight while becoming a selectable branch field for the active event
- [x] build, tests, smoke, and docs stayed aligned after the iteration

## Slice 3 Acceptance Criteria

- share/export presentation becomes richer without introducing frontend-side secret risk
- calibration history becomes easier to read than a plain chronological list
- ripple history exposes more than only the latest bend
- the current shell remains fast and the public contracts stay unchanged

## Slice 3 Completed

- [x] share/export presentation is richer and no longer purely text-first
- [x] Archive contains a visual poster/export layer without changing public contracts
- [x] calibration history is easier to read than a plain chronological list
- [x] ripple history now exposes a track instead of only the latest bend
- [x] build, tests, smoke, and docs stayed aligned after the iteration

## Slice 4 Acceptance Criteria

- the archive artifact becomes export-ready beyond in-app presentation alone
- calibration can be read comparatively across recent records, not only as isolated dots
- the linefield / ripple system reveals more event-to-event continuity without becoming heavy
- the public shell keeps startup and interaction responsiveness inside the current MVP baseline

## Checklist

### Completed before this slice

- [x] bootstrap monorepo
- [x] import safe contracts and fixtures
- [x] implement API core
- [x] wire basic web shell
- [x] add CI baseline
- [x] add one-click start / stop scripts

### In progress now

- [x] add local export actions for archive poster and share bundle
- [ ] turn the archive poster layer into a stronger export-ready artifact flow
- [x] turn calibration pattern into a comparative archive atlas
- [x] compare calibration records by pattern and tendency, not only chronology
- [ ] deepen calibration comparison across wider archive slices if the current atlas proves too shallow
- [x] turn Ripple into a continuity explorer instead of a single replay strip
- [x] deepen ripple continuity beyond the current replay track
- [ ] broaden Ripple from one continuity chain into a stronger multi-path replay archive
- [ ] decide whether multi-event exploration belongs in the linefield, archive, or a future dedicated scene
- [ ] keep docs, tests, and smoke aligned with each iteration

### Deferred after this slice

- [ ] continue polishing Observatory density and wording
- [ ] revisit whether the branch-field overlay should remain in-shell or become a dedicated future scene
- [ ] consider model-driven layer narration once the public shell expression stabilizes

## Verification Plan

- `npm run build`
- `npm run test`
- `npm run smoke`
- one local visual pass for `/`
- one local visual pass for `/world/:projectId`

## Blocker Record

Write real blockers to `BLOCKERS.md` only if they stop autonomous progress.
