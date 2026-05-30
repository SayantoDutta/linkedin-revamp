# linkedin-revamp

> Turn any bland LinkedIn profile into a premium, social-media-manager-grade profile in one session — without writing a line of code.

A [Claude](https://claude.ai) skill suite that rebuilds your LinkedIn profile end to end. It reads your CV, audits your current profile, interviews you about your goals, drafts every section, and then **drives the LinkedIn website for you** through the Claude Chrome extension — pushing each change live only after you approve it.

Built for people who have never used Claude Code before. Every question is plain English. Every change is previewed. You can type `abort` at any point.

---

## What's in this repo

Three skills. The core skill works on its own; the other two are optional add-ons it offers when your material fits.

| Skill | What it does |
|-------|--------------|
| [`linkedin-revamp`](linkedin-revamp/) | The core 8-phase rebuild: discovery → audit → persona interview → draft → live edits → verify. |
| [`linkedin-revamp-notion`](linkedin-revamp-notion/) | Turns your projects into publishable Notion case-study pages and links them to your Featured section. Needs Notion connected. |
| [`linkedin-revamp-walkthrough`](linkedin-revamp-walkthrough/) | Builds short animated MP4 walkthrough videos of your work. Needs `ffmpeg`. |

---

## Install

### Requirements

- The [Claude](https://claude.ai) desktop app (recommended — it can drive your browser), web, or CLI.
- The **Claude Chrome extension**, installed and signed in. See [`linkedin-revamp/references/install.md`](linkedin-revamp/references/install.md) for step-by-step setup.
- Google Chrome (or a Chrome-based browser) with LinkedIn signed in.
- Your CV as a PDF or plain text.

### macOS / Linux

```bash
git clone https://github.com/ShayantoDutta/linkedin-revamp.git
cd linkedin-revamp
cp -r linkedin-revamp linkedin-revamp-notion linkedin-revamp-walkthrough ~/.claude/skills/
```

### Windows (PowerShell)

```powershell
git clone https://github.com/ShayantoDutta/linkedin-revamp.git
cd linkedin-revamp
Copy-Item -Recurse linkedin-revamp,linkedin-revamp-notion,linkedin-revamp-walkthrough $env:USERPROFILE\.claude\skills\
```

Then restart Claude. The skills register automatically.

> You don't have to use the browser automation. On first run the skill shows you a menu of what to switch on. If you'd rather paste the changes in yourself, it writes everything as copy-paste-ready text instead of driving Chrome.

---

## Use

In Claude, type any of:

```
/linkedin-revamp
fix my LinkedIn
rebuild my LinkedIn profile
make my LinkedIn better
```

Answer its questions, approve the changes you like, and watch it work. Type `abort` to stop, `resume` to pick a stopped session back up.

---

## What it will *not* do

- It will **never** type your password or sign in for you. You sign in yourself.
- It will **never** push a change without your explicit OK. A built-in safety hook pauses and asks before anything hard to undo — a delete, a file upload, or a settings change.
- It will **never** notify your network — it turns that setting off before editing and restores it after.
- It will **never** touch your messages, billing, saved jobs, or anything outside profile editing.

Full detail in [`linkedin-revamp/SECURITY.md`](linkedin-revamp/SECURITY.md).

---

## Before / after

Three anonymized rebuilds — a junior engineer, a solo founder, and an independent consultant — are in [`linkedin-revamp/examples/before-after-anon.md`](linkedin-revamp/examples/before-after-anon.md). Every detail there is synthetic; the *structure* of each fix is what the skill actually does.

---

## Contributing

New personas, copy templates, and banner styles are welcome. See [`linkedin-revamp/CONTRIBUTING.md`](linkedin-revamp/CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). Please keep all example content anonymized — the repo must contain zero real personal data.

## Security

Found a security issue? See [`linkedin-revamp/SECURITY.md`](linkedin-revamp/SECURITY.md) and report it privately rather than as a public issue.

## License

MIT — see [`LICENSE`](LICENSE). You are responsible for any change pushed to your LinkedIn profile.
