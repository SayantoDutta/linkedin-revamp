# Notion page style — markdown to blocks

How to turn an approved markdown draft into a clean Notion page via the Notion MCP. A case study that looks like a wall of text gets skimmed and closed. Structure earns the read.

---

## Block mapping

Map each part of the six-part structure to a specific Notion block type:

| Draft part | Notion block | Why |
|------------|--------------|-----|
| Page title | Page title | The project name. Short. No tagline here. |
| One-line summary | **Callout** (with an emoji, e.g. 💡 or 🎯) | Sits at the very top, visually distinct. The one line everyone reads. |
| Section names (Problem, Approach…) | **Heading 2** | Scannable. A reader jumps to "Outcome" first — make it findable. |
| Body paragraphs | **Paragraph** | Keep each to 2–4 sentences. Break long ones up. |
| Stack / key decisions | **Bulleted list**, or a **Toggle** titled "Technical detail" | Toggle hides depth from non-technical readers while keeping it for those who want it. |
| Outcome numbers | **Callout** (📈) or **bold** inline | Make the result impossible to miss. |
| Proof screenshot | **Image** block | The single most persuasive element. Place it right after the Outcome. |
| Live link / repo | **Bookmark** block | Renders a rich preview card, not a bare URL. |
| User quote | **Quote** block | Visually signals "someone else said this", which carries more weight. |
| What's next | **Paragraph** under a Heading 2 | Closes the page on forward motion. |

---

## Layout order on the page

```
[Callout]  One-line summary
─────────────────────────────
H2  The problem
    paragraph
H2  The approach
    paragraph(s)
    Toggle ▸ "How it's built" (optional technical detail)
H2  The outcome
    [Callout 📈]  the headline number/result
    paragraph
    [Image]  proof screenshot
    [Bookmark]  live link
H2  What's next
    paragraph
```

---

## Formatting do's and don'ts

**Do**
- Keep paragraphs short. Notion's default font is large — a 6-line paragraph looks like an essay.
- Use exactly one callout at the top and (optionally) one for the headline number. More than two callouts and they stop standing out.
- Put the proof image high — right after the outcome, not buried at the bottom.
- Use a bookmark block for any external link so it renders a preview.
- Use sentence case for headings ("The approach", not "THE APPROACH" or "The Approach").

**Don't**
- Don't dump the whole tech stack in the body. Toggle it or bullet it.
- Don't use more than two heading levels. H2 for sections is enough; nest with bullets, not H3/H4.
- Don't leave a bare URL as text — always a bookmark or link block.
- Don't add a "Table of contents" block for a page this short. It's overkill.
- Don't use Notion's database/table blocks here — a case study is a narrative, not a dataset.

---

## Creating blocks via the MCP

When calling the Notion MCP to build the page:

1. Create the page under the chosen parent with the project name as the title.
2. Append blocks in layout order. If the MCP takes a markdown-or-blocks payload, send the structured blocks rather than one big markdown string — you get cleaner callouts, toggles, and bookmarks that way.
3. For the image: if the user gave a public image URL, use an image block with that URL. If they gave a local file, you likely can't upload it through the API — tell the user to drag the image into the page once, after it's created.
4. After the page exists, publish to web (or hand the user the one-click publish step) and capture the public URL.

---

## Quality bar before publishing

Before you tell the user a page is ready:

- The summary callout reads true and fits on one or two lines.
- Every section heading is present and in order.
- The outcome is concrete (a number, or an honest "early, here's the visible result").
- There's at least one piece of proof (image or link).
- No cliché survived the cringe filter.
- The page reads cleanly top to bottom — no wall of text, no bare URLs, no orphan headings.
