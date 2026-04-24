# Current Status

Updated: 2026-04-24
Status: Active
Phase: `experience-first rebuild / slice 20 archive calibration drift map completed`

## One-line Summary

`MiroWorld-dev` now has a working standalone monorepo, public contracts, fixture-backed API, prompt/fixture project creation, replay/share/calibration flow, tests, CI, one-click local startup, and a worldline theatre shell where `/world/:projectId` progressively reveals events through a Next-driven stage instead of reading as a report stack. Prompt-generated projects now compile into prompt-specific key events, actants, cost lenses, process-trace artifacts, and branches immediately; when local MiniMax credentials are configured, a backstage reasoning job can enrich the project asynchronously and expose an ordered trail of safe runtime computation artifacts in the stage. Theatre reading progress persists in project snapshots, and the stage has a first `.impeccable.md`-guided orbital polish pass so it reads more like an exhibition instrument than a report page. Ripple and Archive now also read as theatre instruments: Ripple exposes a replay console, authored drift reading, local trace export, and copy/export actions, while Archive exposes an afterimage capsule, authored wall reading, calibration constellation, branch-filtered calibration drift reading, event-to-event calibration drift map, and copy/export actions. The browser benchmark now enforces a stricter exhibition budget, and mobile / low-height viewport reachability is covered by Playwright.

The main product risk is no longer "can it run." It is "how far the public experience has been pushed":

- the shell now reads as a progressive worldline theatre instead of a long panel stack or report page
- a viewer can press Next without writing an intervention and still reach a complete Archive afterimage
- core display text now rewrites old public-opinion terms such as initiator, public climate, platform, and public view into trigger source, field conditions, rule layer, and observable layer
- the canvas now uses lower line density, pointer throttling, reduced-motion fallback, and a smaller singularity so the worldline remains primary
- backend process-trace files now appear while the line advances, with FACT / INFERENCE / VALUE / ACTION outputs for the current node
- prompt starts now drive a real three-node worldline from the submitted seed instead of reusing the generic fixture-like event template
- live MiniMax seed enrichment now works when local credentials are present: MiniMax `<think>` prefaces are stripped before JSON parsing, the timeout is long enough for the current model, and failures are recorded as visible fallback process artifacts instead of silent template downgrades
- MiniMax enrichment now runs as backstage computation after prompt creation, so the entry action returns a driveable deterministic worldline immediately instead of waiting for the full model response
- MiniMax backstage computation now writes an ordered checkpoint trail for queued, model request, merge, completed, fallback, and failed phases so viewers can inspect process files instead of only waiting
- high-pressure nodes now expose intervention windows that jump into the Intervention drawer with a recommended input type
- process artifacts now include orbit progress, runtime artifact strip, preview metrics, and an expanded selected-layer inspector
- browser performance now has a repeatable Playwright benchmark instead of only manual impressions
- theatre reading progress now saves back to the project snapshot and restores through `stage.surface_defaults` after refresh
- `.impeccable.md` now captures the durable design context: cosmic, precise, consequential, with the worldline and cost of choice as the primary visual subject
- the theatre UI now has a topbar orbit readout and central event orbit map bound to real reveal state
- the archive/share space now reads more like a curator-facing artifact chamber instead of a utility output list
- and its core artifact can now leave the UI as a local poster SVG or share bundle
- and the archive can now leave the UI as a self-contained exhibit HTML artifact instead of only fragmented exports
- and the archive poster can now also leave the UI as a browser-side PNG while the whole artifact set can be saved as a single bundle
- calibration no longer reads as a plain log; it now exposes dominant outcomes, recent tendency, and branch focus
- and calibration can now be read through recent, prior, full, and branch-focused slices instead of stopping at one atlas row
- Ripple now lets the viewer steer event focus and branch focus from inside the continuity surface itself
- and the linefield opens wider on the Ripple surface so continuity reads across more events than before
- Ripple now also lets the viewer compare active, primary, and alternate drift paths side by side
- and Ripple can now read the selected path as replay-history slices of upstream tension, hinge branch, and downstream drift
- and Ripple can now switch between named replay sets such as current, stabilizing, and pressure readings without leaving the surface
- and Ripple can now read each replay set through clearer dossier anchors such as entry, hinge pressure, and terminal exposure
- and Ripple can now turn the selected replay dossier into a portable local packet instead of leaving it as an in-scene reading only
- and Ripple can now keep authored replay packets on a small project-persisted shelf so replay states can be revisited instead of only exported once
- and Ripple now lets the viewer rewrite the replay title and curatorial note before saving or exporting a replay set
- and Ripple now also lets the viewer rewrite the replay deck line and closing note before saving or exporting a replay set
- and calibration can now be read not only by branch and window, but also by decision type and longer-horizon archive slices
- and the archive exports can now also leave the shell as a denser local media packet instead of only a row of separate files
- and Ripple can now leave the shell not only as a technical packet, but also as a more authored replay artifact and replay exhibit
- and the project replay shelf now also reads as a replay atlas instead of only a plain restore list
- and saved replay sets now persist with the project snapshot instead of living only inside browser-local state
- and Ripple now has a theatre-native replay console with revealed-track metrics and a frontend-only trace packet export
- and Ripple now derives an authored drift-reading text from revealed track, selected branch, latest bend, visible ripple cards, and saved replay count
- and Archive now has a theatre-native afterimage capsule with reveal, decision, calibration, and export/copy affordances
- and Archive calibration now reads as a constellation of actual outcomes, dominant result, latest return, calibrated branches, and confidence residue
- and Archive calibration can now be filtered by branch slice and read as authored calibration drift instead of only constellation metrics
- and Archive calibration now also shows event-to-event drift maps so actual outcomes read as temporal movement across the worldline
- and Archive now produces an authored wall-reading text derived from the selected worldline, branch, cost, ripple, and calibration state instead of only a structured data capsule
- and the performance benchmark now targets 45 FPS desktop frame cadence plus sub-150 ms Next-step reveal latency instead of the earlier loose MVP budget
- and mobile / low-height viewport checks now guard theatre reachability, process panel visibility, Next control access, and horizontal overflow
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

### Frontend experience rebuild slice 4 (export actions pass)

- Archive can export its current poster artifact as a local SVG without involving the backend or exposing secrets
- Archive can export a local share-bundle text file that packages summary, share text, decision log, and calibration notes
- frontend tests now cover the export actions at a minimal interaction level

### Frontend experience rebuild slice 4 (calibration atlas pass)

- Archive calibration view now compares the recent window against the full archive rather than only listing records
- calibration now surfaces dominant outcomes, recent tendency, and the most-tested branch as first-pass comparative cues
- frontend route tests now cover the presence of the calibration atlas

### Frontend experience rebuild slice 4 (ripple continuity explorer pass)

- Ripple now contains an event-to-event continuity explorer instead of only a single replay strip
- Ripple can change event focus and branch focus directly inside the scene without returning to Observatory
- the worldline canvas opens to the full event span on the Ripple surface so continuity reads across more nodes

### Frontend experience rebuild slice 4 (exhibit html export pass)

- Archive can now export a self-contained exhibit HTML artifact instead of only separate SVG / TXT fragments
- the exhibit export packages poster copy, wall text, decision trace, and calibration snapshot into one offline file
- frontend route tests now cover the additional export action

### Frontend experience rebuild slice 4 (multi-path ripple archive pass)

- Ripple now compares active, primary, and alternate drift paths side by side instead of staying on one continuity chain
- each path node can directly retarget the stage to its event and branch
- frontend route tests now cover the multi-path ripple archive interaction

### Frontend experience rebuild slice 4 (replay-history archive pass)

- Ripple now contains a deeper replay-history archive layered beneath the path comparison view
- each replay-history slice reads as upstream tension, hinge branch, and downstream drift for the chosen path
- replay-history entries can retarget the stage directly and frontend route tests now cover the new interaction

### Frontend experience rebuild slice 4 (artifact bundle and image export pass)

- Archive can now export the poster as a browser-side PNG instead of relying on SVG alone
- Archive can now export a richer artifact bundle JSON that carries the share snapshot, logs, calibration state, and embedded export surfaces together
- frontend route tests now cover the extended export actions without changing backend contracts or secret handling

### Frontend experience rebuild slice 4 (calibration slice deck pass)

- Archive calibration now exposes wider window slices for recent, prior, and full archive comparison
- calibration now also surfaces branch-focused slice cards so dominant branch families can be compared directly
- frontend route tests now cover the deeper calibration slice deck interaction layer

### Frontend experience rebuild slice 4 (calibration longitudinal pass)

- Archive calibration now also reads by matched decision type instead of only by branch family and time window
- calibration now exposes origin, hinge, and latest chronological slices so longer-horizon drift can be compared directly
- frontend route tests now cover the decision-type and longitudinal calibration views

### Frontend experience rebuild slice 4 (media packet pass)

- Archive can now bundle poster svg, poster png, share text, exhibit html, artifact bundle json, and a manifest into one local media packet zip
- the media packet stays frontend-only and secret-safe by assembling the packet entirely from existing local export surfaces
- frontend route tests now cover the denser archive packet export alongside the earlier single-file export actions

### Frontend experience rebuild slice 4 (replay authorship pass)

- Ripple now derives a more authored replay artifact from the selected replay set instead of stopping at a technical dossier and packet
- the authored replay artifact can now be copied or exported as a standalone replay exhibit html while saved shelf entries can re-export that exhibit later
- frontend route tests now cover the authored replay artifact and its added export actions alongside the existing replay dossier flow

### Frontend experience rebuild slice 4 (replay atlas pass)

- Ripple shelf now reads as a replay atlas instead of only a restore list, with quick-restore atlas cards for saved replay sets
- saved replay sets can now leave Ripple together as a bundled replay atlas html export instead of only as one-by-one replay files
- frontend route tests now cover the atlas view and replay atlas export path alongside the existing replay shelf flow

### Frontend experience rebuild slice 4 (persisted replay set pass)

- saved replay sets now persist inside project snapshots instead of browser-local storage only
- Ripple now saves and removes replay shelf entries through backend routes while keeping replay atlas and replay exhibit exports working
- API contract validation no longer depends on deprecated `jsonschema.RefResolver`

### Frontend experience rebuild slice 4 (authored replay set pass)

- Ripple now exposes an editable replay author deck so title and curatorial note can be rewritten before save or export
- authored replay edits now flow through dossier, artifact, packet, exhibit, and replay shelf persistence instead of stopping at a temporary preview
- persisted replay sets can now coexist as authored variants when the same replay focus is saved under different curatorial titles

### Frontend experience rebuild slice 4 (replay curation field pass)

- Ripple author deck now exposes richer curatorial fields beyond title and note, including deck line and closing note
- the extra curatorial fields now flow through the authored replay artifact preview, export packet, exhibit output, and replay shelf restoration
- frontend route tests now cover the wider author deck fields and their persistence-aware restore path

### Frontend experience rebuild slice 4 (replay set library pass)

- Ripple now exposes a small replay set library instead of only one replay-history reading
- named replay sets such as current, stabilizing, and pressure can switch the saved replay view without leaving Ripple
- frontend route tests now cover the replay set library interaction layer

### Frontend experience rebuild slice 4 (replay dossier pass)

- Ripple now gives each replay set a dossier layer instead of only a selectable set card and history list
- the dossier now surfaces entry anchor, hinge pressure, and terminal exposure so the line reads more like an authored replay
- frontend route tests now cover the replay dossier interaction layer

### Frontend experience rebuild slice 5 (worldline theatre pass)

- `/world/:projectId` now opens as a worldline theatre with a left lens rail, central progressive linefield, right observation rail, drawer surfaces, and a bottom Next control
- pressing Next with no input progressively reveals key events, selects the default primary branch, updates the visible track, and reaches Archive
- legacy public-opinion wording is removed from the rendered core UI and seed-generation defaults now frame the system through actants, rules, environments, materials, natural objects, institutions, and constraints
- `.ui-ref/` and `ui-ref/` are ignored so the local reference package cannot be staged accidentally
- the canvas now reduces line density, throttles pointer sampling, supports reduced motion, and keeps the black hole as a smaller anchor rather than the visual center of gravity

### Experience rebuild slice 6 (process trace and intervention windows)

- backend stage payloads now include deterministic `process_trace` data derived from the current world state
- each process step writes a safe local runtime JSON artifact under ignored `data/runtime/process/...`
- the theatre center now shows the current event's process file path, layer results, and calculation summary during progressive reveal
- high-pressure or contradiction-heavy steps expose an intervention window that opens the Intervention drawer with the recommended input type and target branch
- route tests, API contract tests, and smoke coverage now include process trace visibility and intervention-window entry

### Experience rebuild slice 7 (computation theatre and performance benchmark)

- process trace display now includes an orbit progress strip, runtime artifact strip, preview metrics, and selected-layer inspector
- FACT / INFERENCE / VALUE / ACTION can now be opened into input / output / confidence-note detail while the data-file path remains visible
- the process panel uses lightweight scanline and transform/opacity treatment with reduced-motion fallback
- Playwright smoke now starts fresh local API / web servers instead of silently reusing stale processes
- `npm run test:perf` now runs a browser benchmark for canvas frame cadence and Next-step latency

### Experience rebuild slice 8 (persistent theatre reading)

- world-state snapshots now include `theatre_progress` with revealed event count, selected event, selected branch, active surface, and saved timestamp
- `POST /api/projects/{projectId}/progress` saves sanitized theatre reading state without exposing secrets or requiring LLM work
- `stage.surface_defaults` now restores persisted theatre defaults so refresh resumes the same reading layer
- the stage saves progress after Next, event selection, branch selection, surface changes, process intervention jumps, replay input, share, and calibration paths
- frontend, API, and E2E coverage now validate progress persistence across reload

### Experience rebuild slice 9 (impeccable theatre polish)

- `.impeccable.md` now stores the project design context and principles for future UI work
- the stage topbar now includes an orbit readout tied to revealed node count
- the central theatre field now includes a lightweight event orbit map that distinguishes latent, revealed, and active nodes
- theatre colors, spacing, panel borders, drawers, and bottom-bar treatment were retuned toward the local `.ui-ref` orbital observatory language without copying or tracking the reference package
- frontend route and smoke tests now cover the new readout/orbit affordances

### Experience rebuild slice 10 (archive/ripple theatre instruments)

- Ripple now exposes a replay console tied to revealed nodes, alternate pressure, saved replay sets, average confidence, latest bend, and visible ripple cards
- Ripple can export a local JSON trace packet from the current stage state without backend work, live LLM calls, or frontend secrets
- Archive now exposes an afterimage capsule tied to share snapshot, revealed track, decision log, and calibration state
- Archive can copy a text capsule or export a JSON capsule locally from existing stage state
- route tests and Playwright smoke now cover the new theatre-native console/capsule affordances

### Experience rebuild slice 11 (exhibition performance budget)

- Playwright performance coverage now uses named exhibition budgets instead of loose MVP assertions
- default desktop frame cadence must stay at or above 45 FPS and ordinary Next reveal latency below 150 ms locally
- the performance spec attaches benchmark JSON evidence for future regression diagnosis
- `WorldlineCanvas` now uses dirty-frame rendering instead of continuous redraw when nothing is changing
- theatre-route constant backdrop blur and infinite process-scan animation were removed to avoid persistent compositor cost
- mobile and low-height viewport checks now verify theatre visibility, process panel reachability, Next control access, and horizontal overflow

### Experience rebuild slice 12 (prompt worldline driver fix)

- prompt project creation has a deterministic seed compiler path, and Slice 13 reconnects the live MiniMax path when local credentials are configured
- the seed compiler now derives prompt-specific actants, key events, branches, costs, knowledge layers, and process traces from the submitted seed
- prompt-generated projects can be opened and advanced through the worldline theatre with no manual intervention
- Playwright smoke now covers prompt generation and one-step advancement
- local smoke can reuse an already running dev server outside CI, while CI still starts clean servers

### Experience rebuild slice 13 (MiniMax reasoning packet fix)

- fixed the OpenAI-compatible MiniMax adapter so reasoning-model responses that prepend `<think>...</think>` can still yield the final JSON object
- raised the recommended MiniMax request timeout to `180` seconds after a real local prompt run proved the 60-second path timed out and silently fell back
- live prompt creation now produces `source_label=seed_prompt+MiniMax`, `minimax_reasoning` knowledge, generated events, and a `data/runtime/process/.../00-minimax-seed-reasoning.json` artifact when MiniMax completes
- failed local MiniMax attempts now write a safe `00-minimax-seed-fallback.json` artifact and expose fallback status in `stage.process_trace.reasoning_run`
- the stage UI now shows the latest model reasoning / fallback artifact strip without exposing API keys or raw provider hidden reasoning

### Experience rebuild slice 14 (async MiniMax backstage reasoning)

- prompt project creation now returns the deterministic worldline first and queues MiniMax seed reasoning in the background when credentials are configured
- `GET /api/projects/{projectId}/reasoning` exposes queued/running/completed/fallback/failed/disabled status, progress step, summary, artifact path, and refreshed stage when available
- completed MiniMax packets merge back into the project snapshot if the viewer has not authored inputs yet
- if the viewer has already intervened or saved authored state, completed reasoning is archived without overwriting their disturbed worldline
- the stage UI polls the reasoning endpoint and shows a backstage computation strip while the model job runs
- real local prompt creation with MiniMax credentials returned in about `0.02s` with the model job running backstage

### Experience rebuild slice 15 (backstage reasoning artifact trail)

- every backstage reasoning phase now writes a safe local checkpoint artifact under ignored `data/runtime/process/.../reasoning/...`
- `GET /api/projects/{projectId}/reasoning` now returns `artifact_trail` with ordered step, status, summary, timestamp, and relative path metadata
- the theatre process panel shows the latest backstage trail while the viewer can keep pressing Next through the worldline
- API and frontend tests now cover queued, completed, fallback, and rendered trail visibility without leaking provider keys or raw hidden reasoning

### Experience rebuild slice 16 (archive calibration constellation)

- Archive now derives a theatre-native calibration constellation from existing `calibration_records`
- the constellation shows dominant result, latest outcome, calibrated branch count, confidence residue, and recent orbiting outcome marks
- empty calibration archives now have a clear dormant constellation state instead of a blank utility area
- the local afterimage capsule export now includes a derived calibration constellation payload

### Experience rebuild slice 17 (archive authored wall reading)

- Archive now derives a curator-facing wall reading from the current worldline, selected branch, cost cue, ripple, and calibration constellation
- the wall reading can be copied or exported locally without backend calls, live LLM dependency, or frontend secrets
- the local afterimage capsule export now includes the authored wall-reading payload
- frontend tests cover rendered wall text and local export affordances

### Experience rebuild slice 18 (ripple authored drift reading)

- Ripple now derives a curator-facing drift reading from the revealed track, selected branch, latest bend, visible ripple cards, and saved replay count
- the drift reading can be copied or exported locally without backend calls, live LLM dependency, or frontend secrets
- the local Ripple trace packet export now includes the authored `drift_reading` payload
- frontend tests cover rendered drift text and local export affordances

### Experience rebuild slice 19 (archive calibration drift reading)

- Archive calibration now exposes branch-filter chips derived from existing calibration records
- Archive now derives an authored calibration drift reading for all records or the selected branch slice
- the reading names dominant result, latest outcome, event drift, and confidence residue in the active UI language
- the local afterimage capsule export now includes the selected calibration drift-reading payload
- frontend tests cover branch filter interaction and rendered calibration drift text

### Experience rebuild slice 20 (archive calibration drift map)

- Archive now exposes a compact event-to-event calibration drift map for the selected calibration slice
- the map shows chronological calibration nodes, branch labels, result labels, actual outcomes, and result-to-result transitions
- the existing branch filter now updates both the authored reading and the temporal drift map
- the local afterimage capsule export now includes the selected calibration drift-map payload
- frontend tests cover all-record and branch-filtered drift sequences

### Verification baseline

- `npm run build` passes
- `npm run test` passes
- `npm run smoke` passes
- `npm run test:perf` passes
- `git diff --check` passes
- secret pattern scan returns no matches for the MiniMax key fragment
- `git ls-files .ui-ref ui-ref` returns no tracked reference files

## Still Missing

### Product / experience gaps

- the new theatre shell restores progressive unfolding, and both Archive/Ripple now have first authored reading outputs, while future writing passes can still become more model-assisted and less deterministic
- the canvas is lighter and now has stricter exhibition budget checks, but real physical display testing is still needed before installation
- calibration history now has a theatre-native constellation, branch-filtered drift reading, and event-to-event drift map, but it can still gain model-assisted takeaways and richer visual navigation
- mobile and low-height exhibition layouts need another visual pass after the new orbital polish

### Content expression gaps

- the UI display layer cleans old public-opinion terms, but more fixture narratives can still be rewritten around non-human actants and natural/material constraints
- live MiniMax enrichment is now asynchronous and file-visible, but the job runner is still an in-process lightweight worker rather than a durable persisted queue
- the layer lens is now visible, but its depth is still mostly presentation-layer driven rather than fully model-driven
- cost narration can become more comparative across branches, not just branch-local
- archive artifacts can become more authored and less template-like as share formats mature

### Documentation gaps

- canonical docs now exist in-repo
- the next improvement is to keep them moving slice by slice without falling back to chat-only history

## Current Focus

The next active slice continues after `Experience Rebuild Slice 20`:

- consider a durable persisted reasoning queue or streaming progress protocol now that checkpoint files are visible but still in-process
- keep mobile and low-height visual review active through future UI passes, especially on real exhibition hardware
- deepen calibration interaction with model-assisted calibration takeaways
- consider a second editorial pass that lets the async MiniMax lane safely enrich Archive/Ripple writing without blocking the theatre
