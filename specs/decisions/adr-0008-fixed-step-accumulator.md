# ADR-0008 — Fixed-timestep simulation with an accumulator

**Status:** Proposed

**Context:** Law 4 requires identical behaviour at 30/60/144 FPS, and v0.2 adds
timers (spawn waves, power-up expiry, invulnerability, boss phases) whose
fairness depends on stable step sizes. Feeding variable render `dt` into the
core makes timers drift with frame rate and makes seeded wave reproduction
fragile (BR-017, ADR-0009). The current implementation integrates whatever `dt`
arrives, clamped to 0.1 s in `cmd/game`.

**Decision:** The simulation advances in **fixed steps of 1/60 s**. `cmd/game`
keeps an accumulator: it adds clamped frame time (≤0.25 s) and calls
`UpdateStepped`/`Update` repeatedly while the remainder is ≥ step; leftover
time carries to the next frame. A max catch-up (≤4 steps per frame) prevents
spiral-of-death after a stall. Render interpolation is deliberately **not**
added in v0.2 (fixed 60 Hz steps at 144 Hz rendering reuse the last state).
`internal/game` exposes the step constant and a deterministic
`Advance(seconds)`-style helper so tests never rely on float loop drift.

**Alternatives considered:**
- Keep variable `dt` — fewer changes, but timers, formations and seeded waves
  become frame-rate dependent; violates the spirit of Law 4 and BR-017.
- Pure fixed-step inside `cmd/game` only — core would still integrate arbitrary
  `dt`; tests would not exercise the shipping path. Rejected.
- Decouple update rate to 120 Hz — doubles CPU for no gameplay benefit.

**Consequences:** `TestFrameRateIndependence` becomes stronger (exact equality
of state after equal simulated time rather than tolerance-based). Long-frame
behaviour must be specified: a 0.25 s stall advances at most 4 steps and drops
the rest, which is a documented, testable rule (AC-135). The existing
`dt`-based API stays for compatibility but is defined in terms of whole steps.

**Reconsider when:** render interpolation is wanted (smooth 144 Hz), or a
variable-step physics requirement appears. Neither is planned.
