# Tasks — Polish, Measurement, and Regression

> Milestone M9. Requirements: NFR-005, NFR-006, NFR-007 from
> `specs/product.md` §5; acceptance criteria AC-186…AC-189 from
> `specs/features/audio-assets/spec.md`. No new requirements are introduced
> here: every task below measures or verifies behaviour specified elsewhere.

## TASK-POL-01 — 60 FPS measurement note (NFR-005)
- **Objective:** record measured frame timing on the reference machine at
  30/60/144 Hz and publish the numbers as evidence, not as a claim.
- **Requirement IDs:** NFR-005, NFR-002 (restated), AC-133
- **Dependencies:** TASK-WAV-05, TASK-SCR-05
- **Files in scope:** `docs/audits/v0.2-baseline.md` (new section or a sibling
  audit file), `specs/traceability.md` (status cell only)
- **Constraints:** measure the shipped `main.wasm`; no synthetic benchmark that
  bypasses the render loop; state the machine and browser version.
- **Expected tests:** none automated — this is documented measurement.
- **Verification evidence:** a table of frame times plus the exact commands
  used, and the traceability row moved from `TODO` to `✔ verified` only if the
  numbers support it.
- **Out of scope:** optimising the renderer.

## TASK-POL-02 — Accessibility pass: contrast, keyboard reachability, pause (NFR-007)
- **Objective:** every canvas screen is operable with the keyboard alone, every
  text element meets the contrast floor, and pause is reachable from every
  gameplay state.
- **Requirement IDs:** NFR-007, FR-009, AC-105, AC-106, AC-110
- **Dependencies:** TASK-MNU-04, TASK-SCR-05
- **Files in scope:** `cmd/game/main.go` (HUD contrast plates, `ctx.font`
  constants), `internal/game/menu.go` (read-only view accessors)
- **Constraints:** no new dependencies; contrast measured against the darkest
  and brightest frame background (starfield allowed, Law 3); screen readers are
  an explicit non-goal (`specs/product.md` §8).
- **Expected tests:** browser checks `a11y: keyboard reaches every menu action`,
  `a11y: HUD contrast plate present`; manual contrast measurement recorded.
- **Verification evidence:** `browser-verify/scripts/verify.sh` PASS lines plus
  a manual contrast ratio table.
- **Out of scope:** canvas ARIA, screen-reader output, mobile/touch input.

## TASK-POL-03 — Full browser regression sweep
- **Objective:** all `browser-verify` checks pass on the final build, including
  the inherited v0.1 checks (Law 7, bootstrap, frame-rate) and the M2–M8
  additions.
- **Requirement IDs:** every `AC` row in `specs/traceability.md` marked
  "verified (browser)"; Law 7
- **Dependencies:** TASK-POL-01, TASK-INFRA-02
- **Files in scope:** `.agents/skills/browser-verify/` (checks and docs),
  `specs/traceability.md`
- **Constraints:** never weaken or delete an existing check to make the suite
  green; a flaky check is quarantined with a `TASK-` reference, not silenced.
- **Expected tests:** the suite itself.
- **Verification evidence:** the full `verify.sh` output attached to the
  release commit, with the browser and version named.
- **Out of scope:** visual-regression goldens.
