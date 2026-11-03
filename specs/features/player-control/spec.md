# Feature — Player Control

## Context
The player pilots a ship near the bottom of the 800×600 world. Movement is
the player's only defensive tool besides shooting. Implements FR-001.

## Actors
Player (keyboard), Simulation (`internal/game`), Renderer (`cmd/game`).

## Preconditions
A run exists (`New()` or `Restart()`); game not over.

## Functional requirements
- **FR-001.1** — Arrow keys AND `WASD` move the ship in 4 directions at
  `playerSpeed` = 300 px/s.
- **FR-001.2** — Simultaneous keys combine (e.g. up+right → diagonal).
- **FR-001.3** — Position is clamped so the ship never leaves the play field
  (`[Radius, Width−Radius] × [Radius, Height−Radius]`).

## Business rules
- BR-005: Movement speed is constant; no acceleration or inertia.

## Acceptance criteria
- **AC-001** — Given the game started, when Right is held for 1 s at 60 FPS,
  then `Player.X` increased by exactly 300 (clamped).
- **AC-002** — Given the ship at the left edge, when Left is held, then
  `Player.X` stays at `Radius`.
- **AC-003** — Given 6 simulated seconds at 30 FPS vs 60 FPS with identical
  inputs, final positions are identical (NFR-002). *(test:
  `TestFrameRateIndependence`)*
- **AC-004** — Diagonal input moves at the same per-axis speed as
  single-direction input (speed is axis-separated, not normalized).

## Edge cases
- Ship at a corner with two clamped directions → stays at corner.
- Input flags all false → no movement; cooldown still ticks.

## Error behavior
- Negative or huge `dt` is not defended inside the simulation (documented in
  the simulation contract); `cmd/game` clamps `dt` ≤ 0.1 s.

## Non-functional requirements
- NFR-001 (determinism), NFR-002 (frame-rate independence).

## Security requirements
- SEC-002: input arrives only from keyboard events on the page.

## Observability requirements
- None (client-only game; see architecture/context.md).

## Out of scope
- Touch/mouse controls, gamepad, acceleration, normalized diagonal speed.

## Open questions
- Should diagonal movement be normalized (≈0.707× per axis)? Current spec
  says no (AC-004). Confirm intent.
