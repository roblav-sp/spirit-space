# Tasks — Procedural Wave Director

> Milestone M5. Spec: `specs/features/procedural-waves/spec.md`; plan:
> `plans/procedural-waves.md`.

## TASK-WAV-01 — Run metadata and seeded options
- **Objective:** `RunMetadata` is created once per run, immutable, and seeded via
  `Options.Seed`.
- **Requirement IDs:** FR-011.7, FR-011.8, BR-017, BC-12, AC-156, AC-159
- **Dependencies:** TASK-DFS-01
- **Files in scope:** `internal/game/metadata.go`, `internal/game/game.go`,
  `internal/game/metadata_test.go`
- **Constraints:** no wall-clock reads in `internal/game` (Law 2); seed comes in
  from `cmd/game`.
- **Expected tests:** `TestMetadataImmutable`, `TestRNGVersionRecorded`.
- **Verification evidence:** test output.
- **Out of scope:** selection logic.

## TASK-WAV-02 — Wave catalogue and validator
- **Objective:** a data catalogue of wave entries plus a validator enforcing
  clearance (120 px), corridor (48 px), caps and telegraph floor.
- **Requirement IDs:** FR-011.3, FR-011.4, FR-011.5, FR-011.10, AC-152,
  AC-153, AC-154
- **Dependencies:** TASK-WAV-01, TASK-FRM-02, TASK-DFS-04
- **Files in scope:** `internal/game/director.go`, `internal/game/director_test.go`
- **Constraints:** validator is pure; fallback wave always valid.
- **Expected tests:** `TestClearanceRule`, `TestCorridorRule`,
  `TestFallbackAlwaysAccepted`, `TestRejectRateBounded`.
- **Verification evidence:** test output.
- **Out of scope:** stage progression.

## TASK-WAV-03 — Stage progression and `VICTORY`
- **Objective:** waves per stage from the budget, 0.8 s inter-wave gap, boss
  stages 5/10/15/20, `VICTORY` after stage 20.
- **Requirement IDs:** FR-011.1, FR-011.6, FR-011.9, AC-155, AC-158
- **Dependencies:** TASK-WAV-02
- **Files in scope:** `internal/game/director.go`, `internal/game/state.go`,
  `internal/game/director_test.go`
- **Constraints:** no unbounded spawning; `VICTORY` freezes like `GAME_OVER`.
- **Expected tests:** `TestWavesPerStage`, `TestVictoryAfterStage20`.
- **Verification evidence:** test output.
- **Out of scope:** boss content (separate task file).

## TASK-WAV-04 — Replace the v0.1 spawner
- **Objective:** delete `spawnEnemies`/`spawnTimer`, re-point spawn tests at the
  director, keep `TestDeterminism` green.
- **Requirement IDs:** FR-011.2, AC-150, AC-151, AC-157
- **Dependencies:** TASK-WAV-03, TASK-FRM-03
- **Files in scope:** `internal/game/game.go`, `internal/game/game_test.go`,
  `internal/game/director.go`
- **Constraints:** separate commit from TASK-WAV-03 so a revert is clean; no
  test deleted without an equivalent replacement.
- **Expected tests:** `TestSeedReproducibility`,
  `TestSeedVariety`, `TestDirectorStepSizeIndependent`.
- **Verification evidence:** test output + `go build` for wasm.
- **Out of scope:** difficulty balancing (M9).

## TASK-WAV-05 — Golden RNG sequence
- **Objective:** freeze the first 10 waves for seed 1 in a test table so any
  accidental draw-order change fails; bumping `RNGVersion` is the only way to
  change it.
- **Requirement IDs:** FR-011.8, AC-159
- **Dependencies:** TASK-WAV-04
- **Files in scope:** `internal/game/director_test.go`
- **Constraints:** the table is generated once from the implementation and then
  reviewed by hand before committing.
- **Expected tests:** `TestGoldenWaveSequenceV1`.
- **Verification evidence:** test output.
- **Out of scope:** replay storage.
