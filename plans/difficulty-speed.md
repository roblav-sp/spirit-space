# Plan — Difficulty and Game Speed

> Implements FR-007, BR-011, BR-012, AC-130…AC-139
> (`specs/features/difficulty-speed/spec.md`). Milestone **M4**. ADR-0012,
> ADR-0008.

## Requirements being implemented
Budget tables, speed scaling at the accumulator, fixed-step loop, fairness
floors, HUD label, validation of invalid values.

## Architecture components affected
- `internal/game` — new `difficulty.go` (tables + accessors), fixed-step
  `Step`/`Advance` in `game.go`; `Update(dt)` redefined as whole steps.
- `cmd/game` — accumulator + max catch-up, `dt × SpeedScale` at the feed.

## Contracts affected
`simulation-api.md` (BC-9, BC-11; `Options`), bootstrap (nothing new).

## Files or modules likely to change
`internal/game/difficulty.go`, `internal/game/game.go`,
`internal/game/difficulty_test.go`, `cmd/game/main.go`.

## Dependency order
1. `Difficulty`/`SpeedScale` types + tables + accessors (pure data).
2. Fixed step + `Advance`; port existing tests to `advance()` built on it.
3. Accumulator in `cmd/game` with clamp (0.25 s) and catch-up cap (4 steps).
4. Apply speed at the feed only; HUD label.
5. Fairness-floor helper used by the wave validator (consumed in M5).

## Data migrations
None. Defaults: `Pilot`, `1.0`.

## Testing strategy
- Unit: AC-130…AC-132 (table-driven), AC-133/AC-134 (same world time across
  speeds), AC-135 (stall), AC-136 (floor), AC-139 (invalid input).
- `TestFrameRateIndependence` is rewritten in terms of whole steps and must
  produce **exact** equality (stricter than the 1e-6 tolerance it uses today).
- Browser: HUD label present (text assertion via canvas snapshot is not
  feasible; check the draw call path through a debug hook or skip to manual).

## Rollout / rollback
Static deploy. Rollback reverts the commit; runs are not persisted yet.

## Risks and mitigations
- **Double scaling** (speed applied in both `cmd/game` and core) → only the
  accumulator multiplies; AC-133 fails loudly if duplicated.
- **Spiral of death** after a stall → catch-up cap + drop remainder (AC-135).
- **Tests with exact float equality** become brittle if steps are not aligned →
  `Advance` takes whole steps only; fractional world time is truncated.
