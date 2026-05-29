# Banner prompts

The LinkedIn banner is 1584 × 396 px. It is the biggest visual element on the profile. Most users leave it default. Don't.

This template gives you both:
1. Local-render parameters for `helpers/build_banner.py` to produce a clean PNG immediately.
2. Copy-paste prompts for Nano Banana / Midjourney / FLUX if the user wants a higher-fidelity image.

---

## Hard rules

1. **Exact dimensions: 1584 × 396 px.** No other.
2. **Safe zone for mobile.** LinkedIn crops to roughly the center 70% on mobile. Anchor all critical text to the center band.
3. **Profile photo zone.** On desktop, the profile photo circle covers roughly the bottom-left 350 × 350 px area. Don't put text in that quadrant.
4. **No AI-generated text.** Image generators garble text. Render text separately in Canva, Figma, or via PIL — never let Nano Banana write the text.
5. **No stock people, no laptops, no abstract goop.** They scream junior.
6. **One accent color max.** Restraint reads expensive.

---

## Banner concept patterns

Pick by `voice_mode` and `target_person`.

### Pattern A — Minimal editorial (Confident or Conservative voice)

Dark base + 1 soft gradient sweep + clean text on the right.

```
Layout:
- Left third: tiny identity strip — single icon + 2 lines of text in sans-serif
- Middle: empty space
- Right two-thirds: hero text in chrome/silver gradient, 3 short lines
- Top-right corner: small URL line

Palette options:
- Charcoal + electric mint (#0F1115, #6FFFB8, #1FB6A0)
- Navy + warm cream (#0A1A2E, #F5F1E8, #FF8A3D)
- Black + silver gradient (#000000, #E8E8E8, single accent color)
```

### Pattern B — Warm gradient (Bold voice)

Diagonal warm gradient base (orange / amber / red) with one bold sentence overlaid.

```
Layout:
- Full-bleed gradient
- Hero text right-aligned, top 60% of canvas
- Sub-tag bottom-right, single line
- Identity glyph + line top-left

Palette options:
- Sunset (#0A0E27, #FF8A3D, #E55934)
- Indigo dusk (#1A1B3E, #FFB36E, #F5F1E8)
- Rose gold (#1F0A1A, #FFB3BC, #F7E7CE)
```

### Pattern C — Pattern overlay (Funny or distinct voice)

Single bold pattern (dots, lines, geometric shapes) with text on top.

```
Layout:
- Background: subtle repeating pattern, low contrast
- Text: large sans-serif center-anchored or left-aligned
- One accent color only

Palette options:
- Cream + black + one accent (#F5F1E8, #000000, plus user-pick)
- Off-white + slate + one accent
```

### Pattern D — Single sentence (any voice)

Solid color background, one sentence in a strong typeface. No other elements.

```
Layout:
- Solid color background, persona-appropriate
- One sentence centered or left-aligned, 60-72pt
- Single line, max 8 words
```

---

## Local render (use immediately)

Call `helpers/build_banner.py` with the chosen pattern's parameters:

```bash
python helpers/build_banner.py \
  --pattern A \
  --hero "Your hero line here." \
  --sub "Role · Specialty · City" \
  --palette "#0F1115,#6FFFB8,#1FB6A0" \
  --url "yourdomain.com" \
  --output snapshots/{handle}-{date}-banner.png
```

The script renders a clean PNG at 1584 × 396. Good enough to ship as-is.

For a higher-fidelity version, use the Nano Banana prompt below.

---

## Nano Banana / Midjourney / FLUX prompts

For each pattern, here is the copy-paste prompt. Replace `{hero}`, `{sub}`, `{palette}`, and `{url}` with the user's choices.

### Pattern A — Minimal editorial prompt

```
A 1584 by 396 pixel LinkedIn banner. Ultra-wide cinematic crop. Premium minimal editorial style.

Background: matte charcoal #0F1115 with a single soft radial gradient light source from the upper-right quadrant. Gradient stops: electric mint #6FFFB8 at center, fading through teal #1FB6A0, deep navy #0A1A2E, to black at the far left edge. Subtle paper grain at 6% opacity across the entire canvas.

No people, no laptops, no abstract particles, no flames, no glitches.
No text rendered inside the image — text will be added separately.

The image should feel like the opening frame of a high-end product film: quiet, expensive, with deep negative space.

Mood: editorial. Color story: cool with one bright mint accent in the top-right corner.

Anchor compositional weight to the right two-thirds of the canvas, leaving the left third open for typography that will be added later.
```

After Nano Banana returns the image, add text in Canva or Figma using:
- Font: Inter Tight Bold for hero, Inter Regular for sub
- Hero size: 96pt
- Hero color: cream/silver gradient (top: #E8FFF4 to bottom: #4A6B6C)
- Sub size: 22pt, color: #B8C2D9
- URL size: 14pt, color: #E5E9F0, top-right corner

### Pattern B — Warm gradient prompt

```
A 1584 by 396 pixel LinkedIn banner. Cinematic widescreen.

Background: deep indigo #1A1B3E base with a warm amber #FF8A3D gradient sweeping diagonally from lower-right to upper-left. Subtle film grain.

In the lower-left, a soft geometric vector wedge in cream #F5F1E8 at 8% opacity, suggesting motion.

No text rendered inside the image. No people, no faces, no devices, no flames.

The image should feel like dusk through tinted glass — warm, premium, intentional.

Anchor compositional weight to the right two-thirds. Leave the bottom-left quadrant open for the profile photo circle.
```

### Pattern C — Pattern overlay prompt

```
A 1584 by 396 pixel LinkedIn banner. Editorial flat design.

Background: cream #F5F1E8 with a subtle repeating pattern of small geometric shapes (dots, hexagons, or triangles — pick one) at low contrast. The pattern should be barely visible — 6% opacity.

One accent color: {hex code chosen by user}. Use it sparingly — only in a single small element top-right or bottom-right.

No text rendered inside the image. No people. No devices.

The image should feel like a well-designed magazine cover — quiet, considered, modern.
```

### Pattern D — Single sentence prompt

If the user picks Pattern D, no prompt is needed. Render the solid color background in Canva or Figma. Add the sentence in a strong typeface. Ship.

---

## Banner copy rules

The hero text in the banner is the user's mission statement, distilled. Pull from:
- `user_profile.north_star` (most direct fit)
- `user_profile.biggest_result` (proof-of-doing)
- `user_profile.mission_90d` (urgency)

Examples by persona:

- **Builder** (Confident voice): "Agents that actually ship.", "Voice AI for India.", "End-to-end product engineer."
- **Designer** (Bold voice): "Most B2B SaaS is ugly. I fix that.", "Design that's actually used."
- **Sales/BD** (Confident voice): "Closing $1M+ in B2B SaaS deals.", "Outbound that works."
- **Founder** (Bold voice): "Building [thing] from zero.", "Year 1 of [company]."
- **Career switcher** (Conservative voice): "From [old] to [new]. The plan: [one-line].", "Learning to build in public."

If the hero is more than 6 words, the banner will feel cluttered. Cut.

---

## What to never produce

- Banners with stock photos of business people in suits
- Banners with motivational quotes that aren't the user's own
- Banners with neon-bright gradients that scream Web3
- Banners with "Open to opportunities" written on them — use the LinkedIn frame instead
- Banners with the user's selfie cropped in
- Banners with sparkles, lens flare, or "AI-feeling" effects
- Banners that include a phone number or email — that's what Contact Info is for
