# Phase 3 — Persona Grill

## What this phase does

Asks the user 7 honest, mission-oriented questions about what they want LinkedIn to do for them. The answers drive every later rewrite — headline, About, experience bullets, skills set, banner direction, Featured tiles.

This phase is the single most important phase in the skill. A profile rewrite is only as sharp as the user's positioning. If the user gives vague answers, the rewrite will be vague.

This phase is conversational and read-only — nothing is changed on the live profile.

---

## How to run this phase

### Step 3.1 — Set expectations

Say:
> I'm going to ask you 7 questions now. They are mission-oriented — about what you want LinkedIn to do for you, who you want it to do it for, and what you actually want to be known for.
>
> Please be honest and specific. "I want to grow my career" gives me nothing to work with. "I want to land a head-of-AI role at a Series A fintech in Bengaluru in the next 6 months" gives me everything.
>
> Vague answers produce a vague profile. Specific answers produce a profile that actually works.
>
> One question at a time. You can change any answer later by typing `redo my answers`.
>
> Ready? Question 1 coming up.

### Step 3.2 — Question 1: 90-day mission

Use the AskUserQuestion tool. Follow the format in `references/question-format.md`.

```
question: |
  In one sentence — what do you want LinkedIn to do for you in the next 90 days?

  Why this matters: this is the single most important answer. It decides who every line of your profile is written for. "Land clients" makes your About read like a quiet sales page; "get hired" makes it answer a recruiter's silent question. They are written very differently.

  My read: {pick from the Phase 2 snapshot — if cv_parsed shows a recent move to freelance/independent or no current employer, say "your CV shows you went independent recently, so my guess is **land clients**." If the LinkedIn "Open to Work" toggle is on, or the CV shows you're employed and looking, say "your profile has 'Open to Work' switched on, so my guess is **get hired**." If neither is clear, say "I don't have a strong signal yet — pick whichever feels truest."}

  If we aim at the wrong reader, the whole profile misses and we'd have to redo the About, so it's worth a real answer. You can change this anytime by typing `redo my answers`.
header: 90-day mission
options:
  - "Get hired for a specific role" — your profile answers a recruiter's silent question: would this person do the job well?
  - "Land paying clients or contracts" — your profile becomes a quiet sales page: proof, outcomes, an easy way to reach you.
  - "Grow my following / build authority" — your profile leans on a clear point of view and the work that backs it up.
  - "Network with peers in my field" — your profile reads as a credible, easy-to-place peer worth connecting with.
  - "All of the above" — honest, but it makes every section work harder. Pick this only if you truly mean it.
```

After the user picks one, ask a one-line follow-up to make it specific:
> Got it. To make this useful, can you describe that goal in one sentence with actual details? For example, "Land a senior PM role at a Series A B2B SaaS company in the US, with a base above $180k." Type your version below.

Capture both the chosen option and the specific sentence. Save as `mission_90d`.

### Step 3.3 — Question 2: Target person

```
question: |
  Who is the one person you most want to land on your profile?

  Why this matters: a profile written for everyone lands with no one. When I know the exact person you're writing for, I can pick the words, the proof, and the order that make *that* person stop scrolling.

  My read: {use Phase 2 + the answer to Q1 — if mission_90d is "land clients", say "you're after clients, so this is probably **a potential client**." If it's "get hired", say "you're job-hunting, so this is likely **a recruiter** or **a hiring manager**." If the CV points at a specific field (e.g. early-stage startups), name it. If nothing is clear, say "no strong signal yet — pick whoever you'd most want to read this."}

  If we pick the wrong reader, the rewrite speaks the wrong language and you'd feel it on every line. You can change this anytime by typing `redo my answers`.
header: Target person
options:
  - "A recruiter" — someone screening many profiles fast, looking for fit and proof.
  - "A hiring manager" — the person who owns the role and wants to see you can do the job.
  - "A potential client" — someone deciding whether to trust you with their money or problem.
  - "An investor" — someone betting on you and the direction you're heading.
  - "A peer in my field" — someone who'd collaborate, refer, or vouch for you.
```

Follow-up:
> Describe them in one sentence. Job title, company type, city if it matters. "Head of Engineering at a Series A fintech in Bengaluru looking for a senior backend hire" — that level of specific.

Save as `target_person`.

### Step 3.4 — Question 3: Biggest result shipped

This one is a free-text answer, not multiple choice. Use AskUserQuestion with a single "Continue" option but ask for the answer in the question text.

```
question: |
  What is the single biggest result you've shipped in the last 12 months? Use numbers if you can. Examples:
  - "Cut customer support response time from 18h to 2h, saving the company $400k/year."
  - "Built a voice agent that qualifies 50 leads/day with 75% accuracy in production."
  - "Grew a product newsletter from 0 to 8,200 subscribers in 9 months."
  - "Closed $1.2M in client work as a solo consultant."
  Type your version below.

  Why this matters: this becomes the single hardest piece of proof on your whole profile — the line a recruiter or client believes before they believe anything else. A number does more work than a paragraph of adjectives.

  My read: {scan cv_parsed for the strongest quantified outcome — if one exists, say "your CV mentions {that result} — if that's your biggest, just confirm it." If the CV has no numbers, say "I don't see a hard number on your CV yet, so this one's on you — dig for the real figure."}

  If you stay vague here ("I worked hard"), every rewrite downstream stays vague too — this answer carries a lot of weight. You can change this anytime by typing `redo my answers`.
header: Biggest result
options:
  - "Continue"
```

If the user gives a vague answer ("I worked hard", "I grew the team"), push back once:
> That's pretty broad. Can you give me one specific number, percentage, or outcome? If you genuinely don't have anything specific to point to, type `nothing specific` and we'll work with what we have.

Save as `biggest_result`.

### Step 3.5 — Question 4: 2-year north star

```
question: |
  What do you want to be known for in 2 years? Not what you do today — what you want people to associate with your name.

  Why this matters: this is the direction your profile points. It decides which parts of your past I pull forward and which I let fade, so the whole profile leans toward where you're going instead of where you've been.

  My read: {compare cv_parsed (what they do today) with the answer to Q1/Q2 — if there's a clear trajectory, name it gently, e.g. "your recent work leans toward {area}, so a north star around that would feel earned." If the CV shows a pivot away from current role, say "you might be aiming somewhere new — that's fine, name where you're headed, not where you are." If nothing's clear, say "no strong signal yet — say it as the thing you'd want said about you in two years."}

  If this is fuzzy, your profile ends up describing your present job instead of your future, which is the most common way good profiles go flat. You can change this anytime by typing `redo my answers`.
header: 2-year identity
options:
  - "Continue"
```

Free-text answer. Example to set the bar:
> Examples: "The person who shipped the first AI agent for Indian voice-based banking." "The best frontend designer for B2B SaaS dashboards in EU." "The go-to consultant for early-stage healthtech founders raising in the US." Type yours.

Save as `north_star`.

### Step 3.6 — Question 5: What to leave off

```
question: |
  What is one tag, identity, or label you wear casually but should NOT lead with on your LinkedIn profile?

  Why this matters: what you leave off is as sharp as what you put on. One stray label can quietly pull every reader toward the wrong idea of who you are, so naming it tells me what to dial down.

  My read: I won't guess this one — it's too personal, and a wrong guess from me would just push you off your own answer. This is yours to name.

  If we miss this, the rewrite might keep amplifying the exact thing you're trying to move away from. You can change this anytime by typing `redo my answers`.
header: What to leave off
options:
  - "Continue"
```

Free-text. This question often surprises people. Give them a beat:
> Take your time. The answer is usually something you list on your profile right now that's pulling people in the wrong direction.

Save as `anti_position`.

### Step 3.7 — Question 6: Bland or fake

```
question: |
  Honest moment — what's bland, generic, or slightly fake on your current LinkedIn profile that you've been avoiding fixing?

  Why this matters: naming the weak spot yourself gives me permission to actually fix it. People defend their profile when I point at it cold; when you point first, we just get to work.

  My read: {use audit_result from Phase 4 — if the cringe detector found phrases, say "the audit flagged {phrase} in your {section}, so that might be the thing." If a section scored very low, name it, e.g. "your headline scored {X}/10 — it's just your job title right now." If the audit came back clean, say "the audit was fairly clean, so this one's about what *you* wince at, not what I caught."}

  No stakes here beyond honesty — the more candid you are, the less generic the rewrite. You can change this anytime by typing `redo my answers`.
header: Bland or fake
options:
  - "Continue"
```

Free-text. The user knows. They've been avoiding it. Let them name it.

Examples to give them:
> "The headline is just my job title." "The About section was written by ChatGPT and it shows." "Half my skills are from Forage simulations." "I haven't posted in 9 months." Pick yours — whatever you actually wince at.

Save as `confessed_problem`.

### Step 3.8 — Question 7: Voice and risk

```
question: |
  One last question — when I rewrite your profile, how should it sound?

  Why this matters: same facts, four very different profiles. The voice decides whether you read as safe-and-hireable, sharp-and-certain, or distinctive-and-divisive. It sets the tone of every sentence I write.

  My read: {use the scraped tone from Phase 2 + the target_person from Q2 — if the current About/posts already read plain and corporate, or the target is a recruiter, say "your current profile reads fairly buttoned-up and you're aiming at recruiters, so **Confident** is usually the safe upgrade." If the target is clients or an audience and the existing writing has personality, say "you're building authority and your writing already has a voice, so **Bold** could pay off." If there's no real signal, say "no strong signal — pick the voice you'd be comfortable defending to a stranger."}

  Pick too bold for a conservative audience and you can put off the exact reader you want; pick too safe and you blend in. You can change this anytime by typing `redo my answers`.
header: Voice and risk
options:
  - "Conservative — stays safe, recruiter-friendly, no edgy claims" — lowest risk, widest appeal, least memorable.
  - "Confident — strong claims, clear positioning, named outcomes" — assertive but still safe for most readers; the usual sweet spot.
  - "Bold — distinct voice, opinion, willing to alienate the wrong audience" — memorable to the right people, off-putting to the wrong ones (on purpose).
  - "Funny — humor, self-aware, breaks the LinkedIn-fluff mold" — stands out hard; only works if you can carry it consistently.
```

Save as `voice_mode`.

### Step 3.9 — Confirm back to the user

Speak the summary in plain English. This is the most important confirmation in the whole skill.

> Here is what I have. Tell me if any of it is wrong.
>
> - **In 90 days:** [mission_90d sentence]
> - **You most want to land:** [target_person sentence]
> - **Your biggest shipped result this year:** [biggest_result]
> - **In 2 years, you want to be known for:** [north_star]
> - **You want OFF your profile:** [anti_position]
> - **The bland/fake thing you've been avoiding:** [confessed_problem]
> - **Voice:** [voice_mode]
>
> Sound right? Type `yes` to lock this in. Type `redo my answers` to redo any of it.

### Step 3.10 — Write to disk

Once the user confirms, write the answers to `snapshots/{handle}-{timestamp}-user-profile.json`:

```json
{
  "captured_at": "ISO8601",
  "mission_90d": { "option": "...", "specific": "..." },
  "target_person": { "option": "...", "specific": "..." },
  "biggest_result": "...",
  "north_star": "...",
  "anti_position": "...",
  "confessed_problem": "...",
  "voice_mode": "..."
}
```

---

## Outputs of Phase 3

- `snapshots/{handle}-{timestamp}-user-profile.json`
- In-memory: `user_profile` — used by every rewrite in Phase 5

---

## What to do if something goes wrong

- **User gives vague answers to every question.** Push back once per question. If they still give vague answers, accept them but flag in Phase 5 that the rewrite will be limited by the input. Do not refuse to continue.
- **User types `redo my answers` mid-flow.** Restart from question 1. Do not preserve prior answers.
- **User contradicts the CV (e.g. CV says marketing manager, user says "I want to be known as a designer").** Trust the user. Flag the gap in Phase 5 — they may need to add Experience entries that demonstrate the new direction.
- **User says "I don't know what I want."** Stop the skill. The user needs to think about their career before a profile rewrite is useful. Suggest they come back in a few days.
- **User wants to skip this phase entirely.** Refuse. Every later rewrite depends on this input. Offer a fast version (just questions 1, 2, and 7) if they are short on time.
