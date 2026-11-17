# Tasks — Audio and Asset Integration

> Milestone M8. Spec: `specs/features/audio-assets/spec.md`; plan:
> `plans/audio-assets.md`. The importer itself is M1 (already validated).

## TASK-AUD-01 — Sound events in the simulation
- **Objective:** emit typed `SoundEvent`s for the spec'd triggers into a bounded
  queue, deterministically, with no DOM types.
- **Requirement IDs:** FR-016.3, FR-016.7, BC-15, AC-180 (precondition)
- **Dependencies:** TASK-LIV-03, TASK-WPN-03
- **Files in scope:** `internal/game/sound.go`, `internal/game/game.go`,
  `internal/game/sound_test.go`
- **Constraints:** ≤16 events per frame, oldest dropped; no audio waits; paused
  produces no events.
- **Expected tests:** `TestSoundEventSequence`, `TestSoundQueueBound`.
- **Verification evidence:** test output.
- **Out of scope:** playback.

## TASK-AUD-02 — WebAudio engine with buses and unlock
- **Objective:** three buses, master×bus gain, one `AudioContext` created on the
  first `keydown`, mute, and silent degradation.
- **Requirement IDs:** FR-016.1, FR-016.2, FR-016.5, FR-016.6, AC-180,
  AC-181, AC-182
- **Dependencies:** TASK-AUD-01
- **Files in scope:** `cmd/game/audio.go`, `cmd/game/main.go`
- **Constraints:** no `AudioContext` before a gesture; one console warning total
  on failure.
- **Expected tests:** browser `audio: unlock on first key`, `audio: silent
  without AudioContext` (init script deletes the constructor).
- **Verification evidence:** browser PASS lines.
- **Out of scope:** music tracks (TASK-AUD-04).

## TASK-AUD-03 — Asset table with proven fallback
- **Objective:** logical IDs resolve through an empty-by-default catalog; every
  draw site falls back to its primitive; missing/undecodable assets warn once.
- **Requirement IDs:** FR-017.1 … FR-017.4, AC-183, AC-184, AC-189
- **Dependencies:** none (can start before any asset exists)
- **Files in scope:** `cmd/game/assets.go`, `cmd/game/main.go`
- **Constraints:** fallback is permanent, not temporary; one warning per ID;
  same-origin only.
- **Expected tests:** `TestAssetIDsMatchFallbacks` (native table compare),
  browser `assets: missing sprite falls back`.
- **Verification evidence:** test + browser PASS.
- **Out of scope:** importing packs.

## TASK-AUD-04 — Import packs, map IDs, music
- **Objective:** human-imported packs recorded in the manifest, IDs mapped to
  real files, three music loops wired and cross-faded.
- **Requirement IDs:** FR-016.4, FR-017.5, FR-017.6, BR-018, SEC-004, AC-186,
  AC-187, AC-188
- **Dependencies:** TASK-AUD-02, TASK-AUD-03, owner approval of asset licenses
- **Files in scope:** `assets/vendor/**`, `assets/asset-manifest.json`,
  `cmd/game/assets.go`, `cmd/game/audio.go`, `docs/ASSET_MANIFEST.md`,
  `.gitignore`, `README.md`
- **Constraints:** never guess ZIP URLs; commit assets only after license
  review; budgets in the contract; no CDN.
- **Expected tests:** `TestManifestBudget`, browser `network: same-origin only`.
- **Verification evidence:** importer output + `.agents/skills/browser-verify/scripts/verify.sh` PASS +
  manifest totals.
- **Out of scope:** original music composition, sprite atlases.

## TASK-AUD-05 — Music sourcing decision (`music.menu`, `music.stage`, `music.boss`)
- **Objective:** decide and document where the three music tracks come from, or
  amend the spec to make music optional, then add the chosen pack to
  `scripts/download_assets.py` `PACKS` with its official page.
- **Requirement IDs:** FR-016.4 (per-state music, ≤300 ms cross-fade),
  `specs/contracts/assets.md` (IDs + budgets)
- **Dependencies:** owner decision (OPEN — see `tasks/index.md`)
- **Files in scope (after the decision only):** `specs/features/audio-assets/spec.md`
  (§Open questions), `specs/contracts/assets.md`,
  `scripts/download_assets.py` (`PACKS`), `docs/ASSET_MANIFEST.md` §5
- **Constraints:** no invented ZIP URL; no invented license verdict; the
  silence fallback (FR-016.6) stays valid if music is dropped.
- **Expected tests:** none until a pack exists; then `--check` plus the budget
  test (`TestManifestBudget`).
- **Verification evidence:** the decision recorded in the feature spec, and
  `python3 scripts/download_assets.py --list` showing the added pack.
- **Out of scope:** composing original music.

> **Gap this task closes.** None of the eight packs already in `PACKS` contains
> loopable stage music, so `music.*` currently has no legal source. Do not add a
> ninth pack before the spec says which one and why.
