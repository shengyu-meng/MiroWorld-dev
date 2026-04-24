# Development Log

## 2026-04-23 - Baseline rebuild scaffold

- initialized the standalone `MiroWorld-dev` monorepo
- connected the repo to `origin/main`
- added strict ignore rules before importing assets and fixtures
- built the FastAPI API core and Vue web shell
- copied public contracts and curated fixtures from the legacy repo
- wired replay, share, and calibration through the new API
- added contract, API, frontend, and smoke verification
- pushed baseline as `87a4424 Bootstrap MiroWorld experience MVP`

## 2026-04-23 - Local startup tooling

- added one-click local start and stop scripts
- made the scripts create `.env`, install dependencies, manage ports, and cleanly stop process trees
- documented startup flow in `README.md`
- pushed the tooling pass as `3adcfab Add one-click local start and stop scripts`

## 2026-04-23 - Experience Rebuild Slice 1

Completed in this iteration:

- created canonical docs inside `MiroWorld-dev`
- rebuilt `/` into a line-first public entry scene
- rebuilt `/world/:projectId` into a single-active-scene stage shell
- centralized Chinese and English UI copy
- exposed `FACT / INFERENCE / VALUE / ACTION` as a visible stage lens
- reorganized archive / replay / annotation presentation into the new shell
- updated frontend tests and smoke flow to follow the new interaction path

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Follow-on opportunities identified during this slice:

- deepen Archive into a fuller `Debrief / Share / Export` destination
- strengthen Observatory branch-comparison density
- decide whether the linefield should gain a dedicated branch-explorer mode

## 2026-04-23 - Experience Rebuild Slice 2 (archive and observatory pass)

Completed in this iteration:

- expanded Archive into a richer chamber with wall label, archive summary, share text, decision trace, and calibration history
- surfaced evidence notes earlier inside Observatory cards for faster branch reading
- kept replay/share/calibration behavior and public contracts unchanged

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 2:

- decide whether branch comparison should become its own scene or a stronger overlay inside the existing linefield
- continue polishing share/export presentation beyond text-first output

## 2026-04-23 - Experience Rebuild Slice 2 (branch field overlay pass)

Completed in this iteration:

- updated the docs to make the overlay-vs-dedicated-scene decision explicit
- added an in-shell branch-field overlay so the linefield becomes a selectable branch surface
- strengthened Observatory with a comparison board for the selected event
- cleaned up the stage-facing copy source while keeping contracts stable

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Next likely slice after this pass:

- evolve share/export toward richer visual artifacts
- make calibration history easier to read at a glance
- deepen ripple history beyond the latest bend

## 2026-04-23 - Experience Rebuild Slice 3 (visual artifact pass started)

Planned in this iteration:

- add a visual poster/export layer inside Archive without changing public contracts
- turn calibration history from a simple list into a more pattern-readable record
- make Ripple read like a propagation track instead of only a latest-bend summary

## 2026-04-23 - Experience Rebuild Slice 3 (visual artifact pass completed)

Completed in this iteration:

- rebuilt Archive around a visual poster/export artifact instead of text-only share output
- added explicit export cards for poster caption, excerpt, archive summary, and copyable share text
- introduced a first-pass calibration pattern meter so recent records can be read at a glance
- reshaped Ripple into a propagation-track timeline rather than a single latest-bend panel
- kept the existing public contracts and backend API behavior unchanged

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Next likely slice after this pass:

- make the archive artifact export-ready beyond in-app presentation
- deepen calibration from pattern view to comparative reading
- keep extending linefield / ripple continuity toward fuller event-to-event exploration

## 2026-04-23 - Experience Rebuild Slice 4 (export actions pass started)

Planned in this iteration:

- add local export actions so the archive poster can leave the UI as a reusable artifact
- add a lightweight share bundle export without introducing frontend-side secret risk
- keep the export flow inside the existing public shell and contracts

## 2026-04-23 - Experience Rebuild Slice 4 (export actions pass completed)

Completed in this iteration:

- added local Archive export actions for poster SVG and share-bundle TXT outputs
- kept the export flow fully frontend-side so no backend contract or secret handling changed
- extended frontend route coverage so the archive export buttons are exercised in tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- deepen the artifact path beyond local SVG / TXT export
- make calibration more comparative than the current pattern view
- extend ripple and linefield continuity beyond the current replay track

## 2026-04-23 - Experience Rebuild Slice 4 (calibration atlas pass started)

Planned in this iteration:

- turn calibration from a simple pattern meter into a more comparative archive view
- surface recent tendency and dominant outcomes without changing public contracts
- keep the archive readable as a public-facing art shell rather than a dashboard

## 2026-04-23 - Experience Rebuild Slice 4 (calibration atlas pass completed)

Completed in this iteration:

- turned the archive calibration panel into a comparative atlas rather than a plain pattern strip
- added dominant-outcome, recent-tendency, and branch-focus cues without changing public contracts
- compared the recent calibration window against the full archive inside the existing art shell
- extended frontend coverage so the archive route checks for the calibration atlas

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- deepen the artifact path beyond local SVG / TXT export
- extend calibration comparison if the current atlas proves too shallow in real use
- extend ripple and linefield continuity beyond the current replay track

## 2026-04-23 - Experience Rebuild Slice 4 (ripple continuity explorer pass started)

Planned in this iteration:

- turn Ripple from a simple replay strip into a clearer event-to-event continuity explorer
- let the ripple scene steer event focus more directly inside the shell
- keep linefield performance intact while showing a broader continuity field on the ripple surface

## 2026-04-23 - Experience Rebuild Slice 4 (ripple continuity explorer pass completed)

Completed in this iteration:

- rebuilt Ripple into an event-to-event continuity explorer instead of a simple replay strip
- made Ripple capable of steering both event focus and branch focus inside the scene
- expanded the worldline canvas on the Ripple surface so continuity spans more events than the earlier windowed view
- extended frontend coverage so the ripple explorer path is exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- deepen the artifact path beyond local SVG / TXT export
- extend calibration comparison if the current atlas proves too shallow in real use
- broaden Ripple from a single continuity chain into a stronger multi-path replay archive

## 2026-04-23 - Experience Rebuild Slice 4 (exhibit html export pass started)

Planned in this iteration:

- add a self-contained archive exhibit HTML export beyond SVG / TXT fragments
- keep the export offline and frontend-only so no secret handling changes
- package poster, wall text, decision trace, and calibration snapshot into one artifact

## 2026-04-23 - Experience Rebuild Slice 4 (exhibit html export pass completed)

Completed in this iteration:

- added a self-contained exhibit HTML export so archive artifacts can travel as one offline file
- packaged poster copy, wall text, decision trace, and calibration snapshot into the exported artifact
- kept the export fully frontend-side so no backend contract or secret handling changed
- extended frontend route coverage so the extra export action is exercised in tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- deepen the artifact path beyond the current HTML / SVG / TXT export set
- extend calibration comparison if the current atlas proves too shallow in real use
- broaden Ripple from a single continuity chain into a stronger multi-path replay archive

## 2026-04-23 - Experience Rebuild Slice 4 (multi-path ripple archive pass started)

Planned in this iteration:

- turn Ripple from one continuity chain into a clearer multi-path replay archive
- let the viewer compare active, primary, and alternate drift paths inside the ripple scene
- keep interaction lightweight by reusing existing event and branch data without changing contracts

## 2026-04-23 - Experience Rebuild Slice 4 (multi-path ripple archive pass completed)

Completed in this iteration:

- turned Ripple from one continuity chain into a side-by-side multi-path replay archive
- added active, primary, and alternate drift path lanes that can retarget the stage directly
- kept the implementation contract-safe by deriving the path archive from existing event and branch data
- extended frontend coverage so the multi-path ripple archive interaction is exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- deepen the artifact path beyond the current HTML / SVG / TXT export set
- extend calibration comparison if the current atlas proves too shallow in real use
- deepen Ripple from the current multi-path view into a richer replay-history archive

## 2026-04-23 - Experience Rebuild Slice 4 (replay-history archive pass started)

Planned in this iteration:

- deepen Ripple from a side-by-side path comparison into a more archive-like replay history surface
- make each replay snapshot readable as upstream tension, hinge branch, and downstream drift without changing contracts
- keep the interaction lightweight by deriving archive cards from the existing stage payload

## 2026-04-23 - Experience Rebuild Slice 4 (replay-history archive pass completed)

Completed in this iteration:

- deepened Ripple from a side-by-side path comparison into a more archive-like replay history surface
- added replay-history slices that read as upstream tension, hinge branch, and downstream drift for the selected path
- kept the implementation contract-safe by deriving archive entries from the existing event and branch payload
- extended frontend coverage so the replay-history archive interaction is exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- deepen the artifact path beyond the current HTML / SVG / TXT export set
- extend calibration comparison if the current atlas proves too shallow in real use
- extend the replay-history archive from derived in-stage slices into richer saved replay sets if needed

## 2026-04-23 - Experience Rebuild Slice 4 (artifact bundle and image export pass started)

Planned in this iteration:

- deepen Archive beyond fragmented SVG / TXT / HTML exports into a more bundle-like artifact output
- add a browser-side image export path so the poster can leave the UI as more than SVG alone
- keep every export frontend-only and contract-safe so no secret handling or backend flow changes

## 2026-04-23 - Experience Rebuild Slice 4 (artifact bundle and image export pass completed)

Completed in this iteration:

- extended Archive export so the poster can leave the UI as a browser-side PNG instead of SVG alone
- added a richer artifact bundle JSON that packages share state, logs, calibration, and embedded export surfaces together
- kept the implementation frontend-only and contract-safe so no backend flow or secret handling changed
- extended frontend coverage so the new export actions are exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON artifact set still feels too fragmented
- extend calibration comparison if the current atlas proves too shallow in real use
- extend the replay-history archive from derived in-stage slices into richer saved replay sets if needed

## 2026-04-23 - Experience Rebuild Slice 4 (calibration slice deck pass started)

Planned in this iteration:

- deepen calibration comparison beyond recent-vs-full into wider archive windows and branch-focused slices
- keep the archive readable as an art shell rather than falling back into a dashboard
- stay contract-safe by deriving all extra slice views from the existing calibration and decision payload

## 2026-04-23 - Experience Rebuild Slice 4 (calibration slice deck pass completed)

Completed in this iteration:

- deepened calibration comparison beyond recent-vs-full into wider archive window slices
- added branch-focused slice cards so the archive can compare dominant branch families directly
- kept the implementation contract-safe by deriving all new comparisons from the existing calibration and decision payload
- extended frontend coverage so the deeper calibration slice deck is exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON artifact set still feels too fragmented
- deepen calibration beyond the current slice deck if decision-type or longer-horizon comparison becomes necessary
- extend the replay-history archive from derived in-stage slices into richer saved replay sets if needed

## 2026-04-23 - Experience Rebuild Slice 4 (replay set library pass started)

Planned in this iteration:

- deepen Ripple from one replay-history reading into a small library of saved replay sets
- keep the replay set library contract-safe by deriving it from the existing event and branch payload
- let the viewer switch between named replay sets without leaving the Ripple surface

## 2026-04-23 - Experience Rebuild Slice 4 (replay set library pass completed)

Completed in this iteration:

- deepened Ripple from one replay-history reading into a small library of saved replay sets
- added named replay sets such as current, stabilizing, and pressure so replay history can switch without leaving Ripple
- kept the implementation contract-safe by deriving each replay set from the existing event and branch payload
- extended frontend coverage so the replay set library interaction is exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON artifact set still feels too fragmented
- deepen calibration beyond the current slice deck if decision-type or longer-horizon comparison becomes necessary
- deepen the replay set library further if persisted or more authored replay sets become necessary

## 2026-04-23 - Experience Rebuild Slice 4 (replay dossier pass started)

Planned in this iteration:

- deepen Ripple from a replay set library into a clearer replay dossier with narrative anchors
- surface entry anchor, hinge pressure, and terminal exposure so each replay set reads more like an authored line
- keep the implementation contract-safe by deriving dossier cues from the existing event and branch payload

## 2026-04-23 - Experience Rebuild Slice 4 (replay dossier pass completed)

Completed in this iteration:

- deepened Ripple from a replay set library into a clearer replay dossier with narrative anchors
- surfaced entry anchor, hinge pressure, and terminal exposure so each replay set reads more like an authored line
- kept the implementation contract-safe by deriving dossier cues from the existing event and branch payload
- extended frontend coverage so the replay dossier interaction is exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON artifact set still feels too fragmented
- deepen calibration beyond the current slice deck if decision-type or longer-horizon comparison becomes necessary
- deepen the replay dossier further if persisted replay sets or more authored writing becomes necessary

## 2026-04-23 - Experience Rebuild Slice 4 (replay export pass started)

Planned in this iteration:

- turn the selected replay dossier into a portable local artifact instead of leaving it only inside the Ripple surface
- keep the implementation frontend-only and contract-safe by deriving the replay packet from the existing event and branch payload
- clean up the dossier narration so it stays locale-safe instead of mixing hard-coded connector text into every language

## 2026-04-23 - Experience Rebuild Slice 4 (replay export pass completed)

Completed in this iteration:

- turned the selected replay dossier into a portable local artifact layer inside Ripple
- added local replay dossier markdown export plus replay packet json export without changing backend contracts
- added a copyable replay excerpt so the currently selected replay set can leave the surface as authored text
- cleaned up dossier narration so the visible summary no longer depends on hard-coded connector text leaking across locales
- extended frontend coverage so the replay export tools and locale-safe excerpt are exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON artifact set still feels too fragmented
- deepen calibration beyond the current slice deck if decision-type or longer-horizon comparison becomes necessary
- deepen the replay dossier further if persisted replay sets or more authored writing becomes necessary

## 2026-04-23 - Experience Rebuild Slice 4 (replay shelf pass started)

Planned in this iteration:

- turn the current replay packet into a small persisted local replay shelf instead of leaving it as a one-off export path
- keep the implementation frontend-only and contract-safe by saving replay packets in browser storage rather than changing the backend
- let saved replay packets be restored and re-exported so authored replay states can accumulate across a session

## 2026-04-23 - Experience Rebuild Slice 4 (replay shelf pass completed)

Completed in this iteration:

- turned the current replay packet into a small persisted local replay shelf inside Ripple
- added save, restore, remove, and re-export actions so authored replay states can accumulate locally per project
- kept the implementation frontend-only and contract-safe by using browser storage instead of changing backend contracts
- extended frontend coverage so the replay shelf save/restore/export/remove flow is exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON artifact set still feels too fragmented
- deepen calibration beyond the current slice deck if decision-type or longer-horizon comparison becomes necessary
- deepen the replay dossier further if persisted replay sets or more authored writing becomes necessary

## 2026-04-23 - Experience Rebuild Slice 4 (calibration longitudinal pass started)

Planned in this iteration:

- deepen calibration beyond branch and window slices into decision-type and longer-horizon longitudinal readings
- keep the implementation contract-safe by deriving the extra views from existing calibration records plus the decision log
- preserve the archive as a readable art shell instead of turning it into an analytics dashboard

## 2026-04-23 - Experience Rebuild Slice 4 (calibration longitudinal pass completed)

Completed in this iteration:

- deepened calibration beyond branch and window slices into decision-type and longer-horizon longitudinal readings
- added derived decision-type cards so the archive can compare how different intervention modes age against later outcomes
- added chronological longitudinal windows so the archive can compare earlier, middle, and latest calibration phases
- kept the implementation contract-safe by deriving every extra view from the existing calibration records plus decision log
- extended frontend coverage so the decision-type and longitudinal calibration views are exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON artifact set still feels too fragmented
- deepen calibration beyond the current slice deck if decision-type or longer-horizon comparison still proves too shallow later
- deepen the replay dossier further if persisted replay sets or more authored writing becomes necessary

## 2026-04-23 - Experience Rebuild Slice 4 (media packet pass started)

Planned in this iteration:

- bundle the current archive exports into a denser media packet instead of leaving them as separate files
- keep the implementation frontend-only and secret-safe so the packet is assembled entirely from existing local export surfaces
- preserve the archive as an exhibition exit rather than turning export into a purely technical utility list

## 2026-04-23 - Experience Rebuild Slice 4 (media packet pass completed)

Completed in this iteration:

- bundled the current Archive exports into a denser local media packet zip instead of leaving them as separate files
- packed poster svg, poster png, share text, exhibit html, artifact bundle json, and a manifest into one frontend-only export flow
- kept the implementation secret-safe by assembling the packet entirely from the existing local export surfaces
- extended frontend coverage so the media packet export is exercised alongside the earlier archive export actions

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON / ZIP artifact set still feels too fragmented
- deepen calibration beyond the current slice deck if decision-type or longer-horizon comparison still proves too shallow later
- deepen the replay dossier further if persisted replay sets or more authored writing becomes necessary

## 2026-04-23 - Experience Rebuild Slice 4 (replay authorship pass started)

Planned in this iteration:

- deepen the current replay dossier into a more authored replay artifact instead of leaving it mostly as a technical packet
- add a portable replay exhibit export so the selected replay can travel as a more exhibition-ready object
- keep the implementation frontend-only and contract-safe by deriving the authored replay artifact from the existing event and branch payload

## 2026-04-23 - Experience Rebuild Slice 4 (replay authorship pass completed)

Completed in this iteration:

- deepened the current replay dossier into a more authored replay artifact instead of leaving it as a technical packet only
- added a portable replay exhibit html export for the selected replay and for replay shelf items restored later
- kept the implementation frontend-only and contract-safe by deriving the authored artifact entirely from the existing event and branch payload
- extended frontend coverage so the authored replay artifact, copy action, and replay exhibit export path are exercised in route tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON / ZIP artifact set still feels too fragmented
- deepen calibration beyond the current slice deck if decision-type or longer-horizon comparison still proves too shallow later
- deepen Ripple further if persisted replay sets or more durable authored narration becomes necessary

## 2026-04-23 - Experience Rebuild Slice 4 (replay atlas pass started)

Planned in this iteration:

- turn the local replay shelf into a more legible replay atlas instead of leaving saved replay sets as a plain restore list
- add a bundled replay atlas export so saved replay sets can leave Ripple as one exhibition-ready object
- keep the implementation frontend-only and contract-safe by deriving the atlas from the existing saved replay shelf state

## 2026-04-23 - Experience Rebuild Slice 4 (replay atlas pass completed)

Completed in this iteration:

- turned the local replay shelf into a more legible replay atlas instead of leaving saved replay sets as a plain restore list
- added atlas cards that can quickly restore saved replay sets while surfacing their pressure and confidence at a glance
- added a bundled replay atlas html export so saved replay sets can leave Ripple together as one exhibition-ready object
- kept the implementation frontend-only and contract-safe by deriving the atlas from the existing saved replay shelf state
- extended frontend coverage so the replay atlas view and export path are exercised alongside the existing replay shelf flow

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON / ZIP artifact set still feels too fragmented
- deepen calibration beyond the current slice deck if decision-type or longer-horizon comparison still proves too shallow later
- deepen Ripple further if persisted replay sets or more durable authored narration becomes necessary

## 2026-04-23 - Experience Rebuild Slice 4 (persisted replay set pass started)

Planned in this iteration:

- move saved replay sets out of browser-local state and into project-level persistence
- keep the replay atlas and replay exhibit flow working after the persistence shift
- keep the implementation contract-safe by adding the smallest backend and stage extensions needed for persisted replay sets

## 2026-04-23 - Experience Rebuild Slice 4 (persisted replay set pass completed)

Completed in this iteration:

- moved saved replay sets out of browser-local state and into project-level snapshots
- added backend replay-set save and delete routes plus stage payload support for persisted replay sets
- rewired Ripple shelf and atlas interactions so save / remove actions now round-trip through the API while replay dossier, packet, exhibit, and atlas exports keep working
- updated API and frontend tests to cover persisted replay-set behavior
- removed the deprecated `jsonschema.RefResolver` path from API contract validation

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed
- `git diff --check` passed
- secret pattern scan returned no matches for the MiniMax secret prefix or provided key fragment
- `git ls-files .ui-ref ui-ref` returned no tracked reference files
- secret pattern scan returned no matches for the provided MiniMax key fragment

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON / ZIP artifact set still feels too fragmented
- deepen Ripple beyond the current persisted replay shelf into richer authored replay sets if later we need stronger curation
- continue polishing Observatory density and wording if the public shell needs tighter reading cues

## 2026-04-23 - Experience Rebuild Slice 4 (authored replay set pass started)

Planned in this iteration:

- add clearer curatorial control so a replay set can be authored before save and export
- keep the persisted replay shelf and replay atlas flow working while the authored layer becomes editable
- preserve the art-first, author-first reading of Ripple rather than turning the surface into a utility form

## 2026-04-23 - Experience Rebuild Slice 4 (authored replay set pass completed)

Completed in this iteration:

- added a replay author deck so the current replay can be given a custom title and curatorial note before save or export
- wired authored replay edits through dossier, artifact, packet, exhibit, and persisted shelf flows instead of leaving them as temporary UI-only text
- adjusted replay-set persistence so different authored titles for the same replay focus can coexist as separate saved variants
- extended API and frontend tests so authored replay variants and restore behavior are exercised

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed
- `git diff --check` passed
- secret pattern scan returned no matches for the provided MiniMax key fragment

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON / ZIP artifact set still feels too fragmented
- deepen Ripple beyond title-and-note authorship into richer authored replay collections or stronger long-form narration if needed
- continue polishing Observatory density and wording if the public shell needs tighter reading cues

## 2026-04-23 - Experience Rebuild Slice 4 (replay curation field pass started)

Planned in this iteration:

- widen the replay author deck beyond title and note so richer curatorial fields can shape the replay artifact before save and export
- keep persisted replay restoration faithful to the authored replay version instead of falling back to derived text only
- preserve the existing replay shelf, atlas, dossier, and exhibit flows while making the author deck denser

## 2026-04-23 - Experience Rebuild Slice 4 (replay curation field pass completed)

Completed in this iteration:

- widened the replay author deck beyond title and note by adding editable deck-line and closing-note fields
- wired the wider curatorial fields through replay artifact preview, replay packet export, exhibit export, and persisted replay restoration
- kept the persisted replay shelf and replay atlas flow stable while making the authored replay layer denser
- extended frontend route coverage so the richer curatorial fields and restore path are exercised in tests

Verification:

- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed
- `git diff --check` passed
- secret pattern scan returned no matches for the provided MiniMax key fragment

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON / ZIP artifact set still feels too fragmented
- deepen Ripple beyond the current curatorial field set into saved authored collections or stronger long-form narration if needed
- continue polishing Observatory density and wording if the public shell needs tighter reading cues

## 2026-04-24 - Experience Rebuild Slice 5 (worldline theatre pass started)

Planned in this iteration:

- replace the report-like stage with a worldline theatre that can unfold through a Next button
- protect the local `.ui-ref` reference package from GitHub upload before using it as visual direction
- remove old public-opinion / platform-era wording from the visible UI, prompt defaults, and curated fixture metadata
- reduce canvas density and black-hole scale so the page feels lighter and the worldline remains primary

## 2026-04-24 - Experience Rebuild Slice 5 (worldline theatre pass completed)

Completed in this iteration:

- added `.ui-ref/` and `ui-ref/` to `.gitignore` and verified the reference package is not tracked
- rebuilt `/world/:projectId` as a worldline theatre with progressive reveal, a central linefield, left lens rail, right observation rail, active drawer, and bottom Next control
- added frontend-local reveal state so a viewer can press Next through all key events and arrive at Archive without writing an intervention
- kept branch selection, intervention, replay, share, and calibration entry points available as secondary surfaces
- updated the canvas renderer with lower line density, smaller singularity, adaptive drawing, pointer throttling, and reduced-motion behavior
- cleaned seed compiler, replay/share text, entry copy, fixture metadata, and rendered stage text away from old public-opinion framing toward actants, rules, environments, materials, natural objects, institutions, and constraints
- renamed the campus fixture to `campus-field-threshold` and renamed the policy fixture to `civic-rule-trust-fracture`
- replaced frontend and e2e tests with the new theatre acceptance path, including a no-input Next-only smoke flow

Verification:

- `npm --workspace apps/web run test` passed
- `npm --workspace apps/web run build` passed
- `npm run test:api` passed
- `npm run test:web` passed
- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed
- `git diff --check` passed

Still open after slice 5:

- visual review against `.ui-ref` can further tune spacing, scale, and atmosphere
- Archive and Ripple advanced export tools should be re-integrated into the theatre language without returning to report density
- reveal progress is currently frontend-local and may later need backend project persistence
- canvas performance has targeted optimizations but still needs a repeatable benchmark before exhibition deployment

## 2026-04-24 - Experience Rebuild Slice 6 (process trace and intervention windows started)

Planned in this iteration:

- expose backend process-trace outputs while the worldline unfolds so the viewer is not simply waiting between nodes
- generate safe runtime process data files under ignored `data/runtime/process/...`
- show FACT / INFERENCE / VALUE / ACTION layer outputs for the currently revealed event inside the theatre shell
- add intervention-window affordances that open the Intervention drawer with a recommended input type at meaningful nodes
- keep ordinary Next navigation local and fast, without requiring live LLM calls for display updates

## 2026-04-24 - Experience Rebuild Slice 6 (process trace and intervention windows completed)

Completed in this iteration:

- added a backend `ProcessTraceBuilder` that derives per-event FACT / INFERENCE / VALUE / ACTION layer results from the current world state
- wrote process trace artifacts as safe local JSON files under ignored `data/runtime/process/...`
- extended the stage response contract and frontend types with a deterministic `process_trace`
- added a central theatre process panel that shows artifact path, layer outputs, and backend calculation cues while the worldline advances
- added intervention-window affordances that open the Intervention drawer with the recommended input type and target branch
- extended API, frontend, and smoke coverage for process trace visibility and intervention-window entry

Verification:

- `npm --workspace apps/web run test` passed
- `npm run test:api` passed
- `npm run build` passed
- `npm run test` passed
- `npm run smoke` initially hit an old reused local server, then passed after `stop-miroworld.ps1` cleared stale 8000 / 4173 processes
- `git diff --check` passed
- secret scan returned no matches for the provided MiniMax key fragment
- `git ls-files .ui-ref ui-ref` returned no tracked reference files

## 2026-04-24 - Experience Rebuild Slice 7 (computation theatre and performance benchmark started)

Planned in this iteration:

- make the process trace panel feel like a computation theatre instrument instead of a debug card
- keep runtime process file paths and preview metrics visible so the stage still shows real backend artifact results
- add expanded selected-layer inputs / outputs / confidence notes to make FACT / INFERENCE / VALUE / ACTION more readable
- add a repeatable browser benchmark for canvas frame cadence and Next-step latency
- prevent Playwright smoke from silently reusing stale local servers from older runs

## 2026-04-24 - Experience Rebuild Slice 7 (computation theatre and performance benchmark completed)

Completed in this iteration:

- reshaped the process trace panel into a computation-theatre instrument with orbit progress, scanline treatment, artifact strip, and preview metrics
- added an expanded selected-layer inspector so FACT / INFERENCE / VALUE / ACTION expose inputs, outputs, and confidence notes
- kept runtime process artifact paths visible so the theatrical layer still points back to real local data files
- added `npm run test:perf` / `npm --workspace apps/web run test:perf` for a browser benchmark covering canvas frame cadence and Next-step latency
- updated Playwright config so smoke and perf tests start fresh API / web servers instead of silently reusing stale local processes

Verification:

- `npm --workspace apps/web run test` passed
- `npm --workspace apps/web run build` passed
- `npm run test:perf` passed
- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed with smoke and performance E2E specs
- `git diff --check` passed
- secret scan returned no matches for the provided MiniMax key fragment
- `git ls-files .ui-ref ui-ref` returned no tracked reference files

## 2026-04-24 - Experience Rebuild Slice 8 (persistent theatre reading started)

Planned in this iteration:

- move theatre reveal progress from frontend-local memory into project snapshots
- add a progress save endpoint and typed frontend API call
- restore revealed event count, selected event, selected branch, and active surface from `stage.surface_defaults`
- show lightweight save state in the theatre without blocking navigation
- cover refresh/resume behavior in API, frontend, and E2E tests

## 2026-04-24 - Experience Rebuild Slice 8 (persistent theatre reading completed)

Completed in this iteration:

- added `TheatreProgress` to the project model and world-state contract so reveal progress is stored with project snapshots
- added `POST /api/projects/{projectId}/progress` with event/branch sanitization and saved timestamp updates
- extended `stage.surface_defaults` so revealed count, selected event, selected branch, active surface, and save timestamp restore after refresh
- wired the theatre UI to save progress after Next, event selection, branch selection, surface changes, process intervention jumps, replay input, share, and calibration paths
- added a lightweight save-state marker in the progress panel without blocking navigation
- extended API, frontend, and Playwright coverage for progress persistence across reload

Verification:

- `npm run test:api` passed
- `npm --workspace apps/web run test` passed
- `npm --workspace apps/web run build` passed
- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed with smoke and performance E2E specs
- `npm run test:perf` passed
- final diff, secret, and reference-folder checks passed before commit and push

Still open after slice 8:

- run a visual review against `.ui-ref` to tune stage rhythm, drawer density, and black-hole scale
- re-integrate advanced Archive and Ripple authored-export surfaces into the theatre language
- tighten the performance benchmark thresholds for exhibition-grade deployment

## 2026-04-24 - Experience Rebuild Slice 9 (impeccable theatre polish started)

Planned in this iteration:

- use the `teach-impeccable` / `frontend-design` workflow to establish durable UI design context before polishing
- add a local `.impeccable.md` design context so future agents do not drift back toward report/dashboard language
- tune the current theatre shell against the local `.ui-ref` orbital observatory direction without copying the reference package
- add lightweight readout/orbit affordances tied to real reveal state
- keep the polish inside existing performance and contract boundaries

## 2026-04-24 - Experience Rebuild Slice 9 (impeccable theatre polish completed)

Completed in this iteration:

- added `.impeccable.md` with audience, tone, aesthetic direction, and design principles for MiroWorld UI work
- added a topbar orbit readout and central event orbit map to the stage route
- bound the orbit map to actual event reveal and active-selection state rather than decorative fake data
- retuned theatre shell colors, panel borders, center-field atmosphere, drawer treatment, and bottom bar toward a thinner orbital instrument language
- extended frontend route and smoke coverage for the new readout/orbit UI

Verification:

- `npm --workspace apps/web run test` passed
- `npm --workspace apps/web run build` passed
- `npm run build` passed
- `npm run test` passed
- `npm run smoke` passed with smoke and performance E2E specs
- `npm run test:perf` passed
- final diff, secret, and reference-folder checks passed before commit and push

Still open after slice 9:

- re-integrate advanced Archive and Ripple authored-export surfaces into the same theatre language
- review mobile and low-height exhibition layouts after the orbital polish pass
- tighten the performance benchmark thresholds for exhibition-grade deployment

## 2026-04-24 - Experience Rebuild Slice 10 (archive/ripple theatre instruments started)

Planned in this iteration:

- turn Ripple's saved replay / continuity export affordances into a theatre-native console rather than a utility drawer
- add a local ripple trace packet export tied to the currently revealed worldline, latest bend, alternate pressure, and saved replay count
- turn Archive's share / calibration / decision state into an afterimage capsule with visible metrics and local artifact actions
- keep all new actions frontend-local and secret-safe, with no live LLM dependency for ordinary navigation or export
- update route and smoke coverage, then run the full build/test/smoke/perf/secret/reference gate before push

## 2026-04-24 - Experience Rebuild Slice 10 (archive/ripple theatre instruments completed)

Completed in this iteration:

- rebuilt the Ripple drawer into a theatre-native replay console with revealed-node, alternate-pressure, saved-replay, average-confidence, latest-bend, and ripple-card readings
- added a frontend-only Ripple trace JSON export assembled from the current stage state
- rebuilt the Archive drawer's first surface into an afterimage capsule with share, reveal, decision, calibration, and ripple-card metrics
- added Archive capsule copy/export actions that use existing stage state only and do not require live LLM calls
- added instrument-specific styling so Ripple and Archive read as orbital theatre tools instead of utility/report cards
- extended frontend route tests and Playwright smoke coverage for the new console/capsule affordances

Verification:

- `npm --workspace apps/web run test` passed
- `npm --workspace apps/web run build` passed
- `npm run test` passed
- `npm run build` passed
- `npm run smoke` passed with smoke and performance E2E specs
- `npm run test:perf` passed

Still open after slice 10:

- tighten performance thresholds toward exhibition deployment
- continue mobile and low-height visual review
- improve the authored prose quality of exported Archive/Ripple artifacts now that the instrument shells are in place

## 2026-04-24 - Experience Rebuild Slice 11 (exhibition performance budget started)

Planned in this iteration:

- replace the loose MVP performance assertion with named exhibition budgets for desktop canvas frame cadence and Next-step latency
- target at least 45 FPS in the default desktop fixture path and under 150 ms for ordinary Next reveal interactions
- add benchmark evidence output so slowdowns are easier to diagnose
- cover low-height and mobile viewport reachability so the theatre, process panel, and bottom action do not collapse out of use
- keep changes frontend-local and contract-safe, then run the full verification and secret/reference gate before push

## 2026-04-24 - Experience Rebuild Slice 11 (exhibition performance budget completed)

Completed in this iteration:

- replaced the loose MVP performance assertions with named exhibition budgets: 45 FPS desktop frame cadence and 150 ms Next-step latency
- added Playwright benchmark evidence attachment for frame cadence and Next reveal latency
- changed `WorldlineCanvas` from continuous redraw to dirty-frame redraw on mount, resize, pointer movement, prop changes, and visibility changes
- removed theatre-route constant backdrop blur and the infinite process-scan animation that were depressing frame cadence in headless Chromium
- added mobile and low-height viewport checks for theatre visibility, process panel reachability, Next control reachability, and horizontal overflow
- hardened theatre CSS for mobile and low-height display reachability without backend or contract changes

Verification:

- `npm run test:perf` initially failed at about 28-30 FPS, then passed after render/compositor hardening
- `npm --workspace apps/web run test` passed
- `npm --workspace apps/web run build` passed
- `npm run test` passed
- `npm run build` passed
- `npm run smoke` passed with the standard smoke path plus the stricter performance and viewport checks

Still open after slice 11:

- deepen Archive/Ripple artifact prose now that their theatre-native shells are stable
- keep real-device / real-display visual review on mobile and low-height exhibition hardware
- make Archive calibration more theatrical and less utility-like

## 2026-04-24 - Experience Rebuild Slice 12 (prompt worldline driver fix completed)

Root cause:

- prompt project creation was calling the live MiniMax adapter synchronously whenever local `LLM_API_KEY` was present
- after that call, the generated title/summary could change, but the actual key events still came from a generic worldline template
- the result could feel stuck or non-driveable: slow entry plus a generated project that did not really unfold from the submitted seed

Completed in this iteration:

- replaced the default prompt path with a deterministic prompt compiler that immediately derives actants, events, branches, costs, knowledge layers, and process traces from the submitted seed
- made live seed enrichment explicitly opt-in through `LLM_SEED_COMPILER_ENABLED=false` by default, so local credentials no longer make ordinary prompt starts block on a network call
- kept MiniMax server-side and secret-safe while preserving the public contracts
- added API coverage proving prompt projects are seed-specific and do not call the live LLM by default
- added a Playwright smoke path for prompt entry, theatre load, process trace visibility, and Next-step advancement
- adjusted Playwright server reuse so local smoke can reuse a current dev server outside CI while CI still starts clean servers

Verification:

- `python -m pytest apps/api/tests/test_api.py -q` passed
- `npm --workspace apps/web run test -- --run` passed
- `npm --workspace apps/web run build` passed
- `npm run smoke` passed with the new prompt-generation path

Still open after slice 12:

- design a proper async MiniMax enrichment lane so model computation can appear as visible backstage progress without blocking project creation
- continue improving the authored quality of generated worldline language
- keep tightening real-device visual and performance review

## 2026-04-24 - Experience Rebuild Slice 13 (MiniMax reasoning packet fix completed)

Root cause:

- the live MiniMax endpoint was reachable, but `MiniMax-M2.7-highspeed` can prepend a `<think>...</think>` block before the final JSON object
- the OpenAI-compatible adapter previously attempted `json.loads(content)` on the full response, swallowed the parse failure, and returned `None`
- the seed compiler then silently fell back to deterministic prompt compilation, so the UI looked like it had run but no model reasoning packet entered the world state
- the local 60-second timeout was also too short for the current seed-compiler packet; a real prompt run completed only after a longer timeout

Completed in this iteration:

- updated the MiniMax adapter to strip reasoning prefaces and recover the final JSON object with `JSONDecoder.raw_decode`
- changed the recommended and local ignored timeout to `LLM_REQUEST_TIMEOUT=180`
- re-enabled local MiniMax seed compilation when credentials are configured while keeping no-key fallback deterministic and safe
- added `ReasoningRunRecord` to world state and exposed the latest reasoning/fallback run through `stage.process_trace.reasoning_run`
- wrote successful MiniMax packets to ignored `data/runtime/process/.../00-minimax-seed-reasoning.json`
- wrote failed MiniMax attempts to ignored `00-minimax-seed-fallback.json` artifacts so future failures are visible instead of silent
- added a frontend process strip for model reasoning / fallback artifacts
- added API tests for `<think>` parsing, structured MiniMax packets, and fallback artifact redaction

Verification:

- real local MiniMax prompt creation returned `source_label=seed_prompt+MiniMax`
- real local MiniMax prompt creation produced `minimax_reasoning` knowledge and a completed `00-minimax-seed-reasoning.json` process artifact
- `python -m pytest apps/api/tests/test_api.py -q` passed
- `npm --workspace apps/web run test` passed
- `npm --workspace apps/web run build` passed
- `npm run smoke` passed

Still open after slice 13:

- MiniMax prompt creation is now real, but still synchronous and can take around two minutes on a fresh run
- the next architecture step should move model reasoning into an async visible backstage lane with progress polling or streaming artifacts
- generated worldline language still needs more authorial editing and less generic model phrasing

## 2026-04-24 - Experience Rebuild Slice 14 (async MiniMax backstage reasoning started)

Planned in this iteration:

- make prompt project creation immediately return a deterministic, driveable worldline even when MiniMax credentials are configured
- enqueue local MiniMax seed reasoning as a background backstage task instead of blocking the entry action
- expose a safe reasoning-status endpoint with status, progress step, summary, and runtime artifact path
- merge completed MiniMax reasoning packets back into the project snapshot so the stage can refresh from deterministic seed to model-enriched worldline
- surface backstage progress in the theatre UI while preserving Next-driven worldline unfolding
- keep all provider keys and raw hidden reasoning out of tracked files, logs, screenshots, and frontend code
- update tests, docs, smoke, secret checks, and push only after the full verification loop passes

## 2026-04-24 - Experience Rebuild Slice 14 (async MiniMax backstage reasoning completed)

Completed in this iteration:

- changed prompt project creation so it always returns the deterministic, driveable worldline first
- added an in-process MiniMax backstage job manager with queued, running, completed, fallback, failed, disabled, and idle statuses
- added `GET /api/projects/{projectId}/reasoning` so the frontend can poll safe backstage computation status
- merged completed MiniMax reasoning packets back into the project snapshot when the viewer has not authored inputs yet
- preserved viewer-authored state by archiving completed reasoning runs instead of overwriting a worldline that already has interventions, decisions, calibration, or saved replay sets
- added a stage-side backstage reasoning strip so viewers can continue unfolding the line while the model works
- added a `reasoning-status` contract plus API and frontend tests for queueing, completion merge, fallback artifact redaction, and UI status display

Verification:

- real local prompt creation with MiniMax credentials returned in about `0.02s` with `stage_source=seed_prompt` and `reasoning_status=running`
- `python -m pytest apps/api/tests/test_api.py -q` passed
- `npm run test` passed
- `npm run build` passed
- `npm run smoke` passed
- `git diff --check` passed

Still open after slice 14:

- the current worker is intentionally lightweight and in-process; exhibition deployment may need a durable persisted queue or streaming protocol
- background progress is visible at a coarse step level, but not yet a fine-grained file-by-file computation theatre
- Archive/Ripple artifact writing and calibration dramaturgy remain good next product slices
