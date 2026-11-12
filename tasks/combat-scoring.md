# Tasks — Combat and Scoring

> **v0.2 note.** Tasks here are v0.1 history. FR-002 work continues in
> `tasks/weapons-powerups.md` (M6); scoring in `tasks/scoring-highscores.md`
> (M7).

## TASK-CMB-01 — Firing with cooldown
- **Objective:** Space fires one bullet per 0.2 s from the ship's nose; first
  shot immediate; bullets fly up at 500 px/s.
- **Requirement IDs:** FR-002.1, FR-002.2, BR-003, AC-009
- **Dependencies:** none (Input mapping exists in `cmd/game`)
- **Files in scope:** `internal/game/game.go` (`updatePlayer` fire block)
- **Constraints:** cooldown decrements every frame regardless of firing.
- **Expected tests:** `TestFireCooldown`.
- **Verification evidence:** test output.
- **Out of scope:** ammo, weapon types.

## TASK-CMB-02 — Bullet despawn
- **Objective:** bullets removed when `Y ≤ −20` or after hitting an enemy.
- **Requirement IDs:** FR-002.3, FR-004.1, BC-5
- **Dependencies:** TASK-CMB-01
- **Files in scope:** `internal/game/game.go` (`updateBullets`)
- **Constraints:** reuse slice capacity (`kept` pattern); no allocations per
  frame beyond appends.
- **Expected tests:** kill test covers on-hit despawn; off-screen despawn
  exercised implicitly.
- **Verification evidence:** test output.
- **Out of scope:** particle effects.

## TASK-CMB-03 — Bullet-enemy collision and scoring
- **Objective:** circle overlap destroys both, +10 score (BR-002).
- **Requirement IDs:** FR-004.1, BR-002, BR-005, AC-010
- **Dependencies:** TASK-CMB-01, TASK-ENS-03
- **Files in scope:** `internal/game/game.go` (`handleCollisions`)
- **Constraints:** each pair collides at most once (Dead flags); collision
  pass must not award score after game over.
- **Expected tests:** `TestBulletDestroyedOnHitAndScored` (with natural
  spawns disabled).
- **Verification evidence:** test output.
- **Out of scope:** piercing, combos.

## TASK-CMB-04 — Render bullets and score
- **Objective:** draw bullets as squares and score text each frame.
- **Requirement IDs:** FR-004.2, AC-010 (visual)
- **Dependencies:** TASK-CMB-01
- **Files in scope:** `cmd/game/main.go` (`draw`)
- **Constraints:** reads state only, never mutates (Law 2); keep in
  `cmd/game`.
- **Expected tests:** e2e via `.agents/skills/browser-verify` (input, rendering) + unit tests; manual spot-check optional.
- **Verification evidence:** manual play note; WASM build.
- **Out of scope:** sprites, HUD layout.
