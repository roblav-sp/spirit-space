# Plan — Boss Encounters

> Implements FR-015, BR-014, AC-190…AC-199 (`specs/features/bosses/spec.md`).
> Milestone **M7** (after weapons/shield, before assets). Depends on M5
> formations and the M6 damage pipeline.

## Requirements being implemented
Boss entity with phases and HP budgets, pattern set with safe corridors,
telegraphs, rewards, stage completion, contact damage window.

## Architecture components affected
- `internal/game` — new `boss.go` (phase state, HP, pattern scheduler),
  pattern emitters in `projectile.go`, stage hook in `director.go`.
- `cmd/game` — HP bar, phase telegraph cue, boss music switch (M8).

## Contracts affected
`simulation-api.md` (BC-11, BC-12 borrowed — no new BC needed),
`assets.md` (`enemy.boss`, `music.boss`).

## Files or modules likely to change
`internal/game/boss.go`, `internal/game/projectile.go`,
`internal/game/director.go`, `internal/game/boss_test.go`, `cmd/game/main.go`.

## Dependency order
1. Boss entity + HP + phase counter, no patterns (killed by bullets).
2. Pattern emitters (`sweep`, `aimed-burst`, `spiral`) + corridor validator
   reuse from M5.
3. Telegraphs and invulnerable transitions.
4. Rewards + stage completion + `VICTORY` hook.
5. Contact damage using the M3 arbiter + 0.5 s window.
6. HP bar and telegraph rendering.

## Data migrations
None. Stage 5/10/15/20 selection already exists in the director (M5).

## Testing strategy
- Unit: AC-190…AC-199. Corridor check (AC-196) is a simulation-level property
  test over 200 seeded fights per difficulty — no browser.
- Determinism: boss pattern sequence identical for equal seed/step count.
- Manual/browser: readability of telegraphs (recorded as manual, not verified).

## Rollout / rollback
Static deploy. Rollback reverts boss files; the director's stage hook must be
written so a missing boss implementation falls back to a normal wave (defensive
but tested only in M9).

## Risks and mitigations
- **Unfair bullet walls** → patterns are parameterised and validated, never
  free-handed; AC-196 gates the merge.
- **Reward double-award** (boss dies on the same step as a wave clear) → award
  is guarded by a one-shot flag and by `GAME_OVER` precedence (AC-194/AC-199).
- **Contact damage shredding lives** → 0.5 s contact window (AC-197), one life
  per window, composed with invulnerability.
