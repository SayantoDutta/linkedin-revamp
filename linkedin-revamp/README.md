# linkedin-revamp

> Turn any bland LinkedIn profile into a premium, social-media-manager-grade profile in one session — without writing a line of code.

`linkedin-revamp` is a [Claude](https://claude.ai) skill that rebuilds your LinkedIn profile end to end. It reads your CV, audits your current profile, interviews you about your goals, drafts every section, and then **drives the LinkedIn website for you** through the Claude Chrome extension — pushing each change live only after you approve it.

Built for people who have never used Claude Code before. Every question is plain English. Every change is previewed. You can type `abort` at any point.

---

## What it does

Eight stages, about 90 minutes to 2 hours the first time:

1. **Welcome + setup** — checks your Chrome extension is connected and you're signed in to LinkedIn.
2. **Discovery** — reads your CV, looks at your profile and portfolio, saves a full backup.
3. **Persona grill** — 7 honest questions about what you want from LinkedIn.
4. **Audit** — scores your profile out of 10 across 12 areas, flags AI-slop clichés.
5. **Plan** — drafts your new headline, About, banner, experience bullets, skills, and Featured tiles, side by side with the current versions. You approve each one.
6. **Execute** — drives LinkedIn for you and pushes the approved changes live.
7. **Verify** — re-checks the profile and produces a before/after report.
8. **Launch** — offers optional add-ons and drafts your first post.

### Optional add-ons

- **`linkedin-revamp-notion`** — turns your projects into publishable Notion case-study pages and links them to your Featured section. Requires the Notion MCP.
- **`linkedin-revamp-walkthrough`** — builds short animated MP4 walkthrough videos of your work, with title cards and brand colors. Requires `ffmpeg`.

The core skill offers these in Phase 8 only if your material fits. Both also run standalone.

---

## Install

### Requirements

- The [Claude](https://claude.ai) app (desktop, web, or CLI).
- The **Claude Chrome extension**, installed and signed in. See [`references/install.md`](references/install.md) for step-by-step setup.
- Google Chrome (or a Chrome-based browser) with LinkedIn signed in.
- Your CV as a PDF or plain text.

### As a Claude skill (recommended)

```bash
git clone https://github.com/ShayantoDutta/linkedin-revamp.git
# copy the three skill folders into your Claude skills directory
cp -r linkedin-revamp                 ~/.claude/skills/
cp -r linkedin-revamp-notion          ~/.claude/skills/
cp -r linkedin-revamp-walkthrough     ~/.claude/skills/
```

On Windows (PowerShell):

```powershell
git clone https://github.com/ShayantoDutta/linkedin-revamp.git
Copy-Item -Recurse linkedin-revamp,linkedin-revamp-notion,linkedin-revamp-walkthrough $env:USERPROFILE\.claude\skills\
```

Then restart Claude. The skill registers automatically.

### Via the Claude plugin marketplace

Search for **linkedin-revamp** in the marketplace and click install. (Coming soon.)

---

## Use

In Claude, type any of:

```
/linkedin-revamp
fix my LinkedIn
rebuild my LinkedIn profile
make my LinkedIn better
```

The skill takes over from there. Answer its questions, approve the changes you like, and watch it work.

To stop at any point, type `abort`. To pick up a stopped session later, type `resume`.

---

## What it will *not* do

- It will **never** type your password or sign in for you. You sign in yourself.
- It will **never** push a change without your explicit OK.
- It will **never** notify your network — it turns that setting off before editing.
- It will **never** touch your messages, billing, saved jobs, or anything outside profile editing.

Full detail in [`SECURITY.md`](SECURITY.md).

---

## Before / after

Three anonymized rebuilds — a junior engineer, a solo founder, and an independent consultant — are in [`examples/before-after-anon.md`](examples/before-after-anon.md). Every detail there is synthetic; the *structure* of each fix is what the skill actually does.

---

## How it's built

```
linkedin-revamp/
├── SKILL.md          orchestrator — the 8-phase flow
├── phases/           one file per phase, loaded on demand
├── templates/        reusable copy formulas (headline, About, bullets, banner, skills, posts)
├── audit/            12-point rubric + cringe-phrase detector
├── execute/          Chrome MCP driver patterns, safety gates, LinkedIn selectors
├── helpers/          build_banner.py — renders a 1584×396 banner, four styles
├── references/       plain-English question style guide + install guide
└── examples/         anonymized before/after case studies
```

The skill loads files incrementally — only the phase it's currently running — to stay fast and focused.

---

## Contributing

New personas, copy templates, and banner styles are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md). Please keep all example content anonymized — the repo must contain zero real personal data.

## Security

Found a security issue? See [`SECURITY.md`](SECURITY.md) for the threat model and how to report.

## License

MIT — see [`LICENSE`](LICENSE). You are responsible for any change pushed to your LinkedIn profile.
