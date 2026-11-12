# Tasks — Main Menu, State Machine, and Pause

> Milestone M2. Spec: `specs/features/main-menu/spec.md`; plan:
> `plans/main-menu.md`. One task = one verifiable objective.

## TASK-MNU-01 — State enum and `New()` starts in `MAIN_MENU`
- **Objective:** `State` exists with all twelve values and `New()` returns a
  game in `StateMainMenu` with no entities and no score.
- **Requirement IDs:** FR-006.1, BC-8
- **Dependencies:** none
- **Files in scope:** `internal/game/state.go`, `internal/game/game.go`,
  `internal/game/state_test.go`
- **Constraints:** no new imports beyond stdlib; no behaviour implemented yet.
- **Expected tests:** `TestNewStartsAtMainMenu` (AC-101); update existing tests
  that assumed immediate play — do not delete assertions.
- **Verification evidence:** `go test ./internal/...` output.
- **Out of scope:** menu rendering, transitions.

## TASK-MNU-02 — Menu model and navigation actions
- **Objective:** up/down wrap, left/right cycle option values, confirm/back are
  edge-triggered and cannot produce out-of-range values.
- **Requirement IDs:** FR-006.2, FR-006.3, AC-103, AC-104
- **Dependencies:** TASK-MNU-01
- **Files in scope:** `internal/game/menu.go`, `internal/game/menu_test.go`
- **Constraints:** pure data; no rendering, no input polling.
- **Expected tests:** `TestMenuWrap`, `TestOptionCycleBounds`,
  `TestMenuEdgeTrigger`.
- **Verification evidence:** test output.
- **Out of scope:** screen layout, audio clicks.

## TASK-MNU-03 — Start, pause, resume, quit to menu
- **Objective:** Start creates a fresh run with the selected options; Escape/P
  toggles `PAUSED` with an exact freeze; Quit to Menu discards the run.
- **Requirement IDs:** FR-006.6 … FR-006.8, FR-006.12, FR-009,
  AC-102, AC-105, AC-106, AC-107, AC-109
- **Dependencies:** TASK-MNU-02
- **Files in scope:** `internal/game/state.go`, `internal/game/game.go`,
  `internal/game/state_test.go`
- **Constraints:** freeze must be byte-exact; no timer may tick in `PAUSED`.
- **Expected tests:** `TestStartCreatesRun`, `TestPauseFreezesEverything`,
  `TestResumeRestoresState`, `TestQuitToMenuDiscardsRun`.
- **Verification evidence:** test output.
- **Out of scope:** lives (M3), difficulty tables (M4).

## TASK-MNU-04 — Renderer dispatch and input clarity
- **Objective:** `draw` renders menu/pause screens from `State`, sets
  `ctx.font` from a constant, and the key handler maps state-aware keys with
  `preventDefault` and blur clearing.
- **Requirement IDs:** FR-006.4, FR-006.5, FR-006.9, FR-006.11, FR-006.12,
  AC-108, AC-110
- **Dependencies:** TASK-MNU-03
- **Files in scope:** `cmd/game/main.go`, `internal/game/menu.go` (read-only
  view accessors)
- **Constraints:** no game rule in `cmd/game` (Law 1); reads state only (Law 2).
- **Expected tests:** browser checks `menu: main menu renders`, `input: arrows
  do not scroll page`, `input: blur clears held keys` in
  `.agents/skills/browser-verify/e2e/verify.mjs`.
- **Verification evidence:** `.agents/skills/browser-verify/scripts/verify.sh` PASS lines.
- **Out of scope:** visual polish, sprites.
