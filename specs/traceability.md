# Traceability Matrix

> Requirements → feature spec → architecture → contract → source → tests.
> `TODO` = mapping not yet established; do not invent entries.
>
> **Rules.** `✔ verified` requires a named, executed test (or the named browser
> check). `partial` means some acceptance criteria are covered and others are
> not. Anything planned-in-words-only is `TODO`. **M1 changed documents only**:
> every v0.2 row below is `TODO` by construction, and no v0.1 row was upgraded.

## 1. Implemented (v0.1) — unchanged by M1

| Requirement | Feature spec | Architecture element | Contract | Source | Tests | Status |
|---|---|---|---|---|---|---|
| FR-001 | `player-control` | Sim (`updatePlayer`) | BC-3; bootstrap keys | `internal/game/game.go`, `cmd/game/main.go` | `TestPlayerClampedToField`, `TestFrameRateIndependence` | ✔ verified |
| FR-002 | `combat-scoring` | Sim (`updatePlayer` fire, `updateBullets`) | BC-4 | `internal/game/game.go` | `TestFireCooldown` | ✔ verified |
| FR-003 | `enemy-spawning` (**SUPERSEDED** by FR-010/FR-011) | `spawnEnemies`, `updateEnemies`, RNG | ADR-0003 | `internal/game/game.go` | `TestFirstSpawnAfterSpawnDelay`, `TestSpawnXWithinField`, `TestEnemyDriftSpeed` | ✔ verified (v0.1 behaviour only) |
| FR-004.1 | `combat-scoring` | `handleCollisions` | BC-6 | `internal/game/game.go` | `TestBulletDestroyedOnHitAndScored` | ✔ verified |
| FR-004.2 | `combat-scoring` | `draw` (score text) | — | `cmd/game/main.go` | manual / e2e "canvas animates" | partial |
| FR-004.3 (player contact) | `game-over-restart` | `handleCollisions` | BC-5 | `internal/game/game.go` | `TestEnemyPlayerCollisionEndsGame` | ✔ verified (superseded by FR-008 in v0.2) |
| FR-004.4 (bottom escape, renumbered) | `game-over-restart` | `handleCollisions` | BC-5 | `internal/game/game.go` | `TestEnemyReachingBottomEndsGame` | ✔ verified (superseded by FR-008 in v0.2) |
| FR-005.1 (banner) | `game-over-restart` | `draw` | BC-2 | `cmd/game/main.go` | e2e only (no pixel assertion) | **TODO** (AC-017 automating needs scripted play-through) |
| FR-005.2 (R inert while running) | `game-over-restart` | `cmd/game` key handler | bootstrap `KeyR` | `cmd/game/main.go` | e2e `input: KeyR while running does not crash or reset` | ✔ verified (browser) |
| FR-005.3 (R restarts, renumbered) | `game-over-restart` | `Restart` | BC-7 | `internal/game/game.go` | `TestRestartResetsState` + e2e | partial (banner flow manual) |
| BR-002 | `product.md` §4 (**SUPERSEDED** by BR-010) | `scorePerKill` | BC-6 | `internal/game/game.go` | `TestBulletDestroyedOnHitAndScored` | ✔ verified (v0.1 behaviour) |
| BR-003 | `product.md` §4 | `updatePlayer` | BC-4 | `internal/game/game.go` | `TestFireCooldown` | ✔ verified |
| BR-005 | `combat-scoring` | `handleCollisions` | BC-6 | `internal/game/game.go` | inspection (no multi-enemy test) | partial |
| BR-006 | `enemy-spawning` | `Game.rng` | ADR-0003 | `internal/game/game.go` | `TestDeterminism` | ✔ verified |
| BR-007 | `game-over-restart` | `handleCollisions` early return | BC-2 | `internal/game/game.go` | inspection | partial |
| BR-008 (renumbered from BR-005) | `player-control` | `updatePlayer` | BC-3 | `internal/game/game.go` | `TestFrameRateIndependence` | ✔ verified |
| NFR-001 | `product.md` | `Game.rng` | BC-1 | `internal/game/game.go` | `TestDeterminism` | ✔ verified |
| NFR-002 | `product.md` | `Update` dt model | BC-1 | `internal/game/game.go` | `TestFrameRateIndependence` | ✔ verified |
| NFR-003 | `product.md` | `components.md` | Laws 1, 6 | `go.mod` (no requires) | `go build` + review | ✔ verified |
| NFR-004 | `product.md` | `context.md` | bootstrap | `cmd/game/main.go`, `index.html` | inspection | ✔ (inspection) |
| SEC-001, SEC-002 | `product.md` | `context.md` trust boundary | bootstrap | whole repo | inspection | ✔ (inspection) |
| BC-1 … BC-7 | `simulation-api.md` | — | — | `internal/game/game.go` | BC-2/3/4/7 tested; BC-5 partial; BC-1/BC-6 inspection | partial |
| Bootstrap contract | `bootstrap.md` | `context.md`, `components.md` | — | `index.html`, `cmd/game/main.go` | e2e suite | ✔ verified (browser) |
| Law 7 (visible boot errors) | `constitution.md` §2 | `context.md` | `bootstrap.md` | `index.html` | e2e `law7: broken wasm shows visible error banner` | ✔ verified (browser) |
| AC-011 | `combat-scoring` | `updateBullets` | BC-5 | `internal/game/game.go` | `TestBulletDespawnOffscreen` | ✔ verified |
| AC-004 (diagonal, non-normalised) | `player-control` | `updatePlayer` | BC-3 | `internal/game/game.go` | **none dedicated** | **TODO** |
| §5 gates (gofmt/vet/test/build) | `constitution.md` §5 | — | — | repo | `go vet ./...` and `go test ./...` **fail natively** (audit §2) | **TODO** — `TASK-INFRA-01` |

## 2. Planned (v0.2) — all `TODO`

Feature spec paths are under `specs/features/`; ADRs under `specs/decisions/`.
Source paths are the planned components from `specs/architecture/components.md`;
none of them exist yet.

### 2.1 Main menu and pause (`main-menu/spec.md`, ADR-0010)

| Req | Feature spec | Architecture element | Contract | Source (planned) | Tests (planned) | Status |
|---|---|---|---|---|---|---|
| FR-006.1 … FR-006.12 | `main-menu` | `state.go`, `menu.go` | BC-8; bootstrap v0.2 keys | `internal/game/state.go`, `cmd/game/main.go` | AC-101 … AC-110 | **TODO** |
| FR-009 (pause) | `main-menu` | `state.go` | BC-8 | `internal/game/state.go` | AC-105, AC-106, AC-129 | **TODO** |
| AC-107 (quit to menu) | `main-menu` | `state.go` | BC-8 | `internal/game/state.go` | — | **TODO** |
| AC-108 (blur clears keys) | `main-menu` | `cmd/game` listeners | bootstrap v0.2 | `cmd/game/main.go` | browser check | **TODO** |
| AC-110 (preventDefault) | `main-menu` | `cmd/game` listeners | bootstrap v0.2 | `cmd/game/main.go` | browser check | **TODO** |

### 2.2 Lives and respawn (`lives-respawn/spec.md`)

| Req | Feature spec | Architecture element | Contract | Source (planned) | Tests (planned) | Status |
|---|---|---|---|---|---|---|
| FR-008.1 … FR-008.10 | `lives-respawn` | `lives.go` | BC-10 | `internal/game/lives.go` | AC-120 … AC-129 | **TODO** |
| BR-009, BR-013 | `lives-respawn` | `lives.go` | BC-10 | `internal/game/lives.go` | AC-120, AC-122 | **TODO** |
| FR-004.3/FR-004.4 supersession | `game-over-restart` → `lives-respawn` | `lives.go` | BC-10 | — | AC-121, AC-125, AC-126 | **TODO** |
| D-2 (bottom escape) | `lives-respawn` (decided: harmless) | — | — | — | AC-125 | **TODO** (decision recorded 2026-11-12) |

### 2.3 Difficulty and speed (`difficulty-speed/spec.md`, ADR-0012)

| Req | Feature spec | Architecture element | Contract | Source (planned) | Tests (planned) | Status |
|---|---|---|---|---|---|---|
| FR-007.1 … FR-007.9 | `difficulty-speed` | `difficulty.go`, accumulator in `cmd/game` | BC-9, BC-11 | `internal/game/difficulty.go` | AC-130 … AC-139 | **TODO** |
| BR-011 | `difficulty-speed` | `difficulty.go` | BC-11 | — | AC-132 | **TODO** |
| BR-012 (fixed step) | `difficulty-speed` | `Step`/`Advance` | BC-9 | `internal/game/game.go` | AC-133, AC-135 | **TODO** |
| NFR-002 (restated) | `difficulty-speed` | accumulator | BC-9 | `cmd/game/main.go` | AC-133 | **TODO** |

### 2.4 Formations and archetypes (`formation-ai/spec.md`)

| Req | Feature spec | Architecture element | Contract | Source (planned) | Tests (planned) | Status |
|---|---|---|---|---|---|---|
| FR-010.1 … FR-010.9 | `formation-ai` | `formation.go` | BC-11 | `internal/game/formation.go` | AC-140 … AC-149 | **TODO** |
| BR-006/BR-017 (draws) | `procedural-waves` | `director.go` | BC-12 | `internal/game/director.go` | AC-146, AC-150 | **TODO** |

### 2.5 Wave director (`procedural-waves/spec.md`, ADR-0009)

| Req | Feature spec | Architecture element | Contract | Source (planned) | Tests (planned) | Status |
|---|---|---|---|---|---|---|
| FR-011.1 … FR-011.10 | `procedural-waves` | `director.go` | BC-12 | `internal/game/director.go` | AC-150 … AC-159 | **TODO** |
| BR-017 (run metadata) | `procedural-waves` | `RunMetadata` | BC-12 | `internal/game/director.go` | AC-156, AC-159 | **TODO** |
| `VICTORY` state | `procedural-waves` | `state.go` | BC-8 | `internal/game/state.go` | AC-158 | **TODO** |

### 2.6 Weapons and power-ups (`weapons-powerups/spec.md`)

| Req | Feature spec | Architecture element | Contract | Source (planned) | Tests (planned) | Status |
|---|---|---|---|---|---|---|
| FR-012.1 … FR-012.10 | `weapons-powerups` | `weapons.go` | BC-13 | `internal/game/weapons.go` | AC-160 … AC-169 | **TODO** |
| BR-016 | `weapons-powerups` | `weapons.go` | BC-13 | — | AC-165, AC-166 | **TODO** |
| AC-162 damage decision | `weapons-powerups` open question | — | — | — | AC-162 | **BLOCKED** on owner |

### 2.7 Scoring, high scores, settings (`scoring-highscores/spec.md`)

| Req | Feature spec | Architecture element | Contract | Source (planned) | Tests (planned) | Status |
|---|---|---|---|---|---|---|
| FR-013.1 … FR-013.6 | `scoring-highscores` | `score.go` | BC-14 | `internal/game/score.go` | AC-170 … AC-173 | **TODO** |
| FR-014.1 … FR-014.8 | `scoring-highscores` | `score.go`, `persist.go`, `cmd/game/storage.go` | BC-14, BC-16; `persistence.md` | `internal/game/persist.go` | AC-174 … AC-179b | **TODO** |
| BR-010 | `scoring-highscores` | `score.go` | BC-14 | — | AC-170, AC-171 | **TODO** |
| BR-015, SEC-003 | `scoring-highscores` | storage bridge | `persistence.md` | `cmd/game/storage.go` | AC-174, AC-175 | **TODO** (Amendment 001 ratified 2026-11-12) |
| NFR-008 (store interface) | `scoring-highscores` | `Store` | BC-16 | `internal/game/persist.go` | fake-store tests | **TODO** |

### 2.8 Audio and assets (`audio-assets/spec.md`, ADR-0011/0013)

| Req | Feature spec | Architecture element | Contract | Source (planned) | Tests (planned) | Status |
|---|---|---|---|---|---|---|
| FR-016.1 … FR-016.7 | `audio-assets` | `cmd/game/audio.go`, `internal/game/sound.go` | BC-15; `assets.md` | `cmd/game/audio.go` | AC-180 … AC-182 | **TODO** |
| FR-017.1 … FR-017.6 | `audio-assets` | `cmd/game/assets.go` | `assets.md` | `cmd/game/assets.go` | AC-183 … AC-189 | **TODO** |
| BR-018, SEC-004 | `audio-assets` | manifest + importer | `assets.md` | `scripts/download_assets.py`, `assets/asset-manifest.json` | importer tests (`scripts/tests/`) | **TODO** (importer validated, packs not imported) |
| NFR-006 (budgets) | `audio-assets` | manifest totals | `assets.md` | `docs/ASSET_MANIFEST.md` | AC-186 | **TODO** |
| NFR-007 (a11y) | `main-menu`, `audio-assets` | canvas drawing | — | `cmd/game/main.go` | manual + contrast check | **TODO** |

### 2.9 Bosses (`bosses/spec.md`)

| Req | Feature spec | Architecture element | Contract | Source (planned) | Tests (planned) | Status |
|---|---|---|---|---|---|---|
| FR-015.1 … FR-015.9 | `bosses` | `formation.go`, `director.go` | BC-11, BC-12 | `internal/game/boss.go` | AC-190 … AC-199 | **TODO** |
| BR-014 | `bosses` | `director.go` | BC-12 | — | AC-190 | **TODO** |

### 2.10 Process requirements

| Requirement | Where | Evidence | Status |
|---|---|---|---|
| FR-004.2 score/HUD rendering extended for v0.2 | `scoring-highscores` | AC-173 HUD assertions | **TODO** |
| NFR-005 (60 FPS measured) | `product.md` §5 | M9 measurement note | **TODO** |
| Amendment 001 ratified | `docs/constitution-amendment-001.md`, `constitution.md` §1/§6 | approval record filled; §1/§6 amended | ✔ verified (documented) |
| `LICENSE` + `CREDITS.md` | audit D-5 | files exist | **TODO** |

## 3. Remaining follow-ups (carried over)

1. **TODO** — AC-017 (game-over banner) and full FR-005 restart flow are
   verified manually only; automating needs scripted play-to-game-over.
2. **TODO** — BC-1/BC-6 semantic guarantees verified by inspection only.
3. **TODO** — AC-004 (diagonal speed, non-normalised) has no dedicated test.
4. **TODO** — Rendering frame-rate independence is not verified (out of scope).
5. **TODO** — `TASK-INFRA-01`: make `go vet ./...` and `go test ./...` pass
   natively (audit §2, owner decision D-6).

## 4. Status summary

- Verified (v0.1): 15 rows.
- Partial: 5 rows.
- TODO (v0.2 + process): 60+ rows, listed above.
- Decided: D-1 (amendment ratified), D-2 (escape harmless).
- Still open: spread damage split (M6), D-3 ID corrections, D-4 scoring
  supersession approval, D-5 `LICENSE`/`CREDITS`, D-6 `TASK-INFRA-01`.
