# Contributing

Thanks for wanting to make `linkedin-revamp` better. The most valuable contributions are **new personas**, **copy templates**, and **banner styles** — the things that make the skill work for more kinds of people.

The hard rule, before anything else: **no real personal data, ever.** Every example, test fixture, and screenshot must be anonymized. The repo ships zero credentials and zero real profiles.

---

## Ways to contribute

### 1. Add a persona

The skill is persona-agnostic by design — it adapts to whoever runs it. But the templates carry persona-specific *examples* that make the output sharper. If you've run the skill for a role that isn't well represented (say, academic researcher, nurse, trades professional, public-sector worker), add example copy for it.

Where personas show up:

- `templates/headline-formulas.md` — add a worked headline for the role.
- `templates/about-skeleton.md` — add a hook example in that role's voice.
- `templates/experience-bullets.md` — add 3–4 outcome bullets with realistic (anonymized) numbers for that field.
- `templates/skills-rubric.md` — add the keep/drop logic for that role's typical skill clutter.
- `examples/before-after-anon.md` — optionally add a full anonymized case.

Keep the voice plain and the numbers believable. No hype.

### 2. Add or improve a banner style

`helpers/build_banner.py` ships four styles (A–D). To add one:

1. Write a `render_pattern_X(hero, sub, palette, url) -> Image.Image` function following the signature of the existing four.
2. Register it in the `PATTERNS` dict.
3. Add a demo entry in `--demo` so `python build_banner.py --demo` renders it.
4. Test: `python build_banner.py --pattern X --hero "Test line." --demo`.

Banners must render at exactly 1584×396 and must not depend on any font that isn't either bundled or covered by the cross-platform font fallback list.

### 3. Improve the cringe detector

`audit/cringe-detector.md` is a blocklist of clichés. If you find a tired phrase it misses ("move the needle", "wear many hats", "ninja", "guru"), add it with a one-line note on why it reads as filler. Keep it to genuinely empty phrases — don't block words that can carry real meaning in context.

### 4. Improve the LinkedIn selectors

`execute/linkedin-selectors.md` holds the selectors the execute phase relies on. LinkedIn changes its UI often. If a selector breaks, fix it and note the date you verified it. Prefer stable, semantic selectors (aria labels, button text) over brittle generated class names.

---

## How to test your change

There is no heavy test harness — this is a content skill, not an app. The checks are:

1. **Every file reads as standalone.** Open the file you changed. Does it make sense without the rest of the repo loaded? Phase and template files are loaded individually at runtime, so each must stand on its own.
2. **The banner helper runs.** `python helpers/build_banner.py --help` and `python helpers/build_banner.py --demo` must both succeed.
3. **The walkthrough helper runs** (if you touched it). `python linkedin-revamp-walkthrough/helpers/build_walkthrough.py --help`.
4. **No PII.** `grep -ri` your change for real names, companies, emails, handles, tokens. The repo must stay clean.
5. **Selectors note a verification date** if you touched `linkedin-selectors.md`.

---

## Style

- **Plain English everywhere the user can see it.** Follow `references/question-format.md`. No jargon in anything a non-technical user reads.
- **Match the existing voice.** Warm, direct, no hype. Read a few existing files before writing.
- **Keep files focused.** One concern per file. The skill loads files incrementally to stay fast — don't merge them.
- **Markdown for instructions, Python for helpers.** No other languages in the core skill.

---

## Pull request checklist

- [ ] No real personal data anywhere in the diff.
- [ ] No committed secrets (keys, tokens, cookies, snapshots).
- [ ] Helper scripts run with `--help` and `--demo`.
- [ ] New user-facing text follows the plain-English style guide.
- [ ] If you touched selectors, you noted the date you verified them against live LinkedIn.
- [ ] `CHANGELOG.md` updated under "Unreleased".

---

## Code of conduct

Be kind, be specific, assume good faith. This skill exists to help people present their real work honestly — keep that spirit in the contributions too. No content that helps people fabricate credentials or mislead.
