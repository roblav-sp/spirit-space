# Plan — Audio and Asset Integration

> Implements FR-016, FR-017, BR-018, SEC-004, AC-180…AC-189
> (`specs/features/audio-assets/spec.md`). Milestone **M8**. ADR-0011,
> ADR-0013.

## Requirements being implemented
Asset import + catalog, sprite drawing with fallback, WebAudio engine with
buses and unlock, sound event mapping, budgets.

## Architecture components affected
- `internal/game` — `sound.go` (typed events, bounded queue).
- `cmd/game` — `assets.go` (ID→path, decode, fallback), `audio.go` (context,
  gain nodes, buffers), `draw` switches from primitives to sprite-or-fallback.
- Tooling — `scripts/download_assets.py` hardened + tested (done in M1).

## Contracts affected
`assets.md` (IDs, budgets, failure modes), `bootstrap.md` (AudioContext,
asset fetch, failure modes).

## Files or modules likely to change
`internal/game/sound.go`, `internal/game/game.go` (emit events),
`cmd/game/audio.go`, `cmd/game/assets.go`, `cmd/game/main.go`,
`assets/asset-manifest.json`, `docs/ASSET_MANIFEST.md`, `.gitignore`,
`README.md`.

## Dependency order
1. Sound event emission in the simulation + queue test (no audio yet).
2. Audio engine with a stub buffer table (silent) → then real files.
3. Asset table with an empty catalog → fallback path proven first.
4. Import packs (human step) → manifest → map IDs → draw sprites.
5. Budget check + `ASSET_MANIFEST.md` totals.
6. Browser checks: unlock, fallback, no third-party requests.

## Data migrations
None. `assets/vendor/**` is new content; nothing existing is rewritten.

## Testing strategy
- Unit: AC-180…AC-185 via injected fakes (no browser): a fake audio backend and
  a fake asset loader. AC-189 compares code ID constants against the catalog.
- Browser: AC-187 (request log), AC-188 (aspect ratio via canvas pixel probe),
  unlock behaviour (AC-180).
- Manual: listen-test for mix levels (documented as manual, not `✔ verified`).

## Rollout / rollback
Ship code with an empty catalog first (fallback-only), then the imported
assets in a separate commit. Reverting assets restores geometric primitives
without code changes.

## Risks and mitigations
- **License mistake when redistributing** → importer never self-approves; human
  verdict recorded in `docs/ASSET_MANIFEST.md` (D-5 adds `LICENSE`/`CREDITS`).
- **Payload bloat** → budgets in the contract; AC-186 parses the manifest.
- **Autoplay warnings in console** → no `AudioContext` before the first
  `keydown`; the existing "no console errors on load" browser check catches it.
