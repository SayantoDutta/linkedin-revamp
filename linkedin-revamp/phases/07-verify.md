# Phase 7 — Verify

## What this phase does

Re-scrapes the profile after Phase 6 and compares the new state against what was approved in Phase 5. Produces a before-after report. Saves a final snapshot.

This phase is read-only.

---

## How to run this phase

### Step 7.1 — Tell the user what is happening

> Pushing is done. Now I'll re-read your profile, compare it against the plan, and show you a before-after report. Takes about 60 seconds.

### Step 7.2 — Re-scrape the profile

Same scrape logic as Phase 2 — read `phases/02-discovery.md` step 2.4 — but skip the CV and portfolio parts. Only re-scrape LinkedIn.

Save the new snapshot to `snapshots/{handle}-{timestamp}-after.json`.

### Step 7.3 — Diff against rewrite pack

For each section in the rewrite pack:

- **Vanity URL** — compare the live slug with the rewrite pack target.
- **Headline** — compare the live headline with the rewrite pack target.
- **About** — compare the live About text with the rewrite pack target.
- **Banner** — verify a banner image is present (not the default LinkedIn pattern).
- **Experience entries** — for each approved entry, compare live description with rewrite pack.
- **Skills** — verify DROP list skills are gone, ADD list skills are present, top 5 pin order matches.
- **Featured tiles** — verify count and titles match.

Classify each section:
- ✅ **MATCH** — live matches rewrite pack
- ⚠️ **PARTIAL** — section was pushed but live state is slightly different (e.g. LinkedIn truncated)
- ❌ **MISSING** — section was approved but did not land live
- ➖ **SKIPPED** — section was marked skipped in Phase 5

### Step 7.4 — Write the completion report

Write `snapshots/{handle}-{timestamp}-completion.md`. Structure:

```markdown
# LinkedIn Revamp — Completion Report
{Name} · {Date}

## Verdict
{One sentence overall, e.g. "9 of 10 sections landed cleanly. 1 skill miscaptured by autocomplete — needs manual fix."}

## Section status

| Section | Status | Detail |
|---------|--------|--------|
| Vanity URL | ✅ MATCH | linkedin.com/in/{slug} |
| Headline | ✅ MATCH | (130 chars) |
| About | ✅ MATCH | (1640 chars) |
| Banner | ✅ MATCH | Uploaded successfully |
| Experience: {Role 1} | ✅ MATCH | (640 chars) |
| Experience: {Role 2} | ✅ MATCH | (510 chars) |
| Skills (drops) | ✅ MATCH | 10 removed |
| Skills (adds) | ⚠️ PARTIAL | 24 of 25 added; "Paypal Integration" appeared instead of "API Integration" |
| Skills (top 5 pin) | ✅ MATCH | Pinned as planned |
| Featured tiles | ✅ MATCH | 4 of 4 |

## Action items for you
- Manually delete the wrong "Paypal Integration" skill and re-add "API Integration"
- {Other items if any}

## Before / After snapshot
- Before: snapshots/{handle}-{timestamp}.json
- After: snapshots/{handle}-{timestamp}-after.json
- Audit log: snapshots/{handle}-{timestamp}-audit-log.jsonl
- Rewrite pack: snapshots/{handle}-{timestamp}-rewrite-pack.md
- Audit report: snapshots/{handle}-{timestamp}-audit.md
```

### Step 7.5 — Score the new profile

Re-run the 12-point rubric from `audit/12-point-rubric.md` against the new state. Show before vs after side-by-side at the top of the completion report.

```markdown
## Before vs after score

| Section | Before | After | Delta |
|---------|--------|-------|-------|
| Profile photo | 3 | 9 | +6 |
| Banner | 0 | 9 | +9 |
| Vanity URL | 2 | 10 | +8 |
| Headline | 4 | 9 | +5 |
| About | 0 | 9 | +9 |
| ... | ... | ... | ... |
| **Composite** | **3.2** | **8.7** | **+5.5** |
```

### Step 7.6 — Show the report

Output the report to the chat. End with:

> That is the verify pass. {N} sections landed cleanly, {M} need manual attention.
>
> Ready for the launch phase — that is where we offer any optional add-ons and draft your first post about the rebuild. Type `launch` to continue, or `done` to finish here.

Wait for the response.

---

## Outputs of Phase 7

- `snapshots/{handle}-{timestamp}-after.json` — post-execution snapshot
- `snapshots/{handle}-{timestamp}-completion.md` — before-after report

---

## What to do if something goes wrong

- **Re-scrape fails (network, anti-bot, signed out).** Retry once after 5 seconds. If it still fails, write a partial completion report and tell the user the verify is incomplete. Ask them to re-run `/linkedin-revamp` and type `verify` to retry just this phase.
- **A section shows up as MISSING that the user expected to land.** Show the audit log entry for that section. If the audit log shows an error, surface the error. Offer to retry just that section by jumping back to the relevant Phase 6 step.
- **Before / after score regressed.** This should never happen, but if it does, alert the user prominently. Investigate which section the regression is in. Offer revert via the Phase 2 snapshot.
- **The user wants to skip Phase 7.** Refuse. The verify report is the user's record of what was changed and how. They need it.
