# Plan — Enemy Spawning

> Implements FR-003, BR-004, BR-006, AC-005…AC-008
> (`specs/features/enemy-spawning/`).

> **v0.2 note: superseded.** This plan describes v0.1 spawning only. Its
> replacement is `plans/formation-ai.md` + `plans/procedural-waves.md` (M5).
> Do not extend it.

## Requirements being implemented
FR-003.1–.3 (interval, random X, constant drift), plus determinism (NFR-001).

## Architecture components affected
- `internal/game` — `spawnEnemies`, `updateEnemies`, seeded RNG in `Game`.

## Contracts affected
- `specs/contracts/simulation-api.md` (spawn timing behavior).
- ADR-0003 (seeded RNG) — implemented by this plan.

## Files or modules likely to change
- `internal/game/game.go`
- `internal/game/game_test.go`

## Dependency order
1. RNG field + seed constant (ADR-0003)
2. Spawn timer logic
3. Downward movement
4. Tests (disable natural spawns via `spawnTimer` override in tests)

## Data migrations
None.

## Testing strategy
- Unit tests for spawn interval (AC-005/006), X range (AC-007), drift (AC-008)
  with a fixed seed; collision tests isolate spawns via `g.spawnTimer = 1e9`.

## Rollout / rollback
- Rebuild WASM; rollback via previous build. No data.

## Risks and mitigations
- Non-deterministic tests if global rand is used → code review enforces the
  per-game RNG (Law 2); vet + review checklist in ai-development-guide.
