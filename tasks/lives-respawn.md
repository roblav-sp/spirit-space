# Tasks — Lives, Damage, and Respawn

> Milestone M3. Spec: `specs/features/lives-respawn/spec.md`; plan:
> `plans/lives-respawn.md`.

## TASK-LIV-01 — Lives counter and damage arbitration
- **Objective:** a run has 3 lives, one damage event costs exactly 1, and the
  applied hazard is neutralised without score.
- **Requirement IDs:** FR-008.1, FR-008.3, FR-008.10, BR-009, BC-10,
  AC-120, AC-121, AC-126
- **Dependencies:** TASK-MNU-01 (state), TASK-CMB-03 (existing collision pass)
- **Files in scope:** `internal/game/lives.go`, `internal/game/game.go`,
  `internal/game/lives_test.go`
- **Constraints:** at most one hazard applied per step; never award score for
  contact kills; `Lives` never < 0.
- **Expected tests:** `TestStartHasThreeLives`, `TestContactCostsOneLife`,
  `TestNoDoublePenalty`.
- **Verification evidence:** test output.
- **Out of scope:** dying/respawning states; the escape rule itself (TASK-LIV-02).

## TASK-LIV-02 — Bottom-escape handling (D-2 decided: harmless)
- **Objective:** an enemy crossing the bottom is removed and costs nothing — no
  life, no score, no `PLAYER_DYING` transition.
- **Requirement IDs:** FR-008.2, AC-125
- **Dependencies:** TASK-LIV-01
- **Files in scope:** `internal/game/lives.go`, `internal/game/game.go`,
  `internal/game/lives_test.go`
- **Constraints:** escaping must not be routed through the damage arbiter at
  all; keep it a separate, named removal path so the D-2 decision is one place.
- **Expected tests:** `TestEscapeIsHarmless` (asserts removal plus unchanged
  `Lives`, `Score`, state and timers).
- **Verification evidence:** test output; decision recorded in the spec.
- **Out of scope:** changing the score or the escape position.

## TASK-LIV-03 — Dying, respawning, and invulnerability
- **Objective:** 0.9 s `PLAYER_DYING`, then 1.5 s invulnerable `RESPAWNING` at
  the start position, then `PLAYING`; input suspended in both.
- **Requirement IDs:** FR-008.4 … FR-008.8, BR-013, AC-122, AC-123, AC-124,
  AC-128, AC-129
- **Dependencies:** TASK-LIV-01, TASK-MNU-03 (pause freeze)
- **Files in scope:** `internal/game/lives.go`, `internal/game/state.go`,
  `internal/game/lives_test.go`
- **Constraints:** timers in fixed steps; invulnerable player consumes nothing;
  pause freezes the timers.
- **Expected tests:** `TestDeathThenRespawnTiming`,
  `TestInvulnerabilityBlocksDamage`, `TestZeroLivesGameOver`,
  `TestPauseFreezesDeathTimer`.
- **Verification evidence:** test output + browser smoke (blink visible).
- **Out of scope:** life pickups, continues.

## TASK-LIV-04 — HUD and restart integration
- **Objective:** life pips render, R restart in `GAME_OVER` restores 3 lives and
  keeps difficulty/speed.
- **Requirement IDs:** FR-008.1, FR-008.9, AC-127
- **Dependencies:** TASK-LIV-03
- **Files in scope:** `cmd/game/main.go`, `internal/game/lives.go`
- **Constraints:** render reads state only; no rule in `cmd/game`.
- **Expected tests:** `TestRestartKeepsOptions`, browser `hud: life pips`.
- **Verification evidence:** test + `.agents/skills/browser-verify/scripts/verify.sh` PASS.
- **Out of scope:** animations beyond blink.
