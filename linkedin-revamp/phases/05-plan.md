# Phase 5 — Plan

## What this phase does

Drafts the proposed new version of every editable section — vanity URL, headline, About, banner concept, experience bullets, skills set, Featured tile suggestions. Shows the user each one side-by-side with the current version. The user approves, edits, or skips each one.

The output is `rewrite-pack.md` — a per-section decision log that Phase 6 reads when pushing changes live.

This phase is still read-only. No live changes are made until Phase 6.

---

## How to run this phase

### Step 5.1 — Set expectations

> Now I'm going to write what I'd propose as the new version of every section. For each one, I'll show you what you have today and what I'd change it to. You'll approve, edit, or skip each one.
>
> Nothing goes live in this phase. We're still in planning. You can change your mind on any section.

### Step 5.2 — Draft each section using the templates

Load the relevant template file from `templates/` for each section. Apply the user's `user_profile` from Phase 3 and the current state from the Phase 2 snapshot.

Sections to draft, in this order:

#### 5.2.1 — Vanity URL

Load `templates/skills-rubric.md` is not needed. This one is mechanical.

Current: `linkedin.com/in/{current-slug}`.

Proposed: extract first/last name from `cv_parsed.full_name`. Propose three candidates:
1. `firstname-lastname` (e.g. `jane-smith`)
2. `firstnamelastname` (e.g. `janesmith`)
3. `firstnamelastinitial` (e.g. `janes`)

Recommend the cleanest available. Note: I can only confirm an option is actually free later, when I'm on the LinkedIn edit page — for now I'm recommending the cleanest one and we'll catch any clash then.

Show the user:
```
## Vanity URL
- Current: linkedin.com/in/{current}
- Proposed: linkedin.com/in/{recommended}
- Alternatives: ...
```

Use AskUserQuestion.

What this is, in plain words: your vanity URL is the web address of your profile — the link you paste into emails, resumes, and DMs. A clean one (your name) looks credible; one with random characters looks half-finished.

Recommend the first available candidate and say why — usually "it's the shortest version that's still clearly your name." If you have no clear winner, say so and let them pick.

Recovery hint: end with "Not sure? Accept the recommended one — you can come back and type `vanity url` to redraft this anytime."

Options:
- Accept the recommended
- Pick one of the alternatives
- Type my own custom link ending (for example, linkedin.com/in/your-name)
- Skip this section

#### 5.2.2 — Headline

Load `templates/headline-formulas.md`. It contains six reusable structures.

Generate four candidate headlines using different formulas. Each candidate must be:
- ≤ 220 characters (LinkedIn limit)
- Includes the user's role, value prop, 2–3 keywords
- Aware of `target_person`, `mission_90d`, and `voice_mode` from user_profile
- Free of every phrase in `audit/cringe-detector.md`

Show the user:
```
## Headline
- Current: "{current_headline}"
- Proposed (recommended): "{candidate_1}"
- Alt A: "{candidate_2}"
- Alt B: "{candidate_3}"
- Alt C: "{candidate_4}"
```

Use AskUserQuestion.

What this is, in plain words: your headline is the line under your name. It follows you everywhere — search results, hover cards, every connection request — so it's the most-seen sentence you own on LinkedIn. It decides whether the right person clicks.

Recommend the candidate that best fits the `target_person` and `mission_90d` from Phase 3, and say why — e.g. "this one leads with the role and keyword a recruiter searches for." If two are close, name the tradeoff in one line.

Recovery hint: end with "Want a different angle? Accept one for now, or type `headline` anytime and I'll write four fresh ones."

Options: Accept / Pick an alt / Edit (free text) / Skip.

#### 5.2.3 — About section

Load `templates/about-skeleton.md`. The template has a hook + 3-paragraph structure.

Draft the About using the user's `biggest_result`, `north_star`, `target_person`, `voice_mode`. Must:
- Hook in first 220 characters that survives mobile truncation
- 2–3 paragraphs after the hook, ~1500 characters total
- A clear "what's next" line near the end
- A clear CTA in the final paragraph (DMs open, email, etc.)
- Voice matches `voice_mode`
- Free of every cringe phrase

Show the user:
```
## About section
### Current
{current about text or "none"}

### Proposed
{drafted about text}
```

Use AskUserQuestion.

What this is, in plain words: the About section is your one chance to talk directly to the reader in your own voice. The first two lines show before the "see more" cut on mobile, so they have to earn the click. Get this right and the rest of the profile feels intentional.

Recommend "Accept" when the draft already matches the `voice_mode` and opens with a strong hook — say so. If the voice feels off, recommend "Rewrite with different voice" instead and name which voice you'd try.

Recovery hint: end with "Nothing here is locked — accept it for now, or type `about` anytime to redraft this section from scratch."

Options: Accept / Edit (offer to do specific tweaks) / Rewrite from scratch with different voice / Skip.

#### 5.2.4 — Banner concept

Load `templates/banner-prompts.md`. It contains prompt structures for image generation tools.

Generate a banner concept based on `voice_mode` and `target_person`:
- Brand palette suggestion (3 colors)
- Hero text proposal (≤ 6 words)
- Sub-tag proposal (≤ 12 words)
- Layout recommendation

Also generate a complete copy-paste prompt for Nano Banana / Midjourney / FLUX that the user can run externally.

Then call `helpers/build_banner.py` to render a draft banner using PIL. The script accepts:
- `--copy "Hero text"` — the main line
- `--sub "subtitle"` — the secondary line
- `--palette "color1,color2,color3"` — hex codes
- `--style minimal|bold|warm|cool` — preset

If the user gave a portfolio URL or attached a background image earlier, use it as the base. Otherwise generate a clean gradient.

Save to `snapshots/{handle}-{timestamp}-banner.png`.

Show the user:
```
## Banner
### Current
{describe current — "blank grey default", "stock photo", etc.}

### Proposed concept
- Palette: {colors}
- Hero text: "{hero}"
- Sub: "{sub}"
- Preview rendered to: snapshots/{handle}-{date}-banner.png
- AI prompt (for higher-fidelity version in Nano Banana): {prompt block}
```

Use AskUserQuestion.

What this is, in plain words: your banner is the wide image behind your photo. Most people leave it the default grey, which is a wasted billboard. A simple branded banner with a few words makes the whole profile look deliberate at first glance.

Recommend "Accept this draft" when the rendered preview already reads clean at a glance — say why. If the user has strong brand colors or their own image in mind, recommend they edit the palette or generate their own instead.

Recovery hint: end with "Not happy with it? Accept for now, or type `banner` anytime and I'll re-render it."

Options:
- Accept this draft
- Edit text & re-render
- Edit palette & re-render
- I'll make my own image from this prompt (skip the automatic upload) — I'll just hand you the copy-paste prompt to run in your own image tool
- Skip banner entirely

#### 5.2.5 — Experience entries

For each Experience entry from the snapshot:

Load `templates/experience-bullets.md`. It contains the PAR/STAR rewrite structure.

For each entry:
- Parse the existing description
- Identify the current role's outcomes from the CV (the CV is usually more honest than the live profile)
- Rewrite into 3–5 outcome-led bullets with numbers
- Add a 1-sentence summary lead-in
- Add a 1-line "why it mattered" close if the user gave good `north_star` context

Show the user each entry separately:
```
## Experience: {Role} at {Company} ({dates})
### Current
{current text}

### Proposed
{rewritten text}
```

Use AskUserQuestion per entry.

What this is, in plain words: each Experience entry is where you prove the headline is true. Outcome bullets with numbers ("cut response time 80%") beat duty lists ("responsible for support") every time — they're what a reader actually believes.

Recommend "Accept" when the rewrite is grounded in real outcomes from the CV — say so. If you had to invent or stretch a number, flag it and recommend the user edit it to something true.

Recovery hint: end each entry with "Accept for now if it reads true — you can type the company name anytime to redraft just that one."

Options: Accept / Edit / Skip this entry.

Loop until all entries are decided.

#### 5.2.6 — Skills section

Load `templates/skills-rubric.md`. It contains the universal keep/drop logic — not a hardcoded tag set.

Audit each current skill against the rubric using `user_profile` and `cv_parsed`. For each, classify:
- **KEEP** — relevant to target_person and north_star
- **DROP** — clutter (Forage sims if they don't support the narrative, expired tech, irrelevant tools)
- **AMBIGUOUS** — relevant for a different career direction; ask the user

Propose ADD list — skills that should be on the profile but aren't, based on cv_parsed and north_star.

Propose top-5 pin order based on positioning weight.

Show the user a 3-column table:
```
## Skills
| Action | Skill | Why |
|--------|-------|-----|
| KEEP | Product Management | Core to role |
| DROP | Microsoft Excel (Forage sim) | Clutter, dilutes signal |
| ADD  | RAG | Critical to north_star direction |
| PIN  | AI Agents | First impression in recruiter search |
```

Use AskUserQuestion as one big approval.

What this is, in plain words: your Skills list is how recruiters and search filters find you. Too many random skills dilute you; the right focused set makes you show up for the searches that matter. The top 5 pinned ones are your first impression in recruiter search.

Recommend "Accept all" when the KEEP/DROP/ADD/PIN logic is grounded in `north_star` and `cv_parsed` — say why. If several skills are AMBIGUOUS, recommend "Review item-by-item" so the user makes those calls.

Recovery hint: end with "Accept for now if it looks right — you can type `skills` anytime to revisit the whole list."

Options: Accept all / Review item-by-item / Skip the skills overhaul.

#### 5.2.7 — Featured tiles

Look at:
- `cv_parsed.projects`
- `portfolio_parsed.projects` (if portfolio exists)
- Existing Notion pages (if Notion MCP is available — Phase 8 will offer the add-on)

Propose 4 Featured tiles:
1. **Portfolio** — if a portfolio URL exists
2–4. **Project case studies** — pulled from cv_parsed.projects + portfolio_parsed.projects, prioritized by which most demonstrate `north_star`

For each tile, draft a title and description (≤ 200 chars).

Show the user:
```
## Featured tiles
1. [Portfolio] {url}
   "{description}"
2. [Project case study] {project name}
   Source: {URL or "needs to be created via /linkedin-revamp-notion sub-skill"}
   "{description}"
...
```

Use AskUserQuestion.

What this is, in plain words: Featured tiles are the clickable cards near the top of your profile — portfolio, case studies, key projects. They turn "trust me" into "here's the proof." A profile with strong Featured tiles converts a curious visitor into a believer.

Recommend the tiles that most demonstrate the `north_star` direction, and say why one beats another (e.g. "this case study shows the exact work your target person is hiring for"). If a tile needs a Notion page that doesn't exist yet, flag that it's a Phase 8 add-on, not something ready today.

Recovery hint: end with "Accept these for now if they fit — you can type `featured` anytime to swap them."

Options: Accept these 4 / Pick which to include (1-4) / Skip Featured for now.

### Step 5.3 — Generate dry-run preview

After all sections are decided, generate a single-page HTML preview of what the user's profile would look like after the rewrite. Save to `snapshots/{handle}-{timestamp}-preview.html`.

Use a simple Bootstrap-style template — no JavaScript, no external dependencies. The preview should look as close to a real LinkedIn profile as possible.

Tell the user:
> I've put together a preview of what your profile would look like after these changes. It's at `{path}`. Open it in your browser. It's a rough approximation, not pixel-perfect — but it shows you the rewrites in context.
>
> When you're ready to push these changes live, type `execute`. If you want to revise anything, type the section name (`headline`, `about`, `banner`, etc.) and I'll redraft just that one.

### Step 5.4 — Save the rewrite pack

Write `snapshots/{handle}-{timestamp}-rewrite-pack.md` with the final decisions per section:

```markdown
# Rewrite Pack — {Name}
{Date}

## Approval status
- Vanity URL: {accepted | edited | skipped}
- Headline: {accepted | edited | skipped}
- About: {accepted | edited | skipped}
- Banner: {accepted | edited | skipped}
- Experience: {N approved, M skipped}
- Skills: {accepted | item-reviewed | skipped}
- Featured: {accepted | partial | skipped}

## Final content per section

### Vanity URL
{final value}

### Headline
{final value}

### About
{final value}

### Banner
- Preview file: {path}
- Concept: {summary}

### Experience
For each entry:
- Title, Company, Dates
- Final description

### Skills
- DROP list: [...]
- ADD list: [...]
- PIN order (top 5): [...]

### Featured
- List of 4 tiles with title + description + URL
```

This is the file Phase 6 reads when pushing to LinkedIn.

---

## Outputs of Phase 5

- `snapshots/{handle}-{timestamp}-banner.png` (or banner prompt file if user opted to generate externally)
- `snapshots/{handle}-{timestamp}-preview.html`
- `snapshots/{handle}-{timestamp}-rewrite-pack.md`

---

## What to do if something goes wrong

- **User says "rewrite the headline" three times in a row.** Show all four candidates again and ask which formula they prefer. Then write four new candidates using that formula. If they reject again, ask them to type the headline themselves and accept it.
- **Banner generation fails (PIL crash).** Save the prompt to a file. Tell the user the script crashed but the prompt is ready for external use. Continue.
- **Skills ADD list contains skills the user has never used.** Trust the user. If they push back, remove the skill from the list. Never add a skill the user has not done.
- **User edits a section and the edit contains a cringe phrase.** Flag it once. If the user insists, push it anyway. Their profile, their call.
- **Preview HTML rendering fails.** Skip the preview. Tell the user. Continue.
