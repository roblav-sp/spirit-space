# Feature — Enemy Spawning and Movement

## Context
Enemies are the game's threat and its scoring source. In v0.1 difficulty is
constant (BR-004). Implements FR-003.

## Actors
Player (indirectly, as target), Simulation, Renderer.

## Preconditions
Game not over. Spawner runs inside `Update`.

## Functional requirements
- **FR-003.1** — A new enemy spawns every `spawnDelay` (1.2 s) of simulated
  time.
- **FR-003.2** — Spawn X is random within `[enemyRadius, Width−enemyRadius]`
  (so enemies spawn fully on-screen); Y is above the top edge (−radius).
- **FR-003.3** — Enemies drift straight down at `enemySpeed` (120 px/s); no
  horizontal motion, no acceleration (BR-004).

## Business rules
- BR-004: spawn delay and enemy speed are constant in v0.1.
- BR-006: the RNG is the game's own seeded instance (determinism, NFR-001).

## Acceptance criteria
- **AC-005** — Given a fresh game, when the simulation advances 1.2 s, then
  exactly one enemy exists.
- **AC-006** — Given a fresh game, when it advances 0.6 s, then no enemy
  exists (first spawn at t = 1.2 s, not t = 0).
- **AC-007** — Every spawned enemy's X is within
  `[enemyRadius, Width−enemyRadius]` across a full run.
- **AC-008** — Given an enemy at Y₀, after dt seconds its Y increased by
  exactly 120·dt.

## Edge cases
- Very long dt crossing a spawn boundary spawns at most one enemy per `Update`
  (timer resets, no catch-up loop).
- Enemies may overlap each other; no enemy-enemy collision exists.

## Error behavior
- Spawning cannot fail; slice append only.

## Non-functional requirements
- NFR-001: same seed ⇒ same spawn sequence.

## Security requirements
- None beyond SEC-002.

## Observability requirements
- None.

## Out of scope
- Difficulty ramping, enemy types, enemy shooting, spawn patterns.

## Open questions
- First spawn delay: currently 1.2 s after start (AC-006). Should the first
  enemy appear sooner to reduce dead time? (product decision)
