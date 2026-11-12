# Contract — Local Persistence (`cmd/game` ↔ `localStorage`)

> **Status: AUTHORISED — Amendment 001 ratified 2026-11-12; implementation
> lands in M7.** Until `TASK-SCR-04` ships, the same contract applies to an
> in-memory store for the session and no `localStorage` call is made. ADR-0007.

## Keys

| Key | Content | Max size |
|---|---|---|
| `spirit-space.scores.v1` | up to 10 entries per `(difficulty, speed)` pair | 32 KiB |
| `spirit-space.settings.v1` | difficulty, speed, master/music/SFX volume, mute | 2 KiB |

No other keys may be read or written. The game never enumerates
`localStorage` (it must not observe other origins' or apps' data — same origin
sharing is still out of scope).

## Scores document (schema v1)

```json
{
  "schema": 1,
  "entries": [
    {
      "alias": "ACE",
      "score": 12450,
      "stage": 7,
      "difficulty": "ace",
      "speed": 1.25,
      "seed": 1234567890123
    }
  ]
}
```

Rules:

- `entries` ≤ 40 (10 per difficulty/speed pair); on write, the lowest-ranked
  entry beyond the cap is dropped.
- `alias`: ≤16 runes, control characters stripped, may be empty.
- `score`: integer 0…1e9. `stage`: 1…20. `difficulty` ∈
  `rookie|pilot|ace|legend`. `speed` ∈ `0.75|1.0|1.25`. `seed`: uint64.
- Ordering on read is re-derived (score desc, stage desc, insertion stable); the
  stored order is never trusted.
- Any violation → discard the whole document, use defaults, keep the previous
  in-memory table, one console warning (not per entry).

## Settings document (schema v1)

```json
{
  "schema": 1,
  "difficulty": "pilot",
  "speed": 1.0,
  "volumes": { "master": 0.8, "music": 0.5, "sfx": 0.9 },
  "mute": false
}
```

Volumes are clamped to `0…1` rather than rejected; unknown fields are ignored
(forward compatibility); an unknown `schema` is discarded.

## Write policy

- Written only on: run end (score insert), settings change, "clear saved data".
- Never on a per-frame or per-input basis.
- Writes are wrapped: an exception downgrades the store to memory-only for the
  rest of the session and emits exactly one warning (AC-175).
- Reads happen once at startup (settings) and once when a score table is shown.

## Read policy (untrusted input)

1. `localStorage.getItem` in a `try`; exception → unavailable.
2. `null`/absent → defaults, no warning.
3. Length > 32 KiB (scores) or > 2 KiB (settings) → discard, one warning.
4. `JSON.parse` failure → discard, one warning.
5. Schema mismatch → discard, one warning.
6. Field validation as above → clamp or discard per the rules.
7. **Never panic.** All of the above is covered by native tests through a fake
   `Store` (NFR-008), no browser required.

## Clearing

"Clear saved data" removes both keys and resets in-memory tables/settings to
defaults. The action is only rendered when persistence is active (the key is
writable and the amendment is ratified).

## Law 5 / Law 6 compliance

- The `localStorage` calls live only in `cmd/game/storage.go`; the simulation
  sees a `Store` interface with `[]byte`, never a `js.Value`.
- No `require` block, no npm package, no network.
