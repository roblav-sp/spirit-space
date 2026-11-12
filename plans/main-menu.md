# Plan — Main Menu, State Machine, and Pause

> Implements FR-006, FR-009, AC-101…AC-110
> (`specs/features/main-menu/spec.md`). Milestone **M2**. ADR-0010.

## Requirements being implemented
State machine + menu model + pause freeze + blur handling. No scoring, no
lives, no waves — those follow in M3–M5.

## Architecture components affected
- `internal/game` — new `state.go` (State enum, transitions), `menu.go` (list
  model, option cycling). `Game` gains `State`; `Update` dispatches by state.
- `cmd/game` — key handler becomes state-aware; `draw` dispatches by state.

## Contracts affected
`simulation-api.md` (BC-8; planned API is implemented here first),
`bootstrap.md` (Escape/P/Enter/arrow/space semantics, blur/focus).

## Files or modules likely to change
`internal/game/state.go`, `internal/game/menu.go`, `internal/game/game.go`,
`internal/game/*_test.go`, `cmd/game/main.go`, `index.html` (no change
expected — verify), `specs/contracts/bootstrap.md` (status flip).

## Dependency order
1. `State` enum + `New()` starting in `MAIN_MENU` (breaks 3 existing tests —
   update them deliberately, do not weaken assertions).
2. Menu model + navigation actions + edge-triggered input.
3. Start → fresh run; pause/resume; quit to menu.
4. Renderer dispatch + fixed `ctx.font`.
5. Blur/`preventDefault` handling.
6. Browser checks in `.agents/skills/browser-verify/`.

## Data migrations
None (in-memory only). `Game` gains one field; `Restart()` must preserve
difficulty/speed selection.

## Testing strategy
- Unit: AC-101…AC-107, AC-109 (table-driven menu transitions; pause
  byte-equality via deep-compare of the exported structs).
- Browser: AC-108, AC-110 (new checks in `e2e/verify.mjs`).

## Rollout / rollback
Static deploy after `./build.sh`. Rollback = revert the commit; no data.

## Risks and mitigations
- **Existing tests break** because `New()` no longer starts `PLAYING` → update
  them in the same commit and keep every assertion; add an explicit test that
  `New()` is in `MAIN_MENU`.
- **Double-firing Space** (menu confirm + fire) → edge-trigger in menus, level
  in playing; test both in one key sequence.
- **Text sizing** defaults differ per browser → set `ctx.font` from a constant
  and assert the string in the browser check.
