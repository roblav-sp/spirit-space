# Spirit Space — Product Specification

> Source of truth for *what* the product does. Architecture lives in
> `specs/architecture/`; per-feature detail in `specs/features/`.
>
> **v0.2 baseline (M1).** This document now states the target product
> **Spirit Space — fixed-screen formation arcade shooter**. Current behaviour
> and planned behaviour are separated explicitly: every requirement below
> carries a status. Nothing marked `PLANNED` exists in code yet.

## 0. Status legend

| Status | Meaning |
|---|---|
| **IMPLEMENTED** | Exists in code at HEAD `3fae24f`, covered by the listed tests. |
| **IMPLEMENTED (partial)** | Present but being redefined by v0.2. |
| **PLANNED** | Specified here, not implemented. Traceability marks it `TODO`. |
| **SUPERSEDED** | Old rule kept for history; no longer governs behaviour. |

## 1. Purpose

A single-player arcade space shooter that runs entirely in the browser as a
WebAssembly build of a Go program. The player pilots a ship inside a fixed
800×600 field, breaks enemy formations, collects weapons, survives escalating
stages, and chases a place on a local high-score table.

Non-goals: multiplayer, accounts, servers, scrolling worlds, external engines.

## 2. Actors

| Actor | Description |
|---|---|
| Player | The only human actor. Keyboard in, canvas out. |
| Browser runtime | Hosts the WASM instance, canvas, keyboard events, optional audio and local storage. |
| Developer | Imports third-party assets at build time (never at runtime). |

## 3. Capabilities and requirements

### v0.1 capabilities (existing)

**FR-001 — Ship movement** — IMPLEMENTED
The ship moves in 4 directions (arrows or WASD) at a constant speed, clamped to
the field. → `specs/features/player-control/`

**FR-002 — Shooting** — IMPLEMENTED
Hold Space to fire a single projectile upward, limited by a cooldown; bullets
despawn above the field. → `specs/features/combat-scoring/`

**FR-003 — Enemy spawning and movement** — SUPERSEDED (v0.1 only)
Random X spawn on a fixed interval, straight downward drift. Replaced by
FR-010/FR-011; kept for historical traceability. → `specs/features/enemy-spawning/`

**FR-004 — Collisions, damage and score** — IMPLEMENTED (partial)
Bullet-enemy overlap destroys both and awards +10 (FR-004.1) and renders the
score (FR-004.2). The v0.1 lethal rules end the run: bottom escape (FR-004.4)
and player contact (FR-004.3). v0.2 changes this asymmetrically — contact costs
a life (FR-008) while **bottom escape becomes harmless** (D-2, decided
2026-11-12): the enemy is removed and nothing is lost.
→ `combat-scoring/`, `game-over-restart/`

**FR-005 — Game over and restart** — IMPLEMENTED
`GAME_OVER` shows a banner; R restarts with a fresh state. v0.2 keeps R in
`GAME_OVER` only. → `specs/features/game-over-restart/`

### v0.2 capabilities (planned)

**FR-006 — App state machine and main menu** — PLANNED
BOOT → MAIN_MENU before gameplay. The menu selects difficulty
(Rookie/Pilot/Ace/Legend) and game speed (Slow 0.75× / Normal 1× / Fast
1.25×), and offers Start, Controls, Sound, High Scores, Back/Return. Escape or
P pauses during play; P/Escape from pause resumes; the pause menu offers
Resume, Restart, Sound, Quit to Menu. All screens are Go-drawn on the existing
canvas. → `specs/features/main-menu/`

**FR-007 — Difficulty and game-speed model** — PLANNED
Difficulty sets **budgets** (enemy count, archetype mix, projectile cadence,
telegraph windows, boss phases); game speed scales **world time only**. The two
axes are independent and both recorded in high-score entries. → `difficulty-speed/`

**FR-008 — Three lives, damage, and respawn** — PLANNED
A run starts with exactly 3 lives. Damage comes only from enemy bodies and
enemy projectiles; one damage event costs at most 1 life, neutralises the
colliding hazard, passes through `PLAYER_DYING` → `RESPAWNING`, then grants
brief invulnerability. Escaping the bottom edge is harmless (D-2). 0 lives →
`GAME_OVER`. No simultaneous double penalty. → `lives-respawn/`

**FR-009 — Pause** — PLANNED
Pause freezes the whole simulation, including timers, invulnerability and
audio events; the freeze is exact (same state in, same state out). → `main-menu/`

**FR-010 — Enemy archetypes and formations** — PLANNED
Archetypes `scout`, `interceptor`, `heavy`, `sniper`, `boss`; formations row, V,
diagonal, zigzag, dive, flanking, bonus. Dives are telegraphed. → `formation-ai/`

**FR-011 — Seeded procedural wave director** — PLANNED
Bounded stages of templated waves chosen by a seeded RNG recorded in run
metadata; spawn safety, projectile safe gaps, concurrency caps and minimum
reaction time are enforced. → `procedural-waves/`

**FR-012 — Weapons and power-ups** — PLANNED
Single projectile at start; `rapid`, `spread`, `shield`, `beam` power-ups with
specified duration, stacking caps, drop probability and HUD indicators. → `weapons-powerups/`

**FR-013 — Extended scoring** — PLANNED
+10 remains the basic-enemy default; class scores, cleared-wave bonus, combo
multiplier and boss rewards are added. → `scoring-highscores/`

**FR-014 — High scores and settings** — PLANNED (conditional)
Local ranking of the best runs per `(difficulty, speed)` and remembered
settings. Persistence requires the ratified amendment
(`docs/constitution-amendment-001.md`); **memory-only** is the baseline and
must work without it. → `scoring-highscores/`

**FR-015 — Boss encounters** — PLANNED
A boss every 5th stage with telegraphed, multi-phase patterns and a distinct
reward. → `bosses/`

**FR-016 — Audio** — PLANNED
Local music and SFX with master/music/SFX volume and mute, unlocked by the
first user gesture, degrading silently when audio is unavailable. → `audio-assets/`

**FR-017 — Sprite rendering with geometric fallback** — PLANNED
Sprites replace primitives incrementally, preserving aspect ratio and
orientation; if an asset is missing or undecodable the geometric shape renders
instead. → `audio-assets/` (asset integration), `architecture/components.md`

## 4. Business rules

| ID | Rule | Status |
|---|---|---|
| BR-001 | One life per run; no continues; first lethal event ends the run. | **SUPERSEDED** by BR-009 |
| BR-002 | Exactly +10 per destroyed enemy; no other scoring source. | **SUPERSEDED** by BR-010 (the +10 default is preserved) |
| BR-003 | Fire cooldown is the only firing constraint; no ammo. | PRESERVED |
| BR-004 | Difficulty is constant in v0.1; no ramping. | **SUPERSEDED** by BR-011 |
| BR-005 | One bullet destroys at most one enemy (no piercing) unless a weapon explicitly says otherwise. | PRESERVED |
| BR-006 | Randomness comes only from the game's own seeded RNG instance. | PRESERVED |
| BR-007 | At most one lethal/damage event is processed per update; no double penalty. | PRESERVED, extended by BR-013 |
| BR-008 | Movement speed is constant; no acceleration or inertia. | PRESERVED (renumbered from the colliding `BR-005`; see audit §4) |
| BR-009 | A run starts with exactly 3 lives; one damage event costs at most 1 life. | PLANNED |
| BR-010 | Basic enemy kill = 10 points; all other rewards come from the scoring table. | PLANNED |
| BR-011 | Difficulty and game speed are independent axes. | PLANNED |
| BR-012 | The simulation advances in fixed 1/60 s steps; render frame rate never changes outcomes. | PLANNED |
| BR-013 | Respawn grants a fixed invulnerability window; overlapping hazards in that window deal no damage. | PLANNED |
| BR-014 | A boss appears every 5th stage. | PLANNED |
| BR-015 | Persistence is limited to local high scores and settings; no analytics, tracking, login, telemetry, cookies or server storage. | PLANNED (needs amendment) |
| BR-016 | Power-ups expire, have stacking caps, and never remove the base weapon. | PLANNED |
| BR-017 | Every run records `(seed, RNG version, difficulty, speed)`; the same inputs reproduce the same run. | PLANNED |
| BR-018 | Third-party assets are local, provenance-tracked, license-reviewed and always optional at runtime. | PLANNED |

## 5. Non-functional requirements

- **NFR-001** — Deterministic simulation: same inputs ⇒ same outcome; seeded
  RNG only (Law 2). **PRESERVED, strengthened** by BR-012.
- **NFR-002** — Frame-rate independence: identical state after equal simulated
  time at 30/60/144 FPS (Law 4). **PRESERVED.**
- **NFR-003** — All game logic in Go, stdlib only, no `require` block (Laws 1,
  6). **PRESERVED.**
- **NFR-004** — Fully offline at runtime; no CDN, no network calls. **PRESERVED.**
- **NFR-005** — Target 60 FPS on ordinary desktop hardware; measured, not
  promised (M9). **PLANNED.**
- **NFR-006** — Asset budget: shipped sprites/audio stay within the size table
  in `specs/features/audio-assets/spec.md`; startup must not regress past a
  measurable budget (M9). **PLANNED.**
- **NFR-007** — Readability and accessibility of the canvas UI: contrast ratio
  ≥ 4.5:1 for text, no colour-only telegraphs, all menu actions reachable by
  keyboard, pause available at any time. **PLANNED.**
- **NFR-008** — All simulation tests run with plain `go test` (no browser);
  browser checks stay in the `browser-verify` skill. **PLANNED/PARTIAL.**

## 6. Security and privacy

- **SEC-001** — The game collects and transmits no user data. *Amended by
  Amendment 001 (RATIFIED 2026-11-12) to permit local-only score and settings
  storage on the page's own origin.*
- **SEC-002** — No network access from the WASM module; the page loads only
  same-origin files. **PRESERVED.**
- **SEC-003** — Any persisted data is versioned, bounded (≤64 KiB), untrusted
  on read, and never transmitted; corrupted data falls back to defaults.
  **PLANNED (needs amendment).**
- **SEC-004** — Assets are imported at development time, recorded with SHA-256
  provenance, and reviewed for license before redistribution. **PLANNED.**

## 7. Milestones (delivery order)

| Milestone | Content | Requirements |
|---|---|---|
| M1 | Audit, research, amendment proposal, specs, ADRs, traceability, asset importer | — (docs only) |
| M2 | State machine + menu | FR-006, FR-009 |
| M3 | Lives, respawn, hit immunity, pause integration | FR-008 |
| M4 | Difficulty and speed | FR-007 |
| M5 | Archetypes, formations, wave director | FR-010, FR-011 |
| M6 | Weapons/power-ups and scoring | FR-012, FR-013 |
| M7 | Bosses and local high scores | FR-015, FR-014 |
| M8 | Asset and audio integration | FR-016, FR-017 |
| M9 | Balancing, browser regression, accessibility, polish | NFR-005…NFR-007 |

## 8. Known gaps

- No mobile/touch controls (out of scope; keyboard contract only).
- No screen-reader support for canvas UI; stated as an explicit limitation
  (NFR-007 covers contrast, keyboard reachability and pause only).
- No CI pipeline; gates are manual.
- No `LICENSE`/`CREDITS` file yet (owner decision D-5).
- Rendering frame-rate independence is not required (simulation only).

## 9. Assumptions

> **Assumption**: spawn X stays inside `[radius, Width-radius]` so enemies are
> never born half off-screen (carried over from v0.1).

> **Assumption**: "enemy reaches the player" means circle overlap, not merely
> crossing the player's row (carried over).

> **Assumption**: keyboard-only input remains the contract for v0.2; mouse
> menus are out of scope unless a later spec says otherwise.

> **Assumption**: audio is optional at runtime; a silent game is fully
> playable and is the state of the world until M8.
