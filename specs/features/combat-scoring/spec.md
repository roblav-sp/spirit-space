# Feature — Combat and Scoring

## Context
The player shoots enemies; destroyed enemies score points. Bullet-enemy
collision is the only scoring mechanism. Implements FR-002, FR-004 (score
part); the game-over part of FR-004 lives in `game-over-restart`.

## Actors
Player, Simulation, Renderer (draws bullets and score).

## Preconditions
Game not over; player may fire (BR-003: cooldown is the only constraint).

## Functional requirements
- **FR-002.1** — Space fires a bullet straight up from the ship's nose
  (`Y − Radius`), radius 4, speed 500 px/s.
- **FR-002.2** — Fire rate is limited to one bullet per `fireCooldown`
  (0.2 s); the first shot is immediate (cooldown starts at 0).
- **FR-002.3** — Bullets despawn when they pass above the top edge
  (`Y ≤ −20`).
- **FR-004.1** — A bullet whose circle overlaps an enemy destroys both
  (both marked `Dead`, removed from state) and awards +10 (BR-002).
- **FR-004.2** — Score is rendered on the canvas each frame.

## Business rules
- BR-002: exactly +10 per kill; no other score source.
- BR-003: no ammo; only the cooldown limits firing.
- BR-005: one bullet destroys one enemy (no piercing).

## Acceptance criteria
- **AC-009** — Given fire held, when cooldown has not elapsed since the last
  shot, then no second bullet appears.
- **AC-010** — Given an enemy directly above the player within bullet path,
  when a bullet reaches it, then enemy and bullet are removed and score
  increases by exactly 10.
- **AC-011** — Given a bullet above `Y = −20`, it no longer exists after the
  next update.
- **AC-012** — A bullet that passes beside an enemy (no overlap) does not
  affect either.

## Edge cases
- Bullet and enemy die in the same collision pass; each collides at most once
  (Dead flags).
- A bullet fired at the moment of game over still moves? No — `Update` is a
  no-op after game over (BC-2).

## Error behavior
- No failure modes; pure state transitions.

## Non-functional requirements
- NFR-001, NFR-002 apply.

## Security requirements
- SEC-001/SEC-002 (no data, no network).

## Observability requirements
- None.

## Out of scope
- Enemy projectiles, ammo, weapon upgrades, piercing shots, combo scoring.

## Open questions
- Collision is circle-circle with summed radii; bullet radius 4 is generous.
  Confirm this is intended (it favors the player).
