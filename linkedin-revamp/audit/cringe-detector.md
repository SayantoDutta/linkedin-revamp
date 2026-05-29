# Cringe-phrase detector

A blocklist of phrases that signal AI-generated text, junior positioning, or LinkedIn-fluff convention. Run against every text field — headline, About, Experience descriptions, Featured tile descriptions, posts.

The detector is not a hard block — it surfaces matches to the user. The user can choose to keep a flagged phrase, but they have to do it knowingly.

---

## Blocklist (case-insensitive)

### Self-description cliches
- "passionate"
- "passionate about"
- "results-driven"
- "hard worker"
- "go-getter"
- "self-starter"
- "team player"
- "detail-oriented"
- "fast learner"
- "natural leader"
- "out of the box thinker"
- "thinks outside the box"
- "wears many hats"
- "wear many hats"
- "jack of all trades"
- "dynamic" (as self-description, says nothing about a person)
- "think outside the box"

### Tech-bro / consultant fluff
- "synergy"
- "synergies"
- "leverage" (as a verb)
- "leveraging"
- "pivot" (when used as positioning)
- "disruptor"
- "disruptive"
- "transformative"
- "game-changer"
- "game-changing"
- "paradigm shift"
- "circle back"
- "deep dive"
- "low-hanging fruit"
- "move the needle"
- "boil the ocean"
- "core competency"
- "value-add"
- "utilize" (just say "use")
- "streamline"
- "holistic"
- "ecosystem" (when used loosely, not a literal technical platform)
- "paradigm"
- "facilitate" (just say "run" or "lead")
- "impactful"
- "crucial"

### Title inflation
- "rockstar"
- "ninja"
- "wizard"
- "guru"
- "evangelist" (unless the role literally is "Developer Evangelist")
- "thought leader"
- "thought leadership"
- "visionary"
- "luminary"
- "trailblazer"
- "unicorn"

### Vague claims with no proof
- "extensive experience"
- "proven track record"
- "demonstrated ability"
- "strong background in"
- "world-class"
- "world-leading"
- "industry-leading"
- "best-in-class"
- "cutting-edge"
- "state-of-the-art"
- "next-generation"
- "award-winning" (unless followed by a specific award name)

### AI-generated tells
- "in today's fast-paced world"
- "in today's rapidly evolving"
- "in today's digital age"
- "in the ever-changing landscape"
- "delve into"
- "delve" (bare — the single most common AI verb tell)
- "underscore"
- "tapestry of"
- "navigate the complexities of"
- "harness the power of"
- "unlock the potential of"
- "robust solutions"
- "innovative solutions"
- "nuanced understanding"
- "comprehensive understanding"
- "multifaceted approach"
- "furthermore" (as a sentence start)
- "moreover" (as a sentence start)
- "additionally" (as a sentence start)

### LinkedIn-specific cliches
- "excited to share"
- "excited to announce"
- "thrilled to announce"
- "humbled to"
- "honored to"
- "blessed to"
- "looking forward to"
- "open to opportunities"
- "feel free to connect"
- "let's connect"
- "open to networking"
- "open to feedback"
- "always learning"
- "lifelong learner"
- "and so much more"
- "to name a few"
- "the list goes on"

### Empty intensifiers
- "very" (when paired with skills)
- "extremely" (when paired with skills)
- "highly motivated"
- "highly skilled"
- "deeply passionate"
- "incredibly talented"
- "absolutely committed"

---

## Anti-AI formatting

The blocklist above catches bad *words*. This section catches bad *structure* — the formatting tells that make prose read as machine-written even when every word is clean. These are not phrase matches. They are checks on the shape of the text. Apply them to every generated text field (headline, About, Experience descriptions, Featured tile descriptions, posts).

1. **No em dashes or en dashes between phrases in prose.** This is the single strongest AI tell. Where a draft uses `—` or `–` to splice two clauses, rewrite. Use a period, a comma, or split into two sentences. The one exception: an en dash inside a numeric range is fine ("18 months", "2024–2026", "$1.2M–$1.5M").
2. **No semicolons in casual writing.** They read as formal and machine-assembled. Replace with a period or a comma. A LinkedIn profile is not an academic paper.
3. **No transition words at sentence starts.** Cut "Furthermore", "Additionally", "Moreover", "In conclusion", "In summary". Human writing rarely signposts like this. Start the sentence with its actual content.
4. **Vary sentence length.** AI prose runs every sentence at the same medium length. Mix short (5–8 words) with longer (15–22 words). The variation is what makes it sound like a person typed it.
5. **At least one noticeably short sentence per paragraph.** A 3–5 word sentence breaks the rhythm and lands a point. "It worked." "That changed everything." Use it for emphasis.
6. **Use contractions naturally.** "I've", "I'm", "it's", "doesn't", "can't". Spelled-out forms ("I have", "it is") in casual prose read as stiff and AI-default. Contract unless the full form is doing deliberate emphasis.

### How to check formatting

For each generated text field, before showing or pushing:

1. Scan for `—` and `–`. If found between clauses (not in a numeric range), flag and rewrite.
2. Scan for `;`. Flag each one.
3. Scan sentence starts for the transition words above.
4. Measure sentence lengths across the field. If they cluster within a narrow band (all 10–15 words, say), the rhythm is too even. Rewrite to add a short one.
5. Check for at least one contraction where the voice is casual.

Treat a formatting violation the same as a blocklist hit: rewrite the line, or surface it to the user with the same "want me to rewrite or leave it?" prompt.

**Run this on every generated text field both before it's shown to the user (Phase 5) and before it's pushed live (Phase 6).** A field can pass the word blocklist and still fail here.

---

## Allowlist overrides per industry

Some flagged words are core vocabulary in specific industries. If the user's CV or `north_star` indicates they work in one of these, do not flag the listed words.

### Crypto / web3
- "decentralized" (would otherwise smell of fluff in some contexts)

### AI / ML
- "fine-tuning" (this is real work, not fluff)
- "embedding" (legitimate technical term)
- "agentic" (current industry term)

### Sales
- "pipeline" (legitimate)
- "closer" (legitimate)
- "outbound" (legitimate)

### Marketing
- "growth" (legitimate)
- "funnel" (legitimate)
- "demand gen" (legitimate)

### Startups / venture
- "GTM" (legitimate)
- "PMF" (legitimate)

---

## How to use this file

When the cringe detector runs, for each text field:

1. Tokenize the field into sentences.
2. For each phrase in the blocklist, do a case-insensitive search across all sentences.
3. If matched, capture:
   - The phrase
   - The field name
   - The sentence it appears in
4. Cross-check against the allowlist override for the user's role. If a match is allowlisted, skip.
5. Output the remaining matches as a list.

---

## What to do with matches

In Phase 4 (audit), the matches are listed in the audit report.

In Phase 5 (plan), before showing any draft to the user, run the cringe detector on the draft itself. If a match is found in the user-facing draft, either:
- Rewrite the line to remove the phrase
- Or flag the match to the user explicitly: "Heads up — this draft uses 'passionate', which is on the cringe blocklist. Want me to rewrite or leave it?"

In Phase 6 (execute), never push a text field to live without passing it through the cringe detector one last time. If a match is found at push time, surface it and require user confirmation.
