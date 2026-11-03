# Contract — Browser Bootstrap (`index.html` ↔ `main.wasm`)

> Interface between the page shell and the WASM module. Both sides must honor
> it; it is not to be changed casually (constitution §7).

## Page → WASM expectations

| Element/Contract | Requirement |
|---|---|
| Canvas element | `id="game"`, `width="800"`, `height="600"` (matches `game.Width/Height`) |
| Glue script | `wasm_exec.js` loaded before bootstrap (copied by `build.sh`) |
| Instantiation | `WebAssembly.instantiateStreaming(fetch("main.wasm"), go.importObject)` then `go.run(instance)` |
| Error surface | instantiation/fetch errors replace the page with a visible `<pre>` (Law 7) |

## WASM → Page (DOM) usage

| Contract | Requirement |
|---|---|
| Event listeners | `keydown`/`keyup` on `document`, using `event.code` values |
| Key codes consumed | `ArrowLeft/Right/Up/Down`, `KeyA/D/W/S` (movement), `Space` (fire), `KeyR` (restart when game over) |
| preventDefault | called for handled keys so the page does not scroll |
| Frame loop | single `requestAnimationFrame` callback; timestamp in ms converted to seconds; `dt` clamped to ≤ 0.1 s |

## Keyboard code table

| `event.code` | Action |
|---|---|
| `ArrowLeft` / `KeyA` | move left |
| `ArrowRight` / `KeyD` | move right |
| `ArrowUp` / `KeyW` | move up |
| `ArrowDown` / `KeyS` | move down |
| `Space` | fire |
| `KeyR` | restart (only when `GameOver`) |

## Failure modes

- Missing `main.wasm` / bad path → error banner via bootstrap catch.
- WASM exception after start → browser console only (documented gap).
- Canvas id renamed on either side → runtime error; change requires updating
  this contract and both implementations together.
