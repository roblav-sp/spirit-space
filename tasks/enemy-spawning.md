# Tasks — Enemy Spawning

## TASK-ENS-01 — Seeded per-game RNG
- **Objective:** `Game` owns a `*rand.Rand` seeded from a constant; recreated
  in `New()`.
- **Requirement IDs:** BR-006, NFR-001; ADR-0003
- **Dependencies:** none
- **Files in scope:** `internal/game/game.go`
- **Constraints:** no package-global rand; no time-based seeding (Law 2).
- **Expected tests:** determinism implicitly covered by spawn tests with the
  fixed seed.
- **Verification evidence:** `go test ./internal/...`.
- **Out of scope:** configurable seed (future ADR).

## TASK-ENS-02 — Spawn timer and X placement
- **Objective:** spawn one enemy every 1.2 s of simulated time at random X in
  `[enemyRadius, Width−enemyRadius]`, Y = −radius.
- **Requirement IDs:** FR-003.1, FR-003.2, AC-005, AC-006, AC-007
- **Dependencies:** TASK-ENS-01
- **Files in scope:** `internal/game/game.go` (`spawnEnemies`)
- **Constraints:** at most one spawn per `Update`; no catch-up loop.
- **Expected tests:** interval tests (1.2 s ⇒ 1 enemy; 0.6 s ⇒ 0 enemies),
  X-range scan across a long run.
- **Verification evidence:** test output.
- **Out of scope:** difficulty ramping (BR-004 excludes it).

## TASK-ENS-03 — Constant downward drift
- **Objective:** enemies move down at 120 px/s·dt.
- **Requirement IDs:** FR-003.3, AC-008, BR-004
- **Dependencies:** TASK-ENS-01
- **Files in scope:** `internal/game/game.go` (`updateEnemies`)
- **Constraints:** no horizontal motion; dt-multiplied.
- **Expected tests:** position delta test (AC-008).
- **Verification evidence:** test output.
- **Out of scope:** enemy types, acceleration.
