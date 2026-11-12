# Feature — Main Menu, State Machine, and Pause

> Implements FR-006 and FR-009. ADR-0010 (Go-drawn canvas UI), ADR-0008
> (fixed step), ADR-0013 (audio unlock).

## Context
v0.1 starts playing immediately. v0.2 needs a front end, a pause, and an
explicit state machine so difficulty/speed are chosen before a run and every
screen is deterministic and testable.

## Actors
Player (keyboard), Simulation (state + menu model), Renderer (`cmd/game`).

## Preconditions
None; this is the entry path from BOOT.

## State machine

```
BOOT → MAIN_MENU → PLAYING ⇄ PAUSED → PLAYER_DYING → RESPAWNING → PLAYING
                                        PLAYING → GAME_OVER → MAIN_MENU | (R) PLAYING
MAIN_MENU → CONTROLS → MAIN_MENU
MAIN_MENU → SOUND → MAIN_MENU
MAIN_MENU → HIGH_SCORES → MAIN_MENU
```

Transitions are owned by `internal/game` as an exported `State` value; the
renderer only reads it.

## Functional requirements
- **FR-006.1** — After boot the game shows `MAIN_MENU`; no enemies, bullets or
  score exist and `Update` does not advance a run.
- **FR-006.2** — Menu items: **Start**, **Controls**, **Sound**,
  **High Scores**, **Return** (Return is hidden/disabled on the root menu).
  Up/Down move the cursor with wrap-around; Enter or Space activates; Escape
  backs out one level.
- **FR-006.3** — Start opens the run-options row: difficulty
  Rookie/Pilot/Ace/Legend (default **Pilot**) and speed Slow 0.75× / Normal 1×
  / Fast 1.25× (default **Normal**). Left/Right cycle values and never produce
  a value outside the enumerated set.
- **FR-006.4** — Controls screen lists movement (arrows/WASD), fire (hold
  Space), pause (Escape or P), restart (R, only on the game-over screen), and
  menu navigation. It is read-only.
- **FR-006.5** — High Scores screen renders the local table (empty state text
  when none) and is read-only.
- **FR-006.6** — Activating Start creates a fresh run: 3 lives, score 0, empty
  entity slices, selected difficulty and speed recorded in run metadata.
- **FR-006.7** — During `PLAYING`, Escape **or** P enters `PAUSED`. During
  `PAUSED`, Escape or P resumes; the pause menu items are Resume, Restart,
  Sound, Quit to Menu.
- **FR-006.8** — `PAUSED` freezes the simulation **exactly**: no timer, spawn,
  invulnerability, power-up or animation tick advances; audio events are not
  queued.
- **FR-006.9** — Entering any non-`PLAYING` state clears held inputs, and a
  window `blur` clears held inputs without changing state (no stuck keys).
- **FR-006.10** — The first `keydown` after load unlocks audio (ADR-0013); the
  Sound screen exposes master/music/SFX volume and mute.
- **FR-006.11** — Every key the game handles calls `preventDefault`, so arrows
  and Space never scroll the page. Unhandled keys are ignored.
- **FR-006.12** — `GAME_OVER` accepts R (restart with the previous
  difficulty/speed) and Enter (back to `MAIN_MENU`); other keys are ignored.

## Business rules
- BR-012 (fixed step), BR-009 (3 lives on Start). No scoring occurs outside
  `PLAYING`.

## Acceptance criteria
- **AC-101** — Fresh load reaches `MAIN_MENU` with zero enemies, bullets and
  score.
- **AC-102** — Start begins a run with exactly 3 lives and the selected
  difficulty/speed recorded.
- **AC-103** — Up at the top item wraps to the last item; Down at the last
  wraps to the first.
- **AC-104** — Left/Right on an option never yields a value outside the
  allowed set (including wrap-around at both ends).
- **AC-105** — Entering `PAUSED` and advancing 10 simulated seconds leaves
  score, entity positions, timers and lives byte-identical.
- **AC-106** — Resume restores the exact pre-pause state and continues.
- **AC-107** — Quit to Menu discards the run: lives, score and seed are gone
  from state, and a later Start is a fresh run.
- **AC-108** — A `blur` during `PLAYING` releases all held keys; on refocus the
  ship does not move until a new `keydown`.
- **AC-109** — Escape and P behave identically in `PLAYING` and `PAUSED`.
- **AC-110** — Handled keys call `preventDefault` (browser check: page does not
  scroll on arrows/space).

## Edge cases
- Pause during `PLAYER_DYING` freezes the death timer (AC-105 applies).
- Pause then Restart re-creates the run with the same difficulty/speed.
- Start with Enter held: only one transition fires (edge-triggered, not level).
- Boot failure is `index.html`'s job (Law 7); the menu never renders on a
  failed boot.

## Error behavior
Pure state transitions; no I/O. Menu rendering failures degrade to geometric
fallback (FR-017).

## Non-functional requirements
NFR-001, NFR-002, NFR-007 (keyboard reachability, ≥4.5:1 contrast).

## Security requirements
None beyond SEC-001/SEC-002. Audio unlock uses no permissions.

## Observability requirements
None (client-only).

## Out of scope
Mouse/touch menus, screen-reader narration, mid-run difficulty changes,
remappable keys (recorded as a future item).

## Open questions
- Should `Return` be omitted entirely (footer only) or shown disabled? Current
  spec: omitted on the root menu.
- Should the pause menu offer "Quit to Menu" only after M3 (lives) lands?
  Spec assumes yes from M2.
