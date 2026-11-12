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
| BC-5 | Bullets despawn above the top edge; enemies below the bottom edge trigger game over. *(v0.2: escape is harmless — enemy removed, no life lost; D-2.)* |
| BC-6 | A kill sets `Dead` on both bullet and enemy and adds +10 to `Score` (BR-002). |
| BC-7 | `Restart()` restores exactly the `New()` state. |

## Error cases

`Update` panics only on programmer error (e.g. negative `dt` is not specially
handled — behavior: entities move backwards; documented, not defended).
Callers must pass `dt ≥ 0` and reasonably small; `cmd/game` clamps to 0.1 s.

## Stability rules

- Adding exported API: allowed with feature spec + traceability update.
- Changing semantics of the table above: ADR required.

## Planned v0.2 API (NOT IMPLEMENTED)

> Nothing in this section exists at HEAD `3fae24f`. It is the contract the
> M2–M8 tasks implement; traceability entries stay `TODO` until each lands.
> Signatures may still change once before implementation if a task proves them
> unworkable; changing them *after* implementation requires an ADR.

```go
// State is the top-level screen/game state (FR-006).
type State int
const (
    StateBoot State = iota
    StateMainMenu; StateRunOptions; StateControls; StateSound; StateHighScores
    StatePlaying; StatePaused; StatePlayerDying; StateRespawning
    StateGameOver; StateVictory
)

type Difficulty int    // Rookie, Pilot, Ace, Legend
type SpeedScale float64 // 0.75, 1.0, 1.25

// RunMetadata is immutable for the run (BR-017).
type RunMetadata struct {
    Seed       uint64
    RNGVersion int
    Difficulty Difficulty
    Speed      SpeedScale
}

type PowerUpID string // "rapid", "spread", "shield", "beam"
type SoundID string   // "shoot", "enemy-kill", ...

type SoundEvent struct{ ID SoundID; Volume float64 }

// Store is the simulation's view of persistence, supplied by cmd/game.
// No DOM types here (Law 5).
type Store interface {
    Read(key string) ([]byte, bool)
    Write(key string, data []byte) error
    Delete(key string) error
}

const StepSeconds = 1.0 / 60.0 // BR-012
type Options struct{ Difficulty Difficulty; Speed SpeedScale; Seed uint64 }

func NewGame(opts Options) *Game
func (g *Game) Step()                         // exactly one fixed step
func (g *Game) Advance(worldSeconds float64)  // whole steps only
func (g *Game) CurrentState() State
func (g *Game) Menu() MenuModel               // read-only view
func (g *Game) SendMenuAction(MenuAction)     // up/down/left/right/confirm/back
func (g *Game) Pause()
func (g *Game) Resume()
func (g *Game) Metadata() RunMetadata
func (g *Game) DrainSoundEvents() []SoundEvent
func (g *Game) EncodeScores(w io.Writer) error // codec lives here
func (g *Game) DecodeScores(r io.Reader) error // validates untrusted input
```

`Update(dt)` and `SetInput` remain for compatibility and are defined as
whole-step advances; `New()` remains as `NewGame` with defaults.

### Planned behavioral contract

| ID | Guarantee |
|---|---|
| BC-8 | Menu/state transitions are edge-triggered; only valid transitions occur; invalid `MenuAction`s are ignored. |
| BC-9 | `Step` advances exactly 1/60 s of world time; `Advance` consumes whole steps and truncates the remainder. |
| BC-10 | One damage event costs ≤ 1 life; while invulnerable, damage is ignored and hazards are not consumed. |
| BC-11 | Difficulty changes budgets only; movement per world second is difficulty-independent. |
| BC-12 | With equal `(seed, RNGVersion, difficulty, speed, input)` the director produces identical waves. |
| BC-13 | Power-ups are timed, capped, and never remove the base weapon. |
| BC-14 | Ranking is totally ordered (score desc, stage desc, insertion stable) and validated on read. |
| BC-15 | Sound events are produced deterministically and drained; audio is never awaited. |
| BC-16 | Persistence codecs never panic on hostile input and reject unknown schema versions. |

`BC-1` is strengthened, not changed: after BC-9 lands, "same inputs" means the
same input sequence over the same number of fixed steps.
