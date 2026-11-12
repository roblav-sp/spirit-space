# Plan — Lives, Damage, and Respawn

> Implements FR-008, BR-009, BR-013, AC-120…AC-129
> (`specs/features/lives-respawn/spec.md`). Milestone **M3**.

## Requirements being implemented
Three lives, single-hazard arbitration, `PLAYER_DYING`/`RESPAWNING` timers,
invulnerability, `GAME_OVER` at zero, R restart preserving settings.

## Architecture components affected
- `internal/game` — new `lives.go`; `handleCollisions` is split into
  `collectDamage` + `applyDamage` so arbiters are testable in isolation.
- `cmd/game` — HUD life pips, death flash, respawn blink.

## Contracts affected
`simulation-api.md` (BC-10; `Restart` semantics), `bootstrap.md` (R only in
terminal states — already true).

## Files or modules likely to change
`internal/game/lives.go`, `internal/game/game.go`, `internal/game/lives_test.go`,
`cmd/game/main.go`.

## Dependency order
1. Add `Lives`, damage arbitration, and hazard neutralisation (no state
   machine yet) — keep v0.1 game-over behaviour testable behind a flag until
   step 2.
2. Add `PLAYER_DYING`/`RESPAWNING` states and timers (depends on M2's `State`).
3. Invulnerability collision filtering + blink rendering.
4. Rewrite the two v0.1 lethal tests as life-loss tests; keep
   `TestGameOverFreezesSimulation` and `TestRestartResetsState`.

## Data migrations
None. New fields default to 3 lives / zero timers via `New()`.

## Testing strategy
- Unit: AC-120…AC-129, including the simultaneous bottom+touch case (AC-126)
  built as a crafted state, not by playing.
- Determinism: damage during a multi-step advance must be identical at 1/60 and
  1/30 (whole steps).
- Browser: death flash/blink visible (pixel-diff, heuristic).

## Rollout / rollback
Static deploy. Rollback reverts the commit; no persisted data is touched.

## Risks and mitigations
- **Double life loss in one step** (enemy + projectile overlap) → arbitration
  picks one hazard, applies once, returns early (AC-126, BR-007).
- **Invulnerability swallowing honest deaths** → 1.5 s is spec'd and tested
  exactly (AC-128), not "about".
- **Hazard consumed while invulnerable** → explicitly forbidden (FR-008.7,
  AC-122) so an invulnerable pass-through cannot farm enemies.
