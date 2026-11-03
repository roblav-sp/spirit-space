# Spirit Space

A single-player browser space shooter written entirely in Go, compiled to
WebAssembly, and rendered to an HTML5 Canvas. No server, no dependencies —
the whole game is the Go standard library.

![gameplay](docs/gameplay.md) <!-- pointer to the gameplay spec -->

## How to run

You need **Go ≥ 1.22** and **any static file server** (e.g. Python, which is
preinstalled on most systems).

```bash
# 1. Build the WebAssembly module and copy the JS glue file
./build.sh

# 2. Serve the folder (WASM cannot be loaded from file://)
python3 -m http.server 8080

# 3. Open the game
#    http://localhost:8080
```

> **Why not `go run`?** `go run` needs a Go entry point in your native
> environment. This project compiles to WebAssembly (`GOOS=js GOARCH=wasm`),
> so there is no native binary to run directly. `go run ./cmd/game` would
> fail because that package only builds for the `js/wasm` platform — use
> `./build.sh` and open `index.html` through a static server instead.

## Controls

| Key | Action |
|---|---|
| `←` `→` `↑` `↓` or `W` `A` `S` `D` | Move ship |
| `Space` | Fire |
| `R` | Restart (after game over) |

Shoot enemies before they reach the bottom of the screen or touch you.
+10 points per kill, one life per run.

## Running the tests

```bash
go test ./internal/...        # simulation tests (13 tests)
go vet ./internal/...         # static analysis
gofmt -l .                    # formatting check (no output = clean)
GOOS=js GOARCH=wasm go build -o main.wasm ./cmd/game   # wasm build check
```

Optional: automated browser checks (headless Chromium, ~150 MB download on
first run) — see `.agents/skills/browser-verify/SKILL.md`:

```bash
.agents/skills/browser-verify/scripts/setup.sh    # once
.agents/skills/browser-verify/scripts/verify.sh   # 8 end-to-end checks
```

## Project layout

```
cmd/game/         WASM entry point: DOM access, input capture, render loop
internal/game/    Pure simulation: state, Update(dt), collisions, scoring
index.html        Page shell + bootstrap script
build.sh          Compiles main.wasm and copies wasm_exec.js
constitution.md   Project laws — read before changing anything
specs/            Product, features, architecture, contracts, ADRs, traceability
plans/, tasks/    Implementation plans and atomic tasks
templates/        Document templates
docs/             Historical gameplay spec (superseded by specs/)
```

The dependency direction is strictly one-way: `cmd/game → internal/game`.
The simulation never touches the DOM, which is what makes it testable with
plain `go test`.

## Specification-driven development

This repository follows a spec-first process (see `constitution.md` and
`ai-development-guide.md`):

- **Laws** that may never be broken: `constitution.md`
- **What the product does**: `specs/product.md` + `specs/features/`
- **How it's built**: `specs/architecture/`, `specs/contracts/`,
  `specs/decisions/`
- **What's done and what's verified**: `specs/traceability.md`
- **How to work on it**: `plans/` + `tasks/` (atomic, ID-referenced tasks)

Change process in short: update the spec first, code second, keep the
traceability matrix honest, and never bypass the quality gates listed above.

## Git setup (first time only)

This project currently has no git history. To initialize:

```bash
git init
git add .
git commit -m "Initial commit: Spirit Space with spec-driven docs"
```

`.gitignore` is already present — it excludes build artifacts
(`main.wasm`, `wasm_exec.js`) and the browser-skill's local
`node_modules`/screenshots, so the commit stays clean.
