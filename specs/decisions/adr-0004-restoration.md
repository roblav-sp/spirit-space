# ADR-0004 — Document-first restoration of the missing implementation

**Status:** Accepted

**Context:** At the start of this migration the repository did not compile:
`internal/game` referenced `spawnEnemies`, `updateEnemies`, `handleCollisions`,
and `clamp`, which did not exist; `cmd/game` was an empty directory; no tests
existed. `build.sh` could not run, so no quality gate could pass and no
spec-driven process could be verified against reality.

**Decision:** Restore the missing pieces to match the pre-existing
specifications (`docs/gameplay.md`, the constitution's tuning values) rather
than inventing new behavior: implement the four missing simulation functions
(including the documented "enemy reaching bottom ends the game" rule), add
`cmd/game/main.go` (input capture, RAF loop, Canvas drawing), and add
`internal/game/game_test.go` covering the constitution's laws and the
gameplay rules.

**Alternatives considered:**
- Document the broken state as-is — rejected: every traceability entry would
  be `TODO` and quality gates permanently red, defeating the purpose.
- Rewrite the game in JS — violates ADR-0001 and Law 1.

**Consequences:** All gates (gofmt, vet, test, WASM build) now pass;
`TestFrameRateIndependence` mechanically verifies Law 4. Behavior restored is
that of gameplay.md v0.1 only; no new features were invented.

**Reconsider when:** never — this ADR records a one-time remediation.
