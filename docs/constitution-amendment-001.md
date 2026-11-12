# Constitution Amendment 001 — Local browser storage for scores and settings

> **Status: RATIFIED — 2026-11-12.** Applied to `constitution.md` §1 and §6 by
> the owner (decision **D-1** in `docs/audits/v0.2-baseline.md` §7). The
> implementation in M7 still requires the tasks in
> `tasks/scoring-highscores.md`; ratification authorises the work, it does not
> implement it.

## 1. Why an amendment is required

`constitution.md` currently states (verbatim):

- §1: "no persistence beyond the page"
- §6: "The game has no server, no auth, no storage, and collects no data."
  and "Do not introduce network calls, cookies, or persistent storage
  without amending this constitution (see §8)."

Feature `scoring-highscores` (FR-014) wants optional local high scores and
settings. Even though `localStorage` is browser-local, it survives page loads
and is therefore persistence. §8 requires a constitutional amendment before
code is written. This proposal is deliberately narrow.

## 2. Proposed text

### 2.1 §1 Mission — replacement paragraph

> Spirit Space is a single-player browser space shooter: the player pilots a
> ship, shoots incoming enemies, and scores points. The entire game is Go
> compiled to WebAssembly, rendered to an HTML5 Canvas. No server, no network
> play, and no persistence other than **optional, local-only browser storage
> of high scores and user settings within the page's own origin**. Out of
> scope: multiplayer, accounts, analytics, backend services, telemetry,
> cookies, and any data leaving the user's browser.

### 2.2 §6 Security and privacy — replacement section

> ## 6. Security and privacy
>
> The game has no server, no auth, and collects no data. Trust boundary:
> nothing from the page may make the simulation depend on DOM state.
>
> **Local storage exception (Amendment 001).** A single, versioned key per
> concern — high scores and user settings — may be persisted in the browser's
> `localStorage` for the page's own origin, subject to all of:
>
> 1. **Content limits.** Only: player-chosen alias (optional, ≤16 chars,
>    free-form, never validated for uniqueness), score, stage reached, chosen
>    difficulty and game speed, audio volumes/mute, control preferences, and
>    schema version. No device identifiers, no timestamps beyond score order,
>    no free-form text other than the optional alias.
> 2. **No transmission.** Stored data is never sent anywhere. `SEC-002`
>    (no runtime network) is unchanged.
> 3. **No cookies, no IndexedDB, no Cache API, no server storage.**
>    `localStorage` only, and only from `cmd/game` (Law 5 keeps
>    `internal/game` free of DOM access; scoring and validation rules still
>    live in Go).
> 4. **Reads are untrusted input.** Corrupted, truncated, oversized, or
>    schema-mismatched data must fall back to a clean default and must never
>    panic. Bounded (≤64 KiB) and versioned.
> 5. **User control.** A visible "Clear saved data" action exists in the
>    settings menu; disabling persistence (or a storage failure, e.g. private
>    browsing quota errors) degrades to memory-only for the session.
> 6. **No new dependency.** `localStorage` is reached through `syscall/js`
>    from `cmd/game`; `go.mod` stays `require`-free (Law 6).
>
> Anything beyond this exception requires a further amendment (§8).

### 2.3 §7 API stability — no change

The `internal/game` API contract keeps growing as documented in
`specs/contracts/simulation-api.md`; storage types are plain Go structs with
no DOM types, so §7 needs no amendment.

## 3. What this amendment does *not* allow

- Analytics, telemetry, error reporting, A/B assignment, crash upload.
- Remote leaderboards, accounts, sync, or any network call at runtime.
- Storing inputs, replays, or full run histories by default.
- Cookies, `IndexedDB`, service-worker caches.
- Reading any storage key not owned by this game.

## 4. Fallback if not approved

`specs/features/scoring-highscores/spec.md` defines the **memory-only** mode
as the required baseline: high scores and settings live for the session only.
If the amendment is rejected, only the persistence layer is dropped; every
acceptance criterion about ranking, ordering and settings behaviour still
applies. M7 can therefore ship either way with no spec rewrite.

## 5. Approval record (to be filled by the owner)

| Field | Value |
|---|---|
| Status | **RATIFIED** |
| Requested | 2026-11-12 (M1) |
| Approved by | roblav-sp (repository owner) |
| Date | 2026-11-12 |
| Notes | Applied verbatim to `constitution.md` §1 and §6. M7 may implement persistence; memory-only remains the required fallback. |
