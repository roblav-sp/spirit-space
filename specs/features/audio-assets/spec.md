# Feature — Audio and Asset Integration

> Implements FR-016 and FR-017. ADR-0011 (asset pipeline + fallback), ADR-0013
> (audio bindings), ADR-0005 (dev-only tooling). No asset is committed by M1.

## Context
Sprites and sound are what make v0.2 feel like a product rather than a
prototype. Both are optional at runtime: the game must stay fully playable with
zero assets, because the shipped state until M8 has none.

## Actors
Player, `cmd/game` (loading, playback, drawing), Simulation (emits sound
events), developer (imports and reviews assets).

## Preconditions
None. Assets are additive.

## Functional requirements

### Audio (FR-016)
- **FR-016.1** — Three buses: `master`, `music`, `sfx`, each 0…1; effective
  volume is `master × bus`.
- **FR-016.2** — The audio engine unlocks on the first `keydown`; before that,
  no `AudioContext` is created.
- **FR-016.3** — SFX events are emitted by the simulation as typed
  `SoundEvent{ID, Volume}` values: `menu-move`, `menu-select`, `shoot`,
  `enemy-hit`, `enemy-kill`, `player-damage`, `player-death`, `powerup-pickup`,
  `boss-enter`, `boss-defeat`, `wave-clear`.
- **FR-016.4** — Music tracks per state: menu, stage, boss. Transitions
  cross-fade in ≤300 ms; a missing track leaves the previous one playing, then
  silence at end.
- **FR-016.5** — Mute forces effective volume 0 for all buses without changing
  the stored volumes.
- **FR-016.6** — Audio failures (no `AudioContext`, decode error, missing file,
  blocked autoplay) degrade to silence; the game remains playable and complete.
- **FR-016.7** — The simulation never waits on audio; the event queue is
  bounded (≤16 per frame, oldest dropped).

### Sprites (FR-017)
- **FR-017.1** — Renderer asset IDs: `ship.player`, `enemy.scout`,
  `enemy.interceptor`, `enemy.heavy`, `enemy.sniper`, `enemy.boss`,
  `bullet.player`, `bullet.enemy`, `pickup.rapid`, `pickup.spread`,
  `pickup.shield`, `pickup.beam`, `ui.cursor`, `fx.explosion`. IDs are stable
  strings used by code and manifest — never file paths.
- **FR-017.2** — Sprites are drawn from their centre with rotation 0 for the
  player and enemies (the fixed-screen world has no scrolling), scaled to the
  entity's collision radius while preserving aspect ratio (uniform scale, fit
  inside `2×radius`).
- **FR-017.3** — If an asset is absent, fails to decode, or its manifest entry
  is missing, the existing geometric primitive renders instead (circle, square,
  triangle); this is the permanent fallback, not a temporary hack.
- **FR-017.4** — A single non-fatal console warning is emitted the first time
  each asset ID falls back.
- **FR-017.5** — Assets are loaded from the page's own origin only; no CDN, no
  data URIs, no network at runtime.
- **FR-017.6** — Asset budget: shipped sprites ≤ 2 MiB, audio ≤ 6 MiB, total
  runtime payload ≤ 12 MiB including `main.wasm`; manifest documents the totals.

## Business rules
BR-018 (local, provenance-tracked, license-reviewed, optional runtime).

## Acceptance criteria
- **AC-180** — With audio present, the first `keydown` creates exactly one
  `AudioContext` and later frames do not re-create it.
- **AC-181** — With `AudioContext` unavailable, the game runs with zero audio,
  no unhandled error, and exactly one console warning.
- **AC-182** — Setting master volume to 0 silences SFX and music; mute overrides
  a non-zero volume; unmute restores the stored volumes.
- **AC-183** — Deleting one sprite file leaves that entity rendered as its
  geometric fallback while all other sprites still draw.
- **AC-184** — A corrupted (undecodable) sprite file also falls back, once, with
  one warning, and does not block other assets.
- **AC-185** — A missing sound file yields no sound for that event and does not
  interrupt gameplay or other sounds.
- **AC-186** — `docs/ASSET_MANIFEST.md` totals stay within FR-017.6 budgets; a
  test parses the manifest and asserts the sums.
- **AC-187** — In a headless-browser run, no network request goes outside the
  page's origin (Playwright request log, existing `browser-verify` skill).
- **AC-188** — A 2:1 sprite is never stretched to fill a square: rendered width
  and height keep the source ratio within 1 px.
- **AC-189** — Every asset ID referenced by code exists either in the manifest
  or in the explicit fallback table (compile-time list compared in a test).

## Edge cases
- Pause: music ducks/continues at reduced gain; SFX events stop being emitted
  (simulation frozen).
- Tab hidden: audio keeps playing until blur handler mutes? Current: no special
  handling in v0.2; browser default applies.
- Power-up sprites rotate? No rotation in v0.2.
- Multiple explosions in one frame reuse one sprite instance; no pooling needed
  at this scale.

## Error behavior
All asset failures are non-fatal (FR-017.3/F). No user-visible error beyond the
console warning; Law 7 concerns boot, which stays unchanged.

## Non-functional requirements
NFR-004 (offline), NFR-005 (decode once at load; no per-frame allocation),
NFR-006 (budgets above), NFR-007 (HUD text readable over sprites → draw a
contrast plate behind HUD text).

## Security requirements
SEC-002 (same-origin only), SEC-004 (provenance + checksums).

## Observability requirements
Console warnings only (one per fallen-back asset ID).

## Out of scope
Music composition, dynamic mixes, positional audio, sprite atlases (possible
later optimisation), animated spritesheets, particle systems, shaders.

## Open questions
- Does FR-017.6's 12 MiB budget conflict with keeping `main.wasm` (2.3 MB
  today) under growth? Recheck at M8.
- Should pause duck music to 30% or stop it? Current: duck.
- Attract-mode/menu music loop is not specified yet; M8 decides whether it is
  required or optional.
