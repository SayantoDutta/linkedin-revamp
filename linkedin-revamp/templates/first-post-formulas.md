# First-post formulas

The user just rebuilt their LinkedIn profile with `/linkedin-revamp`. The first post about it is high-leverage. Three formulas below — pick by `voice_mode`.

---

## Hard rules

1. **First 220 characters carry the post.** LinkedIn shows them before "...see more". The user clicks (or doesn't) on the hook alone.
2. **Visual matters.** Posts with a before-after image get 2–3× the reach. Use the `snapshots/{handle}-{date}-completion.md` data to build one.
3. **No "Excited to share".** Banned phrase. The post is the announcement; let it speak.
4. **Plain language.** Don't say "leveraged AI tooling to optimize my personal brand". Say what happened.
5. **One CTA max.** The user wants either DMs, comments, or a link click. Pick one. Three CTAs equal zero CTAs.

---

## Formula 1 — "Showed up" (Confident / Conservative voice)

Direct, narrative, before-after. Best for builders, engineers, designers.

```
Hook line (220 char max):
[Specific claim about what just happened. Past tense.]

Body (5–7 lines):
[Line about the before state — what the profile looked like before. 1-2 sentences.]
[Line about what changed — the rebuild itself, in plain terms.]
[Line about the result — the actual change in profile.]
[Line about what it took — tools used, time spent, surprises.]
[Optional: one specific learning that other people can use.]

CTA (1 line):
[One of:
  - "If you want to do this for your own profile, the skill is open-source: <link>"
  - "DMing the first 10 people who want me to run it on theirs."
  - "Drop a 'rebuild' in the comments if you want me to show how it worked."
]
```

Example (builder):
```
Rebuilt my LinkedIn profile end-to-end with an AI agent yesterday. 21 tasks, 3 hours, zero hand-typed text.

Before: blank banner, "Building AI Agents" headline, 0 featured tiles, 10 Forage-sim skills.
After: branded banner, sharp headline, 4 case studies in Featured, 24 AI-builder skills, About that doesn't read like a CV.

It's all open-source. The skill drives the LinkedIn UI directly, asks 7 honest questions about what you actually want from LinkedIn, then writes and pushes every section.

GitHub: github.com/ShayantoDutta/linkedin-revamp

If you want me to run it on your profile, DM me. First 10 for free.
```

---

## Formula 2 — "Burned a weekend" (Bold or vulnerable voice)

More transparent. Better for founders, indies, anyone who wants the human angle.

```
Hook line:
[A confession or vulnerability about the old profile, said in 1 sharp sentence.]

Body (5–7 lines):
[Line naming the specific things that were bad about the old profile. Be honest.]
[Line about why it had been that way — too busy, too embarrassed, too uncertain.]
[Line about what changed in the past 24-48 hours.]
[Line about what's now true that wasn't before.]
[Optional: what surprised you most.]

CTA:
[One of:
  - "Skill is open-source if you want it: <link>"
  - "Reply 'fix mine' if you want a free run."
  - "Comment what you wince at on your profile and I'll send you a plan."
]
```

Example (anyone):
```
My LinkedIn profile has been quietly embarrassing me for 18 months.

Headline was a job title. Banner was grey. About section was 0 characters. Skills section had three "Microsoft Excel (Forage)" tags I couldn't bring myself to delete.

Yesterday I gave it 3 hours and rebuilt the whole thing with an AI agent I wrote. It drives the LinkedIn site directly, asks you 7 honest questions, writes every section, and pushes everything live after you approve.

Today my profile is sharp. Headline works. About has a hook. Featured tiles point to real case studies.

I'm putting the agent on GitHub today. <link>

If you want me to run it on your profile this week, DM "rebuild". First 5 for free.
```

---

## Formula 3 — "The recruiter's view" (Funny or distinct voice)

Third-person, observational. Better when the user is willing to be a little funny about themselves.

```
Hook line:
[A line that sets up the recruiter / observer's perspective. Light tone.]

Body (5–7 lines):
[Describe what a recruiter or peer would have seen on the old profile — gently roasted.]
[Pivot to what changed.]
[Describe the rebuild process — the agent, the questions, the time.]
[Describe what the new profile looks like.]
[Optional: a one-line joke about the cringe phrases the audit caught.]

CTA:
[One of:
  - "Skill is here if you want to roast your own profile too: <link>"
  - "DM 'audit' and I'll send you the cringe phrases on yours."
]
```

Example:
```
A recruiter scanning my old LinkedIn profile last week probably saw:

→ A headline that just said my job title
→ A banner that was the default LinkedIn grey
→ An About section that did not, in fact, exist
→ A Skills section featuring "Microsoft Excel (Forage)" five times somehow
→ Last post: a repost from 8 months ago

I rebuilt the whole thing yesterday with an AI agent I wrote. It drives LinkedIn directly, asks you 7 questions about what you actually want from the platform, writes everything, pushes it live after you approve.

3 hours. Profile went from 3.2/10 to 8.7/10 on its own rubric.

Putting the skill on GitHub today. <link>

If you want a "before" audit of your profile (the agent does this read-only in 60 seconds), DM "audit". I'll send you yours.
```

---

## Visual recommendations

Pick one to attach to the post. In priority order:

1. **Before/after side-by-side screenshot of the LinkedIn profile.**
   - Top half: old profile (banner blank, headline boring, About missing)
   - Bottom half: new profile (banner branded, headline sharp, About hooked)
   - Render at 1200 × 1500 for LinkedIn feed.

2. **Score table from `snapshots/{handle}-{date}-completion.md`.**
   - Use the "Before vs after score" table. Render as a single image.
   - The 5.5-point composite delta visualizes the win.

3. **The audit cringe-phrases table from `snapshots/{handle}-{date}-audit.md`.**
   - The "Cringe phrases found" table is darkly funny on its own.
   - Render the table as an image with the user's old profile screenshot above it.

4. **A short looping GIF of the agent running.**
   - Hard to produce, but very high engagement.
   - Use the screen recording of any one of the Chrome MCP edit flows (skills add, headline change).
   - Loop at 5–8 seconds.

5. **Just the new banner.**
   - Cleanest. Lowest signal but lowest production cost.

---

## CTA selection

Pick exactly one. Avoid more than one.

| Goal | Pick this CTA |
|------|---------------|
| Build the user's network | "DM 'rebuild' and I'll send you a 60-second audit of your profile." |
| Drive traffic to the skill repo | "Skill is open-source: github.com/ShayantoDutta/linkedin-revamp" |
| Get comments | "What's the worst thing on your current profile? I'll roast it in the comments." |
| Get reach (algorithm bait) | "Comment 'audit' for a free read-only check of your profile." |
| Find clients | "If you want me to run it on your profile this week, DM. First 5 free." |

---

## What to never produce

- Posts that start with "Excited to share..." — instant skip
- Posts that thank Claude / Anthropic / a tool — keep the tool out of the headline
- Posts that use the word "leverage", "synergy", "pivot", "transformative", "game-changer"
- Posts with more than 3 hashtags — fewer hashtags reach better in 2025+
- Posts that ask for likes ("If you found this useful, give it a like!") — backfires
- Posts longer than ~1500 chars — past that, LinkedIn buries them
- Posts without a single concrete number or specific detail — too vague to engage
