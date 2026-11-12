# Tasks — Game Over and Restart

> **v0.2 note.** Terminal-state tasks remain valid; the lethal-event tasks
> are superseded by `tasks/lives-respawn.md` (M3).

## TASK-GOR-01 — Lethal collision checks
- **Objective:** game over when an enemy reaches the bottom edge or overlaps
  the player; check runs before scoring in the same pass (BR-007).
- **Requirement IDs:** FR-004.2, FR-004.3, BR-001, AC-013, AC-014
- **Dependencies:** TASK-ENS-03 (enemy motion)
- **Files in scope:** `internal/game/game.go` (`handleCollisions`)
- **Constraints:** at most one lethal event per update; return immediately.
- **Expected tests:** `TestEnemyReachingBottomEndsGame`,
  `TestEnemyPlayerCollisionEndsGame`.
- **Verification evidence:** test output.
- **Out of scope:** lives, continues.

## TASK-GOR-02 — Freeze simulation after game over
- **Objective:** `Update` returns immediately when `GameOver` (BC-2).
- **Requirement IDs:** FR-005.1, AC-015
- **Dependencies:** TASK-GOR-01
- **Files in scope:** `internal/game/game.go` (top of `Update`)
- **Constraints:** must not consume RNG or timers while frozen.
- **Expected tests:** `TestGameOverFreezesSimulation`.
- **Verification evidence:** test output.
- **Out of scope:** pause feature.

## TASK-GOR-03 — Restart function
- **Objective:** `Restart()` restores the exact `New()` state (BC-7).
- **Requirement IDs:** FR-005.1, AC-016, BC-7
- **Dependencies:** none
- **Files in scope:** `internal/game/game.go` (`Restart`)
- **Constraints:** must recreate the seeded RNG (determinism per run).
- **Expected tests:** `TestRestartResetsState`.
- **Verification evidence:** test output.
- **Out of scope:** high scores.

## TASK-GOR-04 — R key wiring and game-over banner
- **Objective:** KeyR triggers `Restart()` only when `GameOver`; renderer
  shows the game-over banner instead of score.
- **Requirement IDs:** FR-005.1, FR-005.2, AC-016, AC-017; contract
  `bootstrap.md`
- **Dependencies:** TASK-GOR-02
- **Files in scope:** `cmd/game/main.go`
- **Constraints:** DOM access only in `cmd/game` (Law 5); no game rules (Law 1).
- **Expected tests:** e2e via `.agents/skills/browser-verify` (KeyR no-op while running); game-over flow manual (TODO: scripted play-through).
- **Verification evidence:** manual play note; WASM build success.
- **Out of scope:** pause menu.
