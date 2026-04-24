# Next Work Plan

Updated: 2026-04-24
Status: Active
Current slice: `Experience Rebuild Slice 8 / Persistent Theatre Reading completed`

## Goal

Continue moving `MiroWorld-dev` from a working scene-shell MVP toward a stronger world-simulation artwork that better matches:

- the legacy Mirror World product principles
- the rebuild direction documented in the old repo
- the local `.ui-ref` visual language, without committing the reference folder
- the user's requirement that the worldline unfolds even when the viewer only presses Next

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
- a non-report-like theatre shell with progressive reveal
- visible process-trace files while the worldline unfolds
- timed intervention windows so the viewer can disturb the line at meaningful nodes
- a more cinematic computation display that still keeps data-file truth visible
- a repeatable browser performance benchmark for canvas FPS and Next-step latency
- persistent theatre reading state so refreshes can resume the same worldline layer
- cleanup of public-opinion / platform-era wording in UI, prompts, and fixtures
- performance-focused canvas simplification with a smaller black-hole anchor
- further documentation sync after each iteration

## Slice 6 Acceptance Criteria

- [x] stage payload exposes a deterministic `process_trace` derived from the current world state
- [x] process trace writes gitignored runtime JSON artifacts under `data/runtime/process/...`
- [x] `/world/:projectId` shows the current event's process file, layer outputs, and backend calculation cues while the viewer advances
- [x] pressing Next still works without user input, but appropriate events show an intervention window with a direct path into the Intervention drawer
- [x] tests cover process trace contract validation, progressive display, and intervention-window entry
- [x] build, tests, smoke, diff check, secret scan, and reference-folder checks pass before push

## Slice 5 Acceptance Criteria

- [x] `.ui-ref/` and `ui-ref/` are ignored and never staged
- [x] `/world/:projectId` reads as a worldline theatre instead of a report panel stack
- [x] pressing Next with no user input progressively reveals all key events and reaches Archive
- [x] legacy public-opinion wording is removed from core UI copy and seed-generation defaults
- [x] actors are framed as agents, rules, environments, materials, natural objects, institutions, and constraints
- [x] canvas density adapts to device size and reduced motion, with the black hole reduced to an anchor rather than the whole scene
- [x] build, tests, smoke, diff check, secret scan, and reference-folder checks pass before push

## Slice 5 Completed

- [x] replaced the report-like stage body with a theatre shell: left lens rail, central progressive worldline, right observation rail, active drawer, and bottom Next control
- [x] added frontend-local reveal state so the viewer can press Next through all key events without writing an intervention
- [x] kept branch selection and intervention/replay entry available without making them the only way to experience the worldline
- [x] cleaned seed-generation defaults, share/replay wording, fixture metadata, entry copy, and rendered stage copy away from old public-opinion language
- [x] renamed the campus fixture to `campus-field-threshold` and moved policy wording toward civic rules and field conditions
- [x] lightened `WorldlineCanvas` with lower density, smaller singularity, adaptive drawing, pointer throttling, and reduced-motion support

## Slice 6 Completed

- [x] added a small backend process-trace builder that derives FACT / INFERENCE / VALUE / ACTION layer outputs per event
- [x] wrote process artifacts into ignored runtime data storage and exposed safe relative artifact paths in the stage response
- [x] added a theatre-side process panel that reveals each event's process layers alongside the worldline
- [x] added intervention-window affordances that select the recommended input type and open the Intervention drawer without forcing the viewer to intervene
- [x] updated API contract, frontend types, unit tests, smoke test, and docs

## Slice 7 Acceptance Criteria

- [x] process trace reads as a computation theatre panel rather than a plain debug card
- [x] current process layer has an expanded inspector for inputs, outputs, and confidence note
- [x] process file truth remains visible through the runtime artifact path and preview metrics
- [x] `npm --workspace apps/web run test:perf` provides a repeatable browser-side canvas FPS and Next-step latency benchmark
- [x] Playwright smoke no longer silently reuses stale local API / web servers
- [x] build, tests, smoke, perf benchmark, diff check, secret scan, and reference-folder checks pass before push

## Slice 7 Completed

- [x] added process orbit / scanline / metric treatment to the theatre center without adding expensive effects
- [x] exposed selected process-layer details in the UI and tests
- [x] added a focused Playwright performance spec for animation frame cadence and Next interaction latency
- [x] updated Playwright server reuse behavior so smoke validates the current checkout
- [x] updated docs after verification

## Slice 8 Acceptance Criteria

- [x] world-state snapshots persist theatre reading state: revealed event count, selected event, selected branch, active surface, and saved timestamp
- [x] stage payload restores persisted defaults so a refresh resumes the current reading instead of returning to the first node
- [x] frontend saves progress after Next, event selection, branch selection, surface changes, and process-window intervention jumps
- [x] UI shows lightweight save state without blocking ordinary navigation
- [x] API, frontend, and E2E tests cover progress persistence across reload
- [x] build, tests, smoke, perf benchmark, diff check, secret scan, and reference-folder checks pass before push

## Slice 8 Planned Work

- [x] add `TheatreProgress` to project models and world-state schema
- [x] add `POST /api/projects/{projectId}/progress`
- [x] include persisted reveal defaults in `stage.surface_defaults`
- [x] add typed frontend API and save-state UI
- [x] update docs after verification

## Slice 8 Completed

- [x] added project-level theatre progress persistence for reveal count, selected event, selected branch, active surface, and saved timestamp
- [x] restored theatre defaults from `stage.surface_defaults` so browser refresh resumes the same reading layer
- [x] saved theatre progress after Next, event/branch/surface changes, process intervention jumps, replay input, share, and calibration paths
- [x] added a lightweight save-state marker that never blocks ordinary stage navigation
- [x] extended API, frontend, and E2E coverage so progress persistence is validated across reload

## Next Candidate Slice

- [ ] run a visual review of the theatre shell against `.ui-ref` and tune spatial rhythm, black-hole scale, and drawer density
- [ ] make Archive and Ripple advanced export/replay tools feel native to the theatre shell instead of utility drawers
- [ ] tighten the existing browser performance benchmark into stricter exhibition thresholds

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
- [x] add a self-contained exhibit HTML export for archive artifacts
- [x] turn the archive poster layer into a stronger export-ready artifact flow
- [x] add a browser-side image export path beyond SVG for the poster artifact
- [x] add a richer saved artifact bundle that carries multiple export surfaces in one package
- [x] bundle the current archive exports into a denser media packet so the exhibit take-away is not only a row of separate files
- [ ] keep extending the archive bundle beyond the current SVG / PNG / TXT / HTML / JSON / ZIP set if a denser media packet becomes valuable
- [x] turn calibration pattern into a comparative archive atlas
- [x] compare calibration records by pattern and tendency, not only chronology
- [x] deepen calibration comparison across wider archive slices if the current atlas proves too shallow
- [x] add wider calibration window slices and branch-family slices so comparison does not stop at recent-vs-full
- [x] deepen calibration into decision-type and longer-horizon longitudinal slices so the archive can compare how different intervention modes age
- [ ] deepen calibration beyond the current slice deck into decision-type or longer-horizon views if needed
- [x] turn Ripple into a continuity explorer instead of a single replay strip
- [x] deepen ripple continuity beyond the current replay track
- [x] turn Ripple into a multi-path replay archive instead of a single continuity chain
- [x] broaden Ripple from one continuity chain into a stronger multi-path replay archive
- [x] deepen Ripple from the current multi-path view into a richer replay-history archive
- [x] add replay-history archive strata so each replay snapshot reads as upstream tension, hinge branch, and downstream drift
- [x] extend the replay-history archive from in-stage derived slices into richer saved replay sets if this first pass proves too shallow
- [x] add a replay set library so saved replay views can be switched without leaving Ripple
- [ ] deepen the replay set library if later we need persisted or more authored replay sets
- [x] add a replay dossier layer so each replay set carries clearer narrative anchors and turning points
- [x] add replay dossier export actions so the selected replay set can leave Ripple as a lightweight local packet
- [x] add a persisted local replay shelf so authored replay packets can be saved, revisited, and re-exported inside Ripple
- [x] deepen the replay dossier into a more authored replay artifact and portable exhibit export
- [x] turn the replay shelf into a more legible replay atlas with a bundled export for saved replay sets
- [x] move saved replay sets from browser-local state into project-level persistence
- [x] remove the deprecated `jsonschema.RefResolver` path from API contract validation
- [x] add clearer curatorial control so replay sets can be authored before save/export instead of only using derived labels
- [x] widen the replay author deck beyond title and note so richer curatorial fields can flow into saved replay artifacts
- [x] move theatre reveal progress from frontend-local memory into project-level persistence
- [ ] deepen the replay dossier further if later we need wider curatorial fields, saved authored collections, or stronger replay writing
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
