# Spirit Space — Gameplay Spec

> **Status: SUPERSEDED.** The authoritative gameplay specs now live in
> `specs/features/` and `specs/product.md`. This file is kept for history and
> must obey the Constitution (`@../constitution.md`); if it conflicts, the
> Constitution and the feature specs win.
> Every tunable below is a starting value, not a promise.

## 1. Core loop

The player pilots a ship at the bottom of the screen. Enemies drift down from
the top. Shooting enemies scores points. If an enemy reaches the player or
collides with the ship, the game ends. One life, no continues.

## 2. Controls

| Input        | Action                    |
|--------------|---------------------------|
| ← / → / ↑ / ↓ (or A/D/W/S) | Move ship  |
| Space        | Fire bullet               |
| R            | Restart after game over   |

## 3. Player

- Moves in all 4 directions, clamped to the play field.
- Fires straight up, one bullet per shot, limited by a cooldown.
- Colliding with an enemy ends the game.

## 4. Enemies

- Spawn at random X positions along the top edge.
- Drift straight down at constant speed.
- Reaching the bottom edge or touching the player ends the game.
- One hit from a bullet destroys an enemy.

## 5. Bullets

- Travel straight up, despawn off-screen.
- No ammo limit; cooldown is the only constraint.

## 6. Scoring

- +10 per enemy destroyed.
- Score is displayed on the canvas; no high-score persistence (Law 1, no
  storage outside the page).

## 7. Difficulty

- Spawn interval starts at 1.2 s and stays constant in v0.1.
- Enemy speed is constant in v0.1.
- (Future: ramp spawn rate and speed with elapsed time.)

## 8. Tuning table

| Parameter    | Value | Where defined            |
|--------------|-------|--------------------------|
| World size   | 800×600 | `game.Width/Height` (fixed by Law 3) |
| Player speed | 300 px/s | `internal/game` const |
| Bullet speed | 500 px/s | `internal/game` const |
| Enemy speed  | 120 px/s | `internal/game` const |
| Fire cooldown| 0.2 s  | `internal/game` const   |
| Spawn delay  | 1.2 s  | `internal/game` const   |
| Score/kill   | 10     | `internal/game`         |
