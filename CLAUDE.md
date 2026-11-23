# Rolex studio

You are working in **Rolex**, a studio that makes premium short-form video for many different companies: product demos and promos, product CG and explode films, brand reveals, Reels, heritage and map stories, footage edits, anime and cinematic shorts. It must look like a real studio made it, never like AI slop.

## Start every video here (in this order)

1. `reel-production` skill: the director's playbook. Spine: client → research → brief → script and voice → look → storyboard → build → sound → edit and QA → deliver, one default tool per stage, one numbers table, hard gates (`scripts/gate.py`), a `TOOLS.md` ledger.
2. `client-studio`: which company is this for? Load or create its private profile (`~/.claude/motion-kit/brands/<client>/`). Every brand, voice, audience and claim comes from there.
3. `brief-amplifier` (runs `creative-visualization`): the user writes short prompts on purpose; expand them into a full brief with an original idea.
4. One branch recipe from the playbook (`ui-promo-film`, `premium-product-film`, `brand-reveal-film`, `edit-kit:director`, …).

Look up any other tool only in `skills/reel-production/references/skill-map.md` (one winner per job, plus a NOT-FOR list). Run `skills/reel-production/scripts/preflight.sh` at the start of a session that will render.

Work goes in `productions/<client>/<slug>/`. Work end to end; stop only for money, publishing, licences, consent, or a brief where two different films would both fit.

## The bar

- One idea per video. The hook lands in the first second; frame 0 already moves. The ending loops or pays off.
- References are a vocabulary, not a template: take what serves this script, brand and audience; copy closely only when the user asks.
- Motion has weight (eased, anticipation, follow-through); real detail everywhere the camera looks; restraint reads as premium.
- Sound is designed: about 1 salient hit per second, visual events on sound, voice on top.
- Render, look at the frames, measure (gate, earshot, lookmeter), fix, re-render. Never call a cut done without looking.

## Rules

- Free tools by default; legitimate free routes for paid capabilities are in `skills/reel-production/references/free-routes.md`. Never bypass paywalls or use others' keys. Paid tools (the `ai` pack, `poppify`) only with the user's explicit OK.
- Clients never mix: one client's logo, colours, voice, claims and assets never appear in another's film.

## Local-only folders (never commit or push)

- `references/` - two finished films made for one client (Mannjal), with source; confidential. Not the general bar (that is `skills/reel-production/references/teardowns.md`).
- `library/` - sound effects, music, HDRIs, maps, the user's licensed kits (`3d-animator`, `motion-graphics-starter-kit`).
- `productions/` - all work, one folder per client; `productions/REQUESTS.md` is the request ledger.
- Client profiles live outside the repo in `~/.claude/motion-kit/brands/`.

## Installing (when asked to "install this repo")

1. Clone to the permanent location if needed (plugins install from it): `git clone --depth 1 https://github.com/titirshu-mannjal/Rolex.git ~/.local/share/rolex/repo`; if it exists, `git -C ~/.local/share/rolex/repo pull --ff-only` (about 1.5 GB: run in the background).
2. `bash install.sh --list`; `core` is the default stack. Run `bash install.sh` (add `--packs …`, `--all`, `--tools` as asked; `--tools` adds yt-dlp, auto-editor, whisper, edge-tts, DepthFlow, rembg, Real-ESRGAN, earshot, the voice engines and fonts).
3. Report the summary, failures and missing system tools with the install command; tell the user to restart Claude Code.

Never delete existing skills: the installer moves replaced folders to `~/.claude/rolex-backup/<timestamp>/`.
