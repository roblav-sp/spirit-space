# Tasks — Infrastructure

> Process and tooling tasks that are not part of a gameplay feature. IDs follow
> the same atomic-task rules (`ai-development-guide.md` §3).

## TASK-INFRA-01 — Make the documented gates runnable natively
- **Objective:** `go vet ./...` and `go test ./...` exit 0 on the host OS so
  Constitution §5 can be followed literally.
- **Requirement IDs:** Constitution §5; audit `docs/audits/v0.2-baseline.md` §2
  (decision D-6)
- **Dependencies:** owner approval of D-6
- **Files in scope:** `cmd/game/main.go` (add `//go:build js && wasm`),
  `cmd/game/stub_notjs.go` (new, `//go:build !(js && wasm)`, `func main() {}`),
  `ai-development-guide.md` §7 (note the variant if the stub approach is
  rejected)
- **Constraints:** no behavior change to the WASM build; `./build.sh` output
  identical in spirit; no test weakened.
- **Expected tests:** the gates themselves; plus a `cmd/game` "builds for
  js/wasm" check inside `build.sh`.
- **Verification evidence:** all four gate commands with exit codes in the PR
  description.
- **Out of scope:** adding CI.

## TASK-INFRA-02 — Browser checks for the new states
- **Objective:** extend the `browser-verify` skill with menu, pause, focus,
  audio-unlock and asset-fallback checks and keep the table in `SKILL.md` and
  `specs/traceability.md` in sync.
- **Requirement IDs:** AC-108, AC-110, AC-180, AC-181, AC-183, AC-187
- **Dependencies:** TASK-MNU-04, TASK-AUD-02, TASK-AUD-03
- **Files in scope:** `.agents/skills/browser-verify/e2e/verify.mjs`,
  `.agents/skills/browser-verify/SKILL.md`
- **Constraints:** dev-only tooling stays inside the skill (ADR-0005); no
  `package.json` at the repo root; never weaken existing checks.
- **Expected tests:** the new checks themselves.
- **Verification evidence:** `scripts/verify.sh` output.
- **Out of scope:** visual regression goldens.

## TASK-INFRA-03 — License and credits files
- **Objective:** repository-level `LICENSE` (code) and `CREDITS.md` (assets),
  referenced from `README.md`.
- **Requirement IDs:** audit §7 decision D-5; SEC-004
- **Dependencies:** owner choice of code license
- **Files in scope:** `LICENSE`, `CREDITS.md`, `README.md`
- **Constraints:** asset credits must match `docs/ASSET_MANIFEST.md`; no claim of
  endorsement by asset authors.
- **Expected tests:** none (documentation); manual review.
- **Verification evidence:** files exist and are linked; license names match the
  manifest.
- **Out of scope:** per-file license headers.

## TASK-INFRA-04 — CI pipeline for the gates
- **Objective:** run gofmt/vet/test/build on push with the same commands the
  constitution lists.
- **Requirement IDs:** audit §5 gap 2
- **Dependencies:** TASK-INFRA-01
- **Files in scope:** `.github/workflows/ci.yml` (or equivalent provider)
- **Constraints:** no runtime dependency changes; browser job optional and
  allowed to be non-blocking until it is stable.
- **Expected tests:** a green run on a deliberately broken branch, then a green
  run on `main`.
- **Verification evidence:** workflow run URL/log.
- **Out of scope:** deployment automation.
