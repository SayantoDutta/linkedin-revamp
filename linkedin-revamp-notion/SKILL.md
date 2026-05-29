---
name: linkedin-revamp-notion
description: Turns a user's projects into publishable Notion case-study pages and links them to the LinkedIn Featured section. Each page follows a proven case-study structure (problem, approach, outcome, proof) in plain language. Triggers when the user says "make case studies", "write up my projects", "Notion case study", or invokes `/linkedin-revamp-notion`. Also offered by `/linkedin-revamp` in Phase 8 when the user has 2+ projects and the Notion MCP is connected. Requires the Notion MCP.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Glob, AskUserQuestion, WebFetch, mcp__notion__*
---

# linkedin-revamp-notion — Case-study pages from your projects

> Optional add-on to `/linkedin-revamp`. Also runs standalone. Turns the projects already on your CV into clean, public Notion case-study pages, then links them to your LinkedIn Featured section so a visitor can click through to the full story.

A LinkedIn Featured tile is a headline. A case-study page is the proof behind it. This sub-skill writes that proof — one page per project, in a structure that recruiters and clients actually read — and publishes each one as a public Notion page you can link anywhere.

**Time required:** about 20 minutes for 2–3 projects.
**You will need:** the Notion MCP connected to Claude, and 2 or more projects worth writing up (from your CV, portfolio, or just described to the skill).

---

## What it produces

For each project, one public Notion page following this structure (detail in `templates/case-study-structure.md`):

1. **One-line summary** — what it is, who it's for.
2. **The problem** — what was broken or missing, in plain terms.
3. **The approach** — what you did, the key decisions, the stack (kept readable for non-technical readers).
4. **The outcome** — numbers if you have them, the visible result if you don't.
5. **Proof** — a screenshot, a link to the live thing, a quote.
6. **A short "what I'd do next" or "what I learned"** — shows judgment, not just execution.

Each page is published to the web, and its public URL is handed back so it can go into LinkedIn Featured.

---

## When this skill offers itself

Through `/linkedin-revamp` Phase 8, the core skill only offers this when **both** are true:

- The user's CV or portfolio surfaced **2+ projects** worth documenting.
- The **Notion MCP is connected** (a `mcp__notion__*` tool — or a Notion search/create tool — responds without error).

If either is false, the core skill skips the offer. Run standalone any time with `/linkedin-revamp-notion`.

---

## Pre-flight

Run these checks silently before greeting the user:

1. **Notion MCP available.** Attempt a lightweight Notion call (search for a known-nonexistent string, or list databases). If it errors with "tool not found" or an auth error, stop and tell the user in plain English:
   > "This add-on writes pages into your Notion. To do that, Claude needs to be connected to your Notion account. In Claude, open Settings → Connectors → Notion and connect it, then come back and type `ready`."
2. **A destination exists.** Notion pages must be created somewhere. Ask the user which Notion workspace/parent page to put the case studies under (Step 1 below). If the MCP can list pages, offer the top few as choices.

Only continue once the Notion MCP responds and a destination is chosen.

---

## Step-by-step

### Step 1 — Find the destination

Ask, plain English — clear hook, a one-line "why this matters", a recommendation, and a way to change the answer later. (If the core `linkedin-revamp` skill is installed alongside this one, follow its `linkedin-revamp/references/question-format.md` style guide; if not, the plain-English rule here is enough.)

> **"Where in your Notion should these case studies live?"**
> ELI10: "I'll create one page per project. They can sit under an existing page (like a 'Portfolio' or 'Work' page) or I can make a fresh parent page called 'Case Studies'. Either is fine — you can move them later."

If the Notion MCP can list pages, present a few as options plus "Make a new 'Case Studies' page". Otherwise ask the user to paste the URL or name of the parent page.

### Step 2 — Identify the projects

If invoked from the core skill, you already have the projects from the CV parse in Phase 2 — reuse them. If standalone, ask:

> **"Which projects should I write up? Name 2 to 4."**
> ELI10: "Pick the ones you most want a visitor to see. Quality over quantity — three strong case studies beat eight thin ones."

For each project, gather what you need to fill the template. Pull from the CV/portfolio first; ask only for what's missing. One project at a time:

> **"For [project], what was the problem you were solving — what was broken or missing before you built it?"**
> **"What did you actually do? Walk me through it like you're explaining to a smart friend, not a panel."**
> **"What was the result? A number is gold — users, time saved, money, speed. If you don't have a number, what's the visible difference?"**
> **"Got a screenshot or a live link I can put as proof?"**

Keep answers honest. If a project has no real outcome yet, say so on the page ("early — first users onboarding now") rather than inventing one. The cringe rules from the core skill apply: no "revolutionary", no "cutting-edge", no "passionate".

### Step 3 — Draft each page

Use `templates/case-study-structure.md` for the section order and `templates/notion-page-style.md` for formatting (headings, callouts, toggle blocks, image placement).

Draft the full page in markdown first. Show it to the user **before** creating anything in Notion:

> "Here's the draft for [project]. Read it — does the problem/approach/outcome read true? Type `looks good` to publish it to Notion, or tell me what to fix."

Run every drafted page through a cliché check before the user sees it — block hype words ("revolutionary", "cutting-edge", "passionate", "game-changing", "leverage", "synergy") and the anti-AI prose tells (no em dashes between phrases, vary sentence length, use contractions). If the core `linkedin-revamp` skill is installed alongside this one, use its fuller blocklist at `linkedin-revamp/audit/cringe-detector.md`.

### Step 4 — Create the Notion page

Once approved, create the page via the Notion MCP under the chosen parent. Map the markdown to Notion blocks:

- Page title = project name.
- One-line summary → a callout block at the top.
- Each section heading → a Notion heading block.
- Body → paragraph blocks.
- Stack/details → a bulleted list or a toggle.
- Proof screenshot → an image block (if the user provided an image; upload or embed by URL).
- Link to the live thing → a bookmark or link block.

After creating, **publish the page to the web** so it has a public URL. The exact mechanism depends on the Notion MCP's capabilities:

- If the MCP exposes a "share to web" / "publish" action, call it and capture the public URL.
- If it does not, create the page and then tell the user the one manual step:
  > "Page created. Notion's API can't flip the 'Share to web' switch, so do this once: open the page, click **Share** (top right) → **Publish** → **Publish to web**, then paste me the public link. I'll add it to your LinkedIn Featured."

Capture the final **public** URL for each page — that's what goes on LinkedIn.

### Step 5 — Hand the URLs to LinkedIn Featured

Collect all published page URLs with their titles and a one-line description each.

- **If running as part of `/linkedin-revamp`:** hand the list back to the core skill's Featured-tile flow (Phase 6 Step 6.7). It adds each as a Featured "link" tile, overriding the auto-fetched title/description with the clean ones from here.
- **If running standalone:** tell the user how to add them:
  > "Your case studies are live. To feature them on LinkedIn: profile → Featured → + → Add a link → paste the URL. Repeat for each. Or run `/linkedin-revamp` and I'll add them for you with proper titles."

### Step 6 — Recap

> "Done. [N] case studies published:
> • [Title] — [public URL]
> • [Title] — [public URL]
> Each one tells the full story behind a Featured tile. You can edit them anytime in Notion — they update live."

---

## Templates

- **`templates/case-study-structure.md`** — the six-part case-study skeleton with a worked, anonymized example and guidance on what makes each section land.
- **`templates/notion-page-style.md`** — how to map the markdown draft to Notion blocks (callouts, headings, toggles, images), plus formatting do's and don'ts for a page that reads clean.

---

## Safety + scope

- **Approval before creation.** No Notion page is created until the user approves the draft. Nothing is published to the web without the user seeing it first.
- **Reads only what the user provides.** Project details come from the CV/portfolio already in context or from the user's answers. The skill doesn't crawl the user's whole Notion.
- **Writes only under the chosen parent.** Pages are created under the destination the user picked in Step 1 — nowhere else.
- **No fabricated outcomes.** If a project has no result yet, the page says so honestly. Cringe filter blocks hype.
- **Public-by-consent.** Publishing to the web is an explicit, named step. The skill never makes a page public silently — if it can publish via the API it tells the user it's doing so; if it can't, the user does the one-click publish themselves.
- **No third-party calls beyond Notion.** Drafting is Claude-only. The only external service touched is the user's own Notion, via the connected MCP.

---

## Troubleshooting

- **"Notion isn't connected."** Settings → Connectors → Notion in Claude, connect, then type `ready`.
- **"The page created but isn't public."** Notion's API often can't toggle web-publish. Open the page, Share → Publish to web, paste the public link back.
- **"The image didn't show up."** If the proof screenshot was a local file, the MCP may need a URL instead. Upload the image somewhere public (or to Notion directly via the UI) and give the skill the URL.
- **"I don't have numbers for my project."** That's fine. The page leads with the visible result and what you learned. Honest beats inflated — recruiters can smell a fake metric.

---

## License

MIT. Part of the `linkedin-revamp` suite. You own the pages you create.
