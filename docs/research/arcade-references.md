# Research — Arcade References for v0.2 (Phase B)

> M1 research record. Retrieval date **2026-11-12** (UTC). Sourced mechanics
> are cited; everything else is marked as *our adaptation*. Nothing here
> authorises copying art, audio, names, code, or level layouts.

## 1. Access status (what could and could not be verified)

| Source | Status | Note |
|---|---|---|
| `https://en.wikipedia.org/wiki/Galaga` | 200 | full article fetched |
| `https://en.wikipedia.org/wiki/Galaxian` | 200 | full article fetched |
| `https://en.wikipedia.org/wiki/Raiden_(video_game)` | 200 | full article fetched |
| `https://en.wikipedia.org/wiki/1942_(video_game)` | 200 | full article fetched |
| `https://en.wikipedia.org/wiki/Ikaruga` | 200 | full article fetched |
| `https://en.wikipedia.org/wiki/Vampire_Survivors` | 200 | full article fetched |
| `https://kenney.nl/assets/space-shooter-remastered` | **403** | bot protection; page content **not verified** |
| `https://kenney.nl/assets/ui-pack-sci-fi` | **403** | not verified |
| `https://kenney.nl/assets/sci-fi-sounds` | **403** | not verified |
| `https://creativecommons.org/publicdomain/zero/1.0/` | 200 | CC0 1.0 legal code reachable |

**What could not be verified this session:** every Kenney landing page
(pack contents, file names, ZIP layout, per-pack license statement). The
importer deliberately does not guess ZIP URLs (`scripts/download_assets.py`);
a human must download each pack in a browser and inspect `License.txt` inside
the ZIP. No Kenney asset is committed by this milestone.

## 2. Sourced mechanics

### 2.1 Galaga (Namco, 1981) — fixed-screen formation shooter

Source: https://en.wikipedia.org/wiki/Galaga (retrieved 2026-11-12)

- Fixed shooter; enemies "fly into formation from the top and sides of the
  screen"; each stage is cleared by defeating all aliens.
- Enemies periodically **dive** at the player "while shooting down
  projectiles"; contact with either an alien or a projectile costs a life.
- Formation leaders ("Boss Galaga") **take two shots**; they can capture the
  player's ship and cost a life; destroying the captor rescues the ship as a
  **dual fighter** with extra firepower and a **larger hitbox**.
- The **third stage and every fourth thereafter is a bonus stage** whose
  aliens fly preset patterns and do not fire.
- Difficulty scales within a run: "more aggressive as the game progresses,
  increasing their number of projectiles and diving down at a faster rate".

### 2.2 Galaxian (Namco, 1979) — formation + escort dive

Source: https://en.wikipedia.org/wiki/Galaxian (retrieved 2026-11-12)

- Enemies appear in formation at the top; they "dive bomb towards the bottom
  of the screen while shooting projectiles".
- A flagship dives **escorted by two ships**; destroying all three awards
  bonus points, with extra for the flagship.
- The player loses a life on contact with an enemy or enemy projectile; run
  ends when all lives are gone.

### 2.3 Raiden (Seibu Kaihatsu, 1990) — power-ups, bombs, boss escalation

Source: https://en.wikipedia.org/wiki/Raiden_(video_game) (retrieved 2026-11-12)

- Eight stages of increasing difficulty; after the eighth the game **loops
  with increased difficulty**.
- Collectibles: **bombs** that "cancel out enemy fire and deal damage over a
  wide area", **weapon power-ups**, and score medals.
- On death, the fighter's shrapnel becomes projectiles that damage enemies.

### 2.4 1942 (Capcom, 1984) — evasion and escort power-up

Source: https://en.wikipedia.org/wiki/1942_(video_game) (retrieved 2026-11-12)

- Vertically scrolling; "sustaining a single hit or colliding with another
  aircraft causes the loss of one life".
- One power-up provides an escort of two smaller fighters (formation wingmen).
- A dedicated **roll button** lets the player "avoid dangerous situations by
  temporarily looping out of" the play area.

### 2.5 Ikaruga (Treasure, 2001) — readable polarity and chain scoring

Source: https://en.wikipedia.org/wiki/Ikaruga (retrieved 2026-11-12)

- Polarity switch: the ship absorbs bullets of its own colour and is killed by
  the opposite colour; absorbed bullets charge a homing laser (one level per
  10 bullets, max 12).
- Shooting the opposite colour does **double damage**.
- Scoring is chain-based: "destroying three enemy fighters of the same colour
  in a row will earn the player a chain bonus", starting at 100 and doubling
  up to 25,600, reset when the order is broken.
- The game has **no pick-ups or power-ups**; readability comes from colour
  rules, not item drops.

### 2.6 Vampire Survivors (poncle, 2022) — escalation and upgrade choices

Source: https://en.wikipedia.org/wiki/Vampire_Survivors (retrieved 2026-11-12)

- Auto-attacking weapons; continuous waves; survival is the goal.
- Each level-up offers "the choice of three or four weapons and power-ups
  named 'passives'"; slots cap at six weapons plus six passives.
- Weapons have evolved forms, reached via a specific passive at max level
  plus a chest drop.
- Sessions have **soft time limits** (15/20/30 min by stage) and escalating
  pressure afterwards, guaranteeing an eventual end.

## 3. Our adaptations (explicitly *not* claimed as sourced)

| Mechanic | Sourced inspiration | Our adaptation (fixed-screen, no scroll) |
|---|---|---|
| Formation entering from top/sides | Galaga, Galaxian | Formations assemble from top edge only; world stays 800×600 (Law 3) |
| Dive waves | Galaga, Galaxian | Template-driven dive paths, telegraphed ≥ 0.6 s before commit |
| Escort/dive leader bonus | Galaxian flagship + escorts | bonus formation when a leader and its escorts die within a window |
| Two-hit leaders | Galaga Boss Galaga | `heavy` and `boss` archetypes have >1 hit points; hit flash |
| Bonus stage every 4th | Galaga | Bonus formation wave with no enemy fire, scored by clean clears |
| Bomb cancels bullets | Raiden | `shield` power-up grants brief immunity, not a screen-clearing bomb (no new key) |
| Weapon pickups + power levels | Raiden | Four power-ups (`rapid`, `spread`, `shield`, `beam`) with expiry |
| Escort power-up | 1942 Tip Tow | `spread` fires three angled bullets; no separate escort entity |
| Evasive roll | 1942 | Not adopted (fixed-screen, no invulnerable roll button) |
| Polarity | Ikaruga | Not adopted; readability instead via colour-coded telegraphs and safe-gap guarantees |
| Chain scoring | Ikaruga | "combo" multiplier for consecutive kills inside a window, capped |
| Escalation by time | Vampire Survivors | Escalation by **stage budget**, not wall clock; run ends at a bounded stage count |
| Level-up choice of three | Vampire Survivors | Power-ups are picked up in-world; the menu offers no mid-run upgrade screen (keeps input model small) |
| Loop with higher difficulty | Raiden | Difficulty tiers (Rookie→Legend) × stages; no infinite loop, bounded wave list |

## 4. License and originality checks

- **No assets, sprites, sounds, or font files are taken from any of the above
  titles.** All arcade references are used as *rules/mechanics* only.
- **No names**: our archetypes are `scout`, `interceptor`, `heavy`, `sniper`,
  `boss`; no arcade enemy names appear in specs, code, or HUD strings.
- **No recognizable layouts**: formations are parametric templates
  (row/V/diagonal/zigzag/flank), not traced from any arcade stage.
- **Music/sound**: sourced only from Kenney CC0 packs once imported and
  reviewed; until then the game ships silent with no placeholder audio files.
- **Kenney license**: the packs are published as CC0, but *this session could
  not verify it* (403). `scripts/download_assets.py` therefore records
  `license_review: REVIEW_REQUIRED|CHECK_LICENSE_CONTENT` and refuses to mark
  a pack approved; a human must inspect `License.txt` in each ZIP.
- CC0 1.0 legal text: https://creativecommons.org/publicdomain/zero/1.0/
  (retrieved 2026-11-12).

## 5. Follow-ups for M8

1. Human downloads each Kenney pack in a browser, checks `License.txt`,
   imports with `python3 scripts/download_assets.py --archive ...`, and
   records the verdict in `docs/ASSET_MANIFEST.md`.
2. Only after that: map logical asset IDs to real filenames (never guessed).
3. Add `CREDITS.md` (pending owner decision D-5).
