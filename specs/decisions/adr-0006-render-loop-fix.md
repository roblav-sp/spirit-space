# ADR-0006 — Fix render loop and background painting in the entry point

**Status:** Accepted

**Context:** Automated browser verification (skill `browser-verify`, ADR-0005)
discovered two defects in `cmd/game/main.go` that unit tests could not catch
because they live in the DOM layer:

1. **Static render loop** — `requestAnimationFrame` was called once at
   startup; the frame callback never re-armed itself, so only the first frame
   was ever drawn (`rafCalls` stayed at 1).
2. **White-screen frame 2+** — `draw()` painted the background with whatever
   `fillStyle` was left from the previous frame. After frame 1 set
   `fillStyle = "#fff"`, the next frame's full-canvas `fillRect` painted the
   entire canvas white, hiding the game.

Both contradict the bootstrap contract and make the game unplayable.

**Decision:** The frame callback re-arms `requestAnimationFrame` on every
frame, and `draw()` sets `fillStyle = "#000"` before painting the background.
Both changes are confined to `cmd/game/main.go`; the simulation is untouched.

**Alternatives considered:**
- setInterval-based loop — breaks frame-rate independence (Law 4) by tying dt
  to timer jitter instead of RAF timestamps.
- Leave as-is and document — rejected: it is a functional defect, not a
  design choice.

**Consequences:** The game actually animates in a browser. Verification is
now mechanical (e2e "canvas animates" check). The lesson is recorded: render
loop correctness is only observable end-to-end, which is why the browser
skill exists.

**Reconsider when:** never — this is a bug fix, not an architecture choice.
