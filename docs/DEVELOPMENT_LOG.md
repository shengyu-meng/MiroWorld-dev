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
- secret pattern scan returned no matches for the provided MiniMax key fragment

Still open inside slice 4:

- keep extending the export path if the current SVG / PNG / TXT / HTML / JSON / ZIP artifact set still feels too fragmented
- deepen Ripple beyond the current persisted replay shelf into richer authored replay sets if later we need stronger curation
- continue polishing Observatory density and wording if the public shell needs tighter reading cues
