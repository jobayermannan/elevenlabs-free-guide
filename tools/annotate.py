"""Draws step markers on the Hacktoberfest / MyMLH / GitHub screenshots.

Run:  python tools/annotate.py
Reads assets/<n>.png (the raw screenshots) and writes assets/step-*.png.
Also redacts the personal email and password visible in the GitHub signup shot.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

PURPLE = (139, 60, 246)
CYAN = (34, 230, 247)
INK = (14, 16, 32)
WHITE = (255, 255, 255)

FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
BN_FONT_PATH = "C:/Windows/Fonts/Nirmala.ttc"  # has Bangla glyphs; Arial does not


def font(size: int, bangla=False) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(BN_FONT_PATH if bangla else FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


def box(draw: ImageDraw.ImageDraw, xy, color=PURPLE, radius=10, width=4):
    """A marker box with a white halo so it reads on light and dark pages."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle((x0 - 3, y0 - 3, x1 + 3, y1 + 3), radius + 3, outline=WHITE, width=width + 3)
    draw.rounded_rectangle(xy, radius, outline=color, width=width)


def badge(draw: ImageDraw.ImageDraw, center, label: str, color=PURPLE, r=26):
    cx, cy = center
    draw.ellipse((cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3), fill=WHITE)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    f = font(int(r * 1.15))
    draw.text((cx, cy + 1), label, font=f, fill=WHITE, anchor="mm")


def redact(draw: ImageDraw.ImageDraw, xy, label="গোপন রাখা হয়েছে"):
    draw.rounded_rectangle(xy, 8, fill=INK)
    x0, y0, x1, y1 = xy
    draw.text(((x0 + x1) / 2, (y0 + y1) / 2), label, font=font(20, bangla=True), fill=(150, 160, 190), anchor="mm")


def open_shot(name: str, crop=None) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Opens a raw screenshot. `crop` is in the raw image's own coordinates;
    marker coordinates below are relative to the cropped image."""
    im = Image.open(ASSETS / name).convert("RGB")
    if crop:
        im = im.crop(crop)
    return im, ImageDraw.Draw(im)


def save(im: Image.Image, name: str, max_w=1400):
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(ASSETS / name, optimize=True)
    print(name, im.size)


# --- Step 1: the promos URL + My Hacktoberfest button -----------------------
im, d = open_shot("1.png")
# The bookmarks bar and the profile avatar are the screenshot owner's own
# business, so they are painted over before this goes public.
d.rectangle((0, 90, im.width, 134), fill=(32, 33, 36))
d.ellipse((1800, 40, 1834, 74), fill=(32, 33, 36))
box(d, (180, 30, 560, 78), CYAN)
badge(d, (608, 54), "1", PURPLE)
box(d, (1500, 168, 1735, 222), CYAN)
badge(d, (1790, 195), "2", PURPLE)
save(im, "step-1-promos.png")

# --- Step 2: the ElevenLabs card and its two requirements -------------------
# Cropped to the ElevenLabs card so the neighbouring cards don't confuse anyone.
im, d = open_shot("2.png", crop=(0, 120, 1476, 480))
box(d, (1030, 42, 1232, 98))
badge(d, (1288, 70), "1")
box(d, (188, 224, 655, 254))
badge(d, (700, 239), "2")
box(d, (188, 259, 708, 289))
badge(d, (753, 274), "3")
save(im, "step-2-elevenlabs.png")

# --- Step 3: MyMLH phone verification ---------------------------------------
im, d = open_shot("3.png")
box(d, (925, 85, 1080, 132))
badge(d, (1123, 108), "1")
save(im, "step-3-phone.png")

# --- Step 4: MyMLH GitHub connection ----------------------------------------
im, d = open_shot("4.png")
box(d, (998, 363, 1152, 408))
badge(d, (1196, 385), "1")
box(d, (933, 420, 1143, 458))
badge(d, (1187, 439), "2")
save(im, "step-4-github-connect.png")

# --- Step 5: GitHub signup (personal details redacted) ----------------------
im, d = open_shot("5.png", crop=(214, 0, 1165, 838))
redact(d, (123, 596, 825, 642))
redact(d, (123, 780, 825, 826))
box(d, (123, 250, 825, 294), CYAN)
badge(d, (876, 272), "1", PURPLE)
box(d, (123, 474, 825, 521), CYAN)
badge(d, (876, 497), "2", PURPLE)
save(im, "step-5-github-signup.png")
