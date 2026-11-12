# Tasks — Difficulty and Game Speed

> Milestone M4. Spec: `specs/features/difficulty-speed/spec.md`; plan:
> `plans/difficulty-speed.md`.

## TASK-DFS-01 — Difficulty and speed types with one data source
- **Objective:** `Difficulty`/`SpeedScale` types, budget table, single accessor,
  defaults and validation of invalid values.
- **Requirement IDs:** FR-007.1, FR-007.2, FR-007.3, FR-007.9, BR-011,
  AC-130, AC-131, AC-132, AC-139
- **Dependencies:** none
- **Files in scope:** `internal/game/difficulty.go`,
  `internal/game/difficulty_test.go`
- **Constraints:** data only, no behaviour; no duplicated constants.
- **Expected tests:** `TestDifficultyDefaults`, `TestBudgetTableMonotone`,
  `TestInvalidDifficultyFallsBack`.
- **Verification evidence:** test output.
- **Out of scope:** applying budgets (M5).

## TASK-DFS-02 — Fixed step and `Advance`
- **Objective:** `Step()` advances exactly 1/60 s; `Advance(seconds)` consumes
  whole steps and truncates the remainder; `Update(dt)` remains as a
  whole-step wrapper.
- **Requirement IDs:** FR-007.4, BR-012, BC-9, AC-133, AC-134
- **Dependencies:** TASK-DFS-01
- **Files in scope:** `internal/game/game.go`, `internal/game/game_test.go`
- **Constraints:** no interpolation; existing behaviour preserved under
  whole-step conversion; `TestFrameRateIndependence` becomes exact equality.
- **Expected tests:** `TestAdvanceWholeSteps`, `TestFrameRateIndependence`
  (rewritten, stricter), `TestSpeedScalesWorldTime`.
- **Verification evidence:** test output.
- **Out of scope:** accumulator (TASK-DFS-03).

## TASK-DFS-03 — Accumulator and stall policy in `cmd/game`
- **Objective:** clamped frame time (≤0.25 s) feeds `dt × SpeedScale` into whole
  steps; at most 4 steps per frame; remainder carries; no spiral of death.
- **Requirement IDs:** FR-007.4, AC-135
- **Dependencies:** TASK-DFS-02
- **Files in scope:** `cmd/game/main.go`
- **Constraints:** no game rule in `cmd/game` (the multiplier is spec'd as an
  accumulator concern, ADR-0012); a small pure helper may live in
  `internal/game` to keep it testable.
- **Expected tests:** `TestAccumulatorStallCap` (helper level, native),
  browser `gameplay: canvas animates`.
- **Verification evidence:** test + `.agents/skills/browser-verify/scripts/verify.sh` PASS.
- **Out of scope:** render interpolation.

## TASK-DFS-04 — Fairness floors and HUD label
- **Objective:** expose the telegraph/corridor floors per difficulty and render
  the `DIFFICULTY · SPEED×` label.
- **Requirement IDs:** FR-007.5, FR-007.8, AC-136, AC-138
- **Dependencies:** TASK-DFS-01, TASK-DFS-02
- **Files in scope:** `internal/game/difficulty.go`, `cmd/game/main.go`,
  `internal/game/difficulty_test.go`
- **Constraints:** floors are in world time; consumed by the M5 validator.
- **Expected tests:** `TestTelegraphFloorPerDifficulty`.
- **Verification evidence:** test output + manual HUD note.
- **Out of scope:** using the floors to reject waves (M5).
