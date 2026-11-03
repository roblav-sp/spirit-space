# Traceability Matrix

> Requirements → feature spec → architecture → contract → source → tests.
> `TODO` = mapping not yet established; do not invent entries.

| Requirement | Feature spec | Architecture element | Contract | Source | Tests | Status |
|---|---|---|---|---|---|---|
| FR-001 | `specs/features/player-control/spec.md` | Simulation (`updatePlayer`) | simulation-api BC-3; bootstrap (movement keys) | `internal/game/game.go`, `cmd/game/main.go` | `TestPlayerClampedToField`, `TestFrameRateIndependence` | ✔ verified |
| FR-002 | `specs/features/combat-scoring/spec.md` | Simulation (`updatePlayer` fire, `updateBullets`) | simulation-api BC-4 | `internal/game/game.go` | `TestFireCooldown` | ✔ verified |
| FR-003 | `specs/features/enemy-spawning/spec.md` | Simulation (`spawnEnemies`, `updateEnemies`, RNG) | simulation-api; ADR-0003 | `internal/game/game.go` | `TestFirstSpawnAfterSpawnDelay`, `TestSpawnXWithinField`, `TestEnemyDriftSpeed` | ✔ verified |
| FR-004 | `specs/features/combat-scoring/spec.md` + `specs/features/game-over-restart/spec.md` | `handleCollisions` | simulation-api BC-5, BC-6 | `internal/game/game.go` | `TestBulletDestroyedOnHitAndScored`, `TestEnemyReachingBottomEndsGame`, `TestEnemyPlayerCollisionEndsGame` | ✔ verified |
| FR-005 | `specs/features/game-over-restart/spec.md` | `Update` guard + `Restart`; KeyR in `cmd/game` | simulation-api BC-2, BC-7; bootstrap (KeyR) | `internal/game/game.go`, `cmd/game/main.go` | `TestGameOverFreezesSimulation`, `TestRestartResetsState`; banner + R manual | ✔ verified (AC-017 manual) |
| BR-001..BR-007 | product.md + feature specs | — | simulation-api | `internal/game/game.go` | BR-002 (`TestBulletDestroyedOnHitAndScored`), BR-001 via AC-013/013; others by code inspection | ✔ / partial |
| NFR-001 | product.md | `Game.rng` (ADR-0003) | simulation-api BC-1 | `internal/game/game.go` | `TestDeterminism` | ✔ verified |
| NFR-002 | product.md | `Update` dt model | simulation-api BC-1 | `internal/game/game.go` | `TestFrameRateIndependence` | ✔ verified |
| NFR-003 | product.md | components.md | constitution Laws 1, 6 | `go.mod` (no requires) | `go build` + review | ✔ verified |
| NFR-004 | product.md | context.md | bootstrap contract | `cmd/game/main.go`, `index.html` | code inspection | ✔ (inspection) |
| SEC-001, SEC-002 | product.md | context.md (trust boundary) | bootstrap contract | whole repo | code inspection | ✔ (inspection) |
| BC-1..BC-7 | — | simulation-api.md | — | `internal/game/game.go` | BC-2, BC-3, BC-4, BC-7 covered; BC-5 partial; BC-1/BC-6 inspection | partial |
| Bootstrap contract | — | context.md, components.md | bootstrap.md | `index.html`, `cmd/game/main.go` | manual only | ✔ (manual) |
| Law 7 (visible bootstrap errors) | constitution §2 | context.md | bootstrap.md | `index.html` | e2e `law7: broken wasm shows visible error banner` (skill browser-verify) | ✔ verified (automated) |
| AC-011 | `specs/features/combat-scoring/spec.md` | `updateBullets` | simulation-api BC-5 | `internal/game/game.go` | `TestBulletDespawnOffscreen` | ✔ verified |

## Gaps requiring follow-up tasks

Resolved in this round (moved out of the TODO list):
- Spawn behavior tests (AC-005…AC-008) — now encoded as
  `TestFirstSpawnAfterSpawnDelay`, `TestSpawnXWithinField`,
  `TestEnemyDriftSpeed`.
- Determinism (NFR-001) — now `TestDeterminism`.
- Law 7 — now automated in the `browser-verify` skill
  (`.agents/skills/browser-verify/`, ADR-0005).

Remaining follow-ups:

1. **TODO** — AC-017 (game-over banner) and full FR-005 restart flow still
   verified manually only; automating requires scripted play-to-game-over
   (future skill extension).
2. **TODO** — BC-1/BC-6 semantic guarantees verified by inspection only.
3. **TODO** — AC-004 (diagonal speed, non-normalized) has no dedicated test.
4. **TODO** — Frame-rate independence of *rendering* (not simulation) is not
   verified; currently accepted as out of scope.
