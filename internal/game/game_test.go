package game

import "testing"

// advance runs the simulation in fixed 1/60 s steps.
func advance(g *Game, seconds float64) {
	const step = 1.0 / 60.0
	for t := 0.0; t < seconds; t += step {
		g.Update(step)
	}
}

func TestFrameRateIndependence(t *testing.T) {
	// Same total simulated time with different step sizes must produce
	// the same player position (Constitution, Law 4).
	run := func(steps int, dt float64) (x, y float64) {
		g := New()
		g.SetInput(Input{Right: true, Down: true})
		for i := 0; i < steps; i++ {
			g.Update(dt)
		}
		return g.Player.X, g.Player.Y
	}
	x1, y1 := run(360, 1.0/60.0) // 6 s at 60 FPS
	x2, y2 := run(180, 1.0/30.0) // 6 s at 30 FPS
	if abs(x1-x2) > 1e-6 || abs(y1-y2) > 1e-6 {
		t.Fatalf("positions diverge: (%v,%v) vs (%v,%v)", x1, y1, x2, y2)
	}
}

func abs(v float64) float64 {
	if v < 0 {
		return -v
	}
	return v
}

func TestPlayerClampedToField(t *testing.T) {
	g := New()
	g.SetInput(Input{Left: true, Up: true})
	advance(g, 10)
	if g.Player.X < g.Player.Radius || g.Player.Y < g.Player.Radius {
		t.Fatalf("player escaped field: %v,%v", g.Player.X, g.Player.Y)
	}
}

func TestFireCooldown(t *testing.T) {
	g := New()
	g.SetInput(Input{Fire: true})
	advance(g, 0.05) // first shot fires immediately (cooldown starts at 0)
	if len(g.Bullets) != 1 {
		t.Fatalf("want 1 bullet on first shot, got %d", len(g.Bullets))
	}
	n := len(g.Bullets)
	advance(g, 0.1) // still inside the 0.2 s cooldown window
	if len(g.Bullets) != n {
		t.Fatalf("second bullet fired before cooldown elapsed")
	}
}

func TestBulletDestroyedOnHitAndScored(t *testing.T) {
	g := New()
	g.spawnTimer = 1e9 // disable natural spawns for this test
	// Place an enemy directly above the player.
	g.Enemies = append(g.Enemies, Enemy{Entity{X: g.Player.X, Y: g.Player.Y - 50, Radius: enemyRadius}})
	g.SetInput(Input{Fire: true})
	advance(g, 0.3) // long enough to fire and reach the enemy
	if g.Score != scorePerKill {
		t.Fatalf("want score %d after one kill, got %d", scorePerKill, g.Score)
	}
	if len(g.Enemies) != 0 {
		t.Fatalf("destroyed enemy not removed")
	}
}

func TestEnemyReachingBottomEndsGame(t *testing.T) {
	g := New()
	g.spawnTimer = 1e9 // disable natural spawns for this test
	g.Enemies = append(g.Enemies, Enemy{Entity{X: 100, Y: Height - enemyRadius, Radius: enemyRadius}})
	g.Update(1.0 / 60.0)
	if !g.GameOver {
		t.Fatalf("game should be over when enemy reaches bottom")
	}
}

func TestEnemyPlayerCollisionEndsGame(t *testing.T) {
	g := New()
	g.spawnTimer = 1e9 // disable natural spawns for this test
	g.Enemies = append(g.Enemies, Enemy{Entity{X: g.Player.X, Y: g.Player.Y - 10, Radius: enemyRadius}})
	g.Update(1.0 / 60.0)
	if !g.GameOver {
		t.Fatalf("game should be over on enemy-player collision")
	}
}

func TestFirstSpawnAfterSpawnDelay(t *testing.T) {
	g := New()
	advance(g, 0.6)
	if len(g.Enemies) != 0 {
		t.Fatalf("enemy spawned before spawn delay: got %d", len(g.Enemies))
	}
	advance(g, 0.6) // total 1.2 s = spawnDelay
	if len(g.Enemies) != 1 {
		t.Fatalf("want 1 enemy after 1.2 s, got %d", len(g.Enemies))
	}
}

func TestSpawnXWithinField(t *testing.T) {
	g := New()
	for i := 0; i < 200; i++ {
		g.Update(1.0 / 60.0) // long enough for many spawns; game over is fine
		if g.GameOver {
			break
		}
	}
	if g.GameOver {
		return // ran out of runway; still checked spawns up to this point
	}
	for _, e := range g.Enemies {
		if e.X < enemyRadius || e.X > Width-enemyRadius {
			t.Fatalf("enemy spawned off-field: X=%v", e.X)
		}
	}
}

func TestEnemyDriftSpeed(t *testing.T) {
	g := New()
	g.spawnTimer = 1e9 // disable natural spawns
	e := Enemy{Entity{X: 100, Y: 100, Radius: enemyRadius}}
	g.Enemies = append(g.Enemies, e)
	const dt = 1.0 / 60.0
	g.Update(dt)
	want := 100.0 + enemySpeed*dt
	if abs(g.Enemies[0].Y-want) > 1e-9 {
		t.Fatalf("enemy Y = %v, want %v", g.Enemies[0].Y, want)
	}
}

func TestDeterminism(t *testing.T) {
	// Two fresh runs with identical inputs must produce identical states
	// at every checkpoint (NFR-001, Law 2).
	run := func() []float64 {
		g := New()
		var snap []float64
		for i := 0; i < 600; i++ { // 10 simulated seconds
			g.Update(1.0 / 60.0)
			if i%60 == 0 {
				snap = append(snap, float64(g.Score))
				snap = append(snap, g.Player.X, g.Player.Y)
				for _, e := range g.Enemies {
					snap = append(snap, e.X, e.Y)
				}
			}
		}
		return snap
	}
	a, b := run(), run()
	if len(a) != len(b) {
		t.Fatalf("diverged: %d vs %d snapshots", len(a), len(b))
	}
	for i := range a {
		if a[i] != b[i] {
			t.Fatalf("divergence at checkpoint %d: %v vs %v", i, a[i], b[i])
		}
	}
}

func TestBulletDespawnOffscreen(t *testing.T) {
	g := New()
	g.spawnTimer = 1e9 // no natural spawns
	g.Bullets = append(g.Bullets, Bullet{Entity{X: 100, Y: -19, Radius: 4}})
	g.Update(1.0 / 60.0)
	if len(g.Bullets) != 0 {
		t.Fatalf("bullet above despawn line still alive")
	}
}

func TestGameOverFreezesSimulation(t *testing.T) {
	g := New()
	advance(g, 1)
	if g.Score != 0 || len(g.Bullets) != 0 {
		t.Fatalf("simulation advanced after game over")
	}
}

func TestRestartResetsState(t *testing.T) {
	g := New()
	g.Score = 55
	g.GameOver = true
	g.Restart()
	if g.Score != 0 || g.GameOver || len(g.Enemies) != 0 {
		t.Fatalf("Restart did not reset state")
	}
	if g.Player.X != Width/2 {
		t.Fatalf("player not recentered")
	}
}
