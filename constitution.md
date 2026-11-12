# Spirit Space — Constitution

> **Status: RATIFIED** (Amendment 001 applied 2026-11-12). Supreme law of the
> codebase. Specs, plans, tasks, and code must obey it. Gameplay tunables live
> in `specs/features/` and may change freely; they may never override an
> Invariant Law. Amendment history: `docs/constitution-amendment-001.md`.

## 1. Mission and scope

Spirit Space is a single-player browser space shooter: the player pilots a
ship, shoots incoming enemies, and scores points. The entire game is Go
compiled to WebAssembly, rendered to an HTML5 Canvas. No server, no network
play, and no persistence other than **optional, local-only browser storage of
high scores and user settings within the page's own origin** (Amendment 001).
Out of scope: multiplayer, accounts, analytics, backend services, telemetry,
cookies, and any data leaving the user's browser.

## 2. Invariant Laws

These may never be violated by any feature, refactor, or spec change.

1. **Single language** — All game logic is Go. JavaScript is limited to the
   bootstrap glue in `index.html`. No game rule may be implemented in JS.
2. **Deterministic simulation** — `game.Update(dt)` depends only on
   (current state, input, dt). Randomness only via the seeded `math/rand.Rand`
   held by `Game`; no wall-clock reads inside `internal/game`. Rendering reads
   state; it never mutates it.
3. **Fixed canvas, world coordinates** — The world is a fixed 800×600 space
   (`game.Width`, `game.Height`). No scrolling camera, no world larger than the
   viewport.
4. **Frame-rate independence** — Movement is units per second × `dt`. The
   simulation must behave identically at 30, 60, or 144 FPS (verified by
   `TestFrameRateIndependence`).
5. **Renderer-agnostic core** — `internal/game` must not import `syscall/js`,
   `net/http`, or any DOM package; it is testable with plain `go test`.
   `cmd/game` is the only package allowed to touch the DOM.
6. **No external dependencies** — Go standard library only. `go.mod` must never
   gain a `require` block. No npm packages.
7. **Graceful failure** — Bootstrap errors must be visible on the page, not a
   silent black screen.

## 3. Architecture and boundaries

```
cmd/game/         WASM entry point: DOM access, input capture, render loop
internal/game/    Pure simulation: state, Update(dt), collisions, scoring
index.html        Page shell + bootstrap script
build.sh          Compiles main.wasm and copies wasm_exec.js
specs/            Product, features, architecture, contracts, ADRs
plans/, tasks/    Implementation plans and atomic tasks
templates/        Document templates
```

Dependency direction is one-way: `cmd/game → internal/game`. The reverse import
is forbidden.

## 4. Specification-first development

- Every feature change starts with (or updates) a feature spec in
  `specs/features/<name>/spec.md` before code is written.
- Every requirement carries a stable ID (`FR-nnn`, `BR-nnn`, `NFR-nnn`,
  `SEC-nnn`, `AC-nnn`). IDs are never reused.
- Every task in `tasks/` references the requirement IDs it implements.
- `specs/traceability.md` maps requirements → architecture → code → tests.
  Unknown mappings are marked `TODO`, never invented.

## 5. Testing and quality gates

Mandatory before merge, in order: `gofmt` (no diffs), `go vet ./...`,
`go test ./...`, and a successful WASM build
(`GOOS=js GOARCH=wasm go build ./cmd/game`). Every behavior change in
`internal/game` ships with a test. Gates must never be weakened or bypassed.

## 6. Security and privacy

The game has no server, no auth, and collects no data. Trust boundary: nothing
from the page may make the simulation depend on DOM state.

**Local storage exception (Amendment 001).** A single, versioned key per
concern — high scores and user settings — may be persisted in the browser's
`localStorage` for the page's own origin, subject to all of:

1. **Content limits.** Only: player-chosen alias (optional, ≤16 chars, never
   validated for uniqueness), score, stage reached, chosen difficulty and game
   speed, audio volumes/mute, control preferences, and schema version. No
   device identifiers, no timestamps beyond score order, no free-form text
   other than the optional alias.
2. **No transmission.** Stored data is never sent anywhere. `SEC-002`
   (no runtime network) is unchanged.
3. **No cookies, no IndexedDB, no Cache API, no server storage.**
   `localStorage` only, and only from `cmd/game` (Law 5 keeps `internal/game`
   free of DOM access; scoring and validation rules still live in Go).
4. **Reads are untrusted input.** Corrupted, truncated, oversized, or
   schema-mismatched data must fall back to a clean default and must never
   panic. Bounded (≤64 KiB) and versioned.
5. **User control.** A visible "Clear saved data" action exists in the
   settings menu; disabling persistence (or a storage failure, e.g. private
   browsing quota errors) degrades to memory-only for the session.
6. **No new dependency.** `localStorage` is reached through `syscall/js` from
   `cmd/game`; `go.mod` stays `require`-free (Law 6).

Anything beyond this exception requires a further amendment (§8).

## 7. API and contract stability

- The exported API of `internal/game` (`Game`, `Update`, `SetInput`, `Restart`,
  `New`, `Input`, entity types) is a public contract documented in
  `specs/contracts/simulation-api.md`. Breaking changes require an ADR.
- The bootstrap contract (`index.html` ↔ `main.wasm`: canvas id, `wasm_exec.js`,
  keyboard codes) is documented in `specs/contracts/bootstrap.md`.

## 8. Change control and governance

1. Propose the change in the relevant spec file first.
2. If it conflicts with an Invariant Law, amend this document explicitly
   (state which law and why) before code is written.
3. Meaningful architectural decisions get an ADR in `specs/decisions/`.
4. Code that contradicts this Constitution is a bug, even if it ships.

## 9. Definition of done

A task is done when: spec and IDs exist or are updated; code passes all gates
in §5; tests cover the new behavior; traceability is updated; no unrelated
files were touched; documentation matches the implemented behavior.

## 10. AI-assisted development

AI agents must follow `ai-development-guide.md`: load only the context pack
relevant to the task, never restate spec content in code comments, never
implement a feature whose spec is unclear, and stop and report conflicts
between specs and code instead of resolving them silently.
