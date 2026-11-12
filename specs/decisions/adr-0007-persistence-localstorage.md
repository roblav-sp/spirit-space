# ADR-0007 — Local browser storage for high scores and settings

**Status:** Accepted 2026-11-12 (Amendment 001 ratified; implementation in M7)

**Context:** v0.2 wants high scores that survive a reload and remembered
settings (difficulty, speed, volumes, mute). Constitution §1 ("no persistence
beyond the page") and §6 ("no storage") forbid this today; §8 requires an
amendment first. Everything else (game rules, scoring validation) must stay
deterministic and DOM-free (Laws 2, 5).

**Decision:** With Amendment 001 ratified (2026-11-12), persistence uses exactly one
`localStorage` key per concern (`spirit-space.scores.v1`,
`spirit-space.settings.v1`), written only from `cmd/game`. Serialization is
versioned, ≤64 KiB, JSON-encoded by Go. `internal/game` owns the
ranking/validation rules and receives plain byte slices or structs; it never
touches `localStorage`. All reads are treated as untrusted: parse errors,
wrong schema version, oversized payloads, or out-of-range values fall back to
defaults without panicking. If the amendment is rejected, the same code paths
operate on an in-memory store for the session.

**Alternatives considered:**
- Memory-only forever — no cross-session scores; simplest, keeps §6 intact,
  but loses the "high score table" feel that motivates retries.
- `sessionStorage` — survives reloads in one tab only; confusing UX, and still
  storage (would need the same amendment).
- `IndexedDB` — overkill for <10 records, larger API surface, async complexity.
- Server leaderboard — violates §1 and SEC-002 outright; rejected.

**Consequences:** One narrow, auditable exception. Corrupt-data handling and a
"clear saved data" action become required acceptance criteria
(AC-174…AC-176). Tests must cover a corrupt payload and a storage quota error
via an injected store interface, so unit tests stay browser-free (NFR-008).

**Reconsider when:** anything beyond scores/settings must persist, any
multi-device or remote ranking is wanted, or the amendment is declined.
