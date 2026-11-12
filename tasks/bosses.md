# Tasks — Boss Encounters

> Milestone M7 (after M6 weapons). Spec: `specs/features/bosses/spec.md`; plan:
> `plans/bosses.md`.

## TASK-BOS-01 — Boss entity, HP, and phases
- **Objective:** boss spawns only on stages 5/10/15/20, has difficulty-based HP
  and 2–3 phases, occupies the stage alone.
- **Requirement IDs:** FR-015.1, FR-015.2, FR-015.3, BR-014, AC-190, AC-191,
  AC-193, AC-198
- **Dependencies:** TASK-FRM-01, TASK-WAV-03
- **Files in scope:** `internal/game/boss.go`, `internal/game/director.go`,
  `internal/game/boss_test.go`
- **Constraints:** HP from the difficulty table, no duplicated constants;
  spawning suppressed while alive.
- **Expected tests:** `TestBossOnFifthStagesOnly`, `TestBossHPLadder`,
  `TestNoSpawnsDuringBoss`.
- **Verification evidence:** test output.
- **Out of scope:** patterns.

## TASK-BOS-02 — Patterns with corridor guarantees
- **Objective:** `sweep`, `aimed-burst`, `spiral` emitters that always leave a
  ≥48 px corridor and respect the projectile cap.
- **Requirement IDs:** FR-015.4, AC-196
- **Dependencies:** TASK-BOS-01, TASK-WAV-02 (validator reuse)
- **Files in scope:** `internal/game/boss.go`, `internal/game/projectile.go`,
  `internal/game/boss_test.go`
- **Constraints:** parameterised, validated, no freehand bullet walls.
- **Expected tests:** `TestPatternCorridor` (200 seeded fights/difficulty).
- **Verification evidence:** test output.
- **Out of scope:** visual telegraph render.

## TASK-BOS-03 — Telegraphs, invulnerability, and rewards
- **Objective:** ≥0.8 s phase telegraph with boss invulnerable, one-shot reward
  on defeat, stage completion, `VICTORY` at stage 20.
- **Requirement IDs:** FR-015.3, FR-015.7, FR-015.9, AC-192, AC-194, AC-195,
  AC-199
- **Dependencies:** TASK-BOS-02
- **Files in scope:** `internal/game/boss.go`, `internal/game/director.go`,
  `internal/game/boss_test.go`
- **Constraints:** reward guarded by a one-shot flag; `GAME_OVER` takes
  precedence.
- **Expected tests:** `TestPhaseTelegraph`, `TestRewardOnce`,
  `TestNoRewardAfterGameOver`, `TestVictoryAfterFinalBoss`.
- **Verification evidence:** test output.
- **Out of scope:** boss music (M8).

## TASK-BOS-04 — Contact damage and HUD
- **Objective:** contact costs one life per 0.5 s window; HP bar and phase cue
  render with geometric fallback.
- **Requirement IDs:** FR-015.6, FR-015.8, AC-197
- **Dependencies:** TASK-BOS-03, TASK-LIV-03
- **Files in scope:** `internal/game/boss.go`, `cmd/game/main.go`
- **Constraints:** reuse the damage arbiter; no rule in `cmd/game`.
- **Expected tests:** `TestBossContactWindow`.
- **Verification evidence:** test output + manual readability note.
- **Out of scope:** sprites (M8).
