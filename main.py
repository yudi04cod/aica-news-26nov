#!/usr/bin/env python3
"""News-image entry for 26 November 2026.

Draws a newspaper front page (1024x1024) summing up Thursday
26 November 2026 with Pillow only. No network, no randomness,
no clock: the same bytes come out of every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (24, 24, 22)
RED = (158, 28, 32)
GREY = (96, 92, 84)
LIGHT = (226, 219, 203)
SKY = (58, 74, 96)
SKY_DARK = (38, 50, 68)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=1.28):
    """Draw a wrapped paragraph; returns the y just below it."""
    size = fnt.size
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def headline(draw, x, y, width, text, fnt, fill=INK, leading=1.02):
    size = fnt.size
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, size=17):
    f = font(SANS_B, size)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + size + 4


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 132], fill=INK)
    draw.text((512, 12), "THE WORLD TODAY", font=font(SERIF_B, 54),
              fill=PAPER, anchor="ma")
    draw.text((512, 78), "THURSDAY  26  NOVEMBER  2026",
              font=font(SANS_B, 22), fill=(232, 214, 170), anchor="ma")
    draw.text((512, 106), "One day's news, in one page  \u2022  No. 330",
              font=font(SANS, 14), fill=(200, 196, 186), anchor="ma")


def draw_lead_panel(draw, x, y, w, h):
    """Dusk skyline under missile streaks, with the toll as a figure.
    The bottom 52 px are a black caption bar; the skyline rises above it."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY_DARK)
    cap_top = y + h - 52
    # stars
    for sx, sy in [(30, 14), (90, 30), (150, 12), (210, 28), (260, 16),
                   (320, 32), (370, 14), (410, 30), (60, 48), (300, 50)]:
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                     fill=(220, 220, 200))
    # missile streaks, kept in the sky above the caption bar
    draw.line([(x + 40, y + 58), (x + 130, y + 14)], fill=(255, 190, 90), width=4)
    draw.line([(x + 330, y + 62), (x + 400, y + 22)], fill=(255, 190, 90), width=4)
    draw.ellipse([x + 126, y + 10, x + 134, y + 18], fill=(255, 220, 140))
    draw.ellipse([x + 396, y + 18, x + 404, y + 26], fill=(255, 220, 140))
    # skyline silhouette rising above the caption bar
    blocks = [(0, 60, 34), (62, 56, 24), (120, 70, 44),
              (192, 50, 28), (244, 66, 38), (312, 54, 22),
              (368, 58, 32), (428, 46, 18), (476, 62, 40),
              (540, 52, 26)]
    for bx, bw, bh in blocks:
        draw.rectangle([x + bx, cap_top - bh, x + bx + bw, cap_top],
                       fill=(16, 20, 28))
        for wy in range(cap_top - bh + 8, cap_top - 6, 16):
            for wx in range(x + bx + 8, x + bx + bw - 6, 15):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 200, 90))
    # blast glow at the foot of the skyline, left
    draw.ellipse([x + 6, cap_top - 16, x + 70, cap_top + 8], fill=(255, 120, 40))
    draw.ellipse([x + 20, cap_top - 8, x + 56, cap_top + 4], fill=(255, 200, 90))
    # toll caption bar
    draw.rectangle([x, cap_top, x + w, y + h], fill=(0, 0, 0))
    draw.text((x + 14, cap_top + 8), "490,334  RUSSIAN SOLDIERS DEAD",
              font=font(SANS_B, 26), fill=(255, 255, 255))


def draw_lead(draw):
    x, y, w = 32, 148, 620
    y = kicker(draw, x, y, "War in Ukraine  \u2022  The reckoning")
    y = headline(draw, x, y, w, "NEARLY HALF A MILLION DEAD",
                 font(SERIF_B, 46), leading=1.0)
    y = headline(draw, x, y, w, "RUSSIA'S OWN FIGURES TELL THE TOLL",
                 font(SERIF_B, 27), leading=1.05)
    y += 6
    y = para(draw, x, y, w,
             "Leaked statistics from Russia's own agency, analysed by the "
             "BBC, count at least 490,334 Russian soldiers killed since the "
             "invasion of Ukraine began in 2022. Experts say the true toll "
             "may run past 600,000.",
             font(SERIF, 19))
    y += 4
    y = para(draw, x, y, w,
             "Kyiv was hit by ballistic missiles as Ukraine says it struck "
             "a Russian air base, damaging five planes.",
             font(SERIF, 19))
    draw_lead_panel(draw, x, y + 8, w, 118)
    return y + 8 + 118


def draw_courthouse(draw, x, y, w, h):
    """Simple courthouse: pediment, columns, steps."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 206, 188))
    # pediment
    draw.polygon([(x + 10, y + 58), (x + w / 2, y + 10), (x + w - 10, y + 58)],
                 fill=(120, 110, 96))
    draw.rectangle([x + 10, y + 58, x + w - 10, y + 68], fill=INK)
    for i in range(4):
        cx = x + 34 + i * ((w - 68) / 3)
        draw.rectangle([cx - 11, y + 68, cx + 11, y + h - 26], fill=(245, 240, 228))
        draw.rectangle([cx - 14, y + 64, cx + 14, y + 70], fill=(245, 240, 228))
        draw.rectangle([cx - 14, y + h - 30, cx + 14, y + h - 24], fill=(245, 240, 228))
    draw.rectangle([x + 6, y + h - 22, x + w - 6, y + h - 16], fill=INK)
    draw.rectangle([x + 2, y + h - 14, x + w - 2, y + h - 8], fill=INK)
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=INK)


def draw_right_column(draw):
    x, y, w = 684, 148, 308
    y = kicker(draw, x, y, "United States  \u2022  The courts")
    y = headline(draw, x, y, w, "JUDGE BLOCKS SECOND BIRTHRIGHT ORDER",
                 font(SERIF_B, 32), leading=1.02)
    y += 6
    y = para(draw, x, y, w,
             "A federal judge in Washington has halted President Trump's "
             "second order denying citizenship to some US-born babies \u2014 "
             "the children of foreign workers.",
             font(SERIF, 18))
    y += 4
    y = para(draw, x, y, w,
             "\u201cThe President cannot carve out new exceptions to "
             "birthright citizenship,\u201d Judge Cooper wrote.",
             font(SERIF, 18))
    draw_courthouse(draw, x, y + 8, w, 118)
    return y + 8 + 118


def draw_storm_panel(draw, x, y, w, h):
    """Rainy New York skyline with a grounded parade balloon.
    The bottom 26 px are a black caption bar."""
    draw.rectangle([x, y, x + w, y + h], fill=(70, 88, 110))
    base = y + h
    cap_top = base - 26
    # skyline, rising above the caption bar
    for bx, bw, bh in [(0, 90, 40), (96, 70, 54), (172, 80, 44),
                       (258, 64, 58), (328, 90, 48), (424, 76, 60),
                       (506, 90, 42), (602, 70, 54), (678, 80, 46),
                       (764, 90, 56), (860, 100, 44)]:
        if bx + bw > w:
            bw = w - bx
        draw.rectangle([x + bx, cap_top - bh, x + bx + bw, cap_top],
                       fill=(30, 40, 56))
    # balloon, drooping low between towers
    cx, cy = x + 300, y + 34
    draw.ellipse([cx - 62, cy - 26, cx + 62, cy + 26], fill=(214, 60, 60))
    draw.ellipse([cx - 40, cy - 32, cx + 40, cy + 32], fill=(232, 90, 70))
    draw.polygon([(cx - 62, cy), (cx - 80, cy + 36), (cx - 40, cy + 20)],
                 fill=(214, 60, 60))
    draw.polygon([(cx + 62, cy), (cx + 80, cy + 36), (cx + 40, cy + 20)],
                 fill=(214, 60, 60))
    draw.text((cx, cy - 8), "100th", font=font(SANS_B, 20), fill=(255, 255, 255),
              anchor="mm")
    # ropes to the street
    draw.line([(cx - 28, cy + 28), (cx - 48, cap_top - 2)], fill=(240, 240, 230), width=2)
    draw.line([(cx + 28, cy + 28), (cx + 48, cap_top - 2)], fill=(240, 240, 230), width=2)
    # rain
    for rx in range(12, w, 34):
        for ry in range(6, h - 30, 40):
            draw.line([(x + rx, y + ry), (x + rx - 7, y + ry + 13)],
                      fill=(200, 214, 228), width=2)
    draw.rectangle([x, cap_top, x + w, base], fill=(0, 0, 0))
    draw.text((x + 12, cap_top + 3), "NO PARADE TODAY \u2014 MOVED TO SATURDAY 28 NOV",
              font=font(SANS_B, 18), fill=(255, 255, 255))


def draw_storm(draw, top):
    x, y, w = 32, top, 960
    rule(draw, x, y, x + w, width=3)
    y += 10
    y = kicker(draw, x, y, "Thanksgiving  \u2022  New York")
    y = headline(draw, x, y, w, "A STORM STEALS THANKSGIVING",
                 font(SERIF_B, 34), leading=1.0)
    y += 4
    y = para(draw, x, y, w,
             "The 100th Macy's Thanksgiving Day Parade is postponed for the "
             "first time ever by weather, as a coastal storm lashes New York "
             "with rain and gusts too strong for the balloons. It marches "
             "instead on Saturday.",
             font(SERIF, 18))
    draw_storm_panel(draw, x, y + 6, w, 92)
    return y + 6 + 92


def small_story(draw, x, y, w, kick, head, body, head_size=21):
    y = kicker(draw, x, y, kick, size=14)
    y = headline(draw, x, y, w, head, font(SERIF_B, head_size), leading=1.02)
    y += 4
    y = para(draw, x, y, w, body, font(SERIF, 16))
    return y


def draw_bottom(draw, top):
    x, y, w = 32, top, 960
    rule(draw, x, y, x + w, width=3)
    y += 10
    col = 308
    small_story(draw, x, y, col, "Colombia  \u2022  Ten years on",
                "PEACE, A DECADE ON",
                "The UN marks ten years since Colombia's peace accord \u2014 "
                "progress praised, promises still unkept.")
    small_story(draw, x + col + 18, y, col, "Health  \u2022  Africa",
                "EBOLA PATIENT GOES HOME",
                "Kenya discharges its last Ebola patient as the DR Congo "
                "toll passes 5,300.")
    small_story(draw, x + 2 * (col + 18), y, col, "Also today",
                "IN BRIEF",
                "Cairo: 31 die in a tanker fire. Nigeria: militants kill "
                "30. N. Korea expels a Swiss diplomat.")


def draw_footer(draw):
    rule(draw, 32, 1000, 992, width=2)
    draw.text((512, 1006), "THURSDAY 26 NOVEMBER 2026  \u2022  THE WORLD TODAY",
              font=font(SANS_B, 14), fill=GREY, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    lead_bottom = draw_lead(d)
    right_bottom = draw_right_column(d)
    storm_bottom = draw_storm(d, max(lead_bottom, right_bottom) + 10)
    draw_bottom(d, storm_bottom + 8)
    draw_footer(d)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img.save(os.path.join(outdir, "entry.png"), "PNG", optimize=True)


if __name__ == "__main__":
    main()
