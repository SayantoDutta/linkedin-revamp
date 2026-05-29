"""Render a LinkedIn banner PNG at exact 1584 × 396 pixel dimensions.

Generic, persona-agnostic. Used by Phase 5 of /linkedin-revamp.

Usage:
    python build_banner.py \\
        --pattern A \\
        --hero "Your hero line." \\
        --sub "Sub-tag here." \\
        --palette "#0F1115,#6FFFB8,#1FB6A0" \\
        --url "yourdomain.com" \\
        --font-family sans \\
        --output banner.png

Patterns:
    A — Minimal editorial (dark base, soft radial accent, chrome text)
    B — Warm gradient (orange/amber sweep, hero text)
    C — Pattern overlay (dot grid, single accent)
    D — Single sentence (solid color, big type)

Premium fonts:
    Ships with OFL-licensed display fonts from the sibling ui-styling skill's
    canvas-fonts/ directory (Bricolage Grotesque, Outfit, Work Sans for sans;
    Young Serif, Gloock, Lora, Crimson Pro for serif). Falls back to system
    fonts (Arial / Segoe UI / DejaVu) only if those are missing.

Dependencies:
    Pillow (PIL)

Run --demo to render four demo banners with synthetic copy.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---- Constants -----------------------------------------------------------

WIDTH, HEIGHT = 1584, 396

# LinkedIn desktop renders a circular profile photo over roughly the
# bottom-left 352 × 352 px of the banner. Left-aligned copy must dodge it.
PROFILE_SAFE_SIZE = 352
# When left-aligned text would intrude into that quadrant, push it right to here.
LEFT_SAFE_X = 384

# Default negative tracking (letter-spacing) applied to large hero display type.
HERO_TRACKING_PX = -2


# ---- Premium font discovery ---------------------------------------------


def _dir_has_ttf(d: Path) -> bool:
    """True only if `d` is a directory containing at least one .ttf file."""
    try:
        return d.is_dir() and any(d.glob("*.ttf"))
    except OSError:
        return False


def _walk_up_for_fonts(start: Path) -> Optional[Path]:
    """Climb parents of `start` looking for .claude/skills/ui-styling/canvas-fonts."""
    rel = Path(".claude") / "skills" / "ui-styling" / "canvas-fonts"
    for parent in [start] + list(start.parents):
        cand = parent / rel
        if _dir_has_ttf(cand):
            return cand.resolve()
    return None


def _resolve_canvas_fonts_dir() -> Optional[Path]:
    """Locate the OFL canvas-fonts directory (absolute), requiring real TTFs.

    A candidate only wins if it actually contains .ttf files — an existing but
    empty cache dir must not shadow a populated one. We try, in order:
      1. The sibling ui-styling skill relative to THIS file (the public-release
         case: linkedin-revamp and ui-styling installed side by side).
      2. The documented user-global skills path.
      3. The Anthropic skills temp cache (canvas-design).
      4. A project-local .claude/skills/ui-styling/canvas-fonts found by walking
         up from this file's location and from the current working directory.
    Returns the first populated directory, else None.
    """
    here = Path(__file__).resolve()
    candidates = [
        # .../skills/linkedin-revamp/helpers/build_banner.py -> .../skills/
        here.parent.parent.parent / "ui-styling" / "canvas-fonts",
        Path.home() / ".claude" / "skills" / "ui-styling" / "canvas-fonts",
        Path(os.environ.get("TEMP", "/tmp"))
        / "anthropic_skills" / "skills" / "canvas-design" / "canvas-fonts",
    ]
    for d in candidates:
        if _dir_has_ttf(d):
            return d.resolve()
    for start in (here, Path.cwd()):
        found = _walk_up_for_fonts(start)
        if found is not None:
            return found
    return None


CANVAS_FONTS_DIR = _resolve_canvas_fonts_dir()


def _cf(name: str) -> str:
    """Absolute path to a font inside CANVAS_FONTS_DIR (or bare name if unknown)."""
    if CANVAS_FONTS_DIR is not None:
        return str(CANVAS_FONTS_DIR / name)
    return name


# Last-resort system fallbacks (kept exactly as before, tried only after premiums).
_SYS_BOLD = [
    r"C:\Windows\Fonts\arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "Inter-Bold.ttf",
]
_SYS_REG = [
    r"C:\Windows\Fonts\segoeui.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "Inter-Regular.ttf",
]
_SYS_SEMIBOLD = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "Inter-SemiBold.ttf",
]

# --- Sans voice (default): premium grotesques tried first --------------------
SANS_BOLD = [
    _cf("BricolageGrotesque-Bold.ttf"),
    _cf("Outfit-Bold.ttf"),
    _cf("WorkSans-Bold.ttf"),
] + _SYS_BOLD
SANS_REG = [
    _cf("Outfit-Regular.ttf"),
    _cf("WorkSans-Regular.ttf"),
    _cf("InstrumentSans-Regular.ttf"),
    _cf("BricolageGrotesque-Regular.ttf"),
] + _SYS_REG
SANS_SEMIBOLD = [
    _cf("Outfit-Bold.ttf"),
    _cf("WorkSans-Bold.ttf"),
    _cf("InstrumentSans-Bold.ttf"),
] + _SYS_SEMIBOLD

# --- Serif voice: high-contrast display + text serifs ------------------------
SERIF_BOLD = [
    _cf("YoungSerif-Regular.ttf"),
    _cf("Gloock-Regular.ttf"),
    _cf("Lora-Bold.ttf"),
    _cf("CrimsonPro-Bold.ttf"),
    _cf("IBMPlexSerif-Bold.ttf"),
] + _SYS_BOLD
SERIF_REG = [
    _cf("CrimsonPro-Regular.ttf"),
    _cf("Lora-Regular.ttf"),
    _cf("IBMPlexSerif-Regular.ttf"),
    _cf("LibreBaskerville-Regular.ttf"),
] + _SYS_REG
SERIF_SEMIBOLD = [
    _cf("Lora-Bold.ttf"),
    _cf("CrimsonPro-Bold.ttf"),
    _cf("IBMPlexSerif-Bold.ttf"),
] + _SYS_SEMIBOLD

# Active candidate lists (default to the sans voice). apply_font_family() can
# repoint these at module scope so the render_* functions pick them up.
FONT_CANDIDATES_BOLD = SANS_BOLD
FONT_CANDIDATES_REG = SANS_REG
FONT_CANDIDATES_SEMIBOLD = SANS_SEMIBOLD

FONT_FAMILIES = {
    "sans": (SANS_BOLD, SANS_REG, SANS_SEMIBOLD),
    "serif": (SERIF_BOLD, SERIF_REG, SERIF_SEMIBOLD),
}


def apply_font_family(family: str) -> None:
    """Point the active FONT_CANDIDATES_* globals at the chosen voice."""
    global FONT_CANDIDATES_BOLD, FONT_CANDIDATES_REG, FONT_CANDIDATES_SEMIBOLD
    bold, reg, semi = FONT_FAMILIES.get(family, FONT_FAMILIES["sans"])
    FONT_CANDIDATES_BOLD = bold
    FONT_CANDIDATES_REG = reg
    FONT_CANDIDATES_SEMIBOLD = semi


# ---- Font loading --------------------------------------------------------


_WARNED_NO_FONT = False


def first_existing_font(candidates: List[str], size: int) -> ImageFont.FreeTypeFont:
    """Try each candidate path; load the first that exists.

    If nothing matches we fall back to PIL's bitmap default, but warn loudly on
    stderr because that font renders at a tiny fixed size and the banner will
    look broken. On Pillow >= 10 we at least pass the requested size through.
    """
    global _WARNED_NO_FONT
    for path in candidates:
        try:
            if path and Path(path).exists():
                return ImageFont.truetype(path, size)
        except (OSError, ValueError):
            continue
    if not _WARNED_NO_FONT:
        sys.stderr.write(
            "[build_banner] WARNING: no TrueType font found in any candidate "
            "path (premium canvas-fonts or system fonts). Falling back to "
            "PIL's bitmap default — text will render tiny and unreadable. "
            "Install the fonts or check CANVAS_FONTS_DIR.\n"
        )
        _WARNED_NO_FONT = True
    try:
        # Pillow >= 10 accepts a size; older versions raise TypeError.
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


# ---- Text helpers --------------------------------------------------------


def tracked_width(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    tracking_px: int = 0,
) -> int:
    """Total pixel width of `text` if drawn char-by-char with `tracking_px`."""
    if not text:
        return 0
    total = 0
    for ch in text:
        bb = draw.textbbox((0, 0), ch, font=font)
        total += (bb[2] - bb[0]) + tracking_px
    # The trailing tracking gap after the last glyph shouldn't count.
    total -= tracking_px
    return total


def draw_tracked(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill,
    tracking_px: int = HERO_TRACKING_PX,
) -> int:
    """Render `text` glyph-by-glyph applying negative/positive letter-spacing.

    PIL has no native tracking, so big display type looks airy with default
    spacing. This advances the pen by each glyph's measured width plus
    `tracking_px`. Returns the total advance width.
    """
    x, y = xy
    start_x = x
    for ch in text:
        draw.text((x, y), ch, fill=fill, font=font)
        bb = draw.textbbox((0, 0), ch, font=font)
        x += (bb[2] - bb[0]) + tracking_px
    return (x - tracking_px) - start_x if text else 0


# ---- Image helpers -------------------------------------------------------


def add_grain(img: Image.Image, opacity: float = 0.055) -> Image.Image:
    """Blend subtle monochrome paper grain over the image.

    Kills the dead-flat "AI-rendered" look. `opacity` ~0.05–0.06.
    """
    base = img.convert("RGB")
    noise = Image.effect_noise((base.width, base.height), 28).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(base, noise_rgb, opacity)


def safe_left_x(x: int, y_top: int, y_bottom: int) -> int:
    """Keep left-aligned copy clear of the bottom-left profile-photo circle.

    If the text starts within the left PROFILE_SAFE_SIZE px AND its vertical
    span overlaps the photo band, push it right to LEFT_SAFE_X.
    """
    band_top = HEIGHT - PROFILE_SAFE_SIZE
    overlaps_band = y_bottom >= band_top and y_top <= HEIGHT
    if x < PROFILE_SAFE_SIZE and overlaps_band:
        return max(x, LEFT_SAFE_X)
    return x


# ---- Color helpers -------------------------------------------------------

_HEXDIGITS = set("0123456789abcdefABCDEF")


def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    """Parse a hex color into an (r, g, b) tuple.

    Accepts '#rgb' shorthand and '#rrggbb', with or without the leading '#'.
    Raises a clear ValueError on anything else.
    """
    original = h
    s = h.strip().lstrip("#").strip()
    if len(s) == 3 and all(c in _HEXDIGITS for c in s):
        s = "".join(c * 2 for c in s)  # #fff -> ffffff
    if len(s) != 6 or any(c not in _HEXDIGITS for c in s):
        raise ValueError(
            "Invalid hex color {!r}: expected '#rgb' or '#rrggbb' "
            "(e.g. '#0F1115' or '#fff').".format(original)
        )
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def parse_palette(palette_str: str) -> List[Tuple[int, int, int]]:
    """Parse a comma-separated palette. Patterns unpack base, accent, mid."""
    if not palette_str:
        return [(15, 17, 21), (111, 255, 184), (31, 182, 160)]
    colors = [hex_to_rgb(c) for c in palette_str.split(",") if c.strip()]
    if len(colors) < 3:
        raise ValueError(
            "Palette needs at least 3 colors (base, accent, mid); got {} "
            "from {!r}. Example: '#0F1115,#6FFFB8,#1FB6A0'.".format(
                len(colors), palette_str
            )
        )
    return colors


# ---- Patterns ------------------------------------------------------------


def render_pattern_a(
    hero: str, sub: str, palette: list, url: str
) -> Image.Image:
    """Pattern A — Minimal editorial. Dark base + soft radial sweep."""
    base, accent, mid = palette[:3]
    img = Image.new("RGB", (WIDTH, HEIGHT), base)
    draw = ImageDraw.Draw(img)

    # Soft radial sweep from upper-right toward lower-left
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    cx, cy = int(WIDTH * 0.75), int(HEIGHT * 0.25)
    max_r = int((WIDTH ** 2 + HEIGHT ** 2) ** 0.5)
    for r in range(max_r, 0, -10):
        t = r / max_r
        # Lerp accent → mid → base
        if t < 0.5:
            f = t * 2
            color = (
                int(accent[0] * (1 - f) + mid[0] * f),
                int(accent[1] * (1 - f) + mid[1] * f),
                int(accent[2] * (1 - f) + mid[2] * f),
                max(0, int(80 * (1 - t))),
            )
        else:
            f = (t - 0.5) * 2
            color = (
                int(mid[0] * (1 - f) + base[0] * f),
                int(mid[1] * (1 - f) + base[1] * f),
                int(mid[2] * (1 - f) + base[2] * f),
                max(0, int(40 * (1 - t))),
            )
        ov_draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Left identity strip
    f_id = first_existing_font(FONT_CANDIDATES_SEMIBOLD, 20)
    f_sub_id = first_existing_font(FONT_CANDIDATES_REG, 14)
    draw.text((64, 44), "*", fill=accent, font=f_id)
    draw.text((92, 46), sub.split("·")[0].strip() if sub else "", fill=(245, 245, 245), font=f_id)
    if sub and "·" in sub:
        rest = " · ".join(p.strip() for p in sub.split("·")[1:])
        draw.text((92, 76), rest, fill=(180, 190, 200), font=f_sub_id)

    # Top-right URL
    if url:
        f_url = first_existing_font(FONT_CANDIDATES_REG, 14)
        bb = draw.textbbox((0, 0), url, font=f_url)
        draw.text((WIDTH - 64 - (bb[2] - bb[0]), 48), url, fill=(220, 225, 235), font=f_url)

    # Hero text right-aligned, multiple lines (tracked for tight display feel)
    lines = [ln for ln in hero.split("\n") if ln.strip()] or [hero]
    f_hero = first_existing_font(FONT_CANDIDATES_BOLD, 78)
    tr = HERO_TRACKING_PX
    line_gap = 6
    line_heights = []
    for ln in lines:
        bb = draw.textbbox((0, 0), ln, font=f_hero)
        line_heights.append(bb[3] - bb[1])
    total_h = sum(line_heights) + line_gap * (len(lines) - 1)
    y_cursor = (HEIGHT - total_h) // 2

    # Shadow pass for soft chrome look
    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow)
    for i, ln in enumerate(lines):
        w = tracked_width(sh_draw, ln, f_hero, tr)
        x = WIDTH - 80 - w
        draw_tracked(sh_draw, (x + 3, y_cursor + 4), ln, f_hero, (0, 0, 0, 110), tr)
        y_cursor += line_heights[i] + line_gap
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=4))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Real text pass
    y_cursor = (HEIGHT - total_h) // 2
    for i, ln in enumerate(lines):
        color = (245, 245, 245) if i < len(lines) - 1 else (250, 240, 225)
        if i == len(lines) - 1 and ln.endswith("."):
            base_text = ln[:-1]
            base_w = tracked_width(draw, base_text, f_hero, tr)
            dot_w = tracked_width(draw, ".", f_hero, tr)
            x = WIDTH - 80 - base_w - tr - dot_w
            draw_tracked(draw, (x, y_cursor), base_text, f_hero, color, tr)
            draw_tracked(draw, (x + base_w + tr, y_cursor), ".", f_hero, accent, tr)
        else:
            w = tracked_width(draw, ln, f_hero, tr)
            x = WIDTH - 80 - w
            draw_tracked(draw, (x, y_cursor), ln, f_hero, color, tr)
        y_cursor += line_heights[i] + line_gap

    return add_grain(img)


def render_pattern_b(
    hero: str, sub: str, palette: list, url: str
) -> Image.Image:
    """Pattern B — Warm gradient. Diagonal sweep, hero text on right."""
    base, accent, _ = palette[:3]
    img = Image.new("RGB", (WIDTH, HEIGHT), base)

    # Diagonal gradient — rendered at low resolution then upscaled with LANCZOS
    # so it's smooth instead of the old 8px-rectangle banding.
    scale = 8
    sw, sh = WIDTH // scale, HEIGHT // scale
    small = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    px = small.load()
    for sy in range(sh):
        for sx in range(sw):
            t = (sx / sw + (sh - sy) / sh) / 2
            if t > 0.5:
                a = int(180 * (t - 0.5) * 2)
                px[sx, sy] = (accent[0], accent[1], accent[2], min(220, a))
    overlay = small.resize((WIDTH, HEIGHT), Image.LANCZOS)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=2))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Hero text right (tracked)
    f_hero = first_existing_font(FONT_CANDIDATES_BOLD, 88)
    tr = HERO_TRACKING_PX
    bb = draw.textbbox((0, 0), hero, font=f_hero)
    w = tracked_width(draw, hero, f_hero, tr)
    x = WIDTH - 80 - w
    y = (HEIGHT - (bb[3] - bb[1])) // 2 - 10
    draw_tracked(draw, (x, y), hero, f_hero, (255, 250, 240), tr)

    # Sub bottom-right
    if sub:
        f_sub = first_existing_font(FONT_CANDIDATES_SEMIBOLD, 22)
        bb = draw.textbbox((0, 0), sub, font=f_sub)
        draw.text(
            (WIDTH - 80 - (bb[2] - bb[0]), HEIGHT - 60),
            sub,
            fill=(255, 220, 195),
            font=f_sub,
        )

    # URL top-right
    if url:
        f_url = first_existing_font(FONT_CANDIDATES_REG, 14)
        bb = draw.textbbox((0, 0), url, font=f_url)
        draw.text((WIDTH - 64 - (bb[2] - bb[0]), 40), url, fill=(255, 240, 220), font=f_url)

    return add_grain(img)


def render_pattern_c(hero: str, sub: str, palette: list, url: str) -> Image.Image:
    """Pattern C — Pattern overlay. Subtle dot grid + single accent + big text."""
    base, accent, _ = palette[:3]
    img = Image.new("RGB", (WIDTH, HEIGHT), base)

    # Dot grid background on a separate RGBA overlay so the alpha is honored
    # (drawing RGBA fill straight onto an RGB image silently drops alpha).
    grid = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for y in range(20, HEIGHT, 28):
        for x in range(20, WIDTH, 28):
            gd.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(accent[0], accent[1], accent[2], 40))
    img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Hero left-aligned — kept clear of the bottom-left profile-photo circle.
    f_hero = first_existing_font(FONT_CANDIDATES_BOLD, 72)
    tr = HERO_TRACKING_PX
    bb = draw.textbbox((0, 0), hero, font=f_hero)
    hero_h = bb[3] - bb[1]
    y = (HEIGHT - hero_h) // 2 - 10
    x_hero = safe_left_x(96, y, y + hero_h)
    draw_tracked(draw, (x_hero, y), hero, f_hero, (0, 0, 0), tr)

    if sub:
        f_sub = first_existing_font(FONT_CANDIDATES_REG, 22)
        sub_y = y + hero_h + 20
        sbb = draw.textbbox((0, 0), sub, font=f_sub)
        x_sub = safe_left_x(96, sub_y, sub_y + (sbb[3] - sbb[1]))
        draw.text((x_sub, sub_y), sub, fill=(80, 80, 80), font=f_sub)

    if url:
        f_url = first_existing_font(FONT_CANDIDATES_REG, 14)
        bb = draw.textbbox((0, 0), url, font=f_url)
        draw.text((WIDTH - 64 - (bb[2] - bb[0]), 40), url, fill=(60, 60, 60), font=f_url)

    return add_grain(img)


def render_pattern_d(hero: str, sub: str, palette: list, url: str) -> Image.Image:
    """Pattern D — Single sentence. Solid background, big type."""
    base, accent, _ = palette[:3]
    img = Image.new("RGB", (WIDTH, HEIGHT), base)
    draw = ImageDraw.Draw(img)

    f_hero = first_existing_font(FONT_CANDIDATES_BOLD, 88)
    tr = HERO_TRACKING_PX
    bb = draw.textbbox((0, 0), hero, font=f_hero)
    w = tracked_width(draw, hero, f_hero, tr)
    x = (WIDTH - w) // 2
    y = (HEIGHT - (bb[3] - bb[1])) // 2 - 10
    draw_tracked(draw, (x, y), hero, f_hero, (255, 255, 255), tr)

    if sub:
        f_sub = first_existing_font(FONT_CANDIDATES_REG, 22)
        bb = draw.textbbox((0, 0), sub, font=f_sub)
        draw.text(
            ((WIDTH - (bb[2] - bb[0])) // 2, y + 100),
            sub,
            fill=accent,
            font=f_sub,
        )

    if url:
        f_url = first_existing_font(FONT_CANDIDATES_REG, 14)
        bb = draw.textbbox((0, 0), url, font=f_url)
        draw.text((WIDTH - 64 - (bb[2] - bb[0]), HEIGHT - 36), url, fill=(180, 180, 180), font=f_url)

    return add_grain(img)


# ---- CLI -----------------------------------------------------------------


PATTERNS = {
    "A": render_pattern_a,
    "B": render_pattern_b,
    "C": render_pattern_c,
    "D": render_pattern_d,
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pattern", default="A", choices=list(PATTERNS.keys()))
    p.add_argument("--hero", default="Your line here.")
    p.add_argument("--sub", default="")
    p.add_argument("--palette", default="")
    p.add_argument("--url", default="")
    p.add_argument(
        "--font-family",
        default="sans",
        choices=list(FONT_FAMILIES.keys()),
        help="Typographic voice: 'sans' (default) or 'serif'.",
    )
    p.add_argument("--output", default="banner.png")
    p.add_argument("--demo", action="store_true", help="Render four demo banners")
    args = p.parse_args()

    apply_font_family(args.font_family)

    if args.demo:
        demos = [
            ("A", "Agents that\nactually\nship.", "AI Builder · End-to-End", "#0F1115,#6FFFB8,#1FB6A0", "yourdomain.com", "demo_A.png"),
            ("B", "Most B2B SaaS\nis ugly.\nI fix that.", "Senior Product Designer · Lisbon", "#1A1B3E,#FFB36E,#F5F1E8", "yourdomain.com", "demo_B.png"),
            ("C", "Frontend that doesn't break.", "Engineering Lead · ex-Stripe · Berlin", "#F5F1E8,#FF5B1F,#000000", "yourdomain.com", "demo_C.png"),
            ("D", "Closing $1M+\nin B2B SaaS deals.", "Outbound · enterprise · NYC", "#0F1115,#FF8A3D,#1FB6A0", "", "demo_D.png"),
        ]
        for pat, hero, sub, pal, url, out in demos:
            img = PATTERNS[pat](hero, sub, parse_palette(pal), url)
            img.save(out)
            print(f"Wrote {out}")
        return 0

    try:
        palette = parse_palette(args.palette)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if args.pattern not in PATTERNS:
        print(f"Unknown pattern: {args.pattern}", file=sys.stderr)
        return 1

    img = PATTERNS[args.pattern](args.hero, args.sub, palette, args.url)
    out_path = Path(args.output)
    if out_path.parent != Path(""):
        out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(f"Wrote {out_path} ({WIDTH}×{HEIGHT})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
