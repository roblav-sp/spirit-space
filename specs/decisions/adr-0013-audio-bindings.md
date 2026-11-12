# ADR-0013 — Audio through `syscall/js` WebAudio bindings in `cmd/game`

**Status:** Proposed

**Context:** v0.2 adds SFX and music from local files. Law 5 keeps
`internal/game` DOM-free; Law 6 forbids dependencies; Law 1 keeps rules in Go.
Browsers block audio until a user gesture, and `Audio`/`AudioContext` are DOM
APIs. The mixer policy (which sound, when, how loud) is game logic and must be
deterministic and testable.

**Decision:**
1. **Decision layer in Go:** `internal/game` emits `SoundEvent` values
   (`{ID, Volume, Pan}`) into a bounded per-frame queue with no DOM types. The
   queue is deterministic: same state + input ⇒ same events (Law 2).
2. **Playback layer in `cmd/game`:** an `audioEngine` wraps `js.Value` WebAudio
   calls, preloads buffers once, keeps per-ID gain nodes, and is unlocked by the
   first `keydown` (required by autoplay policy). It never decides *what* plays.
3. **Failure policy:** if `AudioContext` is unavailable, buffers fail to
   decode, or the unlock gesture never arrives, the engine becomes a no-op and
   the game continues silently; one console warning total, no page error
   (Law 7 concerns boot, not audio, but the same "never fail silently-wrong"
   spirit applies).
4. **User control:** master/music/SFX volumes and mute live in settings
   (FR-014/FR-016), persisted only if amendment 001 passes; otherwise
   session-only.

**Alternatives considered:**
- HTML `<audio>` elements — simpler, but tag management, gaps and no mixer;
  also puts sound choice in JS (Law 1 risk).
- Audio in `internal/game` — impossible without DOM imports (Law 5).
- Third-party mixer library — violates Law 6.
- No audio — contradicts FR-016; rejected by product.

**Consequences:** Sound logic is unit-testable (assert the event queue, not the
sound), and the browser layer is thin and replaceable. Cost: manual buffer
plumbing in `syscall/js`, and a headless-browser check for unlock behaviour
(AC-181, AC-184) that pixel checks cannot cover.

**Reconsider when:** spatial audio, dynamic music layers, or a Web Audio
library becomes acceptable (would require a Law 6 amendment).
