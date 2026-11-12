# ADR-0009 — Seeded wave director with recorded run metadata

**Status:** Proposed (extends ADR-0003)

**Context:** ADR-0003 fixed the seed at `rngSeed = 1`, so every v0.1 run is
identical. v0.2 needs run-to-run variety (procedural waves, power-up drops,
boss choice) while keeping NFR-001 determinism, reproducible bug reports, and
seeded tests. A single global `math/rand` or time-based seeding would break
all of those.

**Decision:** One `*rand.Rand` per `Game`, seeded from a `RunSeed` recorded in
a `RunMetadata` struct (seed value, RNG version, difficulty, speed). The
director draws from that instance only, and every draw happens in a fixed
order determined by the director, not by frame timing. Techniques that consume
different numbers of draws depending on caller behavior are forbidden (no
shared pool, no draw-per-frame jitter). The RNG version tag means changing the
draw sequence is an explicit, versioned event: old seeds keep their sequence
when the version is bumped. Default seed for "new run" comes from an explicit
input supplied by `cmd/game` (CSPRNG or timestamp); tests pass fixed seeds.

**Alternatives considered:**
- Keep the constant seed — zero variety, defeats the point of FR-011.
- Per-system RNGs (one for spawns, one for drops) — more isolation, but
  ordering across systems becomes the new determinism hazard and replay format
  grows. Rejected for v0.2; the metadata field leaves room to add it.
- Hash-based draws (`hash(seed, stage, index)`) — attractive, but more code
  than a single `rand.Rand` and no cheaper to test.

**Consequences:** Runs are reproducible from `(seed, RNG version, difficulty,
speed, input sequence)`. Wave content is constrained by templates (ADR-0010
family) so a seed changes *selection*, never *validity*: every generated wave
passes the same budget/safe-gap checks. Existing ADR-0003 remains Accepted for
v0.1 history; its "reconsider when" condition is now met.

**Reconsider when:** cross-system independence is needed, or replays are
stored (would then require a serialized input stream, not just a seed).
