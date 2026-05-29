# Phase 8 — Launch

## What this phase does

Detects whether the user's material is a fit for either optional add-on sub-skill. Offers them if relevant. Always offers to draft a launch post the user can publish to LinkedIn about the rebuild itself. Cleans up the session lock and closes out.

This phase is conversational.

---

## How to run this phase

### Step 8.1 — Tell the user what is happening

> Last phase. I'll suggest two optional add-ons if your material is a fit, and offer to write a draft of your first LinkedIn post about the rebuild. Take any of these or none — your call.

### Step 8.2 — Detect Notion add-on fit

**Trigger conditions** (must all be true):
1. The user's CV (`cv_parsed.projects`) contains 2 or more projects worth documenting.
2. The user's `north_star` from Phase 3 mentions something that benefits from showcasing project work (e.g. "build authority", "land clients", "hiring manager").
3. The Notion MCP is available — test by calling `mcp__1bd9c9fa-*__notion-search` with a trivial query like "test" and verifying it returns without an auth error.
4. At least 1 Featured tile in the rewrite pack referenced "needs to be created via sub-skill".

If all four hold, offer:
> You've got {N} projects in your CV that I think deserve their own write-ups — like one-page case studies that live in Notion and feed into your Featured section.
>
> There's a sub-skill for this called `/linkedin-revamp-notion`. It takes about 30 minutes per project. It writes the case study, publishes it to web, and adds it to your LinkedIn Featured.
>
> Want me to run it now? Type `yes`, `later`, or `no`.

If yes, invoke the `linkedin-revamp-notion` sub-skill using the Skill tool.

### Step 8.3 — Detect walkthrough add-on fit

**Trigger conditions** (must all be true):
1. The user's CV or portfolio contains 3 or more relevant images/screenshots of their work.
2. The user's `voice_mode` is "Confident" or "Bold" (the walkthroughs feel out of place for "Conservative").
3. `ffmpeg` is on PATH — check via Bash: `where ffmpeg`.
4. PIL is installed — check via Bash: `python -c "import PIL"`.

If all four hold, offer:
> You've got screenshots in your portfolio that would make great 20-second animated walkthroughs — like little explainer videos. Quick title card, pan through the screenshots with captions, sign-off card.
>
> The sub-skill for this is `/linkedin-revamp-walkthrough`. About 10 minutes per video.
>
> Want me to make a couple? Type `yes`, `later`, or `no`.

If yes, invoke the `linkedin-revamp-walkthrough` sub-skill.

### Step 8.4 — Draft the launch post (always offered)

Whether the sub-skills ran or not, offer to draft a launch post:

> Last thing. You just rebuilt your LinkedIn profile end-to-end with an AI agent. That itself is a story worth one good post.
>
> Want me to draft your first post about this? It will use the work you just shipped. Type `yes` or `no`.

If yes, load `templates/first-post-formulas.md` and generate three candidate posts using different hook structures:
1. **Showed up** structure — direct, narrative, before-after
2. **Burned a weekend** structure — vulnerable, transparent
3. **The recruiter's view** structure — third-person, observational

For each candidate:
- Hook (line 1, ≤ 220 chars — must survive mobile truncation)
- Body (5–8 short lines)
- Visual recommendation (before-after image, screenshot of audit, etc.)
- CTA (DM offer, link to skill repo, comment prompt)

Voice matches `voice_mode` from Phase 3.

Show all three. User picks one or asks for a revision.

Save the chosen post draft to `snapshots/{handle}-{timestamp}-launch-post.md`.

### Step 8.5 — Close the session

After everything is offered and accepted/declined:

1. Delete `snapshots/.session-lock`.
2. Show a final summary:

```
linkedin-revamp session complete.

What's in your snapshots folder:
- {handle}-{date}.json              — original profile snapshot (revert anchor)
- {handle}-{date}-user-profile.json — your 7-question answers
- {handle}-{date}-audit.md          — pre-rebuild audit
- {handle}-{date}-rewrite-pack.md   — every approved change
- {handle}-{date}-banner.png        — rendered banner
- {handle}-{date}-after.json        — post-rebuild snapshot
- {handle}-{date}-completion.md     — before/after report
- {handle}-{date}-audit-log.jsonl   — every Chrome MCP action
- {handle}-{date}-launch-post.md    — your first post draft (if you opted in)

Keep these around. If you want to revert anything, point me at the original snapshot.

Good luck with the new profile.
```

3. Stop. Do not propose further actions.

---

## Outputs of Phase 8

- (optional) Notion case study pages, if the add-on ran
- (optional) MP4 walkthrough files, if the add-on ran
- (optional) `snapshots/{handle}-{timestamp}-launch-post.md` — chosen launch post draft

---

## What to do if something goes wrong

- **Notion MCP auth error.** Don't offer the Notion add-on. Skip silently. Continue to walkthrough offer.
- **ffmpeg not on PATH.** Don't offer the walkthrough add-on. Skip silently.
- **The user declines all add-ons and the post draft.** That's fine. Close out normally.
- **The sub-skill fails partway through.** Inherit its error state. Tell the user what failed. Do not auto-rollback the main `linkedin-revamp` changes — those are already live and unaffected.
