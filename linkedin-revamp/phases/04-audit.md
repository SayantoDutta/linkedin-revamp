# Phase 4 — Audit

## What this phase does

Scores the current LinkedIn profile against a 12-point rubric, runs a cringe-phrase detector across every text field, and produces a one-page audit report. This is read-only.

The audit gives the user a clear picture of what is bland, missing, or actively hurting their profile before Phase 5 proposes a rewrite.

---

## How to run this phase

### Step 4.1 — Tell the user what is happening

> Now I'm going to score your current profile out of 10 across 12 areas. I'll also run a quick check for cringe phrases — the AI-generated cliches like "passionate", "rockstar", "ninja", "leverage", "synergy". This is a one-page report. Takes about 30 seconds. It will feel a little harsh in places. That's the point.

### Step 4.2 — Load the rubric

Read `audit/12-point-rubric.md`. That file contains the scoring criteria, score bands, and example justifications for each of the 12 areas.

### Step 4.3 — Score each area

For each of the 12 areas, score 0–10 with a one-line justification. Use the snapshot from Phase 2 as input. Compare against the user_profile from Phase 3 — for example, if the user said in Phase 3 their target person is a recruiter, score the headline harder for keyword density.

The 12 areas:

1. **Profile photo** — present, clear, professional. 0 if missing, 4 if amateur selfie, 7 if decent phone shot, 10 if pro headshot with clean background.
2. **Banner** — exists, on-brand, mobile-safe. 0 if missing, 3 if default LinkedIn pattern, 7 if generic stock photo, 10 if branded with intentional copy.
3. **Vanity URL** — clean handle, no random characters. 10 if `/firstname-lastname`, 0 if includes random suffix like `-27a5b7233`.
4. **Headline** — clear positioning, keyword-dense, target-person-aware. 10 if includes role + value prop + 2-3 keywords; 0 if "Open to Work" or just a job title.
5. **About** — hook in the first 220 characters (mobile-truncation limit), no AI cringe, specific. 10 if first sentence makes you want to read the rest; 0 if missing.
6. **Featured** — at least 3 tiles, OG previews work, links resolve. 0 if missing, 7 if 1-2 tiles, 10 if 4+ tiles with strong previews.
7. **Experience** — outcome bullets with numbers, no jargon, no fluff. 10 if every entry has a measurable result; 0 if entries are job-title-only.
8. **Education** — current, relevant, with dates. 10 standard; deduct only for missing or clearly wrong dates.
9. **Skills** — top 5 pinned, relevant to current positioning, no clutter (Forage sims, irrelevant tools, expired tech). 10 if focused; 5 if generic; 0 if missing or all junk.
10. **Recommendations** — 3+ written, recent, specific. 10 if 5+ recent specific recs; 0 if zero.
11. **Activity** — original posts in the last 30 days. 10 if 3+ original posts/week; 5 if 1 post/month; 0 if pure repost graveyard or silent.
12. **Privacy & safety** — share-profile-updates toggle, public visibility appropriate, "Open to Work" frame configured correctly. 10 if all sane; deduct for misconfigurations.

For each score, write one sentence of justification that names a specific thing on the profile.

### Step 4.4 — Run the cringe detector

Read `audit/cringe-detector.md`. It contains the blocklist phrases.

Run the detector against every text field in the snapshot:
- Headline
- About
- Each Experience description
- Each Featured tile description
- Each recent post

For each match, record:
- The phrase
- The field it appeared in
- The context (5 words before and 5 words after)

### Step 4.5 — Compute the top 3 fixes

Sort the 12 areas by score ascending. The top 3 fixes are the lowest-scoring areas with the highest reach (a Headline fix has higher reach than an Education fix because the Headline appears in search results, on hover cards, on connection requests).

Reach weighting:
- Headline: ×1.5
- About: ×1.4
- Banner: ×1.3
- Profile photo: ×1.3
- Vanity URL: ×1.2
- Featured: ×1.2
- Experience: ×1.1
- Skills: ×1.0
- Education: ×0.6
- Languages: ×0.4
- Recommendations: ×0.9
- Activity: ×1.0
- Privacy & safety: ×0.8

Final priority = (10 - score) × reach weight. Highest = top fix.

### Step 4.6 — Write the audit report

Write `snapshots/{handle}-{timestamp}-audit.md`. Structure:

```markdown
# LinkedIn Profile Audit — {Name}
{Date}

## Verdict
{One sentence overall. e.g. "Your profile has a strong career story but is bleeding signal through five fixable misses."}

## Top 3 fixes to make first
1. **{Area}** — {one-sentence what to do}
2. **{Area}** — {one-sentence what to do}
3. **{Area}** — {one-sentence what to do}

## Full scorecard

| # | Area | Score | Why |
|---|------|-------|-----|
| 1 | Profile photo | X/10 | {justification} |
| 2 | Banner | X/10 | {justification} |
| ... | ... | ... | ... |
| 12 | Privacy & safety | X/10 | {justification} |

## Cringe phrases found
| Phrase | Where | Context |
|--------|-------|---------|
| "passionate" | About paragraph 1 | "...I am a passionate marketer with a..." |
| ... | ... | ... |

If no cringe phrases found, say "Clean — no phrases from the cringe blocklist appeared. Nice."

## What this audit does NOT cover
- We did not assess your actual work quality, only how it is presented.
- We did not check if your claims are honest. That is on you.
- We did not look at messages, network graph, or activity engagement quality.
```

### Step 4.7 — Show the report and ask for the next step

Output the report to the chat. End with:

> That is the audit. Anything in there that surprised you, or do you want me to dig into any one area in more depth before we move on?
>
> When you are ready to see what I'd propose as a rewrite, type `plan it`.

Wait for `plan it` (or equivalent) before advancing to Phase 5.

---

## Outputs of Phase 4

- `snapshots/{handle}-{timestamp}-audit.md`
- In-memory: `audit_result` — score table, cringe matches, top 3 fixes

---

## What to do if something goes wrong

- **A profile section is missing entirely.** Score it 0 and note "missing" in the justification.
- **The cringe detector matches the user's job title or industry term.** Manually exclude. The blocklist file in `audit/cringe-detector.md` has a per-industry allowlist override.
- **The user gets defensive about a low score.** Stand by the score. Offer to walk through the specific evidence. Do not change the score to be nice.
- **The audit feels too harsh and the user is discouraged.** Remind them this is the worst the report will look — Phase 5 is where we fix everything. The audit is the baseline, not the verdict.
