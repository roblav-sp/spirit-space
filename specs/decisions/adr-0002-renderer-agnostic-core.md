# ADR-0002 — Renderer-agnostic simulation core

**Status:** Accepted (pre-existing; ratified by constitution)

**Context:** Testability and determinism conflict with direct DOM access. If
game rules live beside `syscall/js` calls, they can only be tested inside a
browser.

**Decision:** `internal/game` contains all state and rules with zero DOM
imports; `cmd/game` is the sole DOM consumer (input capture + drawing).
Dependency direction: `cmd/game → internal/game`, never reversed.

**Alternatives considered:**
- Single package mixing logic and rendering — simpler, but untestable via
  `go test` and violates the already-ratified constitution.
- ECS/framework abstraction — overkill for ~300 lines of code.

**Consequences:** Simulation is unit-testable natively (see
`internal/game/game_test.go`); `cmd/game` must re-sync input each frame.
Two-package split adds minor indirection.

**Reconsider when:** the simulation needs browser services (audio timers,
localStorage) — that would require an amendment to Law 5.
