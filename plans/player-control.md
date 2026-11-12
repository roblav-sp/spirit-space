# Plan — Player Control

> Implements FR-001, BR-008, AC-001…AC-004 (`specs/features/player-control/`).

> **v0.2 note.** Unchanged behaviour. Menu states suspend movement
> (`plans/main-menu.md`, M2) and game speed scales world time only
> (`plans/difficulty-speed.md`, M4). The local `BR-005` reference is now `BR-008`.

## Requirements implemented
FR-001 (movement + clamping), BR-008, AC-001…AC-004.

## Architecture components affected
- `internal/game` — `updatePlayer` (simulation).
- `cmd/game/main.go` — key→Input mapping (already implemented; no change
  expected).

## Contracts affected
- `specs/contracts/simulation-api.md` (BC-3 clamp guarantee).
- `specs/contracts/bootstrap.md` (movement key codes).

## Files likely to change
- `internal/game/game.go` (movement code)
- `internal/game/game_test.go` (movement tests)

## Dependency order
1. Simulation movement + clamping
2. Key mapping in `cmd/game` (depends on `Input` shape)
3. Tests

## Data migrations
None.

## Testing strategy
- Unit tests in `internal/game/game_test.go`: clamp, speed, frame-rate
  independence, diagonal behavior.
- Manual: play in browser and verify all 4 directions + WASD.

## Rollout / rollback
- Static files rebuilt via `build.sh`; rollback = rebuild previous commit.
- No data or compatibility concerns.

## Risks and mitigations
- Frame-rate dependence regression → `TestFrameRateIndependence` guards it.
- Diagonal speed dispute (open question in spec) → left as documented
  behavior; decision needed before changing.
