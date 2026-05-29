# Phase 6 — Execute

## What this phase does

Drives the LinkedIn website through the Chrome MCP and pushes each approved change live, in order. Every section requires a separate user confirmation. Destructive actions require a second confirmation.

This is the only phase that changes anything on the live profile. Everything before this was planning.

---

## Pre-execution safety preamble

Before running any Chrome MCP action, verify all of the following. If any check fails, stop and report.

1. **Snapshot exists.** Check `snapshots/{handle}-{timestamp}.json` exists and is non-empty. If missing, refuse to execute and tell the user "I won't push live changes without a backup. Please run Phase 2 again."
2. **Rewrite pack exists.** Check `snapshots/{handle}-{timestamp}-rewrite-pack.md` has at least one section marked "accepted".
3. **Notify network setting is Off.** Navigate to LinkedIn Settings → Visibility. Read the "Share profile updates" value. If On, turn it Off now and confirm to the user: "Turned off network notifications so your connections won't get spammed."
4. **No LinkedIn anti-bot warning is visible.** Take a screenshot of the homepage. If any anti-bot dialog is up, pause and tell the user to clear it manually.
5. **Audit log file ready.** Create `snapshots/{handle}-{timestamp}-audit-log.jsonl` if it doesn't exist.

Once all five checks pass, tell the user:

> Pre-flight clean. Notifications are off, backup is in place, rewrite pack has the approved sections.
>
> I'm about to start pushing changes live. We'll go in this order:
> 1. Vanity URL
> 2. Headline
> 3. About
> 4. Banner upload
> 5. Experience (one entry at a time)
> 6. Skills (deletes first, then adds, then top-5 pin)
> 7. Featured tiles (one at a time)
>
> Each section asks for confirmation before pushing. Type `proceed` to start.

Wait for `proceed`.

---

## How to run this phase

Load `execute/chrome-driver.md` for reusable Chrome MCP patterns. Load `execute/safety-gates.md` for the per-section gate definitions. Load `execute/linkedin-selectors.md` for the stable selectors per UI element.

### Step 6.1 — Vanity URL (lowest risk)

If the rewrite pack marks this as accepted:

1. Tell the user: "Updating your vanity URL to `linkedin.com/in/{new-slug}`. This is reversible if the slug you picked is taken — I'll fall back to the next candidate."
2. Navigate to `https://www.linkedin.com/public-profile/settings`.
3. Click the pencil next to "Edit your custom URL".
4. Wait for the inline edit field to appear.
5. Use the React-friendly value setter (see `execute/chrome-driver.md`) to clear and set the new slug.
6. Click Save.
7. Wait 2 seconds. Take a screenshot. Verify the new URL is displayed.
8. If the slug is taken, fall back to the next candidate from the rewrite pack and retry once. If both fail, ask the user for a custom slug.
9. Append to audit log: `{"timestamp": "...", "action": "set_vanity_url", "target": "...", "status": "ok"}`

### Step 6.2 — Headline

If accepted:

1. Navigate to `https://www.linkedin.com/in/{slug}/`.
2. Click the pencil on the intro card (top-right of profile section).
3. Wait for the Edit intro modal.
4. Scroll to the Headline field.
5. Triple-click the existing text to select all. Press Delete.
6. Type the new headline.
7. Take a screenshot. Verify the headline shows correctly.
8. **Pause for confirmation.** Tell the user: "Headline draft is ready in the modal. Look at the preview. Type `push it` to save, or `let me see again` for me to re-screenshot."
9. On confirm, click Save.
10. Watch for the LinkedIn "Notify your network?" popup. If it appears, click "Don't notify".
11. Append to audit log.

### Step 6.3 — About section

If accepted:

1. Look for an existing About section on the profile. If present, click its edit pencil. If missing, click "Add section" → "Add about".
2. Wait for the Edit about modal.
3. Click the description textarea.
4. Use React-friendly value setter to clear and set the new content. Do NOT use the `type` action directly — it produces typos in long text. Use the JS setter.
5. Verify the character count is under 2600.
6. Take a screenshot.
7. Pause for confirmation: "About section is ready. Push it?"
8. On confirm, click Save.
9. Watch for notify popup. Auto-decline.
10. Append to audit log.

### Step 6.4 — Banner upload

Only run if the user accepted the proposed banner AND chose to upload the rendered PNG (not the "I'll generate my own" option).

1. Banner upload requires the file to be in a session-shareable location. Check `helpers/build_banner.py` output is at `snapshots/{handle}-{timestamp}-banner.png`.
2. **Important caveat.** The Chrome MCP `file_upload` tool only accepts files the user has attached in the current chat session. If the rendered banner is not in a session-shared location, ask the user to attach it: "Please drag the file `snapshots/{handle}-{timestamp}-banner.png` into the chat. I'll handle the rest."
3. Once attached, navigate to the profile page. Click the camera icon on the banner area.
4. Click "Add cover image" in the dropdown.
5. Use the `file_upload` Chrome MCP tool with the attached file path and the upload button's ref.
6. Wait for upload to complete.
7. Take a screenshot.
8. Append to audit log.

If the user opted to generate their own banner externally, skip this step and tell the user: "I've left the banner upload to you. The prompt is in `snapshots/{handle}-{timestamp}-banner-prompt.txt`. Generate the image in your tool of choice, then upload to LinkedIn directly when ready."

### Step 6.5 — Experience entries (one at a time)

For each Experience entry approved in the rewrite pack:

1. Navigate to `https://www.linkedin.com/in/{slug}/details/experience/`.
2. Click the pencil next to the target entry.
3. Wait for the Edit experience modal.
4. Verify the "Notify network" toggle inside the modal is **Off**. If On, turn Off.
5. Scroll to the Description field.
6. Click the textarea. Use the React-friendly value setter to clear and set the new description.
7. Take a screenshot.
8. Pause for confirmation: "Experience entry for {Role} at {Company} ready. Push it?"
9. On confirm, click Save.
10. The "People you may know" suggestions modal often appears after save. Click Skip.
11. Append to audit log.
12. Continue to next entry.

### Step 6.6 — Skills section (drops, then adds, then pin)

This is the most error-prone section. Take it slow.

**Drops.** For each skill in the DROP list:
1. Navigate to `https://www.linkedin.com/in/{slug}/details/skills/`.
2. Find the skill by name. Click its pencil.
3. Click "Delete skill".
4. Confirm "Delete" in the modal.
5. Wait 3 seconds for the page to reload.
6. Append to audit log.

**Adds.** For each skill in the ADD list:
1. Click the + button on the Skills section header.
2. Click into the "Skill" search field.
3. Type the skill name.
4. Wait 2 seconds for autocomplete.
5. Press ArrowDown then Enter to select the first suggestion.
6. Check the boxes for the user's relevant Experiences (typically the most recent 3 entries).
7. Click Save.
8. On the "Add more skills?" modal, click "Add more skills" if there are more to add, else click "No thanks".
9. Append to audit log.

**Pin top 5.** After all adds:
1. Click the ⋯ menu on the Skills section.
2. Choose "Reorder".
3. Drag the top 5 skills from the rewrite pack to the top, in order.
4. Save.
5. Append to audit log.

**Watch for autocomplete misses.** If the autocomplete picks a different skill than typed (e.g. "API Integration" → "Paypal Integration"), the skill will show on the profile with the wrong name. After all adds, verify each newly added skill name against the ADD list. Delete any miscaptured ones and re-add with a more specific query.

### Step 6.7 — Featured tiles (one at a time)

For each Featured tile approved in the rewrite pack:

1. Navigate to `https://www.linkedin.com/in/{slug}/details/featured/`.
2. Click the + button.
3. Choose "Add a link" (default — works for portfolios, Notion pages, Articles).
4. Paste the URL. Click Add.
5. Wait for LinkedIn to fetch OG preview.
6. If the title/description fields auto-populated, use the React-friendly value setter to override with the user's approved title and description from the rewrite pack. **Do not use `type` for these fields — the typo rate is high. Use JS.**
7. Click Save.
8. Append to audit log.

### Step 6.8 — Final confirmation

After all sections are pushed:

> All approved changes are live. Type `verify` to run the post-execution check.

Wait for `verify` to proceed to Phase 7.

---

## Outputs of Phase 6

- Live changes on the user's LinkedIn profile
- `snapshots/{handle}-{timestamp}-audit-log.jsonl` — every action logged

---

## What to do if something goes wrong

- **A Chrome MCP click times out (renderer frozen).** Take a screenshot. If the screenshot returns, the page recovered. Retry the action. If the screenshot also times out, navigate to the LinkedIn homepage, wait 3 seconds, then re-navigate to the target page.
- **LinkedIn shows an anti-bot dialog.** Stop immediately. Tell the user. Ask them to clear it manually in Chrome. Resume when they confirm.
- **A section fails (Save button errors).** Append failure to audit log. Offer the user three options: Retry / Skip / Abort all.
- **The user types `abort` mid-execution.** Stop immediately. The audit log preserves what was done. Tell the user: "Stopped. {N} sections done, {M} remaining. Type `resume` to pick up where we left off in a future session, or run `/linkedin-revamp` again to start fresh."
- **An autocomplete miss puts a wrong skill on the profile (e.g. Paypal Integration instead of API Integration).** After all skill adds, audit the live skills section by re-scraping. Compare against the ADD list. Delete and re-add any mismatches.
- **The notify-network popup appears despite the global toggle being Off.** Auto-decline anyway. Some sections (e.g. Experience date changes) trigger it per-action. The auto-decline catches them all.
- **The user has an unlocked LinkedIn premium trial and a Premium-specific popup blocks the flow.** Tell the user. Ask them to dismiss it manually. Resume.
