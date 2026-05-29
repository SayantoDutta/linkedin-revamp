# Install — Chrome extension setup (plain English)

This skill drives the LinkedIn website for you. To do that, it needs the **Claude Chrome extension** — a small add-on for your Chrome browser that lets Claude see and click on the same web pages you can see.

You only set this up once.

---

## What you need

1. **Google Chrome** (or a Chrome-based browser — Brave, Edge, and Arc also work).
2. **The Claude app you are using right now** — already done.
3. **The Claude Chrome extension** — the one piece you may not have yet.

---

## Step 1 — Install the Chrome extension

1. Open Chrome.
2. Go to the Chrome Web Store and search for **"Claude in Chrome"** (published by Anthropic), or use the link the skill shows you in Phase 1.
3. Click **Add to Chrome**, then **Add extension** in the popup.
4. You'll see the Claude icon appear in your Chrome toolbar (top-right, near the address bar). You may need to click the little puzzle-piece icon and "pin" Claude so it stays visible.

> If you don't see "Claude in Chrome" in the store, the extension may be in a limited preview. Check `claude.ai` → Settings → Connectors, or ask the person who shared this skill with you for the current install link.

## Step 2 — Sign in to the extension

1. Click the Claude icon in your toolbar.
2. Sign in with the **same Claude account** you're using right now.
3. Grant the permissions it asks for. The extension needs permission to read and act on web pages — that's how it edits LinkedIn for you.

## Step 3 — Sign in to LinkedIn yourself

1. Open a new tab.
2. Go to **linkedin.com** and sign in normally, with your own email and password.
3. **The skill never sees or types your password.** You log in yourself. The skill only acts after you're already signed in.
4. Leave that LinkedIn tab open.

## Step 4 — Tell the skill you're ready

Come back to this chat and type **`ready`**. The skill will check that the extension is connected and that LinkedIn is open, then start.

---

## How the skill checks everything is connected

When you say `ready`, the skill runs a silent check using the Chrome extension's `list_connected_browsers` tool. Three outcomes:

- **Connected, LinkedIn open** → the skill greets you and starts Phase 1.
- **Extension found, LinkedIn not open** → "I can see Chrome, but I don't see LinkedIn open and signed in. Open linkedin.com, sign in, then type `ready` again."
- **No extension** → "I can't reach the Chrome extension. Make sure it's installed and you're signed in, then restart Claude and try again." (Restarting Claude is sometimes needed for a freshly installed extension to register.)

---

## Troubleshooting

**"It says no browser connected, but I installed it."**
Restart the Claude app fully (quit, not just close the window), then reopen. A freshly installed extension often needs one restart to register.

**"The extension icon is gone."**
Click the puzzle-piece icon in Chrome's toolbar, find Claude, and click the pin so it stays visible.

**"I'm signed in to LinkedIn on my phone, not my computer."**
This skill needs LinkedIn open in Chrome **on the same computer** as the Claude app. Phone sessions don't count.

**"I use a password manager / 2FA on LinkedIn."**
That's fine and good. You sign in yourself, however you normally do, including any 2-factor step. The skill picks up only after you're in.

**"Is this safe?"**
The extension can see what you can see in your browser. This skill only navigates the parts of LinkedIn it needs to edit your profile — it never opens your messages, billing, or saved jobs. See `SECURITY.md` for the full picture. If anything feels off, type `abort` and nothing further happens.
