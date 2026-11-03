# Contract — `internal/game` Simulation API

> Public Go API of the simulation package. Consumed only by `cmd/game` today,
> but it is the project's principal interface (constitution §7). Breaking
> changes require an ADR.

```go
package game // import "spirit-space/internal/game"

// Constants
const Width  = 800  // world width (fixed, Law 3)
const Height = 600  // world height

// Entities
type Entity struct{ X, Y, Radius float64; Dead bool }
type Player struct{ Entity; Cooldown float64 }
type Bullet struct{ Entity }
type Enemy  struct{ Entity }

// Input holds the current keyboard state (one flag per direction + fire).
type Input struct{ Left, Right, Up, Down, Fire bool }

// Game holds the full game state.
type Game struct {
    Player  Player
    Bullets []Bullet
    Enemies []Enemy
    Score   int
    GameOver bool
}

func New() *Game                       // fresh run; player at (Width/2, Height-80)
func (g *Game) Restart()               // full reset to New() state
func (g *Game) SetInput(in Input)      // replace input snapshot
func (g *Game) Update(dt float64)      // advance simulation; no-op when GameOver
```

## Behavioral contract

| ID | Guarantee |
|---|---|
| BC-1 | `Update` reads only (state, input, dt); deterministic given the seeded RNG (NFR-001). |
| BC-2 | `Update` is a no-op once `GameOver` is true. |
| BC-3 | Player position is always clamped to `[Radius, Width-Radius] × [Radius, Height-Radius]`. |
| BC-4 | Firing is rate-limited to one bullet per `fireCooldown` (0.2 s); the first shot is immediate. |
| BC-5 | Bullets despawn above the top edge; enemies below the bottom edge trigger game over. |
| BC-6 | A kill sets `Dead` on both bullet and enemy and adds +10 to `Score` (BR-002). |
| BC-7 | `Restart()` restores exactly the `New()` state. |

## Error cases

`Update` panics only on programmer error (e.g. negative `dt` is not specially
handled — behavior: entities move backwards; documented, not defended).
Callers must pass `dt ≥ 0` and reasonably small; `cmd/game` clamps to 0.1 s.

## Stability rules

- Adding exported API: allowed with feature spec + traceability update.
- Changing semantics of the table above: ADR required.
