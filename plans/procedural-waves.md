# Plan — Procedural Wave Director

> Implements FR-011, BR-017, AC-150…AC-159
> (`specs/features/procedural-waves/spec.md`). Milestone **M5** (after
> formations). ADR-0009.

## Requirements being implemented
Seeded wave selection from a validated catalogue, run metadata, safe-gap and
clearance validators, stage progression, `VICTORY`.

## Architecture components affected
- `internal/game` — new `director.go` (catalogue, selection, validation,
  stage/wave progression), `metadata.go` (immutable `RunMetadata`), `victory`
  transition in `state.go`; replaces `spawnEnemies`.
- `cmd/game` — seed supply for a new run (CSPRNG or `Date.now()`), stage/wave
  HUD, pause screen seed display.

## Contracts affected
`simulation-api.md` (BC-12; `Options.Seed`, `Metadata()`), bootstrap (seed
source is not a DOM rule, but it is the only new cross-boundary input).

## Files or modules likely to change
`internal/game/director.go`, `internal/game/metadata.go`,
`internal/game/game.go`, `internal/game/director_test.go`, `cmd/game/main.go`.

## Dependency order
1. `RunMetadata` + `Options.Seed` plumbing (`NewGame`).
2. Wave catalogue as data (template, mix, count, anchor, divePlan).
3. Validator: clearance, corridor, caps, telegraph floor.
4. Selection loop with 10-attempt cap + guaranteed fallback.
5. Stage/wave progression + `VICTORY` at 20.
6. Delete `spawnEnemies` and re-point `advance()`-based tests.

## Data migrations
`Game.rng` persists but is seeded from metadata; `spawnTimer` disappears.
No persistence exists yet, so nothing to migrate.

## Testing strategy
- Unit: AC-150/AC-151 (determinism + variety), AC-152/AC-153 (validators over a
  fixed seed matrix, e.g. 50 seeds × 4 difficulties), AC-154…AC-158,
  AC-159 (RNG version tag).
- Golden-ish test: store the first 10 waves for seed 1 in a table in the test
  file so an accidental draw-order change fails loudly (this is the RNG-version
  guard).
- No browser test; distribution is a simulation property.

## Rollout / rollback
Static deploy. Rollback restores the v0.1 spawn loop from the reverted commit.
Keep the old `spawnEnemies` in tree until step 6 passes, then delete it in a
separate commit for a clean revert boundary.

## Risks and mitigations
- **Draw order drifting on refactor** → explicit RNG version + golden table
  (AC-159); bumping the version is the only sanctioned way to change it.
- **Validator rejecting everything** → fallback wave is always accepted, and a
  counter in tests asserts the rejection rate stays below a threshold.
- **Player-input-dependent draws** → draws happen only at wave boundaries in
  fixed order; AC-157 asserts step-size independence.
