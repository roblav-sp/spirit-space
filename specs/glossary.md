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

## v0.2 terms (planned features)

| Term | Definition |
|---|---|
| **State** | Top-level screen/phase owned by `internal/game`: `MAIN_MENU`, `PLAYING`, `PAUSED`, `PLAYER_DYING`, `RESPAWNING`, `GAME_OVER`, `VICTORY`, plus menu sub-screens. |
| **Difficulty** | Budget level `Rookie/Pilot/Ace/Legend`; changes threat density, never movement per world second. |
| **Speed scale** | Multiplier on world-time accrual (`0.75/1.0/1.25`); scales all timers together (ADR-0012). |
| **World time** | Simulated seconds; advances only by fixed steps and only outside `PAUSED`, `GAME_OVER`, `VICTORY`. |
| **Fixed step** | The single simulation tick, `1/60 s` (BR-012). |
| **Stage** | Bounded group of waves; stage 5, 10, 15, 20 are boss stages; stage 20 completion is `VICTORY`. |
| **Wave** | One formation instance with a begin and a completion condition. |
| **Formation** | Named slot template (`row`, `V`, `diagonal`, `zigzag`, `dive`, `flank`, `bonus`) and its motion rules. |
| **Archetype** | Enemy class (`scout`, `interceptor`, `heavy`, `sniper`, `boss`) with HP, score, projectile and behaviour. |
| **Telegraph** | A visible warning of fixed minimum duration that precedes a dive, phase change or attack. |
| **Safe corridor** | A guaranteed ≥48 px gap through a projectile pattern, checked by the wave validator. |
| **Life** | One of 3 per run; a damage event costs at most one (BR-009). |
| **Damage event** | One applied hazard: enemy body or enemy projectile only. Bottom escape is harmless (D-2). |
| **Invulnerability** | Post-respawn window (1.5 s) in which hazards deal no damage and are not consumed. |
| **Power-up** | Timed weapon or defence pickup (`rapid`, `spread`, `shield`, `beam`); never removes the base weapon. |
| **Combo** | Consecutive-kill multiplier (`×1.00…×5.00`, +0.25 per kill inside a 2 s window). |
| **Run metadata** | Immutable `(seed, RNG version, difficulty, speed)` tuple recorded per run (BR-017). |
| **RNG version** | Integer tag for the director's draw sequence; bumping it is a deliberate compatibility event (ADR-0009). |
| **Memory-only mode** | Persistence fallback: scores/settings live for the session, nothing is written (FR-014.3). |
| **Logical asset ID** | Stable string (`ship.player`, `sfx.shoot`) used by code; maps to a file via the catalog, never hardcoded. |
| **Asset manifest** | `assets/asset-manifest.json` — machine record of pack provenance, SHA-256 checksums and license review flags (SEC-004). |
| **Fallback** | The geometric primitive or silence used when an asset is absent, undecodable or unmapped (FR-017.3). |
