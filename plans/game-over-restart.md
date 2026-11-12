# Plan — Game Over and Restart

> Implements FR-004 (lethal events), FR-005, BR-001, BR-007, AC-013…AC-017
> (`specs/features/game-over-restart/`).

> **v0.2 note.** Freeze + banner + R restart are preserved (M2/M3). The
> lethal rules move to `plans/lives-respawn.md`; this plan's lethal-event
> section is historical.

## Requirements being implemented
Bottom-edge and player-collision game over (FR-004), frozen simulation
(FR-005.1), restart via R (FR-005.1–.2).

## Architecture components affected
- `internal/game` — `handleCollisions` lethal checks, `Restart`.
- `cmd/game/main.go` — KeyR listener (bootstrap contract), game-over banner.

## Contracts affected
- `specs/contracts/simulation-api.md` (BC-2, BC-7).
- `specs/contracts/bootstrap.md` (`KeyR` semantics).

## Files likely to change
- `internal/game/game.go`
- `internal/game/game_test.go`
- `cmd/game/main.go` (only if restart key handling changes)

## Dependency order
1. Lethal collision checks (bottom edge, player overlap)
2. GameOver freeze in `Update`
3. `Restart()`
4. KeyR wiring in `cmd/game`
5. Tests + banner rendering check

## Data migrations
None.

## Testing strategy
- Unit tests: bottom-edge (AC-013), player collision (AC-014), freeze
  (AC-015), restart reset (AC-016).
- Manual: die in browser, press R, verify fresh run (AC-017).

## Rollout / rollback
- Rebuild; rollback via previous build. No data.

## Risks and mitigations
- Restart pressed while running (FR-005.2 violation) → guarded by checking
  `g.GameOver` in the key handler; verified manually.
