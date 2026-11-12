# Feature — Procedural Wave Director

> Implements FR-011 and BR-017. ADR-0009 (seeded director + run metadata),
> ADR-0008 (fixed step). Supersedes the v0.1 spawn timer (FR-003.1/FR-003.3).

## Context
Waves must vary between runs yet stay reproducible, valid and fair. The director
chooses *from validated templates*; it never invents geometry at runtime.

## Actors
Player, Simulation (director), Renderer (stage/wave HUD).

## Preconditions
State `PLAYING`; `RunMetadata` exists and is immutable.

## Functional requirements
- **FR-011.1** — A **stage** is a bounded sequence of waves: stages 1–4 have
  `wavesPerStage` waves from the difficulty budget (3–6), stage 5 is a boss
  stage (M7), and the pattern repeats every 5 stages up to stage 20.
- **FR-011.2** — Each wave is chosen by the director from a fixed catalogue of
  `(template, archetypeMix, count, entryAnchor, divePlan)` entries, using the
  run's seeded RNG. Selection order is fixed (no draw depends on player input
  or frame timing).
- **FR-011.3** — **Spawn safety**: no enemy slot may be within 120 px
  horizontally of the player's position at wave start, and no slot may be below
  `y = 200`.
- **FR-011.4** — **Projectile safe gap**: the validator rejects any wave whose
  projected projectile paths would leave no corridor of ≥ 48 px within
  `1.0 s` of the first enemy shot.
- **FR-011.5** — **Concurrency caps** from the difficulty budget apply to live
  enemies and enemy projectiles.
- **FR-011.6** — Wave completion: a wave ends when all its enemies are destroyed
  or have exited; the next wave begins after a 0.8 s inter-wave pause.
- **FR-011.7** — `RunMetadata{Seed, RNGVersion, Difficulty, Speed}` is created
  at run start, exposed read-only, and recorded in high-score entries.
- **FR-011.8** — RNG draws are versioned: `RNGVersion = 1` for v0.2. Changing
  the draw sequence requires incrementing the version (ADR-0009).
- **FR-011.9** — After stage 20 the run ends in `VICTORY` (new state) with the
  final score eligible for the high-score table; no infinite looping.
- **FR-011.10** — Every generated wave must pass the validator before it is
  accepted; a rejected candidate consumes a draw and the next candidate is
  tried, with a hard cap (10 attempts) then a guaranteed-safe fallback wave.

## Business rules
BR-017 (reproducible run), BR-011 (budgets), BR-014 (boss every 5th stage).

## Acceptance criteria
- **AC-150** — Two runs with the same `(seed, RNGVersion, difficulty, speed)` and
  the same input sequence produce identical wave sequences, spawn positions and
  timings.
- **AC-151** — Across five distinct seeds, at least two produce different first
  waves (variety exists, determinism is not accidental).
- **AC-152** — For 500 generated waves per difficulty, no slot violates the
  120 px player clearance at wave start.
- **AC-153** — For the same sample, every accepted wave has a ≥ 48 px corridor
  at the first shot time (validator test, not a play test).
- **AC-154** — Live enemies and projectiles never exceed the budget caps.
- **AC-155** — Waves per non-boss stage equal `wavesPerStage` for the difficulty.
- **AC-156** — `RunMetadata` cannot be mutated after construction (API returns
  values; mutation attempts do not affect the run).
- **AC-157** — Stepping the same run at 1/60 and 1/30 (whole steps) yields
  identical director state; no draw depends on `dt`.
- **AC-158** — Reaching stage 20 completion yields `VICTORY`; no enemies spawn
  afterwards.
- **AC-159** — The RNG version is present in metadata and asserted by the
  determinism test; a version change fails a dedicated compatibility test.

## Edge cases
- A wave whose enemies all exit without dying still counts as complete.
- If the player dies mid-wave, the wave continues behind the death/respawn
  states; no re-roll.
- `VICTORY` freezes the simulation like `GAME_OVER` and offers the same menu
  actions (Enter → menu, R → new run).
- Validator fallback wave is always accepted regardless of seed.

## Error behavior
No I/O. Exhausted candidate attempts fall back deterministically; the game never
stalls waiting for a valid wave.

## Non-functional requirements
NFR-001 (determinism), NFR-002 (step-based), NFR-005 (validation cost is
one-off per wave, not per frame).

## Security requirements
None beyond SEC-001/SEC-002.

## Observability requirements
None at runtime. Tests expose a debug structure of generated waves for
assertions (test-only, not shipped).

## Out of scope
Endless mode, score attacks, daily seeds, replays, sharing seeds across
players (no network).

## Open questions
- Should the seed be visible in the HUD for reproducible bug reports? Proposed:
  yes, on the pause screen only.
- Is 20 stages the right bound, or should `VICTORY` be reachable earlier at
  Legend? Current: same bound for all difficulties.
