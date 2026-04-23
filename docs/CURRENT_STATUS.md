# Current Status

Updated: 2026-04-23
Status: Active
Phase: `experience-first rebuild / scene-shell slice 4 multi-path ripple archive pass complete`

## One-line Summary

`MiroWorld-dev` now has a working standalone monorepo, public contracts, fixture-backed API, replay/share/calibration flow, tests, CI, one-click local startup, and a scene-based public shell whose archive exports poster/bundle/exhibit artifacts while Ripple now supports a clearer multi-path replay archive.

The main product risk is no longer "can it run." It is "how far the public experience has been pushed":

- the shell now reads as a scene-based worldline interface instead of a long panel stack
- the archive/share space now reads more like a curator-facing artifact chamber instead of a utility output list
- and its core artifact can now leave the UI as a local poster SVG or share bundle
- and the archive can now leave the UI as a self-contained exhibit HTML artifact instead of only fragmented exports
- calibration no longer reads as a plain log; it now exposes dominant outcomes, recent tendency, and branch focus
- Ripple now lets the viewer steer event focus and branch focus from inside the continuity surface itself
- and the linefield opens wider on the Ripple surface so continuity reads across more events than before
- Ripple now also lets the viewer compare active, primary, and alternate drift paths side by side
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

### Verification baseline

- `npm run build` passes
- `npm run test` passes
- `npm run smoke` passes

## Still Missing

### Product / experience gaps

- the linefield and Ripple now act more like a multi-path continuity surface, but they are not yet a fuller replay archive across multiple synthesized histories
- the archive now exports local poster, text, and exhibit html artifacts, but it does not yet generate richer saved multi-format bundles or image pipelines beyond SVG
- calibration history is now comparative at a first pass, but it is not yet deeper across branch families, broader time windows, or decision types
- ripple continuity is now multi-path at a first pass, but it still needs a deeper archive of replay histories and richer path narration

### Content expression gaps

- the layer lens is now visible, but its depth is still mostly presentation-layer driven rather than fully model-driven
- cost narration can become more comparative across branches, not just branch-local
- archive artifacts can become more authored and less template-like as share formats mature

### Documentation gaps

- canonical docs now exist in-repo
- the next improvement is to keep them moving slice by slice without falling back to chat-only history

## Current Focus

The next active slice is still `Experience Rebuild Slice 4`:

- deepen the export path beyond local SVG / TXT into stronger artifact options
- keep evolving the archive export path beyond the current HTML artifact if a richer bundle format becomes necessary
- deepen calibration comparison beyond the current atlas into richer archive perspectives if needed
- keep extending the linefield / ripple system toward a deeper replay archive without regressing shell speed
