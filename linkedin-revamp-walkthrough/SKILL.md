---
name: linkedin-revamp-walkthrough
description: Builds short animated MP4 walkthrough videos of a user's work — title card, fitted screenshots with captions, brand colors, and an outro — sized for a LinkedIn Featured tile or Notion embed. Triggers when the user says "make a walkthrough video", "turn my screenshots into a video", "animate my project", or invokes `/linkedin-revamp-walkthrough`. Also offered by `/linkedin-revamp` in Phase 8 when the user has 3+ screenshots and ffmpeg is installed. Requires ffmpeg on PATH.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Glob, AskUserQuestion
---

# linkedin-revamp-walkthrough — Animated work videos for LinkedIn

> Optional add-on to `/linkedin-revamp`. Also runs standalone. Turns a handful of screenshots into a short, branded MP4 you can drop into your LinkedIn Featured section.

A still screenshot scrolls past. A 20-second video with a title card and your name on it makes someone stop. This sub-skill builds that video — no video-editing software, no timeline, no manual work. You give it screenshots and a few captions; it renders an MP4.

**Time required:** about 15 minutes.
**You will need:** `ffmpeg` installed, and 3 or more screenshots of your work (product, dashboard, code, design — whatever shows the thing).

---

## What it produces

A single MP4, 1920×1080, 30fps, roughly 15–25 seconds:

1. **Title card** — project name, one-line tagline, a detail strip, your brand accent color.
2. **Scenes** — each screenshot fitted onto a dark stage with a one-line caption underneath.
3. **Outro card** — "Built by [you]", your site and LinkedIn handle.

The file is sized to upload straight into a LinkedIn Featured tile, or embed in a Notion case study.

---

## When this skill offers itself

If invoked through `/linkedin-revamp` Phase 8, the core skill only offers this when **both** are true:

- The user's CV or portfolio surfaced **3+ screenshots or images** of their work.
- **`ffmpeg` is on PATH** (checked with `ffmpeg -version`).

If either is false, the core skill skips the offer rather than setting the user up to fail. Run standalone any time by typing `/linkedin-revamp-walkthrough`.

---

## Pre-flight

Before doing anything, run these checks silently:

1. **ffmpeg present.** Run `ffmpeg -version`. If it errors, stop and tell the user in plain English:
   > "This add-on needs a free tool called ffmpeg to stitch the video together. Install it from ffmpeg.org (or `brew install ffmpeg` on Mac, `winget install ffmpeg` on Windows), then come back and type `ready`."
2. **Pillow present.** Run `python -c "import PIL"`. If it errors, run `pip install Pillow` and report it.
3. **Helper present.** Confirm `helpers/build_walkthrough.py` exists in this skill directory.

Only continue once ffmpeg and Pillow are both available.

---

## Step-by-step

### Step 1 — Gather the material

Ask the user, one question at a time, in plain English (clear hook, a one-line "why this matters", a recovery hint). If the core `linkedin-revamp` skill is installed alongside this one, follow its `linkedin-revamp/references/question-format.md` style guide; if not, the plain-English rule here is enough.

1. **"What's the project called, and what does it do in one line?"**
   ELI10: "This becomes the title card — the first thing a viewer sees. Keep the one-liner to about 8 words."

2. **"Drop me the screenshots, in the order you want them shown."**
   ELI10: "3 to 6 works best. More than 6 and the video drags. Order matters — lead with the most impressive one." Accept files the user attaches to the chat, or paths to files on disk.

3. **"One short caption per screenshot — what is the viewer looking at?"**
   ELI10: "One line each, like a museum placard. 'Master dashboard — routes to 8 sub-agents' beats 'Screenshot 1'."

4. **"What two brand colors should I use — a dark background and a bright accent?"**
   ELI10: "Give me two hex codes, or name a vibe ('warm orange on near-black') and I'll pick. The accent is the bar under your title and the caption color." Default: `#0F1115` background, `#6FFFB8` accent.

5. **"How should the outro read — your name, and your site or LinkedIn handle?"**
   ELI10: "This is the last frame, the 'who made this' card. e.g. 'Built by Jordan Lee' / 'jordanlee.dev · linkedin.com/in/jordanlee'."

Reflect the plan back before rendering:
> "Here's the video I'll build: title **'[name] — [tagline]'**, then [N] screenshots with your captions, then an outro card with your name. Colors: dark [bg], accent [accent]. About [estimate] seconds. Type `render` to build it, or tell me what to change."

### Step 2 — Write the spec

Build a JSON spec for `helpers/build_walkthrough.py`. Write it to `walkthrough-spec.json` in the working directory.

```json
{
  "output": "walkthrough.mp4",
  "palette": { "bg": "#0F1115", "accent": "#6FFFB8" },
  "title":  { "lines": ["Project Name", "One-line tagline"],
              "subtitle": "Detail  ·  Detail  ·  Detail" },
  "scenes": [
    { "image": "/abs/path/shot1.png", "caption": "What screen one shows", "duration": 5 },
    { "image": "/abs/path/shot2.png", "caption": "What screen two shows", "duration": 5 }
  ],
  "outro":  { "lines": ["Built by", "Your Name"],
              "subtitle": "yourdomain.com  ·  linkedin.com/in/you" }
}
```

Notes on durations: title 2.5s, each scene 5s (4s if there are 6 screenshots so the total stays under ~28s), outro 3s. The helper holds the last frame so the video doesn't cut to black abruptly.

Use **absolute paths** for every screenshot. If the user attached files to the chat, resolve their on-disk paths first.

### Step 3 — Render

Run the helper:

```bash
python helpers/build_walkthrough.py --spec walkthrough-spec.json
```

Watch the output. The helper prints the ffmpeg command and the final file size. If ffmpeg errors, the helper prints the last 2000 chars of stderr — read it, fix the spec (most common cause: a screenshot path that doesn't exist or isn't a readable image), and re-run.

### Step 4 — Show and confirm

Tell the user where the file landed and how big it is:
> "Done — `walkthrough.mp4` (1920×1080, ~[N] seconds, [size] KB). Open it and check the captions read well and the screenshots aren't cut off."

If the user wants changes (different order, a caption fix, different colors), edit the spec and re-render. Cheap to iterate — it's a few seconds per render.

### Step 5 — Hand off to upload

If running standalone, tell the user how to add it to LinkedIn:
> "To put this on your profile: go to your profile → Featured section → + → Add media → upload `walkthrough.mp4`. Give it the same title as the project."

If running as part of `/linkedin-revamp`, hand the file path back to the core skill's Featured-tile flow (Phase 6 Step 6.7), which uploads it via the Chrome extension.

---

## The helper — what it does

`helpers/build_walkthrough.py` is a single self-contained script:

- **`make_card(...)`** renders title and outro cards — gradient background, centered accent bar, big title, accent subtitle, muted detail strip.
- **`fit_screenshot(...)`** fits any screenshot inside 1920×1080 on a dark stage (preserving aspect ratio, never stretching) with a caption strip along the bottom.
- **`build_video(...)`** writes an ffmpeg concat list and renders the MP4 (libx264, yuv420p, faststart for web).
- **`render_from_spec(...)`** is the driver — reads the JSON spec, renders all frames, builds the video.

Cross-platform fonts: it tries Windows, macOS, and Linux font paths in order and falls back to a default if none are found.

Run `python helpers/build_walkthrough.py --demo` to render a title+outro demo with no screenshots, to confirm ffmpeg and Pillow are wired up.

---

## Safety + scope

- **No network, no third-party services.** Everything renders locally with Pillow + ffmpeg.
- **Only reads the screenshots the user provides.** It doesn't scan the disk for images.
- **Writes only to the working directory** — the spec, the rendered frames (in a scratch folder), and the MP4.
- **No PII baked into the helper.** All names, sites, and copy come from the spec the user approved.

---

## Troubleshooting

- **"ffmpeg not found."** Install it (ffmpeg.org / `brew install ffmpeg` / `winget install ffmpeg`), reopen the terminal so PATH refreshes, retry.
- **A screenshot looks tiny in the frame.** That screenshot is low-resolution. The helper never upscales (that would look blurry). Use a higher-res capture.
- **Captions get cut off.** The caption is too long for one line. Keep captions under ~60 characters.
- **The video is too long.** Reduce screenshot count or drop each scene's duration to 4s in the spec.
- **Colors look wrong.** Check the hex codes in the spec. Background should be dark, accent bright, for contrast.

---

## License

MIT. Part of the `linkedin-revamp` suite. You own the videos you create.
