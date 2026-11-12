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

## Planned v0.2 additions (NOT IMPLEMENTED)

> None of this exists at HEAD `3fae24f`. Recorded now so the page shell, the
> WASM module and the browser skill can be changed together in M2–M8.

### Additional key codes

| `event.code` | Action | State |
|---|---|---|
| `Escape` / `KeyP` | pause ⇄ resume; back out of a menu level | any |
| `Enter` / `NumpadEnter` | confirm menu item | menus, `GAME_OVER` |
| `KeyR` | restart (unchanged: only in `GAME_OVER`; also `VICTORY`) | terminal states |
| `Space` | confirm (menus) **and** fire (playing) — context-dependent | all |
| `ArrowUp/Down/Left/Right`, `KeyW/A/S/D` | menu navigation in menus; movement in `PLAYING` | all |
| `KeyM` | toggle mute (documented in Controls) | all |

Rules that stay invariant:

- `preventDefault` is called for every handled key, in every state.
- Input is edge-processed in menus (one action per `keydown`), level-processed
  in `PLAYING` (held movement/fire).
- `blur` clears all held keys; no state transition on blur.
- The canvas keeps `id="game"`, `width="800"`, `height="600"` (Law 3).

### New DOM surfaces used by the WASM module

| Surface | Purpose | Constraint |
|---|---|---|
| `document.addEventListener("blur"/"focus")` | clear stuck keys | no game rule in JS |
| `AudioContext` (+ `decodeAudioData`) | SFX/music buses | created only after the first `keydown` (FR-016.2); failure ⇒ silence |
| `window.localStorage` | scores/settings | **only if amendment 001 is ratified**; keys `spirit-space.scores.v1`, `spirit-space.settings.v1`; ≤64 KiB; every access wrapped, exceptions ⇒ memory-only |
| `fetch` of local asset files | sprites/audio | same-origin only; failure ⇒ geometric/silent fallback (FR-017.3) |

`index.html` gains **no** new markup, no new script logic and no global state:
it stays bootstrap glue (Law 1). Storage, audio and asset decoding are all
driven from Go through `syscall/js` in `cmd/game`.

### Failure modes added

- `localStorage` throws (private mode, quota) → session-only memory store, one
  console warning, gameplay unaffected (AC-175).
- `AudioContext` missing/blocked → silent game, one console warning (AC-181).
- One asset 404 / decode error → that asset falls back; others keep loading
  (AC-183/AC-184). Boot itself is unaffected, so Law 7's banner stays reserved
  for `main.wasm`/glue failures.
