# 12-point audit rubric

Each area is scored 0–10. Use the score bands below. Always include a one-line justification that names a specific thing on the user's profile.

---

## 1. Profile photo

| Score | What it means |
|-------|---------------|
| 0 | Missing entirely or LinkedIn default avatar |
| 3 | Poorly cropped, dim lighting, group photo, sunglasses |
| 5 | OK phone selfie, neutral background, head visible |
| 7 | Decent quality, even lighting, smart-casual attire |
| 10 | Professional headshot, clean background, eye contact, light smile |

Justification format: "Photo is [description]. Lighting is [description]. Background is [description]."

---

## 2. Banner

| Score | What it means |
|-------|---------------|
| 0 | Default LinkedIn grey pattern |
| 3 | Generic stock photo, abstract design with no tie to the user |
| 5 | OK personalized image with weak/no copy |
| 7 | Branded with intentional layout, no copy or weak copy |
| 10 | Branded, hero text that sells the user's mission, mobile-safe layout |

Justification format: "Banner is [missing / stock / personalized] and the copy is [none / weak / strong]."

---

## 3. Vanity URL

| Score | What it means |
|-------|---------------|
| 0 | Random characters (e.g. `/in/john-smith-27a5b7233`) |
| 5 | Long but clean (e.g. `/in/john-smith-product-manager-bengaluru`) |
| 8 | First-last hyphenated (e.g. `/in/john-smith`) |
| 10 | First-last clean (e.g. `/in/johnsmith` or `/in/jsmith`) |

Justification format: "Slug is `/in/[slug]`. [Has / doesn't have] random characters."

---

## 4. Headline

| Score | What it means |
|-------|---------------|
| 0 | "Open to Work" or completely missing |
| 3 | Just a job title (e.g. "Software Engineer") |
| 5 | Job title + company (e.g. "Software Engineer at Stripe") |
| 7 | Role + 1-2 keywords + city (or company) |
| 10 | Role + verb-driven outcome + 2-3 keywords + city or audience |

Justification format: "Headline is '[truncated to 80 chars]'. It [is / isn't] aware of the target person."

---

## 5. About

| Score | What it means |
|-------|---------------|
| 0 | Missing entirely |
| 3 | Generic AI-written paragraph with cringe phrases |
| 5 | OK summary, no hook, generic CTA |
| 7 | Has hook, mostly specific, weak CTA |
| 10 | Hook works mobile-truncated, specific, voice matches target persona, clear CTA |

Justification format: "About is [N chars]. First sentence is '[hook]'. [Includes / doesn't include] cringe phrases."

---

## 6. Featured

| Score | What it means |
|-------|---------------|
| 0 | Missing section entirely |
| 3 | 1 tile, generic |
| 5 | 1-2 tiles, OK content |
| 7 | 3 tiles, decent OG previews |
| 10 | 4+ tiles, strong OG previews, every tile resolves and is on-brand |

Justification format: "[N] tiles. [All / some / none] have OG preview images. [All / some] link to live content."

---

## 7. Experience

| Score | What it means |
|-------|---------------|
| 0 | Entries with only job title, no description |
| 3 | Generic role descriptions, no outcomes |
| 5 | Some bullets, no numbers |
| 7 | Outcome bullets in most entries, some numbers |
| 10 | Every entry has a 1-line summary + 3-5 outcome bullets with numbers + stack line |

Justification format: "[N] entries. [N] have descriptions. [N] have at least one number/metric. [Strongest entry is X / weakest is Y]."

---

## 8. Education

| Score | What it means |
|-------|---------------|
| 0 | Missing or wildly outdated |
| 5 | Present but bare (school name only) |
| 8 | Degree + dates + school |
| 10 | Degree + dates + school + relevant honors/clubs (only if they support positioning) |

Justification format: "[N] education entries. [Includes / doesn't include] dates."

---

## 9. Skills

| Score | What it means |
|-------|---------------|
| 0 | Missing entirely |
| 3 | All clutter (Forage sims, irrelevant tech, "Microsoft Office") |
| 5 | Mix of relevant + clutter, no top 5 pinned |
| 7 | Mostly relevant, weak top 5 pin |
| 10 | Focused tag set (< 35 skills), top 5 pinned to match target person, no clutter |

Justification format: "[N] skills total. Top 5 is [list]. Includes [X] clutter items."

---

## 10. Recommendations

| Score | What it means |
|-------|---------------|
| 0 | Zero |
| 5 | 1-2 |
| 7 | 3-4, mostly old or generic |
| 10 | 5+, recent, specific, mix of managers/peers/clients |

Justification format: "[N] recommendations. Most recent is [date]. [Generic / specific]."

---

## 11. Activity

| Score | What it means |
|-------|---------------|
| 0 | Nothing in 6+ months, or only reposts |
| 3 | 1 post in last 90 days |
| 5 | 1 post per month |
| 7 | 1 original post per week |
| 10 | 3+ original posts per week, consistent voice |

Justification format: "[N] original posts in last 30 days. [N] reposts. Last post was [date]."

---

## 12. Privacy & safety

| Score | What it means |
|-------|---------------|
| 0 | "Share profile updates with network" is On (will spam connections), "Open to Work" public ring is enabled (kills inbound from execs), public visibility is fully closed when it shouldn't be |
| 5 | One or two settings off-recommended |
| 8 | Most settings sane |
| 10 | "Share profile updates" Off (or appropriately On for the user's strategy), "Open to Work" frame configured correctly, public visibility appropriate for target audience |

Justification format: "Share-profile-updates is [On/Off]. Open-to-Work ring is [public/recruiters-only/off]. Public visibility is [appropriate/inappropriate]."

---

## Composite score

```
composite = sum(score × reach_weight) / sum(reach_weight)
```

Reach weights:
- 1 Profile photo: 1.3
- 2 Banner: 1.3
- 3 Vanity URL: 1.2
- 4 Headline: 1.5
- 5 About: 1.4
- 6 Featured: 1.2
- 7 Experience: 1.1
- 8 Education: 0.6
- 9 Skills: 1.0
- 10 Recommendations: 0.9
- 11 Activity: 1.0
- 12 Privacy & safety: 0.8

Round composite to 1 decimal. Show as `X.Y / 10`.

---

## Top 3 fixes

Sort by:
```
priority = (10 - score) × reach_weight
```

Highest priority three are the "Top 3 fixes" in the audit report. Phase 5 weights these higher when generating rewrites.

---

## Target-person-adaptive weights

The reach weights above are the default. Once Phase 3 has established the `target_person`, shift the weights to match what that reader actually scans. The composite formula stays the same. Only the weights move.

| target_person | Bump | Drop | Why |
|---------------|------|------|-----|
| Recruiter | Skills (+0.4), Headline (+0.3) | Activity (-0.4) | Recruiters search by keyword and scan the headline first. Post cadence barely registers in a search-driven screen. |
| Client / buyer | Featured (+0.4), About (+0.3) | Education (-0.2) | A buyer wants proof of outcomes and a clear story. Featured tiles and the About hook carry that. Degree matters little. |
| Hiring manager / peer | Experience (+0.3), About (+0.2) | Vanity URL (-0.2) | They read the work history closely and judge the narrative. The slug is cosmetic to them. |
| Investor / partner | About (+0.3), Featured (+0.3), Activity (+0.2) | Skills (-0.3) | They want vision, traction, and a public point of view. A tag list does nothing for them. |

Apply the shift, then renormalize as usual (`sum(score × weight) / sum(weight)`). Note in the audit report which weighting was used: "Scored for a recruiter audience: Skills and Headline weighted higher, Activity lower."

---

## Output QA: does the rewrite actually beat the baseline?

A high rubric score is necessary but not sufficient. A draft can score 9/10 and still read like every other AI-written profile. Before shipping any generated draft (headline, About, top Experience entry), run this head-to-head check. Sketch a 30-second generic-AI version of the same field in your head (the "results-driven professional passionate about..." version), then score the real draft against it on five dimensions:

| Dimension | Question | Generic AI loses when... |
|-----------|----------|--------------------------|
| Domain specificity | Could this only have been written about this person's actual field? | It uses interchangeable nouns ("solutions", "results", "organizations"). |
| Lived-experience signal | Does it sound like someone who did the work, not someone describing it? | It narrates roles instead of naming a specific thing that happened. |
| Operational concreteness | Are there numbers, named tools, or real scope? | It has zero numbers and no named tool. |
| Compression | Is every line earning its place? | It pads with adjectives and transition words. |
| Voice | Does it match the user's `voice_mode` and read like a person typed it? | It's flat, evenly-paced, and could be any voice. |

**Only ship the draft if it clearly beats the sketched baseline on a majority of these.** If it ties or wins on only two, regenerate. The bar is not "is this good?" It's "would anyone be able to tell a human stood behind this rather than a model?"

Record the result briefly in the plan: "Headline beats the generic baseline on domain specificity, concreteness, and voice. Shipping."

---

## The 5-question message test (gate before showing any copy)

Borrowed from positioning and brand work. Before any generated text field is shown to the user, it must pass all five. This is a gate, not a score. A single clear "no" means rewrite before showing.

1. **Clear.** Would the target_person understand what this person does in one read, with no jargon they'd have to decode?
2. **Differentiated.** Could a direct competitor copy this line onto their own profile word-for-word and have it be just as true? If yes, it's not differentiated. Sharpen it until only this person could have written it.
3. **Credible.** Is every claim backed by something real in the CV or discovery? No invented numbers, no borrowed credentials.
4. **Compelling.** Does it give the reader a reason to keep reading or to reach out? A true-but-boring line still fails.
5. **Consistent with voice.** Does it match the `voice_mode` set in Phase 3, and is it free of the formatting tells in `audit/cringe-detector.md`?

The Differentiated test is the one most drafts fail. When in doubt, run it first: if a competitor could say the exact same thing, the copy isn't done.
