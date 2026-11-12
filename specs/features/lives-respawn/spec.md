# Feature — Lives, Damage, and Respawn

> Implements FR-008; supersedes the v0.1 lethal rules (FR-004.3/FR-004.4) and
> BR-001. **D-2 resolved 2026-11-12: escaping the bottom edge is harmless.**

## Context
v0.1 ends the run on the first contact or escape. v0.2 gives the player three
lives so a single mistake is recoverable, while keeping the run finite and the
failure state readable.

## Actors
Player, Simulation, Renderer (life pips, death/respawn feedback).

## Preconditions
State `PLAYING`; `Lives > 0`.

## Functional requirements
- **FR-008.1** — A run starts with exactly **3** lives. The HUD shows remaining
  lives as pips plus a numeric fallback.
- **FR-008.2** — Damage sources are exactly two: (a) an enemy body overlapping
  the player circle, (b) an enemy projectile overlapping the player circle.
  An enemy that crosses the world bottom is **removed and costs nothing** — no
  life, no score, no state transition (D-2, decided 2026-11-12). The fixed-screen
  threat mechanic is therefore *contact only*, and surviving by dodging costs
  the player nothing but the missed score.
- **FR-008.3** — One damage event costs **at most one life**. Within a single
  update step, at most one damage source is applied; the applied hazard is
  neutralised (the colliding enemy or projectile is removed) so it cannot
  damage again on the next step.
- **FR-008.4** — Losing a life transitions `PLAYING → PLAYER_DYING` for
  **0.9 s** (world time), then `RESPAWNING` for **1.5 s** of invulnerability,
  then `PLAYING`.
- **FR-008.5** — On respawn the ship returns to its start position
  `(Width/2, Height−80)`; enemy and projectile positions are *not* cleared.
- **FR-008.6** — During `PLAYER_DYING` and `RESPAWNING` the player cannot move
  or fire; enemies, projectiles and timers keep advancing.
- **FR-008.7** — While invulnerable, the player renders with a visible blink
  and takes no damage from any source; hazards pass through (they are not
  neutralised by an invulnerable player).
- **FR-008.8** — Reaching 0 lives transitions to `GAME_OVER`, which freezes the
  simulation (BC-2) and shows lives, score, stage and a restart hint.
- **FR-008.9** — R in `GAME_OVER` starts a fresh run (3 lives, score 0) with the
  run's difficulty/speed preserved.
- **FR-008.10** — Contact kills award **no** score (BR-010 covers bullet kills
  only); surviving hazard removal never increases score.

## Business rules
- BR-009 (three lives, ≤1 per event), BR-007/BR-013 (no double penalty,
  invulnerability window), BR-005 unchanged.

## Acceptance criteria
- **AC-120** — `New()` reports `Lives == 3`.
- **AC-121** — An enemy touching the player costs exactly 1 life, is removed,
  and awards no score.
- **AC-122** — With invulnerability active, an overlapping enemy and an
  overlapping projectile cost 0 lives.
- **AC-123** — During `PLAYER_DYING`/`RESPAWNING`, input does not move the ship
  but enemy positions still advance.
- **AC-124** — The third damage event sets `GAME_OVER`; `Lives` never goes
  negative.
- **AC-125** — An enemy crossing the bottom edge is removed, leaves `Lives`,
  `Lives` timers and `Score` unchanged, and triggers no life-loss state
  (no `PLAYER_DYING`).
- **AC-126** — An enemy that both touches the player and crosses the bottom in
  the same step costs exactly 1 life (the touch), never 2, and no second enemy
  escape may add a penalty.
- **AC-127** — R in `GAME_OVER` restores 3 lives and score 0, keeping
  difficulty/speed.
- **AC-128** — Invulnerability ends exactly 1.5 s after respawn (step-quantised),
  and the blink stops on the same step.
- **AC-129** — Pausing during `PLAYER_DYING` freezes the 0.9 s timer.

## Edge cases
- Two enemies hit the player in the same step → 1 life, one hazard neutralised,
  the other survives (it will hit during invulnerability and do nothing).
- Boss body contact (M7) follows the same rules as an enemy body.
- Damage during `PLAYER_DYING` cannot occur (state guard), even if a hazard
  overlaps the respawn point.

## Error behavior
No failure modes; transitions are idempotent and guarded by state.

## Non-functional requirements
NFR-001/NFR-002 (timers quantised to fixed steps, ADR-0008).

## Security requirements
None beyond SEC-001/SEC-002.

## Observability requirements
None.

## Out of scope
Continues, extra-life pickups, shields as extra lives (a shield absorbs a hit
but is a power-up, not a life), checkpoints.

## Resolved questions
- **D-2 (closed 2026-11-12):** bottom escape does **not** cost a life. The
  enemy is removed, no score is awarded, and time-to-flight is the only cost.
  Reopening this decision changes FR-008.2 and AC-125 only.

## Open questions
- Should invulnerability blink have a minimum on-time for photosensitivity
  (NFR-007)? Current: 6 Hz blink, below the 3-flashes-per-second guideline at
  1.5 s duration → requires a check in M9.
