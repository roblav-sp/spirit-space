# Feature — Combat and Scoring

> **v0.2 status.** FR-002 (base weapon) is PRESERVED: the initial weapon stays
> a single projectile. Its stats become weapon data in
> `specs/features/weapons-powerups/spec.md` (FR-012), which owns the firing
> modes. FR-004.1 (+10 kill) is PRESERVED as the default basic-enemy reward;
> BR-002 ("+10 is the only score source") is **SUPERSEDED** by BR-010 and the
> ladder in `specs/features/scoring-highscores/spec.md` (FR-013).
> FR-004.2 (score rendering) is unchanged, and the miss scenario in
> `acceptance.feature` is **AC-012**, not AC-011.

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
- BR-002: exactly +10 per kill; no other score source. *(v0.2: SUPERSEDED by
  BR-010 — keep 10 as the basic-enemy default, add class/wave/combo rewards via
  FR-013.)*
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
