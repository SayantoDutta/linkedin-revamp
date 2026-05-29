# Phase 1 — Welcome and Setup

## What this phase does

Greets the user, checks that the Chrome extension is installed and signed in, confirms LinkedIn is signed in, and collects the three pieces of information needed to begin: the user's CV, their portfolio URL (optional), and their LinkedIn profile URL.

This phase touches no live profile data. It is read-only and entirely conversational.

---

## How to run this phase

### Step 1.1 — Plain-English greeting

Speak this greeting to the user, verbatim or close to it. Adapt only if the user has already shown signs of familiarity with Claude Code.

> Hi. I'm going to help you rebuild your LinkedIn profile from the ground up.
>
> Here is what is about to happen, in plain English:
>
> 1. I'll ask you for your CV, a link to your portfolio if you have one, and the link to your LinkedIn profile.
> 2. I'll read all of that and look at your current profile. I'll save a backup of everything you have today so we can roll anything back later.
> 3. I'll ask you 7 honest questions about what you want LinkedIn to do for you. Specific answers will give you a much better profile than vague ones.
> 4. I'll show you a one-page report of what is bland, fake, or missing on your profile right now.
> 5. I'll write a proposed new version of every section — headline, About, banner, experience bullets, skills, Featured tiles — and show them to you side-by-side with what you have today.
> 6. You'll approve, edit, or skip each one.
> 7. After you say go, I'll drive the LinkedIn website for you and push each approved change live. You'll confirm anything that can't be undone easily.
> 8. We'll do a quick verify pass to make sure everything went through.
>
> A few important promises before we start:
>
> - I will never type your password or sign in for you. You're already signed in to LinkedIn in Chrome, right? If not, please do that now and tell me when you're ready.
> - I will never push a change to your profile without you saying so.
> - I will turn off the "Share profile updates with your network" setting before I touch anything, so your connections don't get spammed.
> - You can type `abort` at any time to stop.
>
> Sound good? Let's start with three quick checks.

Wait for the user to respond. If they raise any concerns, address them before moving on.

### Step 1.1b — Feature menu: what you can turn on

Before the checks, show the user what this skill can do and let them choose how much to switch on. Nothing here is forced. Use `AskUserQuestion` with `multiSelect: true`, following the plain-English style in `references/question-format.md`.

Say first, in plain words:

> This skill works best with the full power of the Claude desktop app — it can drive your Chrome browser and make the changes on LinkedIn for you, so you don't have to copy and paste anything. But it's your call. Tell me which parts you want to use. You can change your mind anytime.

Then present the menu (multi-select):

| Option | Plain-English description |
|--------|---------------------------|
| **Let me edit LinkedIn for you in Chrome** (Recommended) | I drive your browser and make each approved change live. The hands-off way. Without this, I'll write everything and hand you copy-paste-ready text to apply yourself. |
| **Design a banner for me** | I render a branded banner image you can upload. Runs locally, no internet needed. |
| **Turn my projects into Notion case-study pages** | Optional add-on. Needs Notion connected. I'll offer it near the end if your work fits. |
| **Make short walkthrough videos of my work** | Optional add-on. Needs a free tool called ffmpeg. I'll offer it near the end if you have screenshots. |

Plain-English explanation under the menu (ELI10):

> The first option is the big one. With it on, I do the clicking and typing on LinkedIn for you — you just approve each change. With it off, I still write everything; you paste it in yourself. The other three are extras you can pick now or decide on later.

**The one safety promise, stated plainly:**

> Whichever you pick, I will always stop and ask you first before I do anything that's hard to undo — deleting something, uploading a file, or changing a privacy or account setting. That pause is built in and can't be switched off.

Recovery hint:

> Not sure? Pick the first option and the banner — that's the normal setup. You can turn anything on or off later by just telling me.

Store the user's choices as `enabled_features` (a list). Carry it through the session:
- If **"Let me edit LinkedIn for you in Chrome"** is **not** selected, skip the Chrome pre-flight checks (Steps 1.2–1.4 below are then informational only), and in Phase 6 switch to **generate-only mode**: produce copy-paste-ready text and a step-by-step "where to paste this" guide for each section instead of driving the browser. Tell the user this is what will happen.
- If it **is** selected, run the checks below as written.
- The Notion and walkthrough picks only set expectations; they're still gated on their real dependencies (Notion connected, ffmpeg present) and re-offered in Phase 8.

### Step 1.2 — Pre-flight check 1: Chrome extension

Run this check using the `mcp__Claude_in_Chrome__list_connected_browsers` tool.

If at least one browser is returned:
> Great — I can see the Claude Chrome extension is connected.

If zero browsers are returned, or the tool errors:
> I can't see the Claude Chrome extension. You'll need that to run this skill, because it's how I'll drive your browser.
>
> Here is the install link: https://chromewebstore.google.com/detail/claude-for-chrome
>
> After installing, sign in to the extension using the same Claude account you're using right now. Then restart Claude and run this skill again.
>
> I'll wait here. Type `ready` when the extension shows as connected.

Loop until the check passes.

### Step 1.3 — Pre-flight check 2: LinkedIn signed in

Use the Chrome MCP to open a tab and navigate to `https://www.linkedin.com/feed/`. Take a screenshot.

- If the screenshot shows the LinkedIn feed (logged-in state), say:
  > Confirmed — you're signed in to LinkedIn.
- If the screenshot shows a login prompt, say:
  > It looks like you're signed out of LinkedIn. Please sign in in Chrome (don't sign in here in the chat — just go to the Chrome tab and sign in there). Tell me `ready` when you're done.

Loop until the check passes.

### Step 1.4 — Pre-flight check 3: Privacy setting peek

Navigate to `https://www.linkedin.com/mypreferences/d/categories/profile-visibility`. Read the page to find the "Share profile updates" row. Read its current value.

- If it says **Off**:
  > Your "Share profile updates with your network" setting is already Off. Good — that means rewriting things won't spam your connections.
- If it says **On**:
  > Heads up: your "Share profile updates with your network" setting is currently On. That means every time we change something later, your connections would get a notification. I'm going to turn this off for you right before I start editing your profile — but flagging it now so there are no surprises.

This is a read-only check at this stage. Do not flip the setting yet.

### Step 1.5 — Collect CV

Ask the user:
> Now I need your CV. Please attach it to the chat — PDF, DOCX, or plain text all work. If you don't have a CV file, just type or paste the content directly here.

Wait for the attachment or paste. Confirm what was received:
> Got it — I can read your CV. It's [N] pages and looks like it covers [give a one-line description, e.g. "5 years of frontend engineering work plus a recent founder year"].

### Step 1.6 — Collect portfolio URL (optional)

Ask the user:
> Do you have a portfolio site, personal website, GitHub profile, or any other public link that showcases your work? If yes, paste the URL. If not, type `skip`.

If the user provides a URL, validate it briefly with `WebFetch` to confirm the page loads. If 404, ask for a corrected URL. If the user types `skip`, store an empty string and continue.

### Step 1.7 — Collect LinkedIn URL

Ask the user:
> Last one — please paste the URL of your LinkedIn profile. It looks something like `https://www.linkedin.com/in/yourname/`.

If the user pastes an invalid URL, ask for a corrected one. Confirm the URL by navigating to it via Chrome MCP and taking a screenshot.

### Step 1.8 — Confirm and proceed

Speak this confirmation:
> Here is what I have:
>
> - **CV:** [filename or "pasted text, ~X words"]
> - **Portfolio:** [URL or "none"]
> - **LinkedIn profile:** [URL]
> - **Chrome extension:** connected
> - **LinkedIn:** signed in
> - **Network notifications:** [Off / will be turned off right before any edits go live]
>
> Ready to move on to discovery? Type `yes` to continue or `change` if anything above is wrong.

If the user says `yes`, advance to Phase 2.

---

## Outputs of Phase 1

Save three items to memory for the rest of the session:

- `cv_content` (string) — full text of the CV
- `portfolio_url` (string or empty) — validated URL
- `linkedin_url` (string) — validated URL of the user's LinkedIn profile

These will be referenced in every later phase.

---

## What to do if something goes wrong

- **User refuses to attach a CV.** Ask why. If they don't have one, offer to build a CV-equivalent by asking 5 questions about their career history. Do not skip — every later phase depends on having career context.
- **Portfolio URL is private or behind login.** Treat as if they said `skip`. Make a note to mention in Phase 4 that we couldn't see the portfolio.
- **LinkedIn URL is the user's profile but the profile is heavily restricted.** Continue. Phase 2 will adapt to what is visible.
- **User says "I don't want a backup."** Explain that without a backup, there is no safe revert path and the skill will refuse to push live changes. Do not negotiate on this rule.
- **User wants to skip this whole phase.** Refuse. Every later phase depends on the context collected here. Offer to do it faster instead.
