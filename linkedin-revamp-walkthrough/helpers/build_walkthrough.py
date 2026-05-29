"""Build an animated walkthrough MP4 from a JSON spec.

Generic, persona-agnostic. Used by /linkedin-revamp-walkthrough to turn a set of
screenshots into a short, branded video for a LinkedIn Featured tile.

Structure of every video:
    Title card  ->  Ken-Burns-free fitted screenshots with captions  ->  Outro card
    1920x1080, 30fps, ~15-25 sec total. Sized for LinkedIn Featured + Notion embed.

Usage:
    python build_walkthrough.py --spec walkthrough.json
    python build_walkthrough.py --demo
    python build_walkthrough.py --help

Spec format (JSON):
    {
      "output": "my_walkthrough.mp4",
      "palette": { "bg": "#0F1115", "accent": "#6FFFB8" },
      "title":  { "lines": ["Project Name", "One-line tagline"],
                  "subtitle": "Detail one  ·  Detail two  ·  Detail three" },
      "scenes": [
        { "image": "shot1.png", "caption": "What this screen shows", "duration": 5 },
        { "image": "shot2.png", "caption": "And this one",           "duration": 5 }
      ],
      "outro":  { "lines": ["Built by", "Your Name"],
                  "subtitle": "yourdomain.com  ·  linkedin.com/in/you" }
    }

Requirements:
    - Pillow (PIL)
    - ffmpeg on PATH
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

# ---- Constants -----------------------------------------------------------

W, H = 1920, 1080
FPS = 30

FONT_CANDIDATES_BOLD = [
    r"C:\Windows\Fonts\arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_CANDIDATES_REG = [
    r"C:\Windows\Fonts\segoeui.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_CANDIDATES_SEMIBOLD = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


# ---- Helpers -------------------------------------------------------------


def first_existing_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    print(
        "WARNING: no TrueType font found in the candidate list; falling back to "
        "PIL's built-in bitmap font. Text will be small and low-resolution. "
        "Install a TTF (e.g. DejaVu/Arial) or edit FONT_CANDIDATES_* to fix this.",
        file=sys.stderr,
    )
    try:
        # Pillow >= 10 accepts a size for the default font; older versions don't.
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    original = h
    h = h.strip().lstrip("#")
    if len(h) == 3:  # expand shorthand, e.g. "fff" -> "ffffff"
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6 or any(ch not in "0123456789abcdefABCDEF" for ch in h):
        raise SystemExit(
            "Invalid hex color {!r}: expected '#RGB' or '#RRGGBB' (e.g. '#6FFFB8'). "
            "Named colors are not supported.".format(original)
        )
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


# ---- Renderers -----------------------------------------------------------


def make_card(text_lines, accent, out_path, subtitle=None, bg_color=(15, 17, 21)):
    """Render a 1920x1080 title/outro card with brand styling."""
    if not text_lines:
        text_lines = ["Walkthrough"]
    im = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(im)

    # Subtle vertical gradient
    for y in range(H):
        c = min(255, int(bg_color[0] + (y / H) * 8))
        draw.line([(0, y), (W, y)], fill=(c, min(255, c + 2), min(255, c + 6)))

    # Accent bar centered above the title
    line_y = H // 2 - 60
    draw.rectangle([(W // 2 - 40, line_y), (W // 2 + 40, line_y + 4)], fill=accent)

    f_title = first_existing_font(FONT_CANDIDATES_BOLD, 92)
    f_sub = first_existing_font(FONT_CANDIDATES_SEMIBOLD, 36)
    f_meta = first_existing_font(FONT_CANDIDATES_REG, 24)

    title = text_lines[0]
    tb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((W - (tb[2] - tb[0])) // 2, H // 2 - 20), title,
              fill=(245, 245, 245), font=f_title)

    if len(text_lines) > 1:
        sub = text_lines[1]
        sb = draw.textbbox((0, 0), sub, font=f_sub)
        draw.text(((W - (sb[2] - sb[0])) // 2, H // 2 + 90), sub,
                  fill=accent, font=f_sub)

    if subtitle:
        bb = draw.textbbox((0, 0), subtitle, font=f_meta)
        draw.text(((W - (bb[2] - bb[0])) // 2, H - 80), subtitle,
                  fill=(160, 168, 180), font=f_meta)

    im.save(out_path, "PNG", optimize=True)


def fit_screenshot(src_path, out_path, caption=None, bg_color=(12, 14, 18)):
    """Fit a screenshot inside 1920x1080 on a dark stage with a caption strip."""
    bg = Image.new("RGB", (W, H), bg_color)
    src = Image.open(src_path).convert("RGB")
    target_h = H - 110  # reserve bottom strip for caption
    target_w = W - 80
    ratio = min(target_w / src.width, target_h / src.height)
    nw, nh = int(src.width * ratio), int(src.height * ratio)
    src_r = src.resize((nw, nh), Image.LANCZOS)
    x = (W - nw) // 2
    y = (target_h - nh) // 2 + 10
    bg.paste(src_r, (x, y))

    if caption:
        draw = ImageDraw.Draw(bg)
        f = first_existing_font(FONT_CANDIDATES_SEMIBOLD, 28)
        bb = draw.textbbox((0, 0), caption, font=f)
        draw.text(((W - (bb[2] - bb[0])) // 2, H - 75), caption,
                  fill=(230, 235, 245), font=f)

    bg.save(out_path, "PNG", optimize=True)


def build_video(scenes, out_mp4, work_dir):
    """scenes: list of (image_path, duration_sec). Build an MP4 via ffmpeg concat."""
    list_file = Path(work_dir) / "_concat.txt"
    with list_file.open("w", encoding="utf-8") as f:
        for img, dur in scenes:
            p = str(Path(img).resolve()).replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{p}'\n")
            f.write(f"duration {dur}\n")
        last = str(Path(scenes[-1][0]).resolve()).replace("\\", "/").replace("'", "'\\''")
        f.write(f"file '{last}'\n")  # last frame held

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264",
        "-vf", f"fps={FPS},format=yuv420p",
        "-fps_mode", "cfr",
        "-movflags", "+faststart",
        str(out_mp4),
    ]
    print("Running:", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ffmpeg STDERR:", r.stderr[-2000:], file=sys.stderr)
        raise SystemExit(1)
    print(f"Wrote {out_mp4} ({Path(out_mp4).stat().st_size // 1024} KB)")


# ---- Spec driver ---------------------------------------------------------


def render_from_spec(spec: dict, work_dir: Path, spec_dir: Path = None) -> Path:
    work_dir.mkdir(parents=True, exist_ok=True)
    spec_dir = Path(spec_dir) if spec_dir is not None else Path.cwd()
    palette = spec.get("palette", {})
    accent = hex_to_rgb(palette.get("accent", "#6FFFB8"))
    bg = hex_to_rgb(palette.get("bg", "#0F1115"))

    scenes: list[tuple] = []

    # Title card
    title = spec.get("title", {})
    title_png = work_dir / "00_title.png"
    make_card(title.get("lines", ["Walkthrough"]), accent, title_png,
              subtitle=title.get("subtitle"), bg_color=bg)
    scenes.append((title_png, 2.5))

    # Scenes
    for i, scene in enumerate(spec.get("scenes", []), start=1):
        img = scene.get("image")
        if not img:
            raise SystemExit("scene {}: missing required 'image' field".format(i))
        img_path = Path(img)
        if not img_path.is_absolute():
            img_path = spec_dir / img_path  # resolve relative to the spec file
        if not img_path.exists():
            raise SystemExit(
                "scene {}: screenshot not found: {}".format(i, img_path)
            )
        out = work_dir / f"{i:02d}_scene.png"
        fit_screenshot(img_path, out, caption=scene.get("caption"), bg_color=bg)
        scenes.append((out, float(scene.get("duration", 5))))

    # Outro card
    outro = spec.get("outro")
    if outro:
        outro_png = work_dir / "99_outro.png"
        make_card(outro.get("lines", ["Thanks"]), accent, outro_png,
                  subtitle=outro.get("subtitle"), bg_color=bg)
        scenes.append((outro_png, 3))

    out_mp4 = Path(spec.get("output", "walkthrough.mp4"))
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    build_video(scenes, out_mp4, work_dir)
    return out_mp4


# ---- CLI -----------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--spec", help="Path to a JSON spec file")
    p.add_argument("--work-dir", default="_walkthrough_frames",
                   help="Scratch dir for rendered frames")
    p.add_argument("--demo", action="store_true",
                   help="Render a demo video using synthetic title/outro cards (no screenshots needed)")
    args = p.parse_args()

    if not shutil.which("ffmpeg"):
        print("ERROR: ffmpeg not found on PATH. Install ffmpeg and try again.",
              file=sys.stderr)
        return 1

    if args.demo:
        work = Path(args.work_dir)
        work.mkdir(parents=True, exist_ok=True)
        accent = hex_to_rgb("#6FFFB8")
        bg = hex_to_rgb("#0F1115")
        t = work / "00_title.png"
        o = work / "99_outro.png"
        make_card(["Demo Project", "What it does in one line"], accent, t,
                  subtitle="Detail one  ·  Detail two  ·  Detail three", bg_color=bg)
        make_card(["Built by", "Your Name"], accent, o,
                  subtitle="yourdomain.com  ·  linkedin.com/in/you", bg_color=bg)
        build_video([(t, 2.5), (o, 3)], "demo_walkthrough.mp4", work)
        return 0

    if not args.spec:
        print("Provide --spec <file.json> or --demo. See --help.", file=sys.stderr)
        return 1

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    render_from_spec(spec, Path(args.work_dir), spec_dir=spec_path.parent)
    return 0


if __name__ == "__main__":
    sys.exit(main())
