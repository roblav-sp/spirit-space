# ADR-0003 — Fixed random seed for enemy spawns

**Status:** Accepted

**Context:** The simulation must be deterministic (constitution Law 2,
NFR-001), but enemy X positions are random. Using the package-global
`math/rand` source or time-based seeding makes runs unreproducible and tests
flaky.

**Decision:** `Game` owns a `*rand.Rand` created from a fixed constant seed
(`rngSeed = 1`) in `New()`. Enemy spawn X is drawn from this per-game RNG.
Determinism is per-run from construction, not globally across runs.

**Alternatives considered:**
- Package-global `rand.Float64()` — simplest, but shared mutable state and
  breaks reproducibility of individual runs.
- Time-based seeding — variety across runs, but destroys testability of
  spawn sequences.
- Precomputed spawn tables — deterministic but rigid and pointless at v0.1
  difficulty (BR-004).

**Consequences:** Every run has the same spawn sequence in v0.1. This is
acceptable (constant difficulty anyway, BR-004) and trivially replaceable
later; making the seed configurable would be a one-line change plus ADR.

**Reconsider when:** run-to-run variety is desired (likely with v0.2
difficulty ramping) — seed from an explicit input instead of a constant.
