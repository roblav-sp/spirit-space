# Feature — Weapons and Power-ups

> Implements FR-012 and BR-016. Extends FR-002 (single projectile stays the
> base weapon) and preserves BR-003 (no ammo) and BR-005 (one bullet, one
> enemy, except the beam).

## Context
The base weapon is deliberately weak so pickups matter. Every power-up must be
readable (HUD), finite (expiry), and must never make the game unlosable.

## Actors
Player, Simulation, Renderer (pickup sprites, HUD indicators).

## Preconditions
State `PLAYING` (pickups do not drift while paused/dying? see edge cases).

## Functional requirements
- **FR-012.1** — Base weapon: one bullet per `fireCooldown` (0.2 s), speed
  500 px/s, radius 4, no piercing. Unchanged from v0.1 except the cooldown is
  now a weapon stat.
- **FR-012.2** — `PU-RAPID`: fire cooldown ×0.5, duration 12 s world time.
- **FR-012.3** — `PU-SPREAD`: three bullets at −12°, 0°, +12°, duration 15 s;
  replaces the single shot while active. Side bullets deal half damage (open
  question below), so total output stays below 3× base.
- **FR-012.4** — `PU-SHIELD`: absorbs the next damage event or expires after
  8 s, whichever comes first; absorption consumes the power-up.
- **FR-012.5** — `PU-BEAM`: piercing shot every 0.35 s, width 8 px, damage 1,
  duration 10 s; replaces bullet fire while active; cannot hit the same enemy
  twice in one shot.
- **FR-012.6** — Pickups drop from destroyed enemies with probability
  `dropChance` (difficulty budget) and a **pity timer**: if no pickup dropped in
  the last 40 kills, the next kill drops one.
- **FR-012.7** — Drop type is chosen by the seeded RNG from the allowed pool
  (`rapid`, `spread`, `shield`, `beam`) weighted 30/30/25/15.
- **FR-012.8** — Stacking: picking up the same type refreshes its duration to
  the full value (no intensity stacking). Different types coexist except
  `spread` and `beam`, which are mutually exclusive — the newer replaces the
  older.
- **FR-012.9** — Pickups drift down at 60 px/s, despawn below the field after
  8 s, and are collected on circle overlap with the player (radius 10).
- **FR-012.10** — The HUD shows one indicator per active power-up with a
  remaining-time bar; the base weapon state is visible when nothing is active.

## Business rules
BR-003 (no ammo), BR-005 (no piercing except `beam`, which is explicitly
specified), BR-016 (expiry, caps, base weapon never removed).

## Acceptance criteria
- **AC-160** — With no power-ups, firing produces exactly one bullet per
  cooldown at 500 px/s.
- **AC-161** — `rapid` halves the interval while active (0.2 → 0.1 s) and the
  interval returns to 0.2 s on expiry.
- **AC-162** — `spread` produces exactly three bullets per shot with the
  specified angles; its total damage per second is measured and documented (see
  open question) and does not exceed 3× base DPS.
- **AC-163** — `shield` absorbs exactly one damage event and then reports
  inactive; a second event in the same step does not also hit the ship.
- **AC-164** — `beam` hits each enemy at most once per shot and passes through.
- **AC-165** — After expiry, the weapon returns to the previous state (base or
  the older non-conflicting power-up).
- **AC-166** — Re-picking the same power-up refreshes duration but does not
  increase damage or angle count.
- **AC-167** — Picking `beam` while `spread` is active removes `spread`
  immediately (and vice versa).
- **AC-168** — Over 10 000 seeded kills the observed drop rate is within ±20%
  of `dropChance`; the pity timer guarantees a drop within 41 kills of the
  previous one.
- **AC-169** — The HUD lists active power-ups with countdowns that stop under
  pause.

## Edge cases
- A pickup collected during `RESPAWNING` is allowed (invulnerability does not
  block collection).
- `shield` absorbing damage during invulnerability: invulnerability wins, the
  shield is not consumed.
- Two pickups overlapping the player in one step: the higher one is collected
  first (deterministic order = slice order).
- Power-up timers freeze in `PAUSED` and during `PLAYER_DYING`? Current:
  freeze in `PAUSED`, continue in `PLAYER_DYING`.

## Error behavior
No I/O. Unknown pickup ID is a compile-time impossibility (typed constants).

## Non-functional requirements
NFR-001/NFR-002 (timers step-quantised), NFR-007 (HUD contrast, no colour-only
indicators).

## Security requirements
None beyond SEC-001/SEC-002.

## Observability requirements
None.

## Out of scope
Weapon levels 1–5 (Raiden-style), ammo, shop/upgrade screens, stacking
intensity, temporary invulnerable rolls.

## Open questions
- **FR-012.3 damage**: do spread side bullets do full damage (≈3× DPS) or half?
  Recommendation: **half**, so spread is area coverage, not a straight upgrade.
  Decision needed before M6; AC-162 records whichever is chosen.
- Should `shield` also cancel nearby projectiles on absorb? Current: no.
- Is 40-kill pity too generous at Legend? M9 measures.
