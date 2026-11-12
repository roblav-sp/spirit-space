# Tasks — Weapons and Power-ups

> Milestone M6. Spec: `specs/features/weapons-powerups/spec.md`; plan:
> `plans/weapons-powerups.md`.

## TASK-WPN-01 — Weapon state and base weapon parity
- **Objective:** a weapon struct reproduces today's single-bullet behaviour
  exactly (0.2 s, 500 px/s, radius 4) so tests stay green before new modes.
- **Requirement IDs:** FR-012.1, AC-160
- **Dependencies:** TASK-DFS-02
- **Files in scope:** `internal/game/weapons.go`, `internal/game/game.go`,
  `internal/game/weapons_test.go`
- **Constraints:** no behaviour change to `TestFireCooldown`.
- **Expected tests:** `TestBaseWeaponParity`.
- **Verification evidence:** existing test suite unchanged and passing.
- **Out of scope:** pickups.

## TASK-WPN-02 — Rapid and spread
- **Objective:** `rapid` halves cadence; `spread` fires three bullets with the
  spec'd angles and damage split; mutual exclusion with `beam` handled.
- **Requirement IDs:** FR-012.2, FR-012.3, FR-012.8, BR-016, AC-161, AC-162,
  AC-166, AC-167
- **Dependencies:** TASK-WPN-01
- **Files in scope:** `internal/game/weapons.go`, `internal/game/game.go`,
  `internal/game/weapons_test.go`
- **Constraints:** expiry restores exactly the previous state; refresh does not
  stack intensity.
- **Expected tests:** `TestRapidCadence`, `TestSpreadAngles`,
  `TestRefreshDoesNotStack`, `TestSpreadBeamExclusion`.
- **Verification evidence:** test output.
- **Out of scope:** beam (next task).

## TASK-WPN-03 — Beam and shield
- **Objective:** beam pierces without double-hitting; shield absorbs exactly one
  damage event and composes with invulnerability.
- **Requirement IDs:** FR-012.4, FR-012.5, AC-163, AC-164, AC-165
- **Dependencies:** TASK-WPN-02, TASK-LIV-03
- **Files in scope:** `internal/game/weapons.go`, `internal/game/lives.go`,
  `internal/game/weapons_test.go`
- **Constraints:** single `applyDamage` path for bullets and beam; shield never
  consumed while invulnerable.
- **Expected tests:** `TestBeamPiercesOnce`, `TestShieldAbsorbsOne`,
  `TestShieldNotConsumedWhileInvulnerable`.
- **Verification evidence:** test output.
- **Out of scope:** screen-clearing bombs.

## TASK-WPN-04 — Drops, pickups, and pity timer
- **Objective:** drop chance from the budget, weighted type choice from the
  seeded RNG, pity timer every 40 kills, pickup drift/despawn/collection.
- **Requirement IDs:** FR-012.6, FR-012.7, FR-012.9, AC-168
- **Dependencies:** TASK-WPN-03, TASK-WAV-01
- **Files in scope:** `internal/game/pickup.go`, `internal/game/game.go`,
  `internal/game/pickup_test.go`
- **Constraints:** draws in fixed order; pity counter is deterministic state.
- **Expected tests:** `TestDropRateTolerance`, `TestPityTimer`,
  `TestPickupLifecycle`.
- **Verification evidence:** test output.
- **Out of scope:** boss guaranteed drops (M7).

## TASK-WPN-05 — HUD indicators
- **Objective:** render one indicator per active power-up with a countdown that
  freezes under pause.
- **Requirement IDs:** FR-012.10, AC-169
- **Dependencies:** TASK-WPN-04
- **Files in scope:** `cmd/game/main.go`
- **Constraints:** geometric fallback when sprites are absent (FR-017.3).
- **Expected tests:** manual/browser pixel smoke.
- **Verification evidence:** `.agents/skills/browser-verify/scripts/verify.sh` PASS + manual note.
- **Out of scope:** animated icons.
