# Spirit Space — Product Specification

> Source of truth for *what* the product does. Architecture lives in
> `specs/architecture/`; per-feature detail in `specs/features/`.

## 1. Purpose

Spirit Space is a single-player arcade space shooter that runs entirely in the
browser as a WebAssembly build of a Go program. The player's goal is to shoot
as many descending enemies as possible before one of them ends the run.

## 2. Actors

| Actor | Description |
|---|---|
| Player | The only actor. Interacts via keyboard; observes via canvas. |
| Browser runtime | Hosts the WASM instance, canvas, and keyboard events. |
| (No external systems, no server, no third-party services.) | |

## 3. Capabilities and requirements

### FR-001 — Ship movement
The player moves the ship in 4 directions (arrows or WASD) at a constant speed,
clamped to the 800×600 play field. → *feature: `player-control`*

### FR-002 — Shooting
The player fires bullets straight up with the Space key, limited by a fire
cooldown; bullets travel up and despawn off-screen. → *feature: `combat-scoring`*

### FR-003 — Enemy spawning and movement
Enemies spawn at random X positions along the top edge on a fixed interval and
drift straight down at constant speed. → *feature: `enemy-spawning`*

### FR-004 — Collisions and scoring
A bullet hitting an enemy destroys both and awards +10 points; an enemy
reaching the bottom edge or touching the player ends the game. Score is
displayed on the canvas. → *feature: `combat-scoring`*

### FR-005 — Game over and restart
When the game ends, a "GAME OVER" state is shown; pressing R restarts with a
fresh state. → *feature: `game-over-restart`*

## 4. Business rules

- **BR-001**: One life per run; no continues. A run ends on the first lethal
  event.
- **BR-002**: Exactly +10 points per destroyed enemy; no other scoring source.
- **BR-003**: The fire cooldown is the only constraint on firing (no ammo).
- **BR-004**: Difficulty is constant in v0.1 (spawn delay and enemy speed do
  not ramp). Future ramping is explicitly out of scope.

## 5. Non-functional requirements

- **NFR-001**: Deterministic simulation — same inputs ⇒ same outcome
  (seeded RNG only; Constitution Law 2).
- **NFR-002**: Frame-rate independence — identical behavior at 30/60/144 FPS
  (Constitution Law 4).
- **NFR-003**: All game logic in Go, stdlib only, no external dependencies
  (Constitution Laws 1, 6).
- **NFR-004**: Runs fully offline in a modern browser with WASM support; no
  network calls at runtime.

## 6. Security & privacy

- **SEC-001**: The game collects, stores, and transmits no user data.
- **SEC-002**: No network access from the WASM module; the page loads only
  `wasm_exec.js` and `main.wasm` from its own origin.

## 7. Known gaps / open questions

- No high-score persistence (deliberate, per gameplay spec v0.1).
- No sound, no animations beyond positions, no mobile/touch controls.
- **Open question**: should difficulty ramping (spawn rate/speed over time) be
  specified for v0.2? (gameplay.md hints "Future".)
- **Open question**: is enemy-player proximity a game-over condition by design
  or should contact push the enemy/destroy the player differently? Current
  code and docs agree: game over.

## 8. Assumptions

> **Assumption**: the enemy spawn X range is `enemyRadius … Width-enemyRadius`
> (spawn fully on-screen). The original spec only said "random X along the top
> edge"; the implementation choice is recorded here.

> **Assumption**: "an enemy reaches the player" in the original docs means
> circle-circle overlap between enemy and player radii (collision), not merely
> crossing the player's row.
