# Task Index — Execution Order

> Master ordering of every atomic task in `tasks/`. This file adds **no new
> requirements**: it only sequences tasks that already exist, using their
> declared dependency edges. Requirement IDs stay in the feature task files and
> in `specs/traceability.md`.
>
> Read order for an agent: `constitution.md` → the task's own file → this index
> (only for "what can I do next").

## Status legend

| Status | Meaning |
|---|---|
| `DONE` | Implemented at HEAD `3fae24f` and covered by the listed test(s). |
| `NEXT` | Unblocked, ordered first in its wave. |
| `TODO` | Specified, dependencies satisfied later in the plan. |
| `BLOCKED` | Cannot start: an owner decision is missing. |

Waves are strictly ordered. Inside a wave, tasks without an edge between them
may run in any order (or in parallel sessions).

---

## Wave 0 — Unblock and de-risk (no gameplay code)

| # | Task | Status | Blocks | Notes |
|---|---|---|---|---|
| 0.1 | `TASK-INFRA-01` build tags so `go vet ./...` / `go test ./...` pass | **NEXT** | INFRA-04, all "gates green" claims | D-6 approved. Only code change in Wave 0. |
| 0.2 | `TASK-INFRA-03` `LICENSE` + `CREDITS.md` | `PARTIAL` | AUD-04 | PolyForm Strict 1.0.0 decided (see `LICENSE`); credits need asset rows at M8. |
| 0.3 | `TASK-INFRA-05` repo visibility + license posture | **BLOCKED** | nothing yet; decide before publishing | Public remote `roblav-sp/spirit-space` under a source-visible, noncommercial license. |

Exit criteria: four gates green on `main`; `LICENSE`/`CREDITS.md` linked from
`README.md`.

---

## Wave 1 — M2: state machine, main menu, pause (FR-006, FR-009)

Spec `specs/features/main-menu/spec.md`; plan `plans/main-menu.md`;
ADR-0010, ADR-0006.

| # | Task | Status | Depends on |
|---|---|---|---|
| 1.1 | `TASK-MNU-01` `State` enum, `New()` → `MAIN_MENU` | `NEXT` | — |
| 1.2 | `TASK-MNU-02` menu model and navigation | `TODO` | 1.1 |
| 1.3 | `TASK-MNU-03` start / pause / resume / quit | `TODO` | 1.2 |
| 1.4 | `TASK-MNU-04` renderer dispatch, `ctx.font`, key clarity | `TODO` | 1.3 |

⚠️ Expected breakage: 1.1 invalidates every existing test that assumes
`New()` starts playable. `TASK-MNU-01` requires updating them, **not** deleting
assertions. This is the largest single test churn in the plan — do it as one
commit.

---

## Wave 2 — M3: lives, damage, respawn (FR-008)

| # | Task | Status | Depends on |
|---|---|---|---|
| 2.1 | `TASK-LIV-01` lives counter + damage arbitration (BC-10) | `NEXT` | 1.1, `TASK-CMB-03` |
| 2.2 | `TASK-LIV-02` bottom escape harmless (D-2) | `TODO` | 2.1 |
| 2.3 | `TASK-LIV-03` `PLAYER_DYING` / `RESPAWNING` + invulnerability | `TODO` | 2.1, 1.3 |
| 2.4 | `TASK-LIV-04` HUD + restart integration | `TODO` | 2.3 |

Note: 2.1 introduces the **damage arbiter** that M5 (dives), M6 (shield) and
M7 (boss contact) all consume. Its signature is the highest-leverage API
decision in the plan — settle it here, not later.

---

## Wave 3 — M4: difficulty and game speed (FR-007)

Spec ADR-0012 (budgets vs. time scale), ADR-0008 (fixed step).

| # | Task | Status | Depends on |
|---|---|---|---|
| 3.1 | `TASK-DFS-01` difficulty/speed types, single data source | `NEXT` | — |
| 3.2 | `TASK-DFS-02` fixed step + `Advance` (BC-9) | `TODO` | 3.1 |
| 3.3 | `TASK-DFS-03` accumulator + stall policy in `cmd/game` | `TODO` | 3.2 |
| 3.4 | `TASK-DFS-04` fairness floors + HUD label | `TODO` | 3.1, 3.2 |

3.2 changes the `Update(dt)` contract in
`specs/contracts/simulation-api.md` → ADR-0008 already covers it; update the
contract text in the same commit.

---

## Wave 4 — M5: archetypes, formations, wave director (FR-010, FR-011)

Two interleaved tracks. **4.1–4.4 (formations) must land their tables before
4.5–4.9 (director) can validate waves.**

| # | Task | Status | Depends on |
|---|---|---|---|
| 4.1 | `TASK-FRM-01` archetype table | `NEXT` | 3.1 |
| 4.2 | `TASK-FRM-02` slot templates | `TODO` | 4.1 |
| 4.3 | `TASK-FRM-03` entry / hold / dive behaviour | `TODO` | 4.2, 2.1 |
| 4.4 | `TASK-FRM-04` bonus formation | `TODO` | 4.3 |
| 4.5 | `TASK-WAV-01` `RunMetadata`, seeded options (BR-017) | `NEXT` | 3.1 |
| 4.6 | `TASK-WAV-02` wave catalogue + validator | `TODO` | 4.5, 4.2, 3.4 |
| 4.7 | `TASK-WAV-03` stage progression + `VICTORY` | `TODO` | 4.6 |
| 4.8 | `TASK-WAV-04` delete the v0.1 `spawnEnemies` | `TODO` | 4.7, 4.3 |
| 4.9 | `TASK-WAV-05` golden RNG sequence | `TODO` | 4.8 |

4.8 is the only task that **removes** shipped behaviour (`spawnEnemies`,
`spawnDelay`). Do not start it before 4.7 is green: it is the point of no
return for v0.1 spawning.

---

## Wave 5 — M6: weapons, power-ups, scoring ladder (FR-012, FR-013)

| # | Task | Status | Depends on |
|---|---|---|---|
| 5.1 | `TASK-WPN-01` weapon state, base weapon parity | `NEXT` | 3.2 |
| 5.2 | `TASK-WPN-02` rapid + spread | `TODO` | 5.1 |
| 5.3 | `TASK-WPN-03` beam + shield | `TODO` | 5.2, 2.1 |
| 5.4 | `TASK-WPN-04` drops, pickups, pity timer | `TODO` | 5.3, 4.5 |
| 5.5 | `TASK-WPN-05` HUD indicators | `TODO` | 5.4 |
| 5.6 | `TASK-SCR-01` class / wave / combo scoring (BR-010) | `NEXT` | 4.1, 4.7 |
| 5.7 | `TASK-SCR-02` ranking table + tie-breakers | `TODO` | 5.6 |
| 5.8 | `TASK-SCR-03` versioned codec + hostile-input table | `TODO` | 5.7 |

🚫 **Blocked inside this wave:** `AC-162` (spread-shot damage split) has no
owner decision. `TASK-WPN-02` may implement the *firing* geometry; the damage
split must stay unimplemented until decided. Do not choose silently.

---

## Wave 6 — M7: bosses and local high scores (FR-015, FR-014)

| # | Task | Status | Depends on |
|---|---|---|---|
| 6.1 | `TASK-BOS-01` boss entity, HP, phases | `NEXT` | 4.1, 4.7 |
| 6.2 | `TASK-BOS-02` patterns with corridor guarantees | `TODO` | 6.1, 4.6 |
| 6.3 | `TASK-BOS-03` telegraphs, invulnerability, rewards | `TODO` | 6.2 |
| 6.4 | `TASK-BOS-04` contact damage + HUD | `TODO` | 6.3, 2.3 |
| 6.5 | `TASK-SCR-04` localStorage bridge (Amendment 001 ratified) | `NEXT` | 5.8 |
| 6.6 | `TASK-SCR-05` High Scores + Sound screens | `TODO` | 5.7, 1.4, 6.5 |

6.5 is the **only** place allowed to touch `localStorage`, and only from
`cmd/game` (constitution §6.1–6.6). Test it with a fake `Store` first.

---

## Wave 7 — M8: audio and assets (FR-016, FR-017)

| # | Task | Status | Depends on |
|---|---|---|---|
| 7.1 | `TASK-AUD-01` sound events in the simulation | `NEXT` | 2.3, 5.3 |
| 7.2 | `TASK-AUD-02` WebAudio engine, buses, unlock | `TODO` | 7.1 |
| 7.3 | `TASK-AUD-03` asset table with proven fallback | `NEXT` | — (startable early) |
| 7.4 | `TASK-AUD-05` music sourcing decision (`music.menu/stage/boss`) | **BLOCKED** | owner decision, spec update |
| 7.5 | `TASK-AUD-04` import packs, map IDs, music | **BLOCKED** | 7.2, 7.3, 0.2, 7.4 |

7.3 is deliberately startable now: it proves the fallback path **before** any
asset exists (AC-183/AC-184), which is the order the plan mandates. Shipping
code with an empty catalog first, then assets in a separate commit, keeps the
rollback trivial.

7.4 exists because none of the eight packs in `scripts/download_assets.py`
contains loopable music. That is an unspecified gap, not an oversight to patch
silently. See `TASK-AUD-05`.

---

## Wave 8 — M9: measurement, accessibility, regression (NFR-005…NFR-007)

| # | Task | Status | Depends on |
|---|---|---|---|
| 8.1 | `TASK-POL-01` 60 FPS measurement note (NFR-005) | `TODO` | 4.9, 6.6 |
| 8.2 | `TASK-POL-02` contrast, keyboard reachability, pause (NFR-007) | `TODO` | 1.4, 6.6 |
| 8.3 | `TASK-POL-03` full browser regression sweep (`browser-verify`) | `TODO` | 8.1 |
| 8.4 | `TASK-INFRA-02` browser checks for the new states | `TODO` | 1.4, 7.2, 7.3 |
| 8.5 | `TASK-INFRA-04` CI pipeline | `TODO` | 0.1 |

---

## Dependency spine (critical path)

```
        INFRA-01 ──────────────────────────────────► INFRA-04
           │
MNU-01 ─► MNU-02 ─► MNU-03 ─► MNU-04 ──────────────► POL-02
   │                  │
   └─► LIV-01 ─► LIV-02, LIV-03 ─► LIV-04
                  │
DFS-01 ─► DFS-02 ─► DFS-03, DFS-04
   │
   ├─► FRM-01 ─► FRM-02 ─► FRM-03 ─► FRM-04
   │               │
   └─► WAV-01 ─► WAV-02 ─► WAV-03 ─► WAV-04 ─► WAV-05 ─► POL-01
                                │
        WPN-01 ─► WPN-02 ─► WPN-03 ─► WPN-04 ─► WPN-05
                                │
        SCR-01 ─► SCR-02 ─► SCR-03 ─► SCR-04 ─► SCR-05
                                │
        BOS-01 ─► BOS-02 ─► BOS-03 ─► BOS-04
                                │
        AUD-01 ─► AUD-02 ─► AUD-04 ◄─ AUD-03 ◄─ AUD-05 (blocked)
```

## Open decisions gating this list

| ID | Decision | Gates | Owner state |
|---|---|---|---|
| D-3 | ID renames from audit §4 | none (already applied) | — |
| D-4 | scoring ladder supersedes BR-002 | 5.6 | assumed accepted (audit) |
| D-5 | `LICENSE` / `CREDITS.md` | 7.5 | **DECIDED: PolyForm Strict 1.0.0, © TEXUGO DO MEL INC.** |
| D-6 | `TASK-INFRA-01` build tags | 0.1 | **DECIDED: yes** |
| — | `AC-162` spread damage split | 5.2 | **OPEN** |
| — | music pack source | 7.4, 7.5 | **OPEN** |
| — | public repo vs. source-visible noncommercial license | 0.3 | **OPEN** |

## Progress

| Wave | Tasks | Done |
|---|---|---|
| v0.1 baseline (PLC/CMB/ENS/GOR) | 14 | 14 |
| 0 Unblock | 3 | 1 partial |
| 1 M2 menu | 4 | 0 |
| 2 M3 lives | 4 | 0 |
| 3 M4 difficulty | 4 | 0 |
| 4 M5 formations/waves | 9 | 0 |
| 5 M6 weapons/scoring | 8 | 0 |
| 6 M7 bosses/highscores | 6 | 0 |
| 7 M8 audio/assets | 5 | 0 |
| 8 M9 polish | 5 | 0 |
| **Total** | **62** | **15** |
