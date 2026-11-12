# Tasks — Player Control

> **v0.2 note.** Unchanged; see `tasks/main-menu.md` (TASK-MNU-04) for the
> blur/preventDefault additions.

## TASK-PLC-01 — Axis movement and clamping
- **Objective:** 4-direction movement at 300 px/s, clamped to the play field.
- **Requirement IDs:** FR-001.1, FR-001.3, BR-005, AC-001, AC-002
- **Dependencies:** none
- **Files in scope:** `internal/game/game.go` (`updatePlayer`, `clamp`)
- **Constraints:** no DOM imports; multiply by dt only (Law 4); stdlib only.
- **Expected tests:** `TestPlayerClampedToField`, `TestFrameRateIndependence`.
- **Verification evidence:** `go test ./internal/...` pass output.
- **Out of scope:** input capture (TASK-PLC-02), diagonal normalization
  (open question).

## TASK-PLC-02 — Keyboard mapping in the entry point
- **Objective:** Map arrow/WASD key codes to `Input` flags; preventDefault.
- **Requirement IDs:** FR-001.1, AC-001; contract `bootstrap.md`
- **Dependencies:** TASK-PLC-01 (Input shape)
- **Files in scope:** `cmd/game/main.go`
- **Constraints:** only `cmd/game` may touch the DOM (Law 5); no game rules
  here (Law 1).
- **Expected tests:** e2e via `.agents/skills/browser-verify` (bootstrap, input) + unit tests; manual spot-check optional.
- **Verification evidence:** manual play note in task completion; WASM build
  success.
- **Out of scope:** non-keyboard input.

## TASK-PLC-03 — Frame-rate independence test
- **Objective:** mechanically verify Law 4 / NFR-002 / AC-003.
- **Requirement IDs:** NFR-002, AC-003
- **Dependencies:** TASK-PLC-01
- **Files in scope:** `internal/game/game_test.go`
- **Constraints:** compare 30 FPS vs 60 FPS runs over the same total time;
  tolerance 1e-6.
- **Expected tests:** `TestFrameRateIndependence`.
- **Verification evidence:** test pass output.
- **Out of scope:** benchmarking.
