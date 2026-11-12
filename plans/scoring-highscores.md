# Plan — Scoring, High Scores, and Settings

> Implements FR-013, FR-014, BR-010, BR-015, SEC-003, AC-170…AC-179b
> (`specs/features/scoring-highscores/spec.md`). Milestone **M7**.
> ADR-0007; blocked on `docs/constitution-amendment-001.md` for persistence.

## Requirements being implemented
Class/wave/combo scoring, ranking with tie-breakers, settings model, versioned
codec, storage bridge, degraded modes.

## Architecture components affected
- `internal/game` — new `score.go` (awards, combo window, table ordering),
  `persist.go` (encode/decode + validation over `Store`/`io.Reader`).
- `cmd/game` — `storage.go` native `localStorage` bridge; High Scores and Sound
  screens draw from the tables.

## Contracts affected
`simulation-api.md` (BC-14, BC-16, `Store`), `persistence.md` (both documents),
bootstrap (new `localStorage` surface + failure mode).

## Files or modules likely to change
`internal/game/score.go`, `internal/game/persist.go`,
`internal/game/score_test.go`, `internal/game/persist_test.go`,
`cmd/game/storage.go`, `cmd/game/main.go`.

## Dependency order
1. Score awards + combo (pure; no storage). 
2. Ranking table + tie-breakers (pure).
3. Codec v1 + validation + fuzz-ish table of hostile payloads (pure).
4. `Store` interface + in-memory implementation (pure).
5. `cmd/game/storage.go` bridge, only if amendment 001 is ratified.
6. Settings model + menu wiring (depends on M2).
7. High Scores screen + "clear saved data" action.

## Data migrations
None: v0.1 stored nothing. Unknown schema versions are discarded (SEC-003).

## Testing strategy
- Unit: AC-170…AC-179b entirely browser-free via a fake `Store`.
- Hostile input table: empty string, `null`, truncated JSON, huge array,
  negative score, non-integer, wrong difficulty string, oversized alias,
  invalid UTF-8 bytes, schema 999. Each asserts "defaults, no panic".
- Browser: real `localStorage` round-trip and quota failure (private mode is
  hard to simulate reliably → two checks: round-trip, and a forced
  `setItem` throw via an init script).

## Rollout / rollback
Ships in two independently revertible pieces: (a) in-memory scoring/ranking,
(b) persistence. If the amendment is declined, ship (a) only; the High Scores
screen states scores are not saved.

## Risks and mitigations
- **Scope creep into accounts/leaderboards** → SEC-003 bounds the keys; any
  network call fails review.
- **Corrupt data bricking the menu** → every read path returns defaults and
  exactly one warning; covered by the hostile-input table.
- **Alias entry requiring text input** → use a cycling 3-letter preset until a
  text-input spec exists (open question in the spec).
