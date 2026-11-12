# Feature — Enemy Archetypes and Formations

> Implements FR-010. Supersedes FR-003 (constant-interval straight drift).
> ADR-0009 (seeded director), ADR-0012 (difficulty budgets).

## Context
v0.1 enemies spawn on a timer and fall straight down. v0.2 needs a readable
formation game: enemies enter, hold formation, then commit to attacks that are
telegraphed, bounded and fair. This spec covers *what an enemy is* and *how
formations behave*; wave selection lives in `procedural-waves`.

## Actors
Player, Simulation, Renderer (sprites with geometric fallback).

## Preconditions
State `PLAYING`; a wave is active.

## Functional requirements

### Archetypes (FR-010.1)
| ID | Archetype | HP (hits) | Score | Behaviour | Projectile |
|---|---|---|---|---|---|
| `ARCH-SCOUT` | scout | 1 | 10 | holds formation; occasional dive | single, 180 px/s |
| `ARCH-INTERCEPTOR` | interceptor | 1 | 20 | flanks horizontally, fast dive | single, 220 px/s |
| `ARCH-HEAVY` | heavy | 3 | 50 | slow; absorbs hits, flashes | 2-way spread, 160 px/s |
| `ARCH-SNIPER` | sniper | 1 | 30 | stays high; aimed shots | aimed, 200 px/s |
| `ARCH-BOSS` | boss | see `bosses` | see `bosses` | phase-based | patterns |

- **FR-010.1** — Every enemy exposes `Archetype`, `HP`, `Score` and a behaviour
  strategy resolved from the table above via one data source.

### Formations (FR-010.2)
- **FR-010.2** — Templates: `row`, `V`, `diagonal`, `zigzag`, `dive`, `flank`,
  `bonus`. Each template is a deterministic function
  `(count, anchorX, anchorY) → []Slot` with distinct, in-field slots.
- **FR-010.3** — Enemies enter from above the top edge and interpolate to their
  slot within `entrySeconds` (default 1.2 s); during entry they cannot fire.
- **FR-010.4** — Formation motion after entry is a bounded oscillation
  (≤ 40 px horizontally, ≤ 12 px vertically) around the slot; no enemy ever
  leaves the world rect.
- **FR-010.5** — A dive is committed only after its telegraph: the enemy
  flashes/outlines for `telegraphSeconds` (per difficulty, ≥ 0.6 s world time),
  then follows a bounded path to below the bottom edge or back to its slot.
- **FR-010.6** — Firing is allowed only from formation (snapshot) or during a
  dive (single shot per dive, after 40% of the path). No fire during entry.
- **FR-010.7** — Enemy projectiles are entities with radius 3, speed and cap per
  archetype/difficulty; they despawn below the bottom edge.
- **FR-010.8** — The `bonus` template never fires and awards a clean-clear bonus
  (FR-013.3) if all its enemies die before leaving.
- **FR-010.9** — Concurrency caps come from the difficulty budget (FR-007.3).

## Business rules
BR-005 (one bullet, one enemy), BR-011 (budgets), BR-017 (determinism).

## Acceptance criteria
- **AC-140** — `Slots(count, …)` returns `count` distinct in-field positions for
  every template and every supported count.
- **AC-141** — The archetype table is read through a single accessor; a
  table-driven test asserts HP/score/projectile values match this spec.
- **AC-142** — A dive never begins earlier than `telegraphSeconds` after the
  telegraph starts, measured in world time.
- **AC-143** — Over a long seeded run, no enemy or enemy projectile position
  leaves the world rect (with a documented projectile below-edge exception).
- **AC-144** — The `bonus` template emits zero projectiles over its lifetime.
- **AC-145** — Live enemy projectiles never exceed the difficulty cap.
- **AC-146** — With a fixed seed and no input, the same formation/anchor
  sequence is produced on two independent runs.
- **AC-147** — A dive path never presents a wall with less than the required
  safe corridor (checked by the wave validator, AC-153).
- **AC-148** — Interceptor flanking is clamped: `X` stays in
  `[radius, Width−radius]` at every step.
- **AC-149** — A heavy requires exactly 3 hits; the first two do not remove it
  and visibly change its hit state.

## Edge cases
- An enemy destroyed during entry leaves its slot empty; remaining enemies keep
  their slots (no re-flow) in v0.2.
- A diving enemy that survives to the bottom exits and is removed without
  damaging the player or costing a life (D-2, decided 2026-11-12).
- Two enemies may share an oscillation phase; slot overlap is impossible but
  path crossing is allowed.
- Formation motion is paused with everything else in `PAUSED`.

## Error behavior
No I/O. Invalid template name → construction error surfaced in tests, never in
the shipped game (templates are compile-time constants).

## Non-functional requirements
NFR-001/NFR-002 (deterministic, step-based), NFR-005 (≤16 enemies × ≤24
projectiles must stay within frame budget on desktop).

## Security requirements
None beyond SEC-001/SEC-002.

## Observability requirements
None.

## Out of scope
Enemy pathfinding, enemy-enemy collisions, morphing archetypes, tractor beams,
captured-ship mechanics, 3D rotation.

## Open questions
- Should formation slots re-flow after a kill (denser formation) or stay fixed?
  v0.2 fixes slots; re-flow would change scoring predictability.
- Is a per-dive random path acceptable, or must paths be named templates for
  fairness review? Current: 3 named dive paths, chosen by the director.
