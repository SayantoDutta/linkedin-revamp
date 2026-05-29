# Experience bullets

Every Experience entry should follow this structure: a 1-line summary, 3–5 outcome bullets with numbers, and an optional "why it mattered" close.

The goal is for any recruiter or client scanning the section to know in 8 seconds: what the user did, what scope they owned, and what they shipped.

---

## Hard rules

1. **Every bullet starts with a verb.** No "Responsible for", no "Tasked with".
2. **Every bullet has a number.** If you can't find a number, name a scope (team size, customer count, dollars handled, latency, volume).
3. **No "helped" or "supported".** If you only helped, you didn't own it. Name what you owned.
4. **No jargon walls.** Mention 1 technical term per bullet max for non-technical roles, 2 for technical.
5. **Past tense for past roles, present for current.** Be consistent within an entry.
6. **3–5 bullets, not 10.** More than 5 = signal-to-noise drops.

---

## Structure per entry

```
[1-line summary — what the role was, what the user owned]

• [Outcome bullet 1 — strongest result, with number]
• [Outcome bullet 2 — second strongest]
• [Outcome bullet 3 — different dimension (operational vs strategic vs technical)]
• [Outcome bullet 4 — optional, if it adds]
• [Outcome bullet 5 — optional, if it adds]

[Optional: 1-line "Why it mattered" close — only for entries that bridge to north_star]

[Optional: Stack line — comma-separated tools used]
```

---

## Outcome bullet formulas

Use whichever fits the specific accomplishment. Mix freely within an entry.

### PAR (Problem · Action · Result)
> "[Problem] · [What I did] · [Result with number]"

Example:
> "Our voice AI funnel was leaking 60% of leads at the qualification step. Rebuilt the prompt routing layer and added a warm-lead override. Cut leakage to 22% in 4 weeks."

### Owned-X
> "Owned [scope] · [Specific work] · [Result]"

Example:
> "Owned the analytics layer for the sales funnel — multi-channel instrumentation across call, chat, and email. Single source of truth for conversion + drop-off."

### Shipped
> "Shipped [thing] for [audience] · [Result/scope]"

Example:
> "Shipped a Slack-native analytics bot — 12 parallel data endpoints, two-stage LLM pipeline. Used by ~200 active users at peak."

### Cut / Grew / Moved
> "[Cut/Grew/Moved] [metric] from [before] to [after] in [time]"

Example:
> "Cut customer support response time from 18h to 2h in 90 days, saving an estimated $400k/yr in headcount."

### Built / Designed
> "Built [thing] from [scratch / baseline] · [Result or scope]"

Example:
> "Built a voice qualification agent from scratch on a self-hosted call stack. 4-checkpoint flow, mid-call multilingual code-switching. Handled ~80 calls/day at peak."

---

## Number examples by role type

If the user has none of these, push them in Phase 5 to think harder. Below is a reference of what good looks like.

### Engineering
- "Cut p95 API latency from 800ms to 180ms across 12 services."
- "Reduced infra spend by $40k/month after migrating 6 workloads to spot instances."
- "Shipped feature [X] used by 200k daily active users."
- "Authored 47 PRs to the team's open-source library."

### Product
- "Owned the activation funnel — moved DAU from 12% to 28% of registered users."
- "Launched 3 features in Q3 that drove $1.2M in incremental ARR."
- "Reduced new-user time-to-aha from 4 days to 18 minutes."

### Design
- "Redesigned 8 core flows used by 500k+ users; bounce rate dropped 31%."
- "Built and shipped a component library across 4 product teams."

### Sales
- "Closed $1.4M in new logo ARR in 11 months, 130% of quota."
- "Built and ran an outbound playbook that generated 84 SQLs in Q4."

### Marketing
- "Grew product newsletter from 0 to 12k subscribers in 8 months at $0 paid spend."
- "Shipped 5 paid campaigns; CAC dropped from $290 to $140."

### Operations / Ops-y roles
- "Onboarded 45 customers per month at <2 hr per onboarding."
- "Rebuilt the QBR process — saved an estimated 80 hrs/quarter for the leadership team."

### Founder / Founder's Office
- "Ran ops, customer success, and partnerships across 11 months. Shipped 3 customers and a $25L corporate order."
- "Built the entire reporting stack the founders use in weekly review."

### Career-switcher / internship
- Even thin roles need a number. Use scope:
  - "Worked on a 4-person team owning the X product"
  - "Tested 3 generative AI tools (SD3, Midjourney, DALL·E 3) against artist briefs"
  - "Wrote 16 customer interview reports across 9 weeks"

---

## "Why it mattered" close

Only add if the entry directly bridges to the user's north_star. Skip otherwise.

Examples:
- "This is where I learned that the highest-leverage operator in an early-stage company is the one who can wire AI into the boring parts of the business."
- "First time I saw a product that I built used by real customers at production scale. It changed how I think about engineering quality."
- "Where the AI builder identity started."

---

## Stack line (optional)

For technical roles, single line at the bottom:
```
Stack: [Tool 1], [Tool 2], [Tool 3], [Tool 4].
```

---

## Sample full entry

```
Product Analyst, Northwind (a B2C marketplace) — Mar 2025 – Jan 2026

Owned the analytics and operational logic that moved a customer through Northwind's multi-channel sales funnel — from first inbound call to a closed deal.

• Designed the funnel instrumentation across our call, chat, and email channels — single source of truth for conversion, drop-off, and agent performance.
• Built the operational logic for voice + WhatsApp + chat routing, cutting handoff latency between channels by ~40%.
• Shipped 10+ call-flow configurations (agent-mapped routing, single-queue ACD) — improved first-touch connectivity by 20-25% and shortened time-to-first-contact by 30% across live campaigns.
• Partnered with engineering on a CRM × messaging integration — iframe UX design, action placement, workflow logic. Reduced agent context switching by ~40%.
• Built and optimized WhatsApp engagement funnels using approved templates; drove ~15-20% higher response rates and reduced manual follow-ups by ~25-30%.

Stack: Python, SQL, Metabase, a CRM, a messaging platform, a contact-center stack.
```

This is what every Experience entry should look like. (The company and tools above are synthetic — swap in the user's real ones.)

---

## What to never produce

- Bullets that just describe what the role is, not what the user did.
  - Bad: "Worked on the marketing team."
  - Good: "Owned paid acquisition across Meta + Google; cut CAC by 51% in 6 months."
- Bullets that claim credit for the team's work.
  - Bad: "Our team grew revenue 80%."
  - Good: "Led the 3-person growth team that grew revenue from $400k to $720k MRR."
- "Responsible for" — instantly recognizable as the cliche it is.
- More than 2 acronyms per bullet.
- Past-tense in a current role (signals the user is unconsciously leaving).
- Bullets longer than 25 words.
