# ADR-0011 — Asset pipeline: dev-time import, runtime-local assets, hard fallback

**Status:** Proposed (extends ADR-0005)

**Context:** v0.2 replaces geometric primitives with sprites and adds sound.
Law 6 forbids runtime dependencies; ADR-0005 already exempts *dev-only*
Node/Playwright tooling. Assets must be served from the same origin (NFR-004,
SEC-002), carry provenance, and must not be assumed to exist — the game has to
run today, before any pack is imported.

**Decision:**
1. **Dev-time only:** `scripts/download_assets.py` (Python, stdlib) imports
   official Kenney ZIPs supplied by a human (`--archive`) or an explicitly
   verified HTTPS URL (`--source`). It never guesses download links. It is
   never invoked at runtime and is not a Go dependency (Law 6 unaffected).
2. **Provenance:** every import appends to `assets/asset-manifest.json`:
   pack id, author, license string, official page, archive source, retrieval
   time, archive SHA-256, per-file SHA-256 and size, license files found, and
   `license_review` (`REVIEW_REQUIRED` / `CHECK_LICENSE_CONTENT`). A human
   verdict is recorded in `docs/ASSET_MANIFEST.md`; the tool never self-approves.
3. **Logical IDs, not filenames:** code refers to `asset.ShipPlayer`,
   `asset.SfxShoot`, etc. A `cmd/game/assets.go` table maps ID → path. Because
   pack contents were unverified at spec time (see
   `docs/research/arcade-references.md` §1), no path is hardcoded in specs.
4. **Fallback is mandatory:** every draw/play call site has a geometric or
   silent fallback. Missing file, decode failure, or 404 must produce a
   playable game and a single non-fatal console warning — never a black
   screen (Law 7) and never a crash.
5. **Repo hygiene:** archives (`*.zip`) are ignored; imported packs under
   `assets/vendor/**` are committed only after license review; generated
   caches are ignored. `.gitignore` changes are part of the task that ships
   them.

**Alternatives considered:**
- Runtime CDN fetch — violates NFR-004/SEC-002 and breaks offline play.
- Embed assets in the WASM binary via `go:embed` — stdlib-legal and offline,
  but inflates the 2.3 MB module and makes binary diffs unreviewable.
- Generate art procedurally — no license risk, but far below the "replace
  primitives with sprites" goal.
- npm-based asset pipeline — unnecessary second runtime for a stdlib script.

**Consequences:** Asset failures become a tested path (AC-183…AC-185). Asset
size must be budgeted (NFR-006) and the manifest is the audit trail for
redistribution. Cost: a manual browser step per pack, and a one-time mapping
edit after import.

**Reconsider when:** packs are mirrored by a stable verified URL, or assets
must be embedded for a single-file distribution build.
