# Next Work Plan

Updated: 2026-04-24
Status: Active
Current slice: `Experience Rebuild Slice 17 / Archive Authored Wall Reading completed`

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
- prompt-generated starts that compile into a real worldline and, when local MiniMax is configured, can consume a structured model reasoning packet instead of silently falling back to a generic template
- an `.impeccable.md` design context so future UI work keeps the artwork's visual language consistent
- a stronger orbital theatre polish pass that makes the current stage feel less like stacked cards
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

## Slice 9 Acceptance Criteria

- [x] project has a reusable `.impeccable.md` design context describing audience, tone, aesthetic direction, and design principles
- [x] `/world/:projectId` gains a stronger orbital-theatre treatment without copying or tracking `.ui-ref`
- [x] central stage includes lightweight orbital event readouts tied to real revealed worldline state
- [x] panel, drawer, and bottom-bar styling moves further away from generic report/card density
- [x] frontend tests cover the new theatre readout/orbit affordances
- [x] build, tests, smoke, perf benchmark, diff check, secret scan, and reference-folder checks pass before push

## Slice 9 Completed

- [x] added `.impeccable.md` with durable art-first UI guidance for future design iterations
- [x] added a topbar orbit readout and a central event orbit map bound to revealed/active worldline state
- [x] retuned theatre colors, spacing, panel borders, drawer treatment, and center-field atmosphere toward the `.ui-ref` orbital observatory language
- [x] preserved reduced-motion behavior and existing canvas performance boundaries
- [x] updated route and smoke coverage for the new readout/orbit UI

## Slice 10 Acceptance Criteria

- [x] Ripple exposes a theatre-native replay console with metrics tied to revealed track, alternate pressure, saved sets, and latest bend
- [x] Ripple can export a local trace packet from the currently revealed worldline without backend calls or secrets
- [x] Archive exposes an afterimage capsule with share, decision, calibration, and reveal metrics
- [x] Archive can export or copy a local capsule artifact from existing stage state without relying on live LLM work
- [x] the new Ripple / Archive affordances use the orbital theatre language rather than generic utility-card styling
- [x] frontend route and smoke coverage assert the new console/capsule affordances
- [x] build, tests, smoke, perf benchmark, diff check, secret scan, and reference-folder checks pass before push

## Slice 10 Planned Work

- [x] mark Slice 10 as the active doc-tracked iteration before code changes
- [x] add typed frontend derived metrics for Ripple and Archive instruments
- [x] add local export helpers for ripple trace and archive afterimage capsule
- [x] retune drawer styling so the advanced tools feel like stage instruments
- [x] add focused frontend and E2E coverage
- [x] update docs after verification

## Slice 10 Completed

- [x] replaced the plain Ripple drawer with a replay console that reads revealed nodes, alternate pressure, saved replay count, average confidence, latest bend, and ripple cards as theatre instrumentation
- [x] added a frontend-only Ripple trace JSON export using current stage state only
- [x] replaced the plain Archive share card with an afterimage capsule carrying reveal, decision, calibration, and ripple-card metrics
- [x] added frontend-only Archive capsule copy/export actions using the existing share snapshot, revealed track, decision log, and calibration state
- [x] added instrument-specific styling so Ripple and Archive read as orbital theatre tools rather than generic report cards
- [x] updated frontend route and Playwright smoke coverage for the new console/capsule affordances

## Slice 11 Acceptance Criteria

- [x] performance benchmark asserts a stricter desktop exhibition budget instead of the old loose MVP threshold
- [x] canvas frame cadence target is at least 45 FPS in the default desktop fixture path
- [x] ordinary Next-step reveal latency target is under 150 ms locally
- [x] performance spec records benchmark evidence so failures are diagnosable
- [x] mobile and low-height exhibition viewports keep the worldline theatre, process panel, and Next control reachable without horizontal overflow
- [x] any responsive hardening stays CSS-only or frontend-local, with no contract or backend changes
- [x] build, tests, smoke, perf benchmark, diff check, secret scan, and reference-folder checks pass before push

## Slice 11 Planned Work

- [x] mark Slice 11 as the active doc-tracked iteration before code changes
- [x] refactor the Playwright performance spec around named exhibition budgets
- [x] add low-height and mobile viewport coverage to the performance/responsive suite
- [x] harden theatre CSS for low-height and mobile interaction reachability
- [x] update docs after verification

## Slice 11 Completed

- [x] replaced the old 24 FPS / 300 ms MVP performance assertions with named exhibition budgets: 45 FPS desktop frame cadence and 150 ms Next-step latency
- [x] attached benchmark JSON evidence from the Playwright performance spec so future regressions have inspectable numbers
- [x] removed wasteful continuous canvas redraws by switching `WorldlineCanvas` to dirty-frame rendering
- [x] removed theatre-route constant backdrop blur and infinite process-scan animation that were depressing headless frame cadence
- [x] added mobile and low-height viewport checks for theatre visibility, process panel reachability, Next control reachability, and horizontal overflow
- [x] hardened theatre CSS for mobile and low-height displays without changing public contracts or backend behavior

## Slice 12 Acceptance Criteria

- [x] pressing the prompt-generation entry action returns a driveable project in deterministic mode without waiting on a live MiniMax call
- [x] generated prompt projects contain prompt-specific actants, key events, branches, cost lenses, knowledge layers, and process traces
- [x] fixture creation and prompt creation both keep public contracts unchanged
- [x] Playwright smoke covers prompt entry, theatre load, process trace visibility, and Next-step advancement
- [x] local smoke can run when a current dev server is already active, while CI still starts clean servers
- [x] build, tests, smoke, diff check, secret scan, and reference-folder checks pass before push

## Slice 12 Completed

- [x] replaced prompt creation's default live-LLM dependency with a deterministic prompt compiler
- [x] separated deterministic prompt compilation from MiniMax availability; Slice 13 then re-enabled local MiniMax reasoning with a longer timeout and visible fallback artifacts
- [x] added prompt-specific worldline derivation so the submitted seed drives the first three events and their process artifacts
- [x] added API tests proving prompt projects are seed-specific and do not call the live LLM by default
- [x] added a prompt-generation smoke path that advances the generated theatre
- [x] changed Playwright local server reuse to `!process.env.CI` so local development is less brittle without weakening CI

## Slice 13 Acceptance Criteria

- [x] MiniMax seed compiler responses that prepend `<think>...</think>` are parsed into the final JSON object instead of being discarded
- [x] local MiniMax prompt generation uses a timeout that matches the observed model latency and can produce a real `seed_prompt+MiniMax` worldline
- [x] successful MiniMax runs write a safe runtime reasoning artifact and surface it through `stage.process_trace.reasoning_run`
- [x] failed MiniMax runs write a safe fallback artifact and expose fallback status instead of silently pretending the model path succeeded
- [x] the frontend process panel shows the latest model reasoning / fallback artifact without exposing API keys or raw hidden reasoning
- [x] API tests cover `<think>` parsing, structured MiniMax packets, and fallback artifact redaction
- [x] real local MiniMax verification, build, tests, smoke, diff check, secret scan, and reference-folder checks pass before push

## Slice 13 Completed

- [x] updated the OpenAI-compatible adapter to recover JSON after MiniMax reasoning prefaces
- [x] raised `LLM_REQUEST_TIMEOUT` guidance to `180` seconds and updated the local ignored `.env`
- [x] proved a real prompt creation path returns `source_label=seed_prompt+MiniMax`, `minimax_reasoning` knowledge, and a completed MiniMax process artifact
- [x] added `ReasoningRunRecord` to world state and exposed the latest run in stage process trace
- [x] added a stage UI strip for model reasoning / fallback artifacts
- [x] added fallback artifact persistence so local failures become diagnosable without leaking secrets

## Slice 14 Acceptance Criteria

- [x] prompt project creation returns a driveable deterministic worldline immediately, even when local MiniMax credentials are configured
- [x] prompt projects created with MiniMax available enqueue a background `seed_compiler` reasoning task instead of blocking the entry route
- [x] `GET /api/projects/{projectId}/reasoning` exposes safe task status, runtime artifact path, progress step, and summary without returning secrets or raw hidden reasoning
- [x] completed background reasoning can merge a structured MiniMax packet into the existing project snapshot and refresh stage process trace
- [x] failed background reasoning records a visible fallback artifact instead of silently disappearing
- [x] the stage UI shows backstage model progress and lets viewers continue pressing Next while the model job runs
- [x] tests cover immediate prompt creation, queued/running/completed/failed reasoning status, merge behavior, and no-key deterministic fallback
- [x] build, tests, smoke, diff check, secret scan, and reference-folder checks pass before push

## Slice 14 Completed

- [x] added a small in-process reasoning job registry and daemon background worker around the existing seed compiler path
- [x] split prompt compilation into deterministic first render plus optional MiniMax enrichment merge
- [x] added safe backend status endpoint and stage payload refresh behavior
- [x] added typed frontend polling and a theatre-native backstage computation strip
- [x] updated API, frontend, and E2E coverage for async reasoning behavior
- [x] updated docs after verification

## Slice 15 Acceptance Criteria

- [x] every queued/running/merge/completed/fallback/failed backstage reasoning phase writes a safe local JSON process artifact under ignored `data/runtime/process/...`
- [x] `GET /api/projects/{projectId}/reasoning` returns an ordered artifact trail with step label, status, summary, timestamp, and relative artifact path
- [x] artifact trail files never include provider secrets, raw hidden reasoning, or frontend-sensitive payloads
- [x] the stage process panel shows the latest backstage artifact trail while the viewer can continue pressing Next
- [x] tests cover artifact trail creation for queued, running, completed, and fallback paths
- [x] build, tests, smoke, diff check, secret scan, and reference-folder checks pass before push

## Slice 15 Completed

- [x] extended the reasoning job manager with a safe artifact journal under ignored runtime data
- [x] added `artifact_trail` to the reasoning-status contract, Pydantic response, and frontend types
- [x] showed a compact backstage file trail in the theatre process panel
- [x] updated API and frontend tests for artifact trail creation, schema validation, redaction, and visibility
- [x] updated docs after verification

## Next Candidate Slice

- [ ] deepen Archive/Ripple artifact writing quality now that their theatre-native instrument shells are in place
- [ ] consider a durable persisted reasoning queue or streaming progress protocol if in-process jobs become too fragile for exhibition deployment
- [ ] continue visual review on mobile and low-height exhibition displays after the new performance hardening
- [ ] make calibration more theatrical inside the Archive drawer instead of remaining utility-like

## Slice 16 Acceptance Criteria

- [x] Archive exposes a calibration constellation / afterimage instrument derived from existing `calibration_records`
- [x] the constellation shows dominant outcome, latest outcome, calibrated branch count, and calibrated-branch confidence residue without adding backend calls or LLM dependency
- [x] recent calibration records render as orbiting archive marks instead of only a form/log
- [x] the afterimage capsule export includes the derived calibration constellation payload
- [x] frontend tests cover the constellation rendering and empty/non-empty archive states
- [x] build, tests, smoke, perf benchmark, diff check, secret scan, and reference-folder checks pass before push

## Slice 16 Completed

- [x] marked Slice 16 as the active doc-tracked iteration before code changes
- [x] derived calibration constellation metrics and recent marks from current stage state
- [x] added a theatre-native constellation card to the Archive drawer
- [x] included constellation data in the local Archive capsule export
- [x] updated frontend tests and docs after verification

## Slice 17 Acceptance Criteria

- [x] Archive exposes an authored wall-reading card derived from current worldline state, selected branch, cost lens, ripple, and calibration constellation
- [x] the wall reading contains curator-facing title, thesis, cost line, calibration line, and closing afterimage note in the active UI language
- [x] wall reading can be copied/exported locally without backend calls, live LLM dependency, or frontend secrets
- [x] afterimage capsule export includes the authored wall-reading payload
- [x] frontend tests cover rendered wall reading and export/copy affordances
- [x] build, tests, smoke, perf benchmark, diff check, secret scan, and reference-folder checks pass before push

## Slice 17 Completed

- [x] marked Slice 17 as the active doc-tracked iteration before code changes
- [x] derived authored archive wall reading from existing stage state
- [x] added wall-reading card and local copy/export actions to Archive
- [x] included wall-reading data in the Archive capsule packet
- [x] updated frontend tests and docs after verification

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
- [x] add the `.impeccable.md` design context and first orbital UI polish pass
- [x] make Archive and Ripple advanced export/replay tools feel native to the theatre shell instead of utility drawers
- [x] tighten the existing browser performance benchmark into stricter exhibition thresholds
- [x] fix prompt-generated project creation so deterministic mode immediately produces a driveable, seed-specific worldline without waiting on live LLM work
- [x] reconnect local MiniMax prompt generation so Pro-style starts can produce a real structured reasoning packet when credentials are configured
- [x] add a background/async model-enrichment lane that can enrich prompt starts after the deterministic worldline is already visible
- [x] add a backstage reasoning artifact trail so async model work is visible as ordered local process files
- [ ] deepen the replay dossier further if later we need wider curatorial fields, saved authored collections, or stronger replay writing
- [x] add authored Archive wall-reading output so the afterimage is not only a structured data packet
- [x] make Archive calibration read as a constellation / afterimage instrument instead of only an input drawer
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
