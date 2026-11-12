# Tasks — Enemy Archetypes and Formations

> Milestone M5. Spec: `specs/features/formation-ai/spec.md`; plan:
> `plans/formation-ai.md`.

## TASK-FRM-01 — Archetype table
- **Objective:** `scout`, `interceptor`, `heavy`, `sniper`, `boss` entries with
  HP, score, projectile speed and behaviour id behind one accessor.
- **Requirement IDs:** FR-010.1, AC-141
- **Dependencies:** TASK-DFS-01 (budgets)
- **Files in scope:** `internal/game/enemy.go`, `internal/game/enemy_test.go`
- **Constraints:** data only; no duplicated HP/score constants elsewhere.
- **Expected tests:** `TestArchetypeTable`.
- **Verification evidence:** test output.
- **Out of scope:** behaviours, sprites.

## TASK-FRM-02 — Slot templates
- **Objective:** `row`, `V`, `diagonal`, `zigzag`, `flank`, `bonus` return
  `count` distinct in-field slots for all supported counts.
- **Requirement IDs:** FR-010.2, AC-140, AC-147
- **Dependencies:** TASK-FRM-01
- **Files in scope:** `internal/game/formation.go`,
  `internal/game/formation_test.go`
- **Constraints:** deterministic function of `(count, anchorX, anchorY)`; no
  RNG; no floating drift between calls.
- **Expected tests:** `TestSlotsDistinctAndInField`,
  `TestSlotsDeterministic`.
- **Verification evidence:** test output.
- **Out of scope:** entry motion.

## TASK-FRM-03 — Entry, hold, and dive behaviour
- **Objective:** enemies interpolate to slots in 1.2 s, hold a bounded
  oscillation, telegraph then dive along a named path, and fire per FR-010.6.
- **Requirement IDs:** FR-010.3 … FR-010.7, FR-010.9, AC-142, AC-143, AC-145,
  AC-148, AC-149
- **Dependencies:** TASK-FRM-02, TASK-LIV-03 (damage arbiter)
- **Files in scope:** `internal/game/formation.go`,
  `internal/game/projectile.go`, `internal/game/game.go`,
  `internal/game/formation_test.go`
- **Constraints:** telegraph ≥ floor in world time; no enemy leaves the field;
  caps read from budgets.
- **Expected tests:** `TestDiveTelegraph`, `TestEnemiesStayInField`,
  `TestProjectileCap`, `TestHeavyThreeHits`.
- **Verification evidence:** test output + browser smoke (telegraph visible).
- **Out of scope:** wave selection (next task file).

## TASK-FRM-04 — Bonus formation
- **Objective:** the `bonus` template never fires and reports a clean-clear flag
  consumed by FR-013.3.
- **Requirement IDs:** FR-010.8, AC-144
- **Dependencies:** TASK-FRM-03
- **Files in scope:** `internal/game/formation.go`,
  `internal/game/formation_test.go`
- **Constraints:** the flag is derived state, not stored twice.
- **Expected tests:** `TestBonusFormationNoFire`,
  `TestBonusCleanClearFlag`.
- **Verification evidence:** test output.
- **Out of scope:** bonus stage pacing (M9).
