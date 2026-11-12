# ADR-0012 — Difficulty is orthogonal to game speed

**Status:** Proposed

**Context:** v0.2 lets the player pick a difficulty (Rookie/Pilot/Ace/Legend)
and a game speed (Slow 0.75× / Normal 1× / Fast 1.25×). Naively multiplying
the whole world by speed would also scale enemy fire rates and dive speeds,
making "Fast + Legend" unfair and "Slow + Rookie" trivial. Conversely, folding
speed into difficulty would prevent the two from being judged independently
and would make leaderboards ambiguous.

**Decision:** Two independent axes.
- **Difficulty** (`Difficulty` enum) sets **budgets**: enemy counts,
  archetype mix, projectile cadence, dive commitment, telegraph window, boss
  phase count. It never changes movement per simulated second.
- **Game speed** (`SpeedScale` ∈ {0.75, 1.0, 1.25}) is a single multiplier
  applied to **world-time accrual**: the accumulator feeds
  `dt * SpeedScale` into the fixed-step loop. All timers, movement and
  animations therefore scale together and stay consistent; nothing is scaled
  twice.

Because gameplay fairness depends on *simulated* time, the fairness checks
(minimum reaction time, projectile safe gaps) are evaluated in world time, and
a speed-adjusted reaction-time check (`telegraphSeconds / SpeedScale`) must
still meet the floor. Leaderboards record `(difficulty, speed)` with every
entry.

**Alternatives considered:**
- Speed multiplies only player/swarm movement — inconsistent timers, weird
  physics; rejected.
- Speed as a difficulty level — conflates two questions and makes "Ace at
  Slow" inexpressible; rejected.
- Variable step size to implement speed — breaks ADR-0008; rejected.

**Consequences:** A single multiplication point in `cmd/game` (accumulator
feed) keeps the core deterministic and speed-agnostic; tests can run the same
scenario at all three speeds and assert a *time-scaling* relation rather than
identical states (AC-136). Difficulty becomes a pure data table, easy to
balance without touching logic (AC-131).

**Reconsider when:** players ask for a "speed only" mode affecting spawn
density, or a fourth axis (e.g. assist mode) appears.
