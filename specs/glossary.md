# Glossary

Single source of truth for terms. Other documents reference, never redefine.

| Term | Definition |
|---|---|
| **Simulation** | The pure game logic in `internal/game`: state + `Update(dt)`. No DOM access. |
| **World** | The fixed 800×600 coordinate space (`game.Width`, `game.Height`). Origin top-left, +y down. |
| **Entity** | Positioned object with a bounding circle: `X, Y, Radius, Dead`. |
| **Player** | The ship. Radius 16, starts at (Width/2, Height−80). |
| **Enemy** | Entity that spawns at the top edge and drifts down. Radius 16. |
| **Bullet** | Projectile fired upward by the player. Radius 4. |
| **Fire cooldown** | Minimum time (0.2 s) between shots. Starts at 0, so the first shot is immediate. |
| **Spawn delay** | Fixed interval (1.2 s) between enemy spawns in v0.1. |
| **Game over** | Terminal state after a lethal event; simulation freezes; only R (restart) acts. |
| **Restart** | Full reset of game state (score 0, player recentered, empty arrays). |
| **Run** | One play session from `New()`/`Restart()` until game over. |
| **Score** | Points accumulated; +10 per destroyed enemy (BR-002). |
| **WASM glue** | `wasm_exec.js` + the bootstrap script in `index.html`; loads and runs `main.wasm`. |
| **Play field** | The world area the player is clamped to; same as the world (Law 3). |
| **Context pack** | The minimal set of docs+code loaded for a task (see `ai-development-guide.md`). |
