# Changelog

All notable changes to `linkedin-revamp` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/), versions follow [SemVer](https://semver.org/).

## [Unreleased]

_Nothing yet._

## [1.0.0] — 2026-05-29

First public release.

### Added

- **Core skill (`linkedin-revamp`)** — eight-phase end-to-end LinkedIn rebuild:
  1. Welcome + setup (Chrome extension + sign-in checks)
  2. Discovery (CV parse, portfolio fetch, profile scrape, backup snapshot)
  3. Persona grill (7 plain-English mission questions → `user-profile.json`)
  4. Audit (12-point rubric + cringe detector → audit report)
  5. Plan (per-section diff preview with accept / edit / skip / explain gates)
  6. Execute (full Chrome MCP drive, per-section safety gates, notify-network forced off)
  7. Verify (re-scrape, diff, before/after report)
  8. Launch (add-on offers + first-post draft)
- **Sub-skill `linkedin-revamp-notion`** — generates publishable Notion case-study pages from CV projects and links them to Featured. Standalone or offered in Phase 8.
- **Sub-skill `linkedin-revamp-walkthrough`** — builds animated MP4 walkthrough videos with title cards, captions, brand colors, and outro. Standalone or offered in Phase 8.
- **Banner helper** (`helpers/build_banner.py`) — renders a 1584×396 LinkedIn banner in four styles (minimal editorial, warm gradient, dot grid, single sentence), persona-agnostic, with `--demo` and cross-platform font fallback.
- **Audit tooling** — 12-point rubric and a cliché blocklist (cringe detector).
- **Execute tooling** — reusable Chrome MCP driver patterns, per-section safety gates, and a dated LinkedIn selector reference.
- **Plain-English UX standard** (`references/question-format.md`) — the six-part question structure every prompt follows, for non-technical first-time users.
- **Security posture** — `SECURITY.md` with full threat model, built-in safeguards, and documented revert path. Backup-before-edit, audit log, rate limiting, session lock, prompt-injection defense against scraped content.
- **Harness-enforced safety hook** — `bin/check-linkedin-gate.py`, a `PreToolUse` hook declared in frontmatter, hard-asks before any destructive Chrome action (delete, file upload, settings/privacy change) regardless of model state.
- **Feature menu (Phase 1)** — users pick which capabilities to switch on (Chrome auto-edit, banner, Notion, walkthroughs). Chrome auto-edit off → skill falls back to generate-only copy-paste mode.
- **Repo hygiene** — `.gitignore` (ignores the runtime `snapshots/` PII directory + build artifacts), `CODE_OF_CONDUCT.md` (Contributor Covenant), GitHub issue templates (bug + selector-break, both with no-real-PII notices) and a pull-request template.
- **Repo docs** — README, MIT LICENSE with usage disclaimer, CONTRIBUTING, anonymized before/after examples.

### Security

- All example content anonymized; repo ships zero real personal data and zero credentials.
- Core skill makes no third-party API calls — all generation via Claude tool calls only. (The optional Notion sub-skill performs an external write to the user's own Notion, gated by explicit confirmation.)
- Scraped LinkedIn content is treated as untrusted data and quarantined; the React value-setter passes values out-of-band (no string interpolation) to close a JS-injection vector.
- Contact info (email/phone) is redacted in the saved snapshot rather than stored in cleartext.
- The forced "Share profile updates" notify-network setting is restored to its original value on abort or completion.

---

## v2 backlog (planned, not yet scheduled)

- **Voice + tone matching** — learn the user's writing voice from their existing posts/articles and match it in the rewrite, instead of a single house voice.
- **A/B headline rotator** — rotate two headlines and track profile-view deltas to pick the winner.
- **Multi-language profile** — generate parallel profiles (e.g. Hindi + English) and switch based on viewer.
- **Recruiter-view simulator** — render the profile as a recruiter's search-result snippet and screen-share view, to test how it lands in that specific context.
- **Headshot polish suggestions** — analyze the current profile photo and suggest crop/lighting/background fixes (analysis only, no editing).
