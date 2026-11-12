# Feature — Difficulty and Game Speed

> Implements FR-007 and BR-011. ADR-0012 (orthogonal axes), ADR-0008 (fixed
> step). Supersedes BR-004 (constant difficulty).

## Context
Players must be able to choose how hard and how fast the game feels. Difficulty
must change *threat density and behaviour*, never movement per simulated
second; speed must scale everything consistently or timers desynchronise.

## Actors
Player (menu choices), Simulation (budgets), Renderer (HUD label).

## Preconditions
A run exists; both values are fixed for the run's lifetime.

## Functional requirements
- **FR-007.1** — Difficulty is an enum `Rookie | Pilot | Ace | Legend`
  (default `Pilot`).
- **FR-007.2** — Game speed is a multiplier `SpeedScale ∈ {0.75, 1.0, 1.25}`
  (default `1.0`), representing Slow / Normal / Fast.
- **FR-007.3** — Difficulty sets **budgets only**, per the table below; it never
  multiplies entity speeds.
- **FR-007.4** — Speed scales **world-time accrual** at the accumulator feed
  (`dt × SpeedScale`) so movement, spawns, cooldowns, invulnerability and
  power-up timers scale together (ADR-0012).
- **FR-007.5** — Fairness floors are evaluated in **world time**: minimum dive
  telegraph ≥ 0.6 s, minimum boss telegraph ≥ 0.8 s, projectile safe corridor
  ≥ 48 px. At Fast these shrink in wall-clock terms but never below the floor
  in world time (AC-136).
- **FR-007.6** — Values cannot change mid-run; changing them requires Quit to
  Menu → Start.
- **FR-007.7** — Every run exposes `RunMetadata{Seed, RNGVersion, Difficulty,
  Speed}`; high-score entries are keyed by `(Difficulty, Speed)`.
- **FR-007.8** — The HUD shows difficulty and speed (e.g. `ACE · 1.25×`).
- **FR-007.9** — An out-of-range or unknown difficulty/speed value is rejected
  at construction and falls back to the default, never panics.

## Difficulty budget table (data, not logic)

| Budget | Rookie | Pilot | Ace | Legend |
|---|---|---|---|---|
| Max concurrent enemies | 6 | 9 | 12 | 16 |
| Enemy projectiles on screen | 6 | 10 | 16 | 24 |
| Waves per stage | 3 | 4 | 5 | 6 |
| Dive commitments per wave | 1 | 2 | 3 | 4 |
| Dive telegraph (world s) | 1.0 | 0.8 | 0.7 | 0.6 |
| Archetype mix | scouts, few heavies | + interceptors | + snipers | all + more heavies |
| Boss phases | 2 | 2 | 3 | 3 |
| Power-up drop chance | 12% | 10% | 8% | 7% |

Values are the M4 baseline; balancing in M9 may change numbers but not the
shape (monotonicity, AC-132).

## Business rules
BR-011 (independent axes), BR-012 (fixed step), BR-017 (metadata recorded).

## Acceptance criteria
- **AC-130** — Menu defaults are `Pilot` and `1.0`.
- **AC-131** — The budget table is a single data source: a table-driven test
  enumerates all four difficulties and reads every budget field through the
  same accessor (no duplicated constants).
- **AC-132** — For each budget field that grows with difficulty, Rookie ≤
  Pilot ≤ Ace ≤ Legend; for telegraph time, Legend ≤ Ace ≤ Pilot ≤ Rookie.
- **AC-133** — A run at 1.25× reaches the same state after 0.8 s as the same run
  at 1.0× after 1.0 s (modulo step quantisation), proving world-time scaling.
- **AC-134** — Power-up and invulnerability timers measured in world time are
  identical across speed settings for equal world time.
- **AC-135** — A single 0.25 s stall advances at most 4 fixed steps and drops
  the remainder (ADR-0008); a 1 s stall does not teleport entities.
- **AC-136** — At Fast × Legend the configured dive telegraph still satisfies
  the 0.6 s world-time floor.
- **AC-137** — High-score entries store difficulty and speed and are never
  merged across settings.
- **AC-138** — The HUD renders the current difficulty and speed label.
- **AC-139** — An invalid difficulty or speed passed to construction yields the
  default pair and does not panic.

## Edge cases
- Speed is applied once, at the accumulator feed; applying it to `Update` calls
  individually would double-scale. Guarded by AC-133.
- Pause must not consume accumulator remainder (AC-105).
- 0.75× with `dt` clamping produces fewer steps per frame; max catch-up still
  applies.

## Error behavior
Invalid values fall back to defaults (AC-139). No I/O, no failure paths.

## Non-functional requirements
NFR-002 (frame-rate equivalence preserved), NFR-005 (measured at all speeds).

## Security requirements
None beyond SEC-001/SEC-002.

## Observability requirements
None.

## Out of scope
Custom/dynamic difficulty, adaptive difficulty, assist modes, per-enemy speed
scaling, mid-run changes.

## Open questions
- Should Legend disable the power-up pity timer (BR-016) as an extra pressure
  lever? Current: no, pity applies to all difficulties.
- Is 1.25× too fast to pass a fair-reaction check at 60 Hz for dive telegraphs?
  M9 measures; floor is in world time, not wall time.
