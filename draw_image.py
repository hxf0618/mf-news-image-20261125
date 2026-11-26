#!/usr/bin/env python3
"""Draw the front page of 25 November 2026's world news in one image.

Loads base.png (the AI-drawn four-panel illustration), overlays a
masthead, a headline, four short news lines and a footer, and writes
entry.png (1024x1024, under 1 MiB).
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(HERE, "base.png")
OUT_PATH = os.path.join(HERE, "entry.png")

SIZE = 1024
MAX_BYTES = 1048576

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MASTHEAD = "25 NOVEMBER 2026"
HEADLINE = "THE WORLD IN ONE DAY"
LINES = [
    "HORMUZ TANKERS MINED \u2014 TWO SHIPS ABLAZE",
    "HOUTHIS STRIKE SAUDI REFINERY",
    "HUAWEI CONVICTED IN U.S. COURT",
    "FIRST FOREIGN ASTRONAUT ABOARD CHINA STATION",
]
FOOTER = "make.fun news-image"


def fit_font(path, size, text, max_width):
    """Largest font size <= size that fits text within max_width."""
    size = int(size)
    while size > 8:
        font = ImageFont.truetype(path, size)
        if font.getlength(text) <= max_width:
            return font
        size -= 1
    return ImageFont.truetype(path, size)


def draw():
    base = Image.open(BASE_PATH).convert("RGB")
    base = base.resize((SIZE, SIZE), Image.LANCZOS)

    img = base.copy()
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    ink = (245, 238, 220)      # warm paper white
    gold = (232, 178, 74)      # headline gold
    red = (198, 52, 40)        # bullet red

    # --- top band: masthead + headline -------------------------------
    draw.rectangle([0, 0, SIZE, 168], fill=(8, 10, 16, 178))
    draw.rectangle([0, 168, SIZE, 172], fill=(232, 178, 74, 255))

    mast_font = fit_font(SERIF_BOLD, 62, MASTHEAD, SIZE - 80)
    w = mast_font.getlength(MASTHEAD)
    draw.text(((SIZE - w) / 2, 18), MASTHEAD, font=mast_font, fill=ink + (255,))

    head_font = fit_font(SERIF_BOLD, 46, HEADLINE, SIZE - 80)
    w = head_font.getlength(HEADLINE)
    draw.text(((SIZE - w) / 2, 96), HEADLINE, font=head_font, fill=gold + (255,))

    # --- bottom band: four news lines + footer ------------------------
    draw.rectangle([0, 792, SIZE, SIZE], fill=(8, 10, 16, 200))
    draw.rectangle([0, 792, SIZE, 796], fill=(232, 178, 74, 255))

    line_font = fit_font(SANS_BOLD, 31, max(LINES, key=len), SIZE - 110)
    y = 812
    for line in LINES:
        draw.rectangle([44, y + 8, 62, y + 26], fill=red + (255,))
        draw.text((78, y), line, font=line_font, fill=ink + (255,))
        y += 44

    foot_font = ImageFont.truetype(SANS, 22)
    fw = foot_font.getlength(FOOTER)
    draw.text((SIZE - fw - 36, SIZE - 34), FOOTER, font=foot_font,
              fill=(180, 175, 160, 255))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img


def save(img):
    """Save as PNG; quantize to a 256-colour palette if over 1 MiB."""
    img.save(OUT_PATH, format="PNG", optimize=True)
    if os.path.getsize(OUT_PATH) <= MAX_BYTES:
        return
    pal = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    pal.save(OUT_PATH, format="PNG", optimize=True)
    if os.path.getsize(OUT_PATH) > MAX_BYTES:
        raise SystemExit(
            "entry.png still over 1 MiB: %d bytes" % os.path.getsize(OUT_PATH)
        )


def main():
    img = draw()
    save(img)
    print("wrote %s (%dx%d, %d bytes)"
          % (OUT_PATH, SIZE, SIZE, os.path.getsize(OUT_PATH)))


if __name__ == "__main__":
    main()
