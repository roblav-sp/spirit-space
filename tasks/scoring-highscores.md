# Tasks — Scoring, High Scores, and Settings

> Milestone M7. Spec: `specs/features/scoring-highscores/spec.md`; plan:
> `plans/scoring-highscores.md`. Persistence tasks are blocked on
> `docs/constitution-amendment-001.md`.

## TASK-SCR-01 — Class, wave, and combo scoring
- **Objective:** class scores, wave-clear bonus, combo multiplier with 2 s
  window and ×5 cap, no score for contact kills.
- **Requirement IDs:** FR-013.1 … FR-013.5, BR-010, AC-170 … AC-173, AC-179b
- **Dependencies:** TASK-FRM-01, TASK-WAV-03
- **Files in scope:** `internal/game/score.go`, `internal/game/game.go`,
  `internal/game/score_test.go`
- **Constraints:** multiplier applies to class score only; +10 stays the basic
  default.
- **Expected tests:** `TestClassScores`, `TestWaveBonusOnce`,
  `TestComboWindowAndCap`, `TestNoScoreOnContact`.
- **Verification evidence:** test output.
- **Out of scope:** ranking tables.

## TASK-SCR-02 — Ranking table with tie-breakers
- **Objective:** top-10 per `(difficulty, speed)` with score desc, stage desc,
  insertion-stable ordering.
- **Requirement IDs:** FR-014.1, FR-014.8, AC-177, AC-178
- **Dependencies:** TASK-SCR-01
- **Files in scope:** `internal/game/score.go`, `internal/game/score_test.go`
- **Constraints:** pure function; no storage types.
- **Expected tests:** `TestRankingOrder`, `TestTablePerSetting`,
  `TestEleventhEntryDropped`.
- **Verification evidence:** test output.
- **Out of scope:** persistence.

## TASK-SCR-03 — Versioned codec and hostile-input table
- **Objective:** encode/decode both documents; reject wrong schema, oversized,
  out-of-range or malformed payloads with defaults and no panic.
- **Requirement IDs:** FR-014.4, FR-014.5, SEC-003, BC-16, AC-174, AC-179
- **Dependencies:** TASK-SCR-02
- **Files in scope:** `internal/game/persist.go`,
  `internal/game/persist_test.go`
- **Constraints:** `Store` interface only; no `js.Value`; ≤64 KiB; alias
  sanitisation without breaking UTF-8.
- **Expected tests:** `TestCodecRoundTrip`, `TestHostilePayloads` (table of ≥10
  cases), `TestAliasSanitisation`.
- **Verification evidence:** test output.
- **Out of scope:** `localStorage` binding.

## TASK-SCR-04 — Storage bridge behind the amendment gate
- **Objective:** `cmd/game/storage.go` implements `Store` over `localStorage`
  when amendment 001 is ratified, and an in-memory store otherwise; exceptions
  degrade with one warning.
- **Requirement IDs:** FR-014.3, FR-014.6, FR-014.7, BR-015, AC-175, AC-176
- **Dependencies:** TASK-SCR-03; Amendment 001 **RATIFIED 2026-11-12**
- **Files in scope:** `cmd/game/storage.go`, `cmd/game/main.go`
- **Constraints:** never enumerates keys; never writes outside the two keys;
  exactly one warning per session (Law 7 spirit).
- **Expected tests:** native fake-store tests (present already), browser
  round-trip + forced `setItem` throw.
- **Verification evidence:** test output + browser PASS.
- **Out of scope:** any network/database path.
- **Unblocked by:** D-1 (Amendment 001 ratified).

## TASK-SCR-05 — High Scores and Sound screens
- **Objective:** render the table (empty state, per-setting tabs) and the
  settings controls including "clear saved data" when persistence is active.
- **Requirement IDs:** FR-014.1, FR-014.2, FR-014.6, AC-176, AC-178
- **Dependencies:** TASK-SCR-02, TASK-MNU-04, TASK-SCR-04
- **Files in scope:** `cmd/game/main.go`, `internal/game/menu.go`
- **Constraints:** read-only views; keyboard only.
- **Expected tests:** browser smoke + manual note.
- **Verification evidence:** `.agents/skills/browser-verify/scripts/verify.sh` PASS.
- **Out of scope:** alias text entry (preset cycling only).
