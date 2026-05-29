# Chrome MCP driver patterns

Reusable patterns for driving LinkedIn through the Chrome MCP. These are battle-tested from real production runs. Use them verbatim where possible.

---

## Tool naming

Chrome MCP tools are prefixed `mcp__Claude_in_Chrome__`. The most-used ones:

- `list_connected_browsers` — confirm the extension is connected
- `select_browser` — pick which browser session to drive
- `tabs_context_mcp` — inspect open tabs
- `tabs_create_mcp` — open a new tab
- `navigate` — go to a URL
- `computer` — click, type, scroll, screenshot, key press
- `find` — locate an element by natural-language query
- `read_page` — accessibility tree of current page
- `read_console_messages` — debug
- `javascript_tool` — run JS in the page
- `browser_batch` — chain N actions in one round-trip
- `file_upload` — upload a file the user has shared with the session

---

## Pattern 1 — Initialize a browser session

Run at the start of every flow.

```
1. mcp__Claude_in_Chrome__list_connected_browsers
   → expect at least one entry. If empty, treat as setup error.

2. mcp__Claude_in_Chrome__select_browser
   → pass the deviceId from step 1.

3. mcp__Claude_in_Chrome__tabs_context_mcp { createIfEmpty: true }
   → returns an array of available tabs and creates a fresh tab if none.
   → store the tabId for all subsequent calls.
```

---

## Pattern 2 — Navigate + screenshot

```
mcp__Claude_in_Chrome__browser_batch with actions:
  [
    { name: "navigate", input: { url: "https://www.linkedin.com/in/{slug}/", tabId: TAB } },
    { name: "computer", input: { action: "wait", duration: 3, tabId: TAB } },
    { name: "computer", input: { action: "screenshot", tabId: TAB } }
  ]
```

Always batch. Each Chrome MCP round-trip is ~1 second. Batching 3 actions cuts that to 1 round-trip.

---

## Pattern 3 — Find an element by natural language

Cleaner than guessing pixel coordinates. Returns a `ref_NNN` you can use in subsequent clicks.

```
mcp__Claude_in_Chrome__find
  input: { query: "edit pencil button next to Headline field", tabId: TAB }
```

Returns the ref. Then click:

```
mcp__Claude_in_Chrome__computer
  input: { action: "left_click", ref: "ref_NNN", tabId: TAB }
```

Use `find` for:
- Buttons by label
- Form fields by purpose
- Links by visible text

`find` fails when:
- The element is offscreen — scroll first
- The element is in a closed modal
- The element is rendered inside a shadow DOM

When `find` fails, fall back to Pattern 4.

---

## Pattern 4 — JavaScript-based form set (the typo-proof pattern)

The Chrome MCP `type` action is fine for short text but produces typos in long strings. Use this instead for any text field with more than ~30 characters.

**The values you set come from scraped/generated content, so they are untrusted.** A headline or About paragraph could contain a backtick, a `${...}`, a quote, or a `</script>`. If you splice that text straight into the JavaScript source, it can break out of the string and run as code in your logged-in LinkedIn page. "Just escape it carefully" is not a real defense — escaping is easy to get wrong and one miss is a full code-execution hole.

**The fix: pass the values out-of-band.** Never interpolate a raw value into the JS source. Instead, serialize the values to JSON on the host side (where `json.dumps` / `JSON.stringify` produces a single safe string token), embed only that JSON token, and have the page-side code `JSON.parse` it back into a plain data object. Inside a JSON double-quoted string, backticks and `${...}` are inert — there is no template-literal evaluation — so a malicious value can travel as data but can never become code.

Build the payload on the host first:

```python
import json

# values come from the rewrite pack — treat as untrusted
payload = {
    "title": new_title,           # e.g. a string containing `${...}` or backticks
    "description": new_description,
}

# json.dumps gives a safe token: quotes/backslashes/control chars escaped,
# and backticks / ${} carry no special meaning inside a JSON string.
payload_json = json.dumps(payload)

# Embed ONLY the JSON token. Note the surrounding single quotes in the JS:
# JSON uses double quotes, so single-quoting the literal needs no extra escaping
# beyond escaping any literal single quote in the token.
js_literal = "'" + payload_json.replace("\\", "\\\\").replace("'", "\\'") + "'"

js_source = """
(() => {
  const DATA = JSON.parse(%s);          // <-- out-of-band data, never code
  function setReactValue(el, val) {
    const proto = el.tagName === 'TEXTAREA'
      ? HTMLTextAreaElement.prototype
      : HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
    setter.call(el, val);
    el.dispatchEvent(new Event('input',  { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }
  const [titleInput, descTextarea] =
    document.querySelectorAll('input[type="text"], textarea');
  setReactValue(titleInput,  DATA.title);
  setReactValue(descTextarea, DATA.description);
  return [titleInput.value, descTextarea.value];
})()
""" % js_literal
```

Then hand `js_source` to the tool — the scraped/generated strings live inside `DATA`, never in the surrounding code:

```
mcp__Claude_in_Chrome__javascript_tool
  input: { tabId: TAB, text: <js_source built above> }
```

This works because LinkedIn's React forms listen to native `input` events even when the value is set programmatically. The `setter.call` bypasses React's controlled-component check.

**Rule:** the only thing that ever gets interpolated into the JS source is a `json.dumps` token. Field values reach the page exclusively through `JSON.parse`. Never reach for a template literal (backtick string) to inject a scraped value — that's the breakout path this pattern exists to close.

---

## Pattern 5 — Triple-click to select all text in a field

For short fields where the typo-proof JS approach is overkill, this pattern clears a field cleanly.

```
mcp__Claude_in_Chrome__browser_batch with actions:
  [
    { name: "computer", input: { action: "triple_click", coordinate: [X, Y], tabId: TAB } },
    { name: "computer", input: { action: "key", text: "ctrl+a", tabId: TAB } },
    { name: "computer", input: { action: "key", text: "Delete", tabId: TAB } },
    { name: "computer", input: { action: "type", text: "new value", tabId: TAB } }
  ]
```

The `ctrl+a` + `Delete` after the triple-click is belt-and-suspenders — some LinkedIn fields don't select-all via triple-click cleanly. Belt + suspenders ensures the field is empty.

---

## Pattern 6 — Scroll an element into view, then click

For buttons that are off-screen.

```
mcp__Claude_in_Chrome__find
  input: { query: "Save button at bottom of edit modal", tabId: TAB }
→ returns ref_NNN

mcp__Claude_in_Chrome__computer
  input: { action: "scroll_to", ref: "ref_NNN", tabId: TAB }

mcp__Claude_in_Chrome__computer
  input: { action: "left_click", ref: "ref_NNN", tabId: TAB }
```

---

## Pattern 7 — Watch for and dismiss the notify-network popup

After any Experience save, this popup may appear: "Want to notify your network about this update?"

```
mcp__Claude_in_Chrome__find
  input: { query: "Don't notify or Skip button on the share-update popup", tabId: TAB }

If found:
  mcp__Claude_in_Chrome__computer
    input: { action: "left_click", ref: <ref>, tabId: TAB }
```

If `find` returns nothing within 2 seconds, assume the popup didn't appear.

Always log: `{"action": "notify_popup_handling", "found": true/false, "outcome": "dismissed"}`

---

## Pattern 8 — File upload (banner, profile photo)

The Chrome MCP `file_upload` tool only accepts files the user has shared with the current chat session. This is intentional — it prevents the agent from uploading files from the user's filesystem without explicit knowledge.

For banner upload:

1. Render banner with `helpers/build_banner.py`. Save to `snapshots/{handle}-{timestamp}-banner.png`.
2. Tell the user: "Please drag `{path}` into the chat. I'll handle the rest."
3. Wait for the user to attach the file.
4. Navigate to the LinkedIn banner edit modal.
5. Click the upload button.
6. Use `find` to locate the file input element.
7. Call `file_upload` with the attached path and the input's ref.

```
mcp__Claude_in_Chrome__file_upload
  input: {
    paths: ["<full path attached by user>"],
    ref: "ref_NNN",
    tabId: TAB
  }
```

---

## Pattern 9 — Auto-decline LinkedIn "People you may know" suggestions

After saving an Experience, LinkedIn often shows a modal suggesting connections. Click Skip.

```
mcp__Claude_in_Chrome__find
  input: { query: "Skip button on People you may know modal", tabId: TAB }

mcp__Claude_in_Chrome__computer
  input: { action: "left_click", ref: <ref>, tabId: TAB }
```

---

## Pattern 10 — Detect anti-bot challenge

LinkedIn occasionally shows a CAPTCHA or "Are you a person?" challenge. Detect it:

```
mcp__Claude_in_Chrome__find
  input: { query: "CAPTCHA or human verification challenge", tabId: TAB }
```

If found, stop the flow. Tell the user: "LinkedIn is showing a verification challenge. Please complete it in Chrome, then type `proceed`." Wait.

---

## Pattern 11 — Rate limiting

After every UI action that changes profile state, wait at least 1.5 seconds before the next action.

```
mcp__Claude_in_Chrome__computer
  input: { action: "wait", duration: 1.5, tabId: TAB }
```

This avoids triggering LinkedIn's behavioral anti-bot signals.

---

## Pattern 12 — Audit log every action

After every Chrome MCP action that changes state, append to the audit log:

```
echo '{"timestamp":"<ISO8601>","action":"<action_name>","target":"<what was changed>","status":"<ok|fail|skipped>","details":"<optional>"}' >> snapshots/{handle}-{timestamp}-audit-log.jsonl
```

Or in Python:
```python
import json, datetime, pathlib
entry = {
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    "action": "set_headline",
    "target": "linkedin headline field",
    "status": "ok",
    "details": "set to 130 chars"
}
with pathlib.Path("snapshots/...audit-log.jsonl").open("a") as f:
    f.write(json.dumps(entry) + "\n")
```

This log is the user's record of every change. Phase 7 uses it to verify nothing was silently changed.

---

## Pattern 13 — Take a screenshot for evidence

After every significant push (save button click + page refresh), take a screenshot. Save it as `snapshots/{handle}-{timestamp}-evidence-{step_name}.png`.

```
mcp__Claude_in_Chrome__computer
  input: { action: "screenshot", tabId: TAB, save_to_disk: true }
```

Pass `save_to_disk: true` so the screenshot persists. Otherwise it's only returned inline and lost when context advances.

---

## Common failures and recovery

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Renderer frozen | screenshot times out | Wait 5 seconds. Retry screenshot. If still timing out, navigate to homepage, wait 3s, re-navigate to target page. |
| Element not found | `find` returns no matches | Scroll the area into view. Retry. If still not found, take a screenshot and ask the user. |
| Anti-bot challenge | CAPTCHA visible | Stop. Ask user to clear manually. Resume. |
| Session signed out | LinkedIn redirects to login | Tell user. Wait for them to sign in. Resume. |
| Save button errors | Generic "Something went wrong" | Take screenshot. Retry once. If still failing, skip and continue to next section. |
| Autocomplete picks wrong option | Wrong skill name appears after save | Detect in Phase 7 verify. Surface to user as an action item. |
