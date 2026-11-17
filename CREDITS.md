# Credits and Third-Party Notices

> Required by `constitution.md` §6 (security/privacy) and SEC-004
> (provenance). Pairs with `docs/ASSET_MANIFEST.md` (human license review) and
> `assets/asset-manifest.json` (machine checksums).

**Code and game content:** © 2026 TEXUGO DO MEL INC. All rights reserved.
Proprietary — see `LICENSE`. This file exists **because** third-party material
requires attribution or notice even in a closed-source product.

## 1. Runtime dependencies

| Component | Version | License | Why it is listed |
|---|---|---|---|
| Go standard library / runtime | 1.22 | BSD-3-Clause | Linked into `main.wasm`; BSD-3 requires retaining the notice in binary distributions. |

No third-party Go modules exist (`go.mod` has no `require` block — Law 6).
No npm packages ship at runtime (dev-only tooling lives in
`.agents/skills/browser-verify/`, ADR-0005).

## 2. Assets

**Status: no packs imported.** The game currently renders geometric primitives
and plays no audio (the permanent fallback, FR-016.6 / FR-017.3).

When a pack is imported, add one row per pack **only after** its license is
approved in `docs/ASSET_MANIFEST.md` §4:

| Pack | Author | License | Official page | Files used | Added |
|---|---|---|---|---|---|
| *(none)* | | | | | |

Rules:
- CC0 1.0 permits use in proprietary works and requires no attribution; credit
  is given here anyway, for provenance and good faith.
- No asset author endorses or is affiliated with this project.
- Never commit a pack whose manifest state is `REVIEW_REQUIRED` or
  `CHECK_LICENSE_CONTENT`.

## 3. Development tooling (not shipped)

| Tool | License | Scope |
|---|---|---|
| Python 3 + `unittest` | PSF-2.0 | `scripts/download_assets.py`, `scripts/tests/` |
| Node + Playwright/Chromium | Apache-2.0 / BSD | `.agents/skills/browser-verify/` only |

Neither tool is bundled into the game or the deployed static payload.

## 4. Non-asset references

`docs/research/arcade-references.md` cites arcade titles (Galaga, Galaxian,
Raiden, 1942, Ikaruga, Vampire Survivors) as **mechanics references only**. No
sprites, sounds, names, layouts, or code are taken from them.
