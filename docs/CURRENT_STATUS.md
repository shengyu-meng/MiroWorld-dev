# Current Status

Updated: 2026-04-24
Status: Active
Phase: `experience-first rebuild / slice 5 worldline theatre completed`

## One-line Summary

`MiroWorld-dev` now has a working standalone monorepo, public contracts, fixture-backed API, replay/share/calibration flow, tests, CI, one-click local startup, and a worldline theatre shell where `/world/:projectId` progressively reveals events through a Next-driven stage instead of reading as a report stack. The canvas has been lightened with a smaller black-hole anchor, `.ui-ref/` is protected from upload, and core UI / prompt / fixture wording has moved away from old public-opinion simulation language toward broader world simulation with actants, rules, environments, materials, natural objects, institutions, and constraints.

The main product risk is no longer "can it run." It is "how far the public experience has been pushed":

- the shell now reads as a progressive worldline theatre instead of a long panel stack or report page
- a viewer can press Next without writing an intervention and still reach a complete Archive afterimage
- core display text now rewrites old public-opinion terms such as initiator, public climate, platform, and public view into trigger source, field conditions, rule layer, and observable layer
- the canvas now uses lower line density, pointer throttling, reduced-motion fallback, and a smaller singularity so the worldline remains primary
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

### Verification baseline

- `npm run build` passes
- `npm run test` passes
- `npm run smoke` passes
- `git diff --check` passes
- secret pattern scan returns no matches for the MiniMax key fragment
- `git ls-files .ui-ref ui-ref` returns no tracked reference files

## Still Missing

### Product / experience gaps

- the new theatre shell restores progressive unfolding, but the Archive/Ripple advanced authored-export surfaces are now visually secondary and may need re-integration into the theatre language
- the current reveal state is frontend-local; if reload persistence becomes important, progression should move into project snapshot state
- the canvas is lighter, but a dedicated FPS benchmark or in-browser performance budget is still needed before exhibition deployment
- calibration history is still available but can become more theatrical inside the Archive drawer instead of remaining mostly utility-like

### Content expression gaps

- the UI display layer cleans old public-opinion terms, but more fixture narratives can still be rewritten around non-human actants and natural/material constraints
- the layer lens is now visible, but its depth is still mostly presentation-layer driven rather than fully model-driven
- cost narration can become more comparative across branches, not just branch-local
- archive artifacts can become more authored and less template-like as share formats mature

### Documentation gaps

- canonical docs now exist in-repo
- the next improvement is to keep them moving slice by slice without falling back to chat-only history

## Current Focus

The next active slice should continue after `Experience Rebuild Slice 5`:

- run a visual/browser review of the new theatre shell against `.ui-ref` and tune spacing, scale, and black-hole size
- re-integrate the deeper Ripple/Archive authored export tools into the theatre drawer language without returning to report density
- decide whether reveal progress should persist in the project snapshot or remain a local exhibition reading
- add a repeatable canvas performance benchmark before pushing the visual system further
