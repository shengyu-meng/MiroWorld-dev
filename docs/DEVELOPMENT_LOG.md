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
