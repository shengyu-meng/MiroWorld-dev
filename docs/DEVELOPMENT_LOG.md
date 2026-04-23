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
