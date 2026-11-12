# Plan — Enemy Archetypes and Formations

> Implements FR-010, AC-140…AC-149 (`specs/features/formation-ai/spec.md`).
> Milestone **M5**. ADR-0009 (draws), ADR-0012 (budgets).

## Requirements being implemented
Archetype table, slot templates, entry animation, bounded formation motion,
telegraphed dives, enemy projectiles, bonus template, concurrency caps.

## Architecture components affected
- `internal/game` — new `formation.go` (templates + `Slots`), `enemy.go`
  (archetype data, behaviour strategies), `projectile.go` (enemy bullets).
  `handleCollisions` gains enemy-projectile/player and bullet/enemy-HP logic.
- `cmd/game` — draw archetypes (sprite or fallback), telegraph outline.

## Contracts affected
`simulation-api.md` (BC-11), `assets.md` (IDs already listed), `persistence.md`
(no change).

## Files or modules likely to change
`internal/game/formation.go`, `internal/game/enemy.go`,
`internal/game/projectile.go`, `internal/game/game.go`,
`internal/game/formation_test.go`, `cmd/game/main.go`.

## Dependency order
1. Archetype data + accessor (no behaviour change to v0.1 enemies yet).
2. `Slots` per template + property tests for distinctness/bounds.
3. Entry interpolation and formation hold motion.
4. Dive telegraph → dive path → return/exit; firing rules.
5. Enemy projectiles + caps + collision.
6. `bonus` template + clean-clear flag for FR-013.3.
7. Remove the v0.1 spawner (`spawnEnemies`) once the director (M5, next plan)
   can drive formations; keep `TestFirstSpawnAfterSpawnDelay` until then.

## Data migrations
None, but `Enemy` gains `Archetype`, `HP`, `State` (enter/hold/dive/return) and
a slot index — coordinate with the director's slot assignment.

## Testing strategy
- Unit: AC-140…AC-149; property-style loops over counts/templates rather than
  random in-test RNG (deterministic seeds only, NFR-001).
- Bounded-run test: 30 simulated seconds with no input must not panic, must not
  exceed caps, and must keep every entity inside the field (AC-143/AC-145).
- Browser: visual smoke only (telegraph visible).

## Rollout / rollback
Static deploy. Rollback = revert; the v0.1 spawner is removed in the same PR
only after the director lands, so a revert restores it.

## Risks and mitigations
- **Enemies overlapping slots** → `Slots` returns distinct positions; AC-140.
- **Impossible dives** → path templates + validator corridor check reused by
  the director (AC-153), so formation and wave fairness cannot drift apart.
- **Projectile cap fights the boss** (M7 needs 24) → cap is read from the
  difficulty budget, not a constant (AC-145, AC-196).
