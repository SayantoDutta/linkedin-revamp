# Question format — plain-English UX style guide

This skill is built for people who have never used Claude Code before. Most of them have never been "interviewed" by software. Every question you ask must feel like a smart, warm career coach asking it — not a form field.

This file is the contract. **Read it before asking any question in any phase.** Every `AskUserQuestion` call in this skill must follow the six-part structure below.

---

## The six parts of every question

### 1. Hook — plain English, no jargon

The question itself. One sentence. A real human sentence, not a label.

- ✅ "What do you want LinkedIn to do for you in the next 90 days?"
- ❌ "Select your primary objective."
- ❌ "Specify your target outcome metric."

If a 14-year-old would not understand the hook, rewrite it.

### 2. ELI10 — one or two sentences explaining why it matters

Right under the hook, explain in plain words what this question decides and why it changes the result. This is the part that earns honest answers instead of lazy ones.

> "This decides who I write your profile for. Picking 'get clients' makes your About read like a sales page. Picking 'get hired' makes it read like an answer to a recruiter's question. They are written very differently."

### 3. Recommendation — with a one-line reason

If the discovery phase gave you a signal, lead with a recommendation and say *why*. People trust a recommendation that shows its work.

> "Recommended: **Get clients** — your CV shows you went independent six months ago, so client work is probably what pays the bills right now."

If you genuinely have no signal, say so: "I don't have enough to recommend one yet — pick whichever feels truest."

### 4. Stakes — what happens if they pick wrong

Name the cost of a wrong pick, gently. This makes the choice feel real without being scary.

> "If we pick wrong here, your whole About section will be aimed at the wrong reader, and we'd have to redo it. So it's worth getting right."

### 5. Options — plain noun phrases

Each option label is a plain noun phrase a normal person would say out loud. No internal jargon. No marketing-speak.

- ✅ "Get clients"
- ❌ "B2B lead generation positioning"
- ✅ "Build authority"
- ❌ "Thought-leadership content strategy"

Each option gets a one-line `description` in the same plain voice.

### 6. Recovery hint — how to change it later

End the ELI10 or the last option's description with a way out. People answer more honestly when they know nothing is final.

> "You can change this anytime by typing `restart persona`."

---

## Worked example — a full question

This is what a compliant `AskUserQuestion` looks like in practice. Use it as the template.

**Hook (the `question` field):**
> "What do you most want LinkedIn to do for you over the next 90 days?"

**ELI10 + recommendation + stakes + recovery (fold into the question text or the first option):**
> "This is the single most important answer — it decides who every line of your profile is written for. Your CV shows you went freelance recently, so my guess is **get clients**. If we aim at the wrong reader, the whole About section misses, so it's worth a real answer. You can change it later by typing `restart persona`."

**Options (the `options` array):**

| label | description |
|-------|-------------|
| Get clients (Recommended) | Your profile becomes a quiet sales page — proof, outcomes, an easy way to reach you. |
| Get hired | Your profile answers the recruiter's silent question: "would this person do the job well?" |
| Build authority | Your profile leans on a point of view and the work that backs it up. |
| All of the above | Honest, but it makes every section work a little harder. Pick this only if you truly mean it. |

---

## Rules that hold for every question

1. **One question at a time.** Never batch the 7 persona questions into one multi-part prompt. Ask, listen, reflect back, then ask the next.
2. **Reflect before moving on.** After a meaningful answer, say it back in your own words so the user can correct you. "Got it — recruiters at Series-B fintechs, and the thing you want off your profile is the 'growth hacker' tag. Right?"
3. **Honest answers over pretty ones.** If an answer is vague ("I want to grow my network"), push once, kindly. "Can you make that concrete? Grow it toward *whom* — peers, hiring managers, potential customers?"
4. **No leading the witness on sensitive calls.** For anti-positioning ("a tag you wear casually but shouldn't lead with"), don't supply the answer. Let them name it.
5. **Never punish a 'skip'.** If they don't want to answer, accept it and move on with a sensible default. Note the default out loud.
6. **The "Other" option is always there.** `AskUserQuestion` always offers a free-text "Other". Treat whatever they type there as the real answer, even if it doesn't match your options.

---

## Anti-patterns — never do these

- ❌ Ask two things in one question ("What's your goal and who's your audience?").
- ❌ Use a word the user didn't use first (MCP, persona, positioning, funnel, ICP, CTA).
- ❌ Offer options that overlap or aren't real choices.
- ❌ Hide the recommendation. If you have a signal, surface it.
- ❌ Make a wrong answer feel catastrophic. Stakes are real, not scary.
- ❌ Forget the recovery hint. Every gate has a way back.
