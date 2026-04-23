# Current Status

Updated: 2026-04-23
Status: Active
Phase: `experience-first rebuild / scene-shell slice 4 calibration longitudinal pass complete`

## One-line Summary

`MiroWorld-dev` now has a working standalone monorepo, public contracts, fixture-backed API, replay/share/calibration flow, tests, CI, one-click local startup, and a scene-based public shell whose archive now exports poster, png, bundle, and exhibit artifacts while calibration reads through wider window, branch, decision-type, and longitudinal slices and Ripple now supports a replay-set library, replay dossier, local replay packet export, and a persisted replay shelf.

The main product risk is no longer "can it run." It is "how far the public experience has been pushed":

- the shell now reads as a scene-based worldline interface instead of a long panel stack
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
- and Ripple can now keep authored replay packets on a small persisted local shelf so replay states can be revisited instead of only exported once
- and calibration can now be read not only by branch and window, but also by decision type and longer-horizon archive slices
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

### Frontend experience rebuild slice 4 (replay set library pass)

- Ripple now exposes a small replay set library instead of only one replay-history reading
- named replay sets such as current, stabilizing, and pressure can switch the saved replay view without leaving Ripple
- frontend route tests now cover the replay set library interaction layer

### Frontend experience rebuild slice 4 (replay dossier pass)

- Ripple now gives each replay set a dossier layer instead of only a selectable set card and history list
- the dossier now surfaces entry anchor, hinge pressure, and terminal exposure so the line reads more like an authored replay
- frontend route tests now cover the replay dossier interaction layer

### Verification baseline

- `npm run build` passes
- `npm run test` passes
- `npm run smoke` passes

## Still Missing

### Product / experience gaps

- the linefield and Ripple now act more like a multi-path replay surface with named replay sets, but they are not yet a fuller replay archive across multiple synthesized histories or backend-saved replay sets
- Ripple now exposes replay sets, dossier anchors, local replay packet export, and a persisted local shelf, but it still does not yet support backend-saved replay sets or deeper authored replay writing
- the archive now exports local svg, png, text, exhibit html, and artifact bundle outputs, but it still does not yet generate richer image pipelines or packaged media sets beyond those first formats
- calibration history is now comparative across windows, branches, decision types, and longer-horizon slices, but it can still become denser if later we need deeper longitudinal narration
- ripple continuity now includes a replay set library and dossier layer, but it still may need persisted replay sets or deeper authored narration later

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
- keep evolving the archive export path beyond the current SVG / PNG / TXT / HTML / JSON set if richer packaged media becomes necessary
- deepen calibration comparison beyond the current slice deck into richer decision-type or longer-horizon archive perspectives if needed
- deepen Ripple beyond the current local replay packet into richer saved replay sets or more authored replay narration if needed
- keep extending the linefield / ripple system toward richer authored or persisted replay sets without regressing shell speed
