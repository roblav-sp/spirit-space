# Architecture — Deployment

> Current architecture: manual static hosting; no CI/CD exists.

## Build

`build.sh`:
1. `GOOS=js GOARCH=wasm go build -o main.wasm ./cmd/game`
2. copies `$(go env GOROOT)/lib/wasm/wasm_exec.js` into the repo root

Artifacts: `main.wasm`, `wasm_exec.js`, plus the checked-in `index.html`.

## Runtime topology

```mermaid
graph LR
    S[Any static file server<br/>e.g. "python -m http.server"] --- A[index.html<br/>main.wasm<br/>wasm_exec.js]
    U[Browser] --> A
```

Serving requires a static server (WASM cannot be fetched from `file://`
with `instantiateStreaming`). Any static host works; none is configured in
the repository.

## Configuration

None. The game has no configuration surface: canvas size is fixed (800×600),
tunables are compile-time constants in `internal/game`. Changing a tunable is
a code change governed by feature specs.

## CI/CD, backups, recovery

- No CI pipeline exists. Quality gates are run manually
  (constitution §5). Adding CI is a recommended future task (TASK list,
  infrastructure item) but is not part of any feature spec.
- Nothing to back up: no data. Recovery = redeploy the static files.
- Migrations: none (no persistence).
