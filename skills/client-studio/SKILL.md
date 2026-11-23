---
name: client-studio
description: Work for many companies without mixing them up - one private profile per client (brand, voice, audience, look, claims, assets, references, past work) in ~/.claude/motion-kit/brands/<client>/, read before every brief, written back after every film. Use at the start of any video for a company or brand ("make a promo for X", "a reel for my client", "new client"), when the user names a different company than last time, or says "set up a client / brand".
---

# Client studio

The user works for several companies. Each one gets its own profile, and nothing from one client leaks into another.

## Where things live

- Profile (private, never committed): `~/.claude/motion-kit/brands/<client>/` with `brand.json`, `brand.md`, `MOTION.md`, `claims.md`, `assets/`, `references/`, `past-work.md` (see `template/README.md`). Edit-Kit's `edit-kit:theme` reads the same `brand.json`.
- Productions: `productions/<client>/<slug>/` in Rolex (local only).
- New client: `bash scripts/new_client.sh "<Client name>"`.

## Before every film

1. Identify the client from the request; if unclear and it matters (logo, colours, claims), ask once.
2. New client: create the profile, then fill it fast: ask for logo files, brand colours/fonts or guidelines, website, 2-3 videos they love, audience, and what they must never show. Fill the rest from their website and with `brand-intake`: save its `brand.md` and `MOTION.md` into the client folder and skip its step that adds a rule to CLAUDE.md (that file is shared by every client). Put any references they send through `reel-production/scripts/teardown.sh` into `references/`.
3. Existing client: read `brand.json`, `brand.md`, `MOTION.md`, `claims.md` and the last 3 entries of `past-work.md` before writing the brief. Respect what they liked and avoid what they rejected.
4. The brief (`brief-amplifier`) takes colours, type, logo rules, voice (`brand.json.voice`), look and never-list from the profile. The creative idea still comes from `creative-visualization`, inside the brand's rules.

## Isolation rules

- Use only this client's logo, colours, fonts, voice, claims and approved assets. Never reuse another client's assets, copy, music cues or devices.
- Do not show a client's unreleased product, data or footage outside their folder; uploads to cloud tools (HF Spaces, stock APIs) only with material the client cleared.
- Claims on screen come only from `claims.md` with a source; regulated sectors (lending, finance, health) follow `brand.json.claims.regulator`.
- Spec work for brands that are not clients carries a "spec, not affiliated" line and never uses their logo as if endorsed.

## After every film

Append to `past-work.md`: date, title, path to the final, the brief's idea in one line, what worked, the client's feedback, what to change next time. Update `brand.json`/`MOTION.md` when the client corrects a colour, font, voice or rule, so the correction holds for every future film.
