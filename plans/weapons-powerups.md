# Plan — Weapons and Power-ups

> Implements FR-012, BR-016, AC-160…AC-169
> (`specs/features/weapons-powerups/spec.md`). Milestone **M6**.

## Requirements being implemented
Weapon state machine (base/rapid/spread/beam), shield charges, drop table with
pity timer, pickup entities, expiry, stacking rules, HUD indicators.

## Architecture components affected
- `internal/game` — new `weapons.go` (weapon state, cadence), `pickup.go`
  (drops, drift, despawn, collection), scoring hook for pickup-independent
  points.
- `cmd/game` — pickup sprites/fallback, HUD timer bars, telegraph colours.

## Contracts affected
`simulation-api.md` (BC-13). `assets.md` IDs `pickup.*` (already reserved).

## Files or modules likely to change
`internal/game/weapons.go`, `internal/game/pickup.go`,
`internal/game/game.go`, `internal/game/weapons_test.go`, `cmd/game/main.go`.

## Dependency order
1. Weapon struct + base weapon equals current behavior (regression-free).
2. `rapid` (cadence only) — smallest surface, validates the model.
3. `spread` / `beam` mutual exclusion + bullet damage field.
4. `shield` via the damage arbiter from M3 (must compose with invulnerability).
5. Drop table + pity timer + pickup lifecycle.
6. HUD indicators.

## Data migrations
`Bullet` gains `Damage`; `Player` gains weapon fields. No persistence yet.

## Testing strategy
- Unit: AC-160…AC-169. Pity timer tested with a scripted kill counter, not RNG
  sampling. Drop-rate tolerance test uses 10 000 seeded kills (fast: no render).
- Composition test: shield + invulnerability + contact in one step yields zero
  life loss and zero shield consumption (AC-163/FR-008.7).
- Browser: HUD timer bars visible (heuristic pixel check).

## Rollout / rollback
Static deploy. Rollback reverts the commit; base weapon behaviour is unchanged,
so a revert is safe mid-run in theory (no persistence yet).

## Risks and mitigations
- **Power-ups making the game trivial** → spread side bullets at half damage
  (pending decision) and hard caps; M9 measures time-to-clear per difficulty.
- **Damage arithmetic duplicated** between bullet and beam paths → single
  `applyDamage(enemy, amount)` used by both; tested by AC-164.
- **Pickup collection order non-determinism** → slice order, documented in the
  spec's edge cases.
