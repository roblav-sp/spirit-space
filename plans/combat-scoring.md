# Plan — Combat and Scoring

> Implements FR-002, FR-004 (score part), BR-002, BR-003, BR-005, AC-009…AC-011
> (`specs/features/combat-scoring/`).

## Requirements being implemented
Firing with cooldown (FR-002.1–.3), bullet-enemy collision and scoring
(FR-004.1), score rendering.

## Architecture components affected
- `internal/game` — firing in `updatePlayer`, `updateBullets`,
  bullet part of `handleCollisions`.
- `cmd/game/main.go` — draws bullets and score; Space key mapping.

## Contracts affected
- `specs/contracts/simulation-api.md` (BC-4, BC-6).
- `specs/contracts/bootstrap.md` (`Space` key).

## Files likely to change
- `internal/game/game.go`
- `internal/game/game_test.go`
- (rendering already in `cmd/game/main.go` — no change expected)

## Dependency order
1. Firing + cooldown
2. Bullet motion + despawn
3. Bullet-enemy collision + scoring
4. Tests

## Data migrations
None.

## Testing strategy
- Cooldown test (AC-009), kill-and-score test with natural spawns disabled
  (AC-010), despawn coverage (AC-011 implied by BC-5), miss test (AC-011).

## Rollout / rollback
- Rebuild; rollback via previous build. No data.

## Risks and mitigations
- Double-collision (one bullet killing two enemies) → Dead flags checked in
  the same pass (BR-005); covered by code inspection + tests.
