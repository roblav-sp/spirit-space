# Feature — Boss Encounters

> Implements FR-015 and BR-014. Builds on `formation-ai` (archetype table) and
> `procedural-waves` (stage structure). Telegraphed, fair, multi-phase.

## Context
Every 5th stage needs a climax that rewards pattern reading rather than raw
firepower. Bosses are the only entity allowed to occupy the stage alone, and the
only one whose defeat ends a stage immediately.

## Actors
Player, Simulation, Renderer (boss sprite, HP bar, phase cue).

## Preconditions
Stage number divisible by 5; previous stage's waves complete.

## Functional requirements
- **FR-015.1** — A boss appears on stages **5, 10, 15, 20**; no normal waves
  spawn during a boss encounter.
- **FR-015.2** — Boss hit points by difficulty: Rookie 60, Pilot 80, Ace 100,
  Legend 120. HP is a budget, not a speed (ADR-0012).
- **FR-015.3** — Phases: 2 (Rookie/Pilot) or 3 (Ace/Legend). Each phase has a
  distinct attack pattern and a **transition telegraph of ≥0.8 s world time**
  during which the boss is invulnerable but not attacking.
- **FR-015.4** — Attack patterns: `sweep` (horizontal fan), `aimed-burst`
  (3 shots toward the player's current position with a fixed lead delay), and
  `spiral` (rotating stream). Every pattern must leave a ≥48 px safe corridor
  and never exceed the Legend projectile cap (24).
- **FR-015.5** — Boss movement is confined to the upper third of the field and
  never exits the world rect.
- **FR-015.6** — Damage feedback: hit flash and an HP bar; a phase change
  resets the bar to the new phase's maximum.
- **FR-015.7** — On defeat: award `500 × stage` (FR-013.2), one guaranteed
  random pickup (open question below), plus the `100 × stage` wave bonus, then
  stage clear.
- **FR-015.8** — Boss body contact damages the player once per contact window
  (0.5 s), following the lives rules (FR-008), not instant death.
- **FR-015.9** — Losing all lives during the boss fight ends the run with no
  boss reward.

## Business rules
BR-005 (one bullet, one enemy), BR-013 (invulnerability), BR-014 (every 5th
stage), BR-012 (step-based).

## Acceptance criteria
- **AC-190** — Bosses spawn on stages 5, 10, 15 and 20, and on no other stage.
- **AC-191** — While a boss is alive, no non-boss enemies spawn.
- **AC-192** — A phase transition always telegraphs for ≥0.8 s before the next
  pattern starts, and the boss takes no damage during it.
- **AC-193** — Boss HP matches the difficulty table; total hits to kill is
  exactly HP (with the base weapon, no power-ups).
- **AC-194** — Defeat awards `500 × stage` exactly once plus one pickup and one
  wave bonus; killing it after `GAME_OVER` awards nothing.
- **AC-195** — Defeating the boss completes the stage and advances the stage
  counter with no residual enemies or projectiles from the fight.
- **AC-196** — Across 200 seeded boss fights per difficulty, every pattern frame
  satisfies the ≥48 px corridor requirement (validator test).
- **AC-197** — Body contact costs exactly 1 life per 0.5 s contact window, never
  more, even while overlapping continuously.
- **AC-198** — Boss position stays within its movement band and inside the world
  rect at every step.
- **AC-199** — A run reduced to 0 lives during the boss sets `GAME_OVER` and
  awards no reward.

## Edge cases
- Boss defeated on the same step the player loses their last life → `GAME_OVER`
  wins; no reward (FR-015.9).
- Player dies during a phase transition → returns into the same phase, boss
  invulnerability timer keeps running.
- The 20th-stage boss defeat triggers `VICTORY` (FR-011.9) instead of another
  stage.
- Multiple bullets hitting on the same step are all applied (no hit-per-step
  cap) but HP never goes below 0.

## Error behavior
No I/O. Invalid phase count for a difficulty is a data error caught by the
table test (AC-193).

## Non-functional requirements
NFR-001/NFR-002 (deterministic pattern stepping), NFR-005 (max 24 projectiles +
boss must hold 60 FPS), NFR-007 (patterns must not rely on colour alone).

## Security requirements
None beyond SEC-001/SEC-002.

## Observability requirements
None.

## Out of scope
Bosses with weak points, multi-part bosses, retreating bosses, boss-specific
music (handled generically by FR-016.4), captured-ship mechanics.

## Open questions
- Should the guaranteed drop be player-chosen (a rarity reward) or random?
  Default: random, to keep input handling unchanged.
- Is 500 × stage too generous at stage 20 with multiplier ×5 (capped at 5000)?
  M9 balances.
- Should phase patterns be seeded per run? Default: yes, via the wave director
  (AC-196 uses several seeds).
