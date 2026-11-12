# ADR-0010 — All UI states rendered by Go on the single canvas

**Status:** Proposed

**Context:** v0.2 adds BOOT, MAIN_MENU, PLAYING, PAUSED, PLAYER_DYING,
RESPAWNING, GAME_OVER and HIGH_SCORES. Two options exist: HTML/JS menus, or
canvas UI drawn from Go. Law 1 limits JS to bootstrap glue and forbids game
rules in JS; Law 3 fixes the world at 800×600. The current `draw()` uses
`fillText` with no `font` set, and input is captured in `cmd/game` only.

**Decision:** All screens are drawn on the existing `#game` canvas by
`cmd/game`, driven by a `State` field owned by `internal/game`. `index.html`
stays bootstrap-only (canvas, glue, error surface) and gains no markup. Menus
are a small retained list model (`[]MenuItem`) in `internal/game` with
keyboard navigation (Up/Down/Left/Right, Enter/Space, Escape/P), so selection
logic is unit-testable and deterministic (Laws 2, 5). Text uses a fixed
`ctx.font` set once per frame from a Go constant; the canvas id, size and
keyboard contract stay unchanged.

**Alternatives considered:**
- HTML overlay menus — better accessibility and typography for free, but moves
  screen logic and hit-testing into JS/HTML (Law 1 risk) and splits state
  ownership across two runtimes.
- Separate menu canvas element — more DOM, no benefit at this scale.
- Menu in WASM but hit-testing via mouse — adds a new input class; keyboard is
  already contracted. Deferred, not forbidden.

**Consequences:** Everything is one draw path, testable state transitions, no
new DOM contract beyond storage/audio. Cost: no native text layout, no focus
ring from the browser; we must define our own contrast and hover/keyboard
focus cues (NFR-007). Screen-reader accessibility stays out of scope and must
be stated as such in the spec.

**Reconsider when:** real accessibility requirements (screen readers, gamepad
menus) appear, or the menu outgrows a list model.
