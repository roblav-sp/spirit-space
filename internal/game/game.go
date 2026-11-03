// Package game implements the core space game logic.
// It is renderer-agnostic: the js entry point in cmd/game draws the state.
package game

import "math/rand"

const (
	Width  = 800
	Height = 600

	playerSpeed = 300.0 // pixels per second
	bulletSpeed = 500.0
	enemySpeed  = 120.0

	fireCooldown = 0.2 // seconds between shots
	spawnDelay   = 1.2 // seconds between enemy spawns

	enemyRadius  = 16.0
	scorePerKill = 10
)

// rngSeed is fixed so the simulation is deterministic (Constitution, Law 2).
const rngSeed = 1

// Entity is a simple positioned object with a bounding radius.
type Entity struct {
	X, Y   float64
	Radius float64
	Dead   bool
}

// Player is the ship controlled by the player.
type Player struct {
	Entity
	Cooldown float64
}

// Bullet is a projectile fired by the player.
type Bullet struct{ Entity }

// Enemy drifts down toward the player.
type Enemy struct{ Entity }

// Input holds the current keyboard state.
type Input struct {
	Left, Right, Up, Down, Fire bool
}

// Game holds the full game state.
type Game struct {
	Player  Player
	Bullets []Bullet
	Enemies []Enemy

	rng        *rand.Rand
	input      Input
	time       float64
	spawnTimer float64
	Score      int
	GameOver   bool
}

func New() *Game {
	return &Game{
		Player: Player{Entity: Entity{
			X:      Width / 2,
			Y:      Height - 80,
			Radius: 16,
		}},
		rng:        rand.New(rand.NewSource(rngSeed)),
		spawnTimer: spawnDelay, // first enemy after one full spawn delay
	}
}

// Restart resets the game to its initial state (used after game over).
func (g *Game) Restart() { *g = *New() }

// SetInput replaces the current input state.
func (g *Game) SetInput(in Input) { g.input = in }

// Update advances the simulation by dt seconds.
func (g *Game) Update(dt float64) {
	if g.GameOver {
		return
	}
	g.time += dt
	g.updatePlayer(dt)
	g.updateBullets(dt)
	g.spawnEnemies(dt)
	g.updateEnemies(dt)
	g.handleCollisions()
}

func (g *Game) updatePlayer(dt float64) {
	p := &g.Player
	if g.input.Left {
		p.X -= playerSpeed * dt
	}
	if g.input.Right {
		p.X += playerSpeed * dt
	}
	if g.input.Up {
		p.Y -= playerSpeed * dt
	}
	if g.input.Down {
		p.Y += playerSpeed * dt
	}
	p.X = clamp(p.X, p.Radius, Width-p.Radius)
	p.Y = clamp(p.Y, p.Radius, Height-p.Radius)

	p.Cooldown -= dt
	if g.input.Fire && p.Cooldown <= 0 {
		g.Bullets = append(g.Bullets, Bullet{Entity{
			X: p.X, Y: p.Y - p.Radius, Radius: 4,
		}})
		p.Cooldown = fireCooldown
	}
}

func (g *Game) updateBullets(dt float64) {
	kept := g.Bullets[:0]
	for i := range g.Bullets {
		b := &g.Bullets[i]
		b.Y -= bulletSpeed * dt
		if b.Y > -20 && !b.Dead {
			kept = append(kept, *b)
		}
	}
	g.Bullets = kept
}

func (g *Game) spawnEnemies(dt float64) {
	g.spawnTimer -= dt
	if g.spawnTimer > 0 {
		return
	}
	g.spawnTimer = spawnDelay
	e := Enemy{Entity{
		X:      clamp(g.rng.Float64()*(Width-2*enemyRadius)+enemyRadius, enemyRadius, Width-enemyRadius),
		Y:      -enemyRadius,
		Radius: enemyRadius,
	}}
	g.Enemies = append(g.Enemies, e)
}

func (g *Game) updateEnemies(dt float64) {
	for i := range g.Enemies {
		g.Enemies[i].Y += enemySpeed * dt
	}
}

func (g *Game) handleCollisions() {
	for i := range g.Enemies {
		e := &g.Enemies[i]
		if e.Dead {
			continue
		}
		// An enemy reaching the bottom edge ends the game.
		if e.Y+e.Radius >= Height {
			g.GameOver = true
			return
		}
		// An enemy touching the player ends the game.
		if dist2(&e.Entity, &g.Player.Entity) < sq(e.Radius+g.Player.Radius) {
			g.GameOver = true
			return
		}
		// One bullet hit destroys an enemy and scores.
		for j := range g.Bullets {
			b := &g.Bullets[j]
			if b.Dead {
				continue
			}
			if dist2(&e.Entity, &b.Entity) < sq(e.Radius+b.Radius) {
				e.Dead = true
				b.Dead = true
				g.Score += scorePerKill
				break
			}
		}
	}
	kept := g.Enemies[:0]
	for _, e := range g.Enemies {
		if !e.Dead {
			kept = append(kept, e)
		}
	}
	g.Enemies = kept
}

func clamp(v, lo, hi float64) float64 {
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}

// dist2 returns the squared distance between two entities.
func dist2(a, b *Entity) float64 {
	dx, dy := a.X-b.X, a.Y-b.Y
	return dx*dx + dy*dy
}

func sq(v float64) float64 { return v * v }
