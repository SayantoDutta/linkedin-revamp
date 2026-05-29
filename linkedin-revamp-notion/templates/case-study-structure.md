# Case-study structure — the six-part skeleton

Every case-study page follows the same six parts, in this order. The order is deliberate: it front-loads the result a busy reader scans for, then lets the curious reader go deeper. Don't reorder it.

The goal of a case study is **proof**, not a brag. Write it like you're explaining your work to a smart friend who wasn't there — honest, specific, no hype.

---

## The six parts

### 1. One-line summary (the callout at the top)

What it is, who it's for, in one sentence. This is the only line many readers see.

- ✅ "A Slack bot that turns support tickets into weekly product-bug reports — built for a 12-person SaaS team."
- ❌ "A revolutionary AI-powered solution leveraging cutting-edge technology."

Formula: *"[What] for [who] — [the one-line why it matters]."*

### 2. The problem

What was broken, missing, or painful before this existed. Two to four sentences. Make the reader feel the friction.

- Name the *before* state concretely. "Support replies took 18 hours on average and the team had no idea which bugs came up most."
- No solution talk yet. Just the pain.

### 3. The approach

What you actually did. This is the longest section — but keep it readable. Three short paragraphs or a tight bulleted list.

- Lead with the key decision, not the tech list. "I decided to classify tickets at intake rather than batch them nightly, so the report was always current."
- Mention the stack, but in service of the story, not as a résumé dump. A non-technical reader should still follow the shape of what you built.
- If there was a hard tradeoff, name it. Showing judgment is more impressive than showing tools.

### 4. The outcome

The result. A number is gold. If you have one, lead with it and make it concrete.

- ✅ "Cut average first-response time from 18 hours to 2. The weekly bug report now drives the team's Monday standup."
- If you have no number yet, state the visible result honestly: "Launched three weeks ago; the first team using it has stopped doing the manual triage entirely."
- **Never invent a metric.** A fake number is the fastest way to lose a reader's trust. "Early, no hard numbers yet" is a fine, honest answer.

### 5. Proof

Show, don't just tell. One or more of:

- A screenshot of the thing working (the single most persuasive element — include one if at all possible).
- A link to the live product, repo, or demo.
- A short quote from a user or stakeholder (anonymized if needed).

### 6. What's next / what I learned

Two or three sentences. This is what separates a doer from a thinker.

- "Next: I want to auto-route the top recurring bug to the right engineer." — shows you're still thinking about it.
- Or: "What I learned: classifying at intake mattered far more than the model choice." — shows judgment.

---

## Worked example (anonymized)

> **Summary (callout):** A Slack bot that turns raw support tickets into a weekly product-bug report — built for a small SaaS team drowning in repeat issues.
>
> **The problem.** The support inbox got ~60 tickets a day. The same bugs came up again and again, but nobody had time to count which ones. Product prioritized from gut feel, and the team's first reply to a customer took about 18 hours on average.
>
> **The approach.** I built a Slack-native bot that classifies each ticket the moment it lands — by feature area and by whether it's a bug, a question, or a request. The key decision was classifying at *intake* instead of running a nightly batch, so the running tally is always current. It posts a digest every Friday: top five recurring bugs, ticket volume by area, and median response time. Stack was deliberately boring — a webhook, a small classifier, and a scheduled post — so the team could maintain it without me.
>
> **The outcome.** First-response time dropped from ~18 hours to about 2. The Friday digest now drives the team's Monday standup — they prioritize the top recurring bug first. Three months in, it's still running untouched.
>
> **Proof.** [screenshot of the Friday digest] · [link to a sanitized demo]
>
> **What's next.** I want it to auto-assign the week's top recurring bug to the right engineer, so the loop closes without a human in the middle.

---

## Rules

1. **Honest over impressive.** Every claim must be true. No invented numbers, no borrowed credit.
2. **Specific over generic.** "60 tickets a day" beats "high volume". "18 hours to 2" beats "much faster".
3. **Readable by a non-expert.** Your future client or recruiter may not be technical. The shape of the story must land even if the details don't.
4. **No clichés.** Run the draft through the core skill's cringe detector. Block "revolutionary", "cutting-edge", "passionate", "game-changing", "leverage", "synergy".
5. **One project per page.** Don't merge two projects to look busier. One clear story per page.
