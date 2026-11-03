# ADR-0001 — Go compiled to WebAssembly as the implementation language

**Status:** Accepted (pre-existing; ratified by constitution)

**Context:** The project is a browser game. Options: JavaScript/TypeScript, a
JS game engine, or another language compiled to WASM. The original author
chose Go→WASM with Canvas rendering; `go.mod`, `build.sh`, and the existing
constitution document all assume it.

**Decision:** All game logic is written in Go, compiled with
`GOOS=js GOARCH=wasm`, executed via `wasm_exec.js` in `index.html`. Standard
library only; no game engines or npm packages.

**Alternatives considered:**
- JavaScript/TypeScript + Phaser/PixiJS — richer ecosystem, but violates the
  single-language law and adds a dependency chain and build toolchain.
- Rust→WASM — also viable, but the existing codebase is Go.

**Consequences:** Pure `internal/game` is testable with plain `go test`;
no node/npm toolchain. Cost: Canvas drawing is manual (no engine), and
`syscall/js` bindings are verbose.

**Reconsider when:** a feature genuinely requires an engine-grade capability
(particles, audio middleware, tiled maps) or WASM size/performance becomes a problem.
