# Feature — Scoring, Combo, High Scores and Settings

> Implements FR-013 and FR-014. Supersedes BR-002 (single score source).
> Persistence is conditional on `docs/constitution-amendment-001.md` (ADR-0007);
> memory-only is the mandatory baseline.

## Context
v0.1 awards +10 per kill and nothing else. v0.2 rewards skill (combos, clean
waves, class targets) and gives runs a place to land: a local ranking table per
difficulty/speed, plus remembered settings.

## Actors
Player, Simulation (scoring), `cmd/game` (storage I/O), Renderer (HUD, tables).

## Preconditions
`PLAYING` for scoring; `GAME_OVER`/`VICTORY` for table insertion.

## Functional requirements

### Scoring (FR-013)
- **FR-013.1** — Basic enemy kill = **10** points (unchanged default, BR-010).
- **FR-013.2** — Class scores: scout 10, interceptor 20, sniper 30, heavy 50,
  boss `500 × stageNumber` (capped at 5000).
- **FR-013.3** — Cleared-wave bonus: `100 × stageNumber` awarded once per wave
  in which every enemy was destroyed (not escaped); `bonus` template doubles it.
- **FR-013.4** — Combo: kills within a 2.0 s window increase the multiplier by
  +0.25, starting at ×1.00 and capped at ×5.00; the window resets on damage
  taken or on timeout. Multiplier applies to enemy class score only, not to
  wave or boss bonuses.
- **FR-013.5** — Kills by collision (enemy neutralised by hitting the player)
  award **no** score.
- **FR-013.6** — The HUD shows score, current multiplier (with a decay ring or
  bar) and stage.

### High scores and settings (FR-014)
- **FR-014.1** — Ranking: best **10** runs per `(difficulty, speed)` pair, each
  entry `{Alias, Score, Stage, Difficulty, Speed, Seed}`; aliases are optional
  and default to empty (rendered as `---`).
- **FR-014.2** — Settings: difficulty, speed, master/music/SFX volume, mute.
- **FR-014.3** — Without the amendment, both live in memory for the session and
  the High Scores screen states that scores are not saved.
- **FR-014.4** — With the amendment: two `localStorage` keys
  (`spirit-space.scores.v1`, `spirit-space.settings.v1`), versioned schema,
  ≤64 KiB total, written only on run end / settings change.
- **FR-014.5** — All reads are untrusted: bounded parse, schema version check,
  range validation (score 0…1e9, stage 1…20, alias ≤16 runes with control
  characters stripped), and a clean fallback on any mismatch.
- **FR-014.6** — "Clear saved data" in the Sound/settings screen removes both
  keys and resets to defaults; available only when persistence is active.
- **FR-014.7** — Any storage exception (quota, disabled storage) degrades to
  memory-only for the session, emits one console warning, and never blocks
  gameplay.
- **FR-014.8** — Ranking rules: descending score; ties broken by higher stage,
  then by earlier insertion (stable). Entries are never merged across
  difficulty/speed.

## Business rules
BR-010 (basic 10), BR-011 (per-setting tables), BR-015 (persistence limits),
SEC-003 (untrusted, bounded, versioned).

## Acceptance criteria
- **AC-170** — A scout kill awards exactly 10 with multiplier ×1.
- **AC-171** — Class scores match the table in FR-013.2 (table-driven).
- **AC-172** — A wave cleared with all enemies destroyed awards exactly
  `100 × stage` once; a wave with an escape awards no wave bonus.
- **AC-173** — Four kills within 2 s yield multiplier ×1.75; a 2.1 s gap resets
  it to ×1.00; the multiplier never exceeds ×5.00.
- **AC-174** — A corrupt, truncated or wrong-version payload produces default
  scores/settings and no panic.
- **AC-175** — An injected storage exception leaves the run playable in
  memory-only mode with exactly one warning.
- **AC-176** — "Clear saved data" empties both keys and reloads defaults.
- **AC-177** — Insertion keeps entries sorted by score with the documented
  tie-breakers; the 11th entry is dropped.
- **AC-178** — A Pilot/Normal score never appears in the Ace/Fast table.
- **AC-179** — Alias sanitisation strips control characters and truncates to 16
  runes without breaking UTF-8.
- **AC-179b** — Combo multiplier applies only to class score: a wave bonus
  earned under ×5.00 is exactly `100 × stage`.

## Edge cases
- Two entries with identical score, stage and settings → stable order preserved.
- A boss killed on the same step the run ends → reward is not awarded after
  `GAME_OVER`.
- Settings saved with volumes out of range → clamped to 0…1, not ignored.
- Clock/`Date` is never used for ranking; insertion order comes from the array.

## Error behavior
Storage failures degrade (FR-014.7). Parse failures fall back. No network, so no
timeout paths.

## Non-functional requirements
NFR-001 (scoring is pure), NFR-008 (storage behind an interface so unit tests
need no browser), NFR-007 (table contrast, keyboard-only selection).

## Security requirements
SEC-003. The alias is stored as plain text and rendered via `fillText` (no HTML
injection surface); no PII beyond what the player types.

## Observability requirements
One console warning on storage degradation (counted: exactly one per session).

## Out of scope
Online leaderboards, accounts, per-stage leaderboards, replay storage, score
verification/anti-cheat, importing/exporting tables.

## Open questions
- **D-4**: approve the scoring ladder and the BR-002 supersession?
- Should `VICTORY` award a completion bonus (e.g. 5000 at 20 stages)? No ID is
  minted until approved; if approved it becomes a new `FR-013.7`.
- Alias entry needs text input, which no spec covers yet: v0.2 proposal is a
  cycling 3-letter preset (`AAA`…`ZZZ`) to stay keyboard-only. Confirm.
