import json
from datetime import date, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "aktualne.json"
BACKGROUND_FILE = ROOT / "assets" / "images" / "social-background.png"
LOGO_FILE = ROOT / "assets" / "logo" / "vitability-v.png"

OUTPUT_DIR = ROOT / "social"
OUTPUT_FILE = OUTPUT_DIR / "aktualne-reel.png"


WIDTH = 1080
HEIGHT = 1920
MARGIN_X = 90


BG = "#F7F4ED"
DEEP = "#385D62"
PRIMARY = "#607D8B"
SAGE = "#91A68C"
TEXT = "#28302F"
MUTED = "#66706D"
ACCENT = "#C9826B"


def load_font(size, bold=False):
    if bold:
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


FONT_SITE = load_font(34, bold=True)
FONT_TITLE = load_font(58, bold=True)
FONT_WEEK = load_font(30)
FONT_DAY = load_font(30, bold=True)
FONT_TIME = load_font(42, bold=True)
FONT_NAME = load_font(40, bold=True)
FONT_PLACE = load_font(28)
FONT_NOTE = load_font(26, bold=True)


MONTHS = [
    "január",
    "február",
    "marec",
    "apríl",
    "máj",
    "jún",
    "júl",
    "august",
    "september",
    "október",
    "november",
    "december",
]


def next_week_text():
    today = date.today()

    this_monday = today - timedelta(days=today.weekday())
    monday = this_monday + timedelta(days=7)
    sunday = monday + timedelta(days=6)

    if monday.month == sunday.month:
        return (
            f"{monday.day}. – {sunday.day}. "
            f"{MONTHS[sunday.month - 1]} {sunday.year}"
        )

    return (
        f"{monday.day}. {MONTHS[monday.month - 1]} – "
        f"{sunday.day}. {MONTHS[sunday.month - 1]} "
        f"{sunday.year}"
    )


with DATA_FILE.open("r", encoding="utf-8") as file:
    data = json.load(file)

lessons = data.get("lessons", [])


# --------------------------------------------------
# Pozadie
# --------------------------------------------------

if BACKGROUND_FILE.exists():
    image = Image.open(BACKGROUND_FILE).convert("RGBA")

    if image.size != (WIDTH, HEIGHT):
        image = image.resize(
            (WIDTH, HEIGHT),
            Image.Resampling.LANCZOS
        )

else:
    image = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        BG
    )


draw = ImageDraw.Draw(image)


# --------------------------------------------------
# Logo + vitability.sk
# --------------------------------------------------

header_y = 85
logo_height = 85
site_x = MARGIN_X

if LOGO_FILE.exists():
    logo = Image.open(LOGO_FILE).convert("RGBA")

    ratio = logo_height / logo.height
    logo_width = int(logo.width * ratio)

    logo = logo.resize(
        (logo_width, logo_height),
        Image.Resampling.LANCZOS
    )

    image.alpha_composite(
        logo,
        (MARGIN_X, header_y)
    )

    site_x = MARGIN_X + logo_width + 24


draw.text(
    (site_x, header_y + 22),
    "vitability.sk",
    font=FONT_SITE,
    fill=DEEP
)


# --------------------------------------------------
# Nadpis
# --------------------------------------------------

title_y = 245

draw.text(
    (MARGIN_X, title_y),
    "Aktuálne hodiny",
    font=FONT_TITLE,
    fill=DEEP
)

week_y = title_y + 82

draw.text(
    (MARGIN_X, week_y),
    next_week_text(),
    font=FONT_WEEK,
    fill=PRIMARY
)

line_y = week_y + 62

draw.line(
    (
        MARGIN_X,
        line_y,
        WIDTH - MARGIN_X,
        line_y
    ),
    fill=SAGE,
    width=4
)


# --------------------------------------------------
# Adaptívna veľkosť kariet
# --------------------------------------------------

count = len(lessons)

if count <= 2:
    card_height = 300
    gap = 42

elif count <= 4:
    card_height = 250
    gap = 30

elif count <= 6:
    card_height = 205
    gap = 22

else:
    card_height = 170
    gap = 18


# --------------------------------------------------
# Pozícia kariet
# --------------------------------------------------

content_top = line_y + 70

y = content_top


# --------------------------------------------------
# Karty
# --------------------------------------------------

for lesson in lessons:
    day = lesson.get("day", "")
    time = lesson.get("time", "")
    name = lesson.get("name", "")
    place = lesson.get("place", "")
    note = lesson.get("note", "")

    card_left = MARGIN_X
    card_top = int(y)
    card_right = WIDTH - MARGIN_X
    card_bottom = card_top + card_height

    shadow_offset = 4

    draw.rounded_rectangle(
        (
            card_left,
            card_top + shadow_offset,
            card_right,
            card_bottom + shadow_offset
        ),
        radius=34,
        fill=(40, 48, 47, 10)
    )

    draw.rounded_rectangle(
        (
            card_left,
            card_top,
            card_right,
            card_bottom
        ),
        radius=34,
        fill=(255, 255, 255, 238)
    )

    content_x = card_left + 50
    content_y = card_top + 36

    draw.text(
        (content_x, content_y),
        day.upper(),
        font=FONT_DAY,
        fill=PRIMARY
    )

    time_bbox = draw.textbbox(
        (0, 0),
        time,
        font=FONT_TIME
    )

    time_width = time_bbox[2] - time_bbox[0]

    draw.text(
        (
            card_right - 50 - time_width,
            content_y - 5
        ),
        time,
        font=FONT_TIME,
        fill=DEEP
    )

    content_y += 66

    draw.text(
        (content_x, content_y),
        name,
        font=FONT_NAME,
        fill=TEXT
    )

    content_y += 60

    draw.text(
        (content_x, content_y),
        place,
        font=FONT_PLACE,
        fill=MUTED
    )

    if note:
        content_y += 46

        draw.text(
            (content_x, content_y),
            note,
            font=FONT_NOTE,
            fill=ACCENT
        )

    y += card_height + gap


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

image = image.convert("RGB")

image.save(
    OUTPUT_FILE,
    "PNG",
    optimize=True
)

print()
print("Hotovo.")
print(f"Vytvorené: {OUTPUT_FILE}")
print(f"Týždeň: {next_week_text()}")
print(f"Počet lekcií: {len(lessons)}")