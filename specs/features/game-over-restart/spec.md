# Feature — Game Over and Restart

> **v0.2 status.** The terminal-state behaviour (freeze + GAME OVER banner +
> R restart) is PRESERVED. The *lethal* rules are **SUPERSEDED** by FR-008
> (`specs/features/lives-respawn/spec.md`): contact costs a life, **bottom
> escape costs nothing** (D-2, decided 2026-11-12), and the run ends at 0 lives.
>
> **ID correction (audit §4):** the bottom-edge rule below is `FR-004.4`
> (`FR-004.2` is score rendering, owned by `combat-scoring`), and the restart
> action is `FR-005.3` (`FR-005.1` is the banner). No behaviour changed.

## Context
Runs are single-life (BR-001). Two lethal events end the game: an enemy
reaching the bottom edge, or an enemy colliding with the player. After game
over, R restarts. Implements FR-004 (lethal part) and FR-005.

## Actors
Player, Simulation, Renderer (draws the GAME OVER banner).

## Preconditions
A run in progress (for the lethal events) or `GameOver == true` (for restart).

## Functional requirements
- **FR-004.4** — An enemy whose bottom edge reaches the world bottom
  (`Y + Radius ≥ Height`) ends the game. *(v0.2: **harmless** — the enemy is
  removed and nothing is lost; D-2, FR-008.2.)*
- **FR-004.3** — An enemy overlapping the player's circle ends the game.
  *(v0.2: costs one life, FR-008.2.)*
- **FR-005.1** — When `GameOver` is true the simulation freezes (`Update` is
  a no-op; BC-2) and the renderer shows a "GAME OVER — press R to restart"
  banner instead of the score.
- **FR-005.3** — Pressing `R` (code `KeyR`) while `GameOver` restarts the
  game: score 0, empty bullet/enemy slices, player recentered, `GameOver`
  false (BC-7).
- **FR-005.2** — R has no effect while the game is running.

## Business rules
- BR-001: one life per run; the first lethal event ends it. *(v0.2:
  SUPERSEDED by BR-009 — three lives, ≤1 lost per damage event.)*
- BR-007: at most one lethal event is processed per update (the check returns
  immediately); no score is awarded by a killing enemy.

## Acceptance criteria
- **AC-013** — Given an enemy at the bottom edge, on the next update
  `GameOver` is true.
- **AC-014** — Given an enemy overlapping the player, on the next update
  `GameOver` is true.
- **AC-015** — Given `GameOver`, advancing the simulation changes nothing
  (score, bullets, enemies).
- **AC-016** — Given `GameOver` with score 55, when `Restart()` is called,
  then score is 0, no enemies/bullets exist, the player is centered, and
  `GameOver` is false.
- **AC-017** — The renderer shows the game-over banner only when `GameOver`
  is true.

## Edge cases
- An enemy simultaneously touching the player and the bottom edge → game over
  either way; identical result.
- Restart during fire-held input: fresh run starts with cooldown 0, so a
  bullet may fire immediately — accepted (matches BC-4).

## Error behavior
- No failure modes; terminal transitions are idempotent.

## Non-functional requirements
- NFR-001 applies (restart produces the exact `New()` state).

## Security requirements
- None beyond SEC-001/SEC-002.

## Observability requirements
- None.

## Out of scope
- Lives, continues, pause menu, high-score persistence.

## Open questions
- None currently.
