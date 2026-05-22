#!/usr/bin/env python3
"""
Animal Coloring Book PDF Generator
- Page 1: Full-color cover page
- Pages 2-21: 20 unique animals as black & white line-art coloring pages
"""

import math
from fpdf import FPDF


class AnimalBook(FPDF):
    def header(self):
        pass

    def footer(self):
        if self.page_no() == 1:
            return  # No footer on cover
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no() - 1} of 20", align="C")
        self.set_text_color(0, 0, 0)


# ─── DRAWING HELPERS ──────────────────────────────────────────────────────────

def star(pdf, cx, cy, r1, r2=None, points=5):
    if r2 is None:
        r2 = r1 * 0.45
    pts = []
    for i in range(points * 2):
        a = math.radians(-90 + i * 180 / points)
        r = r1 if i % 2 == 0 else r2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pdf.polygon(pts, style="D")


def smile(pdf, cx, cy, w, h):
    """Draw a smile arc."""
    pdf.arc(cx, cy, w, h, 0, 180, style="D")


def eye(pdf, cx, cy, r=2, pupil=True):
    """Draw a simple eye."""
    pdf.circle(cx, cy, r, style="D")
    if pupil:
        pdf.circle(cx, cy, r * 0.4, style="DF")



# ─── COVER PAGE (FULL COLOR) ─────────────────────────────────────────────────

def draw_cover(pdf):
    """Colorful cover page with title and animal illustrations."""
    # Background border (rainbow)
    colors = [(255, 100, 100), (255, 180, 80), (255, 230, 80),
              (130, 220, 130), (100, 180, 255), (180, 130, 230)]
    pdf.set_line_width(2)
    for i, c in enumerate(colors):
        pdf.set_draw_color(*c)
        pdf.rect(8 + i * 1.5, 8 + i * 1.5,
                 210 - 16 - i * 3, 297 - 16 - i * 3, style="D")

    # Title banner background
    pdf.set_fill_color(255, 220, 100)
    pdf.set_draw_color(50, 50, 50)
    pdf.set_line_width(0.8)
    pdf.rect(20, 28, 170, 35, style="DF")

    # Title text
    pdf.set_text_color(200, 50, 50)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_xy(20, 32)
    pdf.cell(170, 12, "MY AMAZING", align="C")
    pdf.set_xy(20, 44)
    pdf.cell(170, 12, "ANIMAL COLORING BOOK", align="C")

    # Subtitle
    pdf.set_text_color(70, 130, 70)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(20, 70)
    pdf.cell(170, 10, "* 20 Fun Animals to Color! *", align="C")

    # Cover animals (colored)
    cover_animals(pdf)

    # Footer
    pdf.set_text_color(100, 100, 200)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_xy(20, 250)
    pdf.cell(170, 8, "This book belongs to:", align="C")

    pdf.set_draw_color(50, 50, 50)
    pdf.set_line_width(0.5)
    pdf.line(60, 265, 150, 265)

    pdf.set_text_color(80, 80, 80)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_xy(20, 275)
    pdf.cell(170, 6, "Grab your crayons and let's color!", align="C")



def cover_animals(pdf):
    """Draw small colored animals on the cover."""
    # Lion (orange/yellow)
    pdf.set_fill_color(255, 180, 60)
    pdf.set_draw_color(80, 40, 0)
    pdf.set_line_width(0.5)
    cx, cy = 50, 110
    # Mane rays
    for i in range(12):
        a = math.radians(i * 30)
        x1 = cx + 10 * math.cos(a)
        y1 = cy + 10 * math.sin(a)
        x2 = cx + 18 * math.cos(a)
        y2 = cy + 18 * math.sin(a)
        pdf.line(x1, y1, x2, y2)
    pdf.circle(cx, cy, 14, style="DF")
    pdf.set_fill_color(255, 220, 150)
    pdf.circle(cx, cy + 1, 9, style="DF")
    # Eyes & nose
    pdf.set_fill_color(0, 0, 0)
    pdf.circle(cx - 3, cy - 2, 1.2, style="DF")
    pdf.circle(cx + 3, cy - 2, 1.2, style="DF")
    pdf.polygon([(cx - 1.5, cy + 1), (cx + 1.5, cy + 1), (cx, cy + 3)], style="DF")

    # Elephant (gray)
    pdf.set_fill_color(170, 170, 180)
    pdf.set_draw_color(60, 60, 70)
    cx, cy = 105, 110
    pdf.ellipse(cx - 18, cy - 8, 30, 22, style="DF")  # body
    pdf.ellipse(cx + 8, cy - 13, 14, 14, style="DF")  # head
    pdf.ellipse(cx + 4, cy - 16, 8, 8, style="DF")    # ear
    # Trunk
    pdf.set_line_width(3)
    pdf.line(cx + 18, cy - 8, cx + 22, cy)
    pdf.line(cx + 22, cy, cx + 18, cy + 6)
    pdf.set_line_width(0.5)
    # Legs
    pdf.rect(cx - 15, cy + 12, 5, 8, style="DF")
    pdf.rect(cx + 5, cy + 12, 5, 8, style="DF")
    # Eye
    pdf.set_fill_color(0, 0, 0)
    pdf.circle(cx + 12, cy - 13, 1, style="DF")

    # Butterfly (purple/pink)
    pdf.set_fill_color(230, 130, 200)
    pdf.set_draw_color(80, 30, 80)
    cx, cy = 160, 110
    pdf.ellipse(cx - 12, cy - 10, 12, 10, style="DF")
    pdf.ellipse(cx, cy - 10, 12, 10, style="DF")
    pdf.set_fill_color(180, 100, 220)
    pdf.ellipse(cx - 10, cy + 2, 9, 8, style="DF")
    pdf.ellipse(cx + 1, cy + 2, 9, 8, style="DF")
    # Body
    pdf.set_fill_color(80, 30, 80)
    pdf.ellipse(cx - 1, cy - 8, 3, 16, style="DF")
    # Antennae
    pdf.line(cx, cy - 10, cx - 3, cy - 16)
    pdf.line(cx, cy - 10, cx + 3, cy - 16)



    # Fish (blue)
    pdf.set_fill_color(100, 180, 240)
    pdf.set_draw_color(20, 60, 120)
    cx, cy = 65, 175
    pdf.ellipse(cx - 12, cy - 7, 24, 14, style="DF")
    pdf.polygon([(cx - 12, cy), (cx - 20, cy - 6), (cx - 20, cy + 6)], style="DF")
    pdf.set_fill_color(0, 0, 0)
    pdf.circle(cx + 6, cy - 1, 1.3, style="DF")
    # Bubbles
    pdf.set_fill_color(200, 230, 255)
    pdf.circle(cx + 14, cy - 8, 2, style="DF")
    pdf.circle(cx + 18, cy - 12, 1.5, style="DF")

    # Turtle (green)
    pdf.set_fill_color(120, 200, 100)
    pdf.set_draw_color(40, 80, 30)
    cx, cy = 130, 175
    pdf.ellipse(cx - 14, cy - 7, 26, 16, style="DF")
    pdf.set_fill_color(80, 160, 70)
    pdf.circle(cx + 10, cy, 5, style="DF")  # head
    # Shell pattern
    pdf.set_draw_color(40, 80, 30)
    pdf.line(cx - 8, cy, cx + 8, cy)
    pdf.line(cx, cy - 7, cx, cy + 7)
    pdf.set_fill_color(0, 0, 0)
    pdf.circle(cx + 12, cy - 1, 0.8, style="DF")

    # Bee (yellow/black)
    pdf.set_fill_color(255, 220, 50)
    pdf.set_draw_color(0, 0, 0)
    cx, cy = 175, 175
    pdf.ellipse(cx - 8, cy - 5, 16, 11, style="DF")
    # Stripes
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(cx - 5, cy - 5, 2, 11, style="F")
    pdf.rect(cx + 1, cy - 5, 2, 11, style="F")
    # Wings
    pdf.set_fill_color(220, 240, 255)
    pdf.set_draw_color(60, 100, 140)
    pdf.ellipse(cx - 5, cy - 12, 7, 6, style="DF")
    pdf.ellipse(cx, cy - 12, 7, 6, style="DF")

    # Stars in corners
    pdf.set_fill_color(255, 230, 80)
    pdf.set_draw_color(200, 150, 0)
    for sx, sy in [(25, 220), (185, 220), (25, 95), (185, 95)]:
        star_filled(pdf, sx, sy, 5)

    # Reset colors
    pdf.set_draw_color(0, 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.set_line_width(0.4)


def star_filled(pdf, cx, cy, r):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    pdf.polygon(pts, style="DF")



# ─── PAGE LAYOUT FOR B&W ANIMAL PAGES ────────────────────────────────────────

def page_header(pdf, animal_name, fact):
    """Add title and fun fact at top of each B&W page."""
    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)

    # Big animal name
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_xy(10, 12)
    pdf.cell(0, 14, animal_name.upper(), align="C")

    # Decorative underline
    pdf.set_line_width(0.6)
    pdf.line(60, 30, 150, 30)
    pdf.set_line_width(0.4)

    # Fun fact
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_xy(15, 32)
    pdf.multi_cell(180, 5, f"Fun fact: {fact}", align="C")


def page_border(pdf):
    """Decorative coloring-page border."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.6)
    pdf.rect(8, 8, 194, 281, style="D")
    pdf.set_line_width(0.3)
    pdf.rect(11, 11, 188, 275, style="D")
    pdf.set_line_width(0.4)


# ─── ANIMAL DRAWING FUNCTIONS (B&W LINE ART) ─────────────────────────────────

def draw_lion(pdf):
    cx, cy = 105, 160
    # Mane (sun rays)
    for i in range(20):
        a = math.radians(i * 18)
        x1 = cx + 38 * math.cos(a)
        y1 = cy + 38 * math.sin(a)
        x2 = cx + 50 * math.cos(a)
        y2 = cy + 50 * math.sin(a)
        pdf.line(x1, y1, x2, y2)
    # Outer mane circle (wavy)
    pts = []
    for i in range(36):
        a = math.radians(i * 10)
        r = 38 + 3 * math.sin(a * 5)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pdf.polygon(pts, style="D")
    # Face
    pdf.circle(cx, cy, 28, style="D")
    # Inner face
    pdf.ellipse(cx - 18, cy - 8, 36, 25, style="D")
    # Ears
    pdf.circle(cx - 22, cy - 22, 6, style="D")
    pdf.circle(cx + 22, cy - 22, 6, style="D")
    pdf.circle(cx - 22, cy - 22, 3, style="D")
    pdf.circle(cx + 22, cy - 22, 3, style="D")
    # Eyes
    eye(pdf, cx - 9, cy - 5, 3)
    eye(pdf, cx + 9, cy - 5, 3)
    # Nose
    pdf.polygon([(cx - 4, cy + 4), (cx + 4, cy + 4), (cx, cy + 9)], style="D")
    # Mouth
    pdf.line(cx, cy + 9, cx, cy + 13)
    pdf.arc(cx - 4, cy + 13, 8, 4, 180, 360, style="D")
    pdf.arc(cx + 4, cy + 13, 8, 4, 180, 360, style="D")
    # Whiskers
    for i in [-1, 0, 1]:
        pdf.line(cx - 8, cy + 10 + i * 2, cx - 22, cy + 7 + i * 4)
        pdf.line(cx + 8, cy + 10 + i * 2, cx + 22, cy + 7 + i * 4)



def draw_elephant(pdf):
    cx, cy = 105, 165
    # Body
    pdf.ellipse(cx - 35, cy - 15, 60, 45, style="D")
    # Head
    pdf.circle(cx + 28, cy - 5, 22, style="D")
    # Ear (big floppy)
    pdf.ellipse(cx + 18, cy - 25, 22, 28, style="D")
    pdf.ellipse(cx + 21, cy - 22, 16, 22, style="D")
    # Trunk (curved tube)
    trunk_pts = [(cx + 50, cy - 5), (cx + 60, cy + 5), (cx + 65, cy + 20),
                 (cx + 60, cy + 30), (cx + 55, cy + 32)]
    for i in range(len(trunk_pts) - 1):
        pdf.line(*trunk_pts[i], *trunk_pts[i+1])
    # Trunk underside
    trunk_pts2 = [(cx + 45, cy + 5), (cx + 53, cy + 12), (cx + 58, cy + 22),
                  (cx + 55, cy + 32)]
    for i in range(len(trunk_pts2) - 1):
        pdf.line(*trunk_pts2[i], *trunk_pts2[i+1])
    # Trunk wrinkles
    for i in range(4):
        x = cx + 50 + i * 3
        y = cy - 2 + i * 6
        pdf.line(x, y, x + 5, y + 2)
    # Tusk
    pdf.polygon([(cx + 44, cy + 8), (cx + 52, cy + 16), (cx + 46, cy + 12)], style="D")
    # Eye
    eye(pdf, cx + 30, cy - 8, 2.5)
    # Legs (chunky)
    pdf.rect(cx - 30, cy + 25, 12, 18, style="D")
    pdf.rect(cx - 12, cy + 25, 12, 18, style="D")
    pdf.rect(cx + 8, cy + 25, 12, 18, style="D")
    pdf.rect(cx + 22, cy + 25, 12, 18, style="D")
    # Toenails
    for lx in [cx - 30, cx - 12, cx + 8, cx + 22]:
        for i in range(3):
            pdf.circle(lx + 2 + i * 4, cy + 41, 1.2, style="D")
    # Tail
    pdf.line(cx - 35, cy + 5, cx - 45, cy + 15)
    pdf.line(cx - 45, cy + 15, cx - 47, cy + 18)
    # Tuft on tail
    pdf.line(cx - 47, cy + 18, cx - 50, cy + 22)
    pdf.line(cx - 47, cy + 18, cx - 44, cy + 22)



def draw_giraffe(pdf):
    cx = 105
    # Body (oval)
    pdf.ellipse(cx - 25, 175, 50, 35, style="D")
    # Long neck
    pdf.polygon([(cx + 5, 180), (cx + 22, 180), (cx + 28, 80), (cx + 12, 80)], style="D")
    # Head
    pdf.ellipse(cx + 5, 65, 28, 18, style="D")
    # Ears
    pdf.ellipse(cx + 6, 58, 5, 8, style="D")
    pdf.ellipse(cx + 25, 58, 5, 8, style="D")
    # Horns (ossicones)
    pdf.line(cx + 11, 60, cx + 10, 50)
    pdf.line(cx + 22, 60, cx + 23, 50)
    pdf.circle(cx + 10, 49, 2, style="D")
    pdf.circle(cx + 23, 49, 2, style="D")
    # Eye
    eye(pdf, cx + 18, 70, 2)
    # Mouth
    pdf.line(cx + 30, 73, cx + 33, 76)
    pdf.arc(cx + 28, 78, 8, 4, 0, 180, style="D")
    # Nostril
    pdf.circle(cx + 32, 72, 0.7, style="DF")
    # Mane (zigzag down neck)
    for i in range(10):
        y = 82 + i * 10
        pdf.line(cx + 13, y, cx + 9, y + 3)
        pdf.line(cx + 9, y + 3, cx + 14, y + 6)
    # Spots on body & neck
    spots = [(cx - 15, 175), (cx + 0, 178), (cx + 12, 185),
             (cx - 8, 195), (cx + 8, 200), (cx - 18, 200),
             (cx + 18, 100), (cx + 18, 120), (cx + 18, 140), (cx + 18, 160)]
    for sx, sy in spots:
        pdf.ellipse(sx, sy, 8, 6, style="D")
    # Legs
    pdf.rect(cx - 18, 205, 6, 35, style="D")
    pdf.rect(cx - 5, 205, 6, 35, style="D")
    pdf.rect(cx + 8, 205, 6, 35, style="D")
    pdf.rect(cx + 20, 205, 6, 35, style="D")
    # Hooves
    for lx in [cx - 18, cx - 5, cx + 8, cx + 20]:
        pdf.rect(lx, 240, 6, 3, style="DF")
    # Tail
    pdf.line(cx - 25, 180, cx - 35, 195)
    pdf.line(cx - 35, 195, cx - 38, 200)
    # Tail tuft
    for i in range(3):
        pdf.line(cx - 38, 200 + i, cx - 42, 204 + i)



def draw_owl(pdf):
    cx, cy = 105, 160
    # Branch
    pdf.line(30, 230, 180, 230)
    pdf.line(30, 232, 180, 232)
    # Leaves on branch
    for lx in [50, 70, 140, 165]:
        pdf.ellipse(lx, 222, 8, 5, style="D")
    # Body (egg shape)
    pts = []
    for i in range(36):
        a = math.radians(i * 10)
        rx = 38
        ry = 50 if math.sin(a) > 0 else 45
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    pdf.polygon(pts, style="D")
    # Tummy pattern (V shapes)
    for r in range(4):
        for c in range(4):
            x = cx - 20 + c * 12
            y = cy + 5 + r * 12
            pdf.line(x, y, x + 4, y - 3)
            pdf.line(x + 4, y - 3, x + 8, y)
    # Wings
    pdf.polygon([(cx - 38, cy - 10), (cx - 30, cy + 25), (cx - 18, cy + 35),
                 (cx - 22, cy - 5)], style="D")
    pdf.polygon([(cx + 38, cy - 10), (cx + 30, cy + 25), (cx + 18, cy + 35),
                 (cx + 22, cy - 5)], style="D")
    # Wing feather lines
    for i in range(4):
        pdf.arc(cx - 28, cy + 5 + i * 7, 14, 5, 200, 340, style="D")
        pdf.arc(cx + 28, cy + 5 + i * 7, 14, 5, 200, 340, style="D")
    # Big round eyes
    pdf.circle(cx - 13, cy - 22, 12, style="D")
    pdf.circle(cx + 13, cy - 22, 12, style="D")
    pdf.circle(cx - 13, cy - 22, 9, style="D")
    pdf.circle(cx + 13, cy - 22, 9, style="D")
    pdf.circle(cx - 13, cy - 22, 4, style="DF")
    pdf.circle(cx + 13, cy - 22, 4, style="DF")
    # Eye highlights
    pdf.set_fill_color(255, 255, 255)
    pdf.circle(cx - 11, cy - 24, 1.5, style="DF")
    pdf.circle(cx + 15, cy - 24, 1.5, style="DF")
    pdf.set_fill_color(0, 0, 0)
    # Beak
    pdf.polygon([(cx - 4, cy - 12), (cx + 4, cy - 12), (cx, cy - 4)], style="D")
    pdf.line(cx, cy - 12, cx, cy - 8)
    # Ear tufts
    pdf.polygon([(cx - 22, cy - 38), (cx - 18, cy - 28), (cx - 14, cy - 35)], style="D")
    pdf.polygon([(cx + 22, cy - 38), (cx + 18, cy - 28), (cx + 14, cy - 35)], style="D")
    # Feet on branch
    pdf.line(cx - 8, cy + 50, cx - 8, cy + 60)
    pdf.line(cx + 8, cy + 50, cx + 8, cy + 60)
    for fx in [cx - 8, cx + 8]:
        for i in range(3):
            pdf.line(fx, cy + 60, fx - 3 + i * 3, cy + 65)



def draw_penguin(pdf):
    cx, cy = 105, 165
    # Snow ground
    pdf.line(20, 235, 190, 235)
    for sx in [40, 70, 130, 170]:
        pdf.arc(sx, 235, 15, 8, 0, 180, style="D")
    # Body (egg)
    pts = []
    for i in range(36):
        a = math.radians(i * 10)
        rx = 35
        ry = 50
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    pdf.polygon(pts, style="D")
    # Belly (white area)
    pdf.ellipse(cx - 22, cy - 15, 44, 60, style="D")
    # Head/face area
    pdf.arc(cx, cy - 25, 60, 30, 180, 360, style="D")
    # Eyes
    eye(pdf, cx - 8, cy - 28, 2.5)
    eye(pdf, cx + 8, cy - 28, 2.5)
    # Beak
    pdf.polygon([(cx - 4, cy - 18), (cx + 4, cy - 18),
                 (cx, cy - 10)], style="D")
    pdf.line(cx, cy - 18, cx, cy - 14)
    # Cheeks (rosy circles)
    pdf.circle(cx - 14, cy - 20, 3, style="D")
    pdf.circle(cx + 14, cy - 20, 3, style="D")
    # Wings (flippers)
    pdf.ellipse(cx - 38, cy - 5, 10, 35, style="D")
    pdf.ellipse(cx + 28, cy - 5, 10, 35, style="D")
    # Feet
    pdf.ellipse(cx - 14, cy + 45, 12, 6, style="D")
    pdf.ellipse(cx + 2, cy + 45, 12, 6, style="D")
    for fx in [cx - 14, cx + 2]:
        pdf.line(fx - 4, cy + 48, fx - 6, cy + 51)
        pdf.line(fx, cy + 48, fx, cy + 52)
        pdf.line(fx + 4, cy + 48, fx + 6, cy + 51)
    # Snowflakes
    for sx, sy in [(40, 60), (170, 70), (50, 100), (160, 110), (30, 140)]:
        pdf.line(sx - 3, sy, sx + 3, sy)
        pdf.line(sx, sy - 3, sx, sy + 3)
        pdf.line(sx - 2, sy - 2, sx + 2, sy + 2)
        pdf.line(sx - 2, sy + 2, sx + 2, sy - 2)



def draw_dolphin(pdf):
    cx, cy = 105, 160
    # Water waves at top and bottom
    for y in [60, 230]:
        pts = []
        for i in range(60):
            x = 20 + i * 3
            yy = y + 2 * math.sin(i * 0.6)
            pts.append((x, yy))
        for i in range(len(pts) - 1):
            pdf.line(*pts[i], *pts[i+1])
    # Body (curved S-shape)
    body_top = []
    body_bot = []
    for i in range(40):
        t = i / 39
        x = cx - 60 + t * 120
        # Top curve
        yt = cy - 25 + 15 * math.sin(t * math.pi)
        # Bottom curve
        yb = cy + 5 + 12 * math.sin(t * math.pi)
        body_top.append((x, yt))
        body_bot.append((x, yb))
    # Draw body outline
    full = body_top + list(reversed(body_bot))
    pdf.polygon(full, style="D")
    # Dorsal fin
    pdf.polygon([(cx - 5, cy - 35), (cx + 8, cy - 50), (cx + 12, cy - 35)], style="D")
    # Tail fluke
    pdf.polygon([(cx + 58, cy - 12), (cx + 75, cy - 25), (cx + 72, cy - 12),
                 (cx + 75, cy + 5), (cx + 58, cy - 5)], style="D")
    # Side fin
    pdf.polygon([(cx - 30, cy + 8), (cx - 35, cy + 22), (cx - 22, cy + 16)], style="D")
    # Eye
    eye(pdf, cx - 45, cy - 18, 2)
    # Smile
    pdf.arc(cx - 48, cy - 10, 14, 6, 0, 90, style="D")
    # Mouth line
    pdf.line(cx - 60, cy - 12, cx - 50, cy - 8)
    # Belly line
    pdf.arc(cx, cy + 8, 100, 20, 0, 180, style="D")
    # Bubbles
    for bx, by in [(40, 100), (170, 110), (50, 200), (160, 210)]:
        pdf.circle(bx, by, 3, style="D")
        pdf.circle(bx + 5, by - 5, 2, style="D")


def draw_butterfly(pdf):
    cx, cy = 105, 160
    # Body
    pdf.ellipse(cx - 2, cy - 30, 4, 60, style="D")
    # Head
    pdf.circle(cx, cy - 35, 4, style="D")
    # Antennae
    pdf.line(cx - 2, cy - 38, cx - 10, cy - 50)
    pdf.line(cx + 2, cy - 38, cx + 10, cy - 50)
    pdf.circle(cx - 10, cy - 50, 1.5, style="D")
    pdf.circle(cx + 10, cy - 50, 1.5, style="D")
    # Upper wings (large)
    pdf.ellipse(cx - 50, cy - 30, 50, 40, style="D")
    pdf.ellipse(cx, cy - 30, 50, 40, style="D")
    # Lower wings (smaller)
    pdf.ellipse(cx - 38, cy + 5, 38, 35, style="D")
    pdf.ellipse(cx, cy + 5, 38, 35, style="D")
    # Wing patterns - circles (eye spots)
    for wx in [cx - 30, cx + 30]:
        pdf.circle(wx, cy - 18, 6, style="D")
        pdf.circle(wx, cy - 18, 3, style="D")
    for wx in [cx - 22, cx + 22]:
        pdf.circle(wx, cy + 15, 4, style="D")
    # Wing curvy patterns
    for wx in [cx - 40, cx + 40]:
        for i in range(3):
            pdf.arc(wx, cy - 35 + i * 5, 20, 4, 180, 360, style="D")
    # Small dots scattered
    for dx, dy in [(cx - 70, cy - 25), (cx + 70, cy - 25),
                   (cx - 55, cy + 15), (cx + 55, cy + 15),
                   (cx - 8, cy - 40), (cx + 8, cy - 40)]:
        pdf.circle(dx, dy, 1.5, style="DF")



def draw_rabbit(pdf):
    cx, cy = 105, 175
    # Grass
    for gx in range(20, 200, 6):
        pdf.line(gx, 245, gx - 2, 240)
        pdf.line(gx, 245, gx + 2, 240)
    # Body (round)
    pdf.ellipse(cx - 28, cy - 15, 56, 50, style="D")
    # Head
    pdf.circle(cx, cy - 25, 22, style="D")
    # Long ears
    pdf.ellipse(cx - 14, cy - 65, 8, 30, style="D")
    pdf.ellipse(cx + 6, cy - 65, 8, 30, style="D")
    # Inner ears
    pdf.ellipse(cx - 14, cy - 65, 4, 22, style="D")
    pdf.ellipse(cx + 6, cy - 65, 4, 22, style="D")
    # Eyes
    eye(pdf, cx - 8, cy - 28, 3)
    eye(pdf, cx + 8, cy - 28, 3)
    # Nose
    pdf.polygon([(cx - 2, cy - 18), (cx + 2, cy - 18), (cx, cy - 14)], style="D")
    # Mouth
    pdf.line(cx, cy - 14, cx, cy - 11)
    pdf.arc(cx - 3, cy - 11, 6, 4, 180, 360, style="D")
    pdf.arc(cx + 3, cy - 11, 6, 4, 180, 360, style="D")
    # Whiskers
    for i in [-1, 1]:
        pdf.line(cx - 5, cy - 14 + i * 2, cx - 20, cy - 14 + i * 4)
        pdf.line(cx + 5, cy - 14 + i * 2, cx + 20, cy - 14 + i * 4)
    # Front paws
    pdf.ellipse(cx - 14, cy + 22, 8, 10, style="D")
    pdf.ellipse(cx + 6, cy + 22, 8, 10, style="D")
    # Back feet
    pdf.ellipse(cx - 25, cy + 28, 18, 8, style="D")
    pdf.ellipse(cx + 7, cy + 28, 18, 8, style="D")
    # Fluffy tail
    pdf.circle(cx + 28, cy + 5, 8, style="D")
    pdf.arc(cx + 28, cy + 5, 14, 14, 0, 360, style="D")
    # Carrot beside rabbit
    pdf.polygon([(cx + 50, cy + 18), (cx + 60, cy + 30), (cx + 56, cy + 30)], style="D")
    # Carrot top
    pdf.line(cx + 50, cy + 18, cx + 48, cy + 12)
    pdf.line(cx + 50, cy + 18, cx + 52, cy + 12)
    pdf.line(cx + 50, cy + 18, cx + 50, cy + 10)
    # Lines on carrot
    pdf.line(cx + 52, cy + 22, cx + 55, cy + 23)
    pdf.line(cx + 54, cy + 26, cx + 57, cy + 27)


def draw_bear(pdf):
    cx, cy = 105, 165
    # Body
    pdf.ellipse(cx - 35, cy - 5, 70, 60, style="D")
    # Head
    pdf.circle(cx, cy - 30, 28, style="D")
    # Round ears
    pdf.circle(cx - 22, cy - 50, 9, style="D")
    pdf.circle(cx + 22, cy - 50, 9, style="D")
    # Inner ears
    pdf.circle(cx - 22, cy - 50, 5, style="D")
    pdf.circle(cx + 22, cy - 50, 5, style="D")
    # Snout
    pdf.ellipse(cx - 12, cy - 22, 24, 16, style="D")
    # Eyes
    eye(pdf, cx - 10, cy - 35, 2.5)
    eye(pdf, cx + 10, cy - 35, 2.5)
    # Nose
    pdf.ellipse(cx - 4, cy - 22, 8, 5, style="DF")
    # Mouth
    pdf.line(cx, cy - 19, cx, cy - 14)
    pdf.arc(cx - 4, cy - 14, 8, 5, 180, 360, style="D")
    pdf.arc(cx + 4, cy - 14, 8, 5, 180, 360, style="D")
    # Belly patch
    pdf.ellipse(cx - 18, cy + 5, 36, 35, style="D")
    # Arms
    pdf.ellipse(cx - 42, cy + 5, 14, 25, style="D")
    pdf.ellipse(cx + 28, cy + 5, 14, 25, style="D")
    # Paw pads
    pdf.circle(cx - 35, cy + 28, 5, style="D")
    pdf.circle(cx + 35, cy + 28, 5, style="D")
    for i in range(3):
        pdf.circle(cx - 38 + i * 3, cy + 35, 1.5, style="D")
        pdf.circle(cx + 32 + i * 3, cy + 35, 1.5, style="D")
    # Legs
    pdf.ellipse(cx - 22, cy + 45, 12, 14, style="D")
    pdf.ellipse(cx + 10, cy + 45, 12, 14, style="D")



def draw_turtle(pdf):
    cx, cy = 105, 165
    # Water/grass below
    pts = []
    for i in range(60):
        pts.append((20 + i * 3, 235 + 2 * math.sin(i * 0.5)))
    for i in range(len(pts) - 1):
        pdf.line(*pts[i], *pts[i+1])
    # Shell (large dome)
    pdf.ellipse(cx - 50, cy - 25, 100, 50, style="D")
    # Shell pattern (hexagons)
    hexagons = [(cx - 25, cy - 5), (cx, cy - 15), (cx + 25, cy - 5),
                (cx - 12, cy + 8), (cx + 12, cy + 8), (cx, cy + 5)]
    for hx, hy in hexagons:
        pts = []
        for i in range(6):
            a = math.radians(i * 60)
            pts.append((hx + 9 * math.cos(a), hy + 9 * math.sin(a)))
        pdf.polygon(pts, style="D")
    # Head
    pdf.ellipse(cx + 38, cy + 5, 22, 16, style="D")
    # Eyes
    eye(pdf, cx + 50, cy + 2, 2.5)
    # Smile
    pdf.arc(cx + 50, cy + 8, 10, 5, 0, 180, style="D")
    # Tail
    pdf.polygon([(cx - 50, cy + 10), (cx - 65, cy + 15), (cx - 50, cy + 18)], style="D")
    # Front legs
    pdf.ellipse(cx + 22, cy + 22, 16, 12, style="D")
    pdf.ellipse(cx - 38, cy + 22, 16, 12, style="D")
    # Back legs
    pdf.ellipse(cx - 25, cy + 30, 14, 10, style="D")
    pdf.ellipse(cx + 12, cy + 30, 14, 10, style="D")
    # Toes
    for fx in [cx + 30, cx + 18, cx - 30, cx - 18]:
        for i in range(3):
            pdf.line(fx - 4 + i * 4, cy + 32, fx - 4 + i * 4, cy + 38)


def draw_cat(pdf):
    cx, cy = 105, 165
    # Body sitting
    pdf.ellipse(cx - 28, cy + 5, 56, 50, style="D")
    # Head
    pdf.circle(cx, cy - 22, 22, style="D")
    # Triangle ears
    pdf.polygon([(cx - 18, cy - 38), (cx - 22, cy - 55), (cx - 8, cy - 42)], style="D")
    pdf.polygon([(cx + 18, cy - 38), (cx + 22, cy - 55), (cx + 8, cy - 42)], style="D")
    # Inner ears
    pdf.polygon([(cx - 16, cy - 38), (cx - 19, cy - 50), (cx - 11, cy - 41)], style="D")
    pdf.polygon([(cx + 16, cy - 38), (cx + 19, cy - 50), (cx + 11, cy - 41)], style="D")
    # Eyes (almond shape)
    pdf.ellipse(cx - 12, cy - 24, 8, 5, style="D")
    pdf.ellipse(cx + 4, cy - 24, 8, 5, style="D")
    pdf.ellipse(cx - 8, cy - 22, 3, 5, style="DF")
    pdf.ellipse(cx + 8, cy - 22, 3, 5, style="DF")
    # Nose
    pdf.polygon([(cx - 3, cy - 14), (cx + 3, cy - 14), (cx, cy - 10)], style="D")
    # Mouth
    pdf.line(cx, cy - 10, cx, cy - 7)
    pdf.arc(cx - 4, cy - 7, 8, 4, 180, 360, style="D")
    pdf.arc(cx + 4, cy - 7, 8, 4, 180, 360, style="D")
    # Whiskers
    for i in [-1, 0, 1]:
        pdf.line(cx - 8, cy - 10 + i * 2, cx - 25, cy - 12 + i * 4)
        pdf.line(cx + 8, cy - 10 + i * 2, cx + 25, cy - 12 + i * 4)
    # Curled tail
    pts = []
    for i in range(20):
        t = i / 19
        a = math.radians(t * 270)
        x = cx + 30 + 18 * math.cos(a) - 18
        y = cy + 25 + 18 * math.sin(a)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        pdf.line(*pts[i], *pts[i+1])
    # Front paws
    pdf.ellipse(cx - 18, cy + 38, 12, 8, style="D")
    pdf.ellipse(cx + 6, cy + 38, 12, 8, style="D")



def draw_frog(pdf):
    cx, cy = 105, 175
    # Lily pad
    pts = []
    for i in range(36):
        a = math.radians(i * 10)
        r = 60
        pts.append((cx + r * math.cos(a), cy + 35 + r * 0.4 * math.sin(a)))
    pdf.polygon(pts, style="D")
    # Lily pad notch
    pdf.line(cx + 45, cy + 35, cx + 50, cy + 50)
    pdf.line(cx + 45, cy + 35, cx + 55, cy + 38)
    # Body
    pdf.ellipse(cx - 35, cy - 5, 70, 45, style="D")
    # Head (overlaps body)
    pdf.ellipse(cx - 30, cy - 30, 60, 40, style="D")
    # Big eye bumps
    pdf.circle(cx - 18, cy - 38, 12, style="D")
    pdf.circle(cx + 18, cy - 38, 12, style="D")
    # Eyeballs
    pdf.circle(cx - 18, cy - 38, 8, style="D")
    pdf.circle(cx + 18, cy - 38, 8, style="D")
    # Pupils
    pdf.ellipse(cx - 19, cy - 39, 3, 5, style="DF")
    pdf.ellipse(cx + 17, cy - 39, 3, 5, style="DF")
    # Wide smile
    pdf.arc(cx, cy - 18, 50, 18, 0, 180, style="D")
    # Smile line
    pdf.line(cx - 25, cy - 18, cx + 25, cy - 18)
    # Nostrils
    pdf.circle(cx - 5, cy - 24, 0.8, style="DF")
    pdf.circle(cx + 5, cy - 24, 0.8, style="DF")
    # Belly
    pdf.ellipse(cx - 18, cy - 5, 36, 35, style="D")
    # Spots on back
    for sx, sy in [(cx - 28, cy - 10), (cx + 22, cy - 12), (cx + 28, cy + 5)]:
        pdf.circle(sx, sy, 3, style="D")
    # Front legs
    pdf.line(cx - 32, cy + 12, cx - 42, cy + 28)
    pdf.line(cx - 42, cy + 28, cx - 38, cy + 32)
    # Webbed feet (front)
    pdf.polygon([(cx - 42, cy + 28), (cx - 50, cy + 32), (cx - 48, cy + 36),
                 (cx - 38, cy + 32)], style="D")
    pdf.line(cx + 32, cy + 12, cx + 42, cy + 28)
    pdf.polygon([(cx + 42, cy + 28), (cx + 50, cy + 32), (cx + 48, cy + 36),
                 (cx + 38, cy + 32)], style="D")
    # Back leg (folded)
    pdf.ellipse(cx - 22, cy + 30, 30, 12, style="D")
    pdf.ellipse(cx + 14, cy + 30, 30, 12, style="D")



def draw_octopus(pdf):
    cx, cy = 105, 145
    # Bubbles
    for bx, by in [(35, 90), (175, 100), (45, 230), (165, 220)]:
        pdf.circle(bx, by, 4, style="D")
        pdf.circle(bx + 5, by - 5, 2, style="D")
    # Head/body (round bulb)
    pdf.ellipse(cx - 38, cy - 35, 76, 60, style="D")
    # Top dome highlight
    pdf.arc(cx, cy - 25, 60, 30, 180, 360, style="D")
    # Big eyes
    pdf.circle(cx - 12, cy - 12, 8, style="D")
    pdf.circle(cx + 12, cy - 12, 8, style="D")
    pdf.circle(cx - 12, cy - 12, 4, style="DF")
    pdf.circle(cx + 12, cy - 12, 4, style="DF")
    # Cheeks
    pdf.circle(cx - 22, cy - 2, 3, style="D")
    pdf.circle(cx + 22, cy - 2, 3, style="D")
    # Smile
    pdf.arc(cx, cy + 5, 16, 8, 0, 180, style="D")
    # Tentacles (8)
    tentacle_starts = [-30, -22, -10, -2, 6, 18, 28, 32]
    for i, sx_offset in enumerate(tentacle_starts):
        sx = cx + sx_offset
        sy = cy + 22
        # Wavy tentacle
        pts = []
        for j in range(20):
            t = j / 19
            wave = math.sin(t * math.pi * 2 + i) * 8
            x = sx + wave + (i - 4) * 3 * t
            y = sy + t * 70
            pts.append((x, y))
        for k in range(len(pts) - 1):
            pdf.line(*pts[k], *pts[k+1])
        # Suction cups
        for j in range(0, 20, 4):
            t = j / 19
            wave = math.sin(t * math.pi * 2 + i) * 8
            x = sx + wave + (i - 4) * 3 * t
            y = sy + t * 70
            pdf.circle(x + 2, y, 1.2, style="D")


def draw_snail(pdf):
    cx, cy = 105, 175
    # Ground
    pdf.line(20, 230, 190, 230)
    # Body (foot)
    pdf.polygon([(cx - 50, cy + 25), (cx + 35, cy + 25),
                 (cx + 50, cy + 35), (cx + 30, cy + 45),
                 (cx - 45, cy + 45), (cx - 55, cy + 35)], style="D")
    # Head bump (right)
    pdf.ellipse(cx + 25, cy + 15, 25, 18, style="D")
    # Spiral shell
    cx2, cy2 = cx - 5, cy - 5
    pdf.circle(cx2, cy2, 38, style="D")
    pdf.circle(cx2, cy2, 30, style="D")
    pdf.circle(cx2, cy2, 22, style="D")
    pdf.circle(cx2, cy2, 14, style="D")
    pdf.circle(cx2, cy2, 7, style="D")
    # Spiral lines
    for i in range(8):
        a = math.radians(i * 45)
        pdf.line(cx2 + 7 * math.cos(a), cy2 + 7 * math.sin(a),
                 cx2 + 38 * math.cos(a), cy2 + 38 * math.sin(a))
    # Eye stalks
    pdf.line(cx + 38, cy + 12, cx + 48, cy - 8)
    pdf.line(cx + 42, cy + 14, cx + 55, cy - 4)
    # Eyes
    pdf.circle(cx + 48, cy - 10, 3, style="D")
    pdf.circle(cx + 48, cy - 10, 1.2, style="DF")
    pdf.circle(cx + 55, cy - 6, 3, style="D")
    pdf.circle(cx + 55, cy - 6, 1.2, style="DF")
    # Smile
    pdf.arc(cx + 35, cy + 22, 8, 4, 0, 180, style="D")
    # Slime trail
    for i in range(8):
        x = cx - 60 - i * 10
        pdf.arc(x, cy + 38, 6, 4, 0, 180, style="D")



def draw_bee(pdf):
    cx, cy = 105, 160
    # Flower below
    cx_f, cy_f = cx - 50, 235
    for i in range(6):
        a = math.radians(i * 60)
        pdf.ellipse(cx_f + 8 * math.cos(a) - 6, cy_f + 8 * math.sin(a) - 4, 12, 8, style="D")
    pdf.circle(cx_f, cy_f, 5, style="D")
    # Stem
    pdf.line(cx_f, cy_f + 8, cx_f, cy_f + 25)
    # Body (oval, fat)
    pdf.ellipse(cx - 35, cy - 18, 75, 40, style="D")
    # Stripes (curved)
    for x_off in [-15, 0, 15]:
        pdf.arc(cx + x_off, cy + 2, 16, 36, 0, 180, style="D")
        pdf.arc(cx + x_off, cy + 2, 16, 36, 180, 360, style="D")
    # Head
    pdf.circle(cx + 32, cy - 5, 16, style="D")
    # Eyes
    pdf.ellipse(cx + 38, cy - 10, 6, 8, style="D")
    pdf.ellipse(cx + 38, cy - 10, 3, 5, style="DF")
    # Smile
    pdf.arc(cx + 38, cy - 1, 10, 5, 0, 180, style="D")
    # Antennae
    pdf.line(cx + 28, cy - 16, cx + 22, cy - 28)
    pdf.line(cx + 35, cy - 19, cx + 32, cy - 32)
    pdf.circle(cx + 22, cy - 28, 1.5, style="DF")
    pdf.circle(cx + 32, cy - 32, 1.5, style="DF")
    # Wings (transparent)
    pdf.ellipse(cx - 18, cy - 38, 22, 18, style="D")
    pdf.ellipse(cx + 8, cy - 38, 22, 18, style="D")
    # Wing details
    pdf.line(cx - 30, cy - 32, cx - 8, cy - 38)
    pdf.line(cx - 4, cy - 32, cx + 18, cy - 38)
    # Stinger
    pdf.polygon([(cx - 38, cy - 5), (cx - 50, cy - 8), (cx - 50, cy - 2)], style="D")
    # Legs
    for lx in [-20, -5, 10]:
        pdf.line(cx + lx, cy + 18, cx + lx - 4, cy + 32)
        pdf.line(cx + lx - 4, cy + 32, cx + lx - 8, cy + 32)
    # Buzz lines
    for bx, by in [(25, 80), (175, 90), (45, 110)]:
        pdf.arc(bx, by, 10, 4, 180, 360, style="D")
        pdf.arc(bx + 5, by - 3, 8, 4, 0, 180, style="D")



def draw_crab(pdf):
    cx, cy = 105, 165
    # Sand below
    pdf.line(20, 235, 190, 235)
    for sx in [40, 80, 130, 170]:
        pdf.circle(sx, 240, 1.5, style="DF")
        pdf.circle(sx + 8, 243, 1, style="DF")
    # Body (oval, wide)
    pdf.ellipse(cx - 40, cy - 15, 80, 35, style="D")
    # Body shell pattern
    pdf.line(cx - 30, cy + 2, cx + 30, cy + 2)
    pdf.arc(cx, cy - 8, 50, 18, 0, 180, style="D")
    # Spots on shell
    for sx, sy in [(cx - 20, cy - 10), (cx + 20, cy - 10), (cx, cy - 5)]:
        pdf.circle(sx, sy, 2, style="D")
    # Eyes on stalks
    pdf.line(cx - 12, cy - 15, cx - 14, cy - 30)
    pdf.line(cx + 12, cy - 15, cx + 14, cy - 30)
    pdf.circle(cx - 14, cy - 32, 4, style="D")
    pdf.circle(cx + 14, cy - 32, 4, style="D")
    pdf.circle(cx - 14, cy - 32, 1.5, style="DF")
    pdf.circle(cx + 14, cy - 32, 1.5, style="DF")
    # Big mouth
    pdf.arc(cx, cy + 5, 16, 8, 0, 180, style="D")
    # Big claws (left and right)
    # Left claw
    pdf.line(cx - 38, cy - 5, cx - 60, cy - 15)
    pdf.line(cx - 38, cy + 5, cx - 60, cy - 5)
    pdf.ellipse(cx - 75, cy - 18, 22, 18, style="D")
    # Pincer split
    pdf.line(cx - 75, cy - 10, cx - 55, cy - 10)
    pdf.line(cx - 64, cy - 18, cx - 60, cy - 14)
    # Right claw
    pdf.line(cx + 38, cy - 5, cx + 60, cy - 15)
    pdf.line(cx + 38, cy + 5, cx + 60, cy - 5)
    pdf.ellipse(cx + 53, cy - 18, 22, 18, style="D")
    pdf.line(cx + 75, cy - 10, cx + 55, cy - 10)
    pdf.line(cx + 64, cy - 18, cx + 60, cy - 14)
    # Side legs (3 on each side)
    for i in range(3):
        # Left
        x1, y1 = cx - 38, cy + 5 + i * 5
        x2, y2 = cx - 50 - i * 4, cy + 18 + i * 6
        pdf.line(x1, y1, x2, y2)
        pdf.line(x2, y2, x2 - 6, y2 + 8)
        # Right
        x1, y1 = cx + 38, cy + 5 + i * 5
        x2, y2 = cx + 50 + i * 4, cy + 18 + i * 6
        pdf.line(x1, y1, x2, y2)
        pdf.line(x2, y2, x2 + 6, y2 + 8)
    # Bubbles
    for bx, by in [(35, 90), (180, 110)]:
        pdf.circle(bx, by, 3, style="D")
        pdf.circle(bx + 5, by - 5, 1.5, style="D")



def draw_peacock(pdf):
    cx, cy = 105, 175
    # Big fan of feathers (semi-circle of feathers)
    for i in range(11):
        a = math.radians(180 - i * 18)
        # Feather end position
        fx = cx + 90 * math.cos(a)
        fy = cy - 30 + 90 * math.sin(a)
        # Feather stem (curved)
        sx = cx + 5 * math.cos(a)
        sy = cy - 25 + 5 * math.sin(a)
        pdf.line(sx, sy, fx, fy)
        # Feather eye-spot
        pdf.ellipse(fx - 6, fy - 6, 12, 12, style="D")
        pdf.ellipse(fx - 4, fy - 4, 8, 8, style="D")
        pdf.circle(fx, fy, 2, style="DF")
        # Small lines around
        for k in range(5):
            ka = math.radians(k * 72)
            pdf.line(fx + 6 * math.cos(ka), fy + 6 * math.sin(ka),
                     fx + 9 * math.cos(ka), fy + 9 * math.sin(ka))
    # Body
    pdf.ellipse(cx - 14, cy - 15, 28, 35, style="D")
    # Neck (curved)
    pdf.line(cx + 5, cy - 10, cx + 15, cy - 35)
    pdf.line(cx - 5, cy - 12, cx + 5, cy - 35)
    # Head
    pdf.circle(cx + 10, cy - 40, 8, style="D")
    # Crown (3 feathers)
    for i in range(3):
        ox = -3 + i * 3
        pdf.line(cx + 10 + ox, cy - 47, cx + 10 + ox, cy - 55)
        pdf.circle(cx + 10 + ox, cy - 56, 1.5, style="D")
    # Eye
    eye(pdf, cx + 13, cy - 42, 1.5)
    # Beak
    pdf.polygon([(cx + 16, cy - 42), (cx + 22, cy - 41), (cx + 16, cy - 39)], style="D")
    # Legs
    pdf.line(cx - 5, cy + 18, cx - 5, cy + 35)
    pdf.line(cx + 3, cy + 18, cx + 3, cy + 35)
    # Feet
    for fx in [cx - 5, cx + 3]:
        pdf.line(fx - 4, cy + 35, fx + 4, cy + 35)
        for i in range(3):
            pdf.line(fx - 4 + i * 4, cy + 35, fx - 4 + i * 4, cy + 38)


def draw_fox(pdf):
    cx, cy = 105, 165
    # Body
    pdf.ellipse(cx - 30, cy + 5, 60, 30, style="D")
    # Head (pointy)
    pdf.polygon([(cx - 25, cy - 18), (cx + 18, cy - 28), (cx + 30, cy - 5),
                 (cx + 18, cy + 5), (cx - 18, cy + 8)], style="D")
    # Pointy ears
    pdf.polygon([(cx - 18, cy - 22), (cx - 25, cy - 42), (cx - 8, cy - 28)], style="D")
    pdf.polygon([(cx + 5, cy - 28), (cx + 12, cy - 48), (cx + 18, cy - 30)], style="D")
    # Inner ears
    pdf.polygon([(cx - 16, cy - 24), (cx - 22, cy - 38), (cx - 11, cy - 28)], style="D")
    pdf.polygon([(cx + 7, cy - 30), (cx + 12, cy - 44), (cx + 16, cy - 32)], style="D")
    # White face patch
    pdf.polygon([(cx + 15, cy - 8), (cx + 28, cy - 5), (cx + 18, cy + 4)], style="D")
    # Eyes
    eye(pdf, cx + 5, cy - 14, 2)
    eye(pdf, cx + 18, cy - 16, 2)
    # Nose (pointy)
    pdf.polygon([(cx + 26, cy - 8), (cx + 32, cy - 6), (cx + 26, cy - 4)], style="DF")
    # Mouth
    pdf.line(cx + 28, cy - 4, cx + 25, cy)
    pdf.arc(cx + 22, cy, 8, 4, 0, 180, style="D")
    # Whiskers
    pdf.line(cx + 22, cy - 5, cx + 32, cy - 8)
    pdf.line(cx + 22, cy - 2, cx + 32, cy)
    # Big bushy tail
    pdf.ellipse(cx - 55, cy - 5, 30, 20, style="D")
    # Tail tip (white)
    pdf.arc(cx - 55, cy - 5, 14, 14, 90, 270, style="D")
    # Tail fluff lines
    for i in range(5):
        a = math.radians(140 + i * 18)
        pdf.line(cx - 55 + 12 * math.cos(a), cy - 5 + 8 * math.sin(a),
                 cx - 55 + 16 * math.cos(a), cy - 5 + 12 * math.sin(a))
    # Legs
    pdf.rect(cx - 22, cy + 25, 5, 15, style="D")
    pdf.rect(cx - 8, cy + 25, 5, 15, style="D")
    pdf.rect(cx + 8, cy + 25, 5, 15, style="D")
    pdf.rect(cx + 20, cy + 22, 5, 15, style="D")



def draw_whale(pdf):
    cx, cy = 105, 165
    # Water waves bottom
    for y in [240]:
        pts = []
        for i in range(60):
            pts.append((20 + i * 3, y + 2 * math.sin(i * 0.5)))
        for i in range(len(pts) - 1):
            pdf.line(*pts[i], *pts[i+1])
    # Body (huge oval, slight rounded)
    pdf.ellipse(cx - 65, cy - 25, 130, 55, style="D")
    # Belly line (curve)
    pdf.arc(cx - 5, cy + 10, 110, 30, 0, 180, style="D")
    # Head distinction line
    pdf.arc(cx - 50, cy + 5, 30, 25, 220, 320, style="D")
    # Eye
    pdf.circle(cx - 40, cy - 5, 3, style="D")
    pdf.circle(cx - 40, cy - 5, 1.2, style="DF")
    # Smile (huge)
    pdf.arc(cx - 50, cy + 5, 50, 14, 0, 90, style="D")
    pdf.line(cx - 65, cy + 5, cx - 35, cy + 12)
    # Pectoral fin
    pdf.polygon([(cx - 30, cy + 18), (cx - 45, cy + 35), (cx - 15, cy + 25)], style="D")
    # Tail fluke
    pdf.polygon([(cx + 60, cy - 15), (cx + 80, cy - 30), (cx + 75, cy - 10),
                 (cx + 80, cy + 15), (cx + 60, cy + 5)], style="D")
    # Spout (water)
    pdf.line(cx - 40, cy - 30, cx - 38, cy - 60)
    pdf.line(cx - 38, cy - 60, cx - 50, cy - 75)
    pdf.line(cx - 38, cy - 60, cx - 26, cy - 75)
    # Spout drops
    for px, py in [(cx - 50, cy - 75), (cx - 38, cy - 78), (cx - 26, cy - 75)]:
        pdf.circle(px, py - 4, 2, style="D")
        pdf.circle(px, py - 9, 1.5, style="D")
    # Belly grooves
    for i in range(6):
        x = cx - 35 + i * 8
        pdf.line(x, cy + 15, x, cy + 28)
    # Bubbles
    for bx, by in [(35, 90), (35, 170), (180, 130)]:
        pdf.circle(bx, by, 3, style="D")
        pdf.circle(bx + 4, by + 4, 1.5, style="D")


def draw_ladybug(pdf):
    cx, cy = 105, 165
    # Leaf below
    pdf.ellipse(cx - 35, cy + 30, 100, 35, style="D")
    pdf.line(cx - 35, cy + 30, cx + 65, cy + 60)  # vein
    for i in range(5):
        x = cx - 25 + i * 18
        pdf.line(x, cy + 25 + i * 6, x + 10, cy + 35 + i * 6)
    # Body (big round)
    pdf.circle(cx, cy, 50, style="D")
    # Head (front part)
    pdf.arc(cx, cy, 100, 40, 200, 340, style="D")
    pdf.ellipse(cx - 30, cy - 20, 60, 35, style="D")
    # Center line down body
    pdf.line(cx, cy - 50, cx, cy + 50)
    # Spots
    spots = [(cx - 25, cy - 15), (cx + 25, cy - 15), (cx - 30, cy + 10),
             (cx + 30, cy + 10), (cx - 18, cy + 35), (cx + 18, cy + 35)]
    for sx, sy in spots:
        pdf.circle(sx, sy, 6, style="DF")
    # Big eyes on head
    pdf.circle(cx - 12, cy - 32, 5, style="D")
    pdf.circle(cx + 12, cy - 32, 5, style="D")
    pdf.circle(cx - 12, cy - 32, 2, style="DF")
    pdf.circle(cx + 12, cy - 32, 2, style="DF")
    # Eye highlights
    pdf.set_fill_color(255, 255, 255)
    pdf.circle(cx - 11, cy - 33, 0.8, style="DF")
    pdf.circle(cx + 13, cy - 33, 0.8, style="DF")
    pdf.set_fill_color(0, 0, 0)
    # Smile
    pdf.arc(cx, cy - 22, 14, 5, 0, 180, style="D")
    # Antennae
    pdf.line(cx - 8, cy - 38, cx - 14, cy - 50)
    pdf.line(cx + 8, cy - 38, cx + 14, cy - 50)
    pdf.circle(cx - 14, cy - 50, 2, style="D")
    pdf.circle(cx + 14, cy - 50, 2, style="D")
    # Legs
    for i in range(3):
        # Left
        pdf.line(cx - 45 + i * 5, cy - 5 + i * 18, cx - 60, cy - 5 + i * 18)
        pdf.line(cx - 60, cy - 5 + i * 18, cx - 65, cy + i * 18)
        # Right
        pdf.line(cx + 45 - i * 5, cy - 5 + i * 18, cx + 60, cy - 5 + i * 18)
        pdf.line(cx + 60, cy - 5 + i * 18, cx + 65, cy + i * 18)



def draw_kangaroo(pdf):
    cx, cy = 105, 165
    # Ground
    pdf.line(20, 240, 190, 240)
    # Body (oval, leaning forward)
    pdf.ellipse(cx - 28, cy - 5, 56, 50, style="D")
    # Head
    pdf.ellipse(cx + 18, cy - 32, 22, 18, style="D")
    # Ears (long)
    pdf.ellipse(cx + 14, cy - 50, 5, 14, style="D")
    pdf.ellipse(cx + 26, cy - 50, 5, 14, style="D")
    # Eye
    eye(pdf, cx + 28, cy - 35, 2)
    # Nose
    pdf.circle(cx + 38, cy - 30, 1.5, style="DF")
    # Mouth
    pdf.line(cx + 38, cy - 28, cx + 35, cy - 25)
    # Pouch (with baby joey peeking out)
    pdf.arc(cx - 5, cy + 5, 36, 28, 0, 180, style="D")
    # Joey head in pouch
    pdf.circle(cx + 5, cy + 5, 6, style="D")
    pdf.ellipse(cx + 3, cy + 0, 3, 5, style="D")  # ear
    pdf.ellipse(cx + 7, cy + 0, 3, 5, style="D")  # ear
    eye(pdf, cx + 3, cy + 5, 1)
    eye(pdf, cx + 7, cy + 5, 1)
    # Front arms (small)
    pdf.line(cx + 8, cy - 12, cx + 18, cy)
    pdf.line(cx + 18, cy, cx + 22, cy + 5)
    pdf.line(cx + 22, cy + 5, cx + 18, cy + 8)
    # Big back legs
    pdf.ellipse(cx - 22, cy + 28, 18, 15, style="D")
    # Foot
    pdf.polygon([(cx - 32, cy + 38), (cx - 50, cy + 42), (cx - 50, cy + 46),
                 (cx - 30, cy + 46)], style="D")
    pdf.line(cx - 50, cy + 42, cx - 50, cy + 46)
    # Other leg behind
    pdf.ellipse(cx - 8, cy + 32, 15, 12, style="D")
    # Big tail
    pts = [(cx - 35, cy + 18), (cx - 55, cy + 30), (cx - 70, cy + 50),
           (cx - 75, cy + 70), (cx - 65, cy + 72), (cx - 50, cy + 50),
           (cx - 35, cy + 30)]
    pdf.polygon(pts, style="D")
    # Sun in corner
    sx, sy = 175, 70
    pdf.circle(sx, sy, 12, style="D")
    for i in range(8):
        a = math.radians(i * 45)
        pdf.line(sx + 14 * math.cos(a), sy + 14 * math.sin(a),
                 sx + 20 * math.cos(a), sy + 20 * math.sin(a))


def draw_panda(pdf):
    cx, cy = 105, 165
    # Bamboo
    for bx in [40, 165]:
        pdf.rect(bx - 4, 60, 8, 180, style="D")
        for i in range(5):
            pdf.line(bx - 4, 80 + i * 35, bx + 4, 80 + i * 35)
        # Leaves
        pdf.ellipse(bx - 12, 70, 16, 6, style="D")
        pdf.ellipse(bx + 4, 70, 16, 6, style="D")
    # Body (round)
    pdf.ellipse(cx - 35, cy - 5, 70, 65, style="D")
    # Head (round)
    pdf.circle(cx, cy - 35, 30, style="D")
    # Round ears (filled black)
    pdf.circle(cx - 22, cy - 58, 9, style="DF")
    pdf.circle(cx + 22, cy - 58, 9, style="DF")
    # Eye patches (filled black, oval)
    pdf.ellipse(cx - 18, cy - 40, 12, 16, style="DF")
    pdf.ellipse(cx + 6, cy - 40, 12, 16, style="DF")
    # Eyes (white, then pupil)
    pdf.set_fill_color(255, 255, 255)
    pdf.circle(cx - 12, cy - 35, 3, style="DF")
    pdf.circle(cx + 12, cy - 35, 3, style="DF")
    pdf.set_fill_color(0, 0, 0)
    pdf.circle(cx - 12, cy - 35, 1.5, style="DF")
    pdf.circle(cx + 12, cy - 35, 1.5, style="DF")
    # Nose
    pdf.ellipse(cx - 4, cy - 25, 8, 5, style="DF")
    # Mouth
    pdf.line(cx, cy - 22, cx, cy - 18)
    pdf.arc(cx - 4, cy - 18, 8, 4, 180, 360, style="D")
    pdf.arc(cx + 4, cy - 18, 8, 4, 180, 360, style="D")
    # Arms (filled black)
    pdf.ellipse(cx - 42, cy + 0, 14, 25, style="DF")
    pdf.ellipse(cx + 28, cy + 0, 14, 25, style="DF")
    # Holding bamboo stalk
    pdf.rect(cx - 8, cy + 5, 4, 25, style="D")
    pdf.line(cx - 8, cy + 12, cx - 4, cy + 12)
    pdf.line(cx - 8, cy + 22, cx - 4, cy + 22)
    # Legs (filled black)
    pdf.ellipse(cx - 22, cy + 38, 13, 15, style="DF")
    pdf.ellipse(cx + 9, cy + 38, 13, 15, style="DF")



def draw_zebra(pdf):
    cx, cy = 105, 165
    # Body
    pdf.ellipse(cx - 38, cy - 10, 76, 45, style="D")
    # Head (long)
    pdf.ellipse(cx + 25, cy - 30, 30, 18, style="D")
    pdf.line(cx + 38, cy - 38, cx + 50, cy - 35)  # nose top
    pdf.line(cx + 50, cy - 35, cx + 52, cy - 28)
    pdf.line(cx + 52, cy - 28, cx + 38, cy - 22)  # nose bottom
    # Neck
    pdf.polygon([(cx + 12, cy - 18), (cx + 18, cy - 38), (cx + 30, cy - 38),
                 (cx + 25, cy - 12)], style="D")
    # Mane (zigzag)
    for i in range(8):
        x = cx + 18 + i * 1.5
        y = cy - 40 - i * 0.5
        pdf.line(x, y, x - 4, y - 6)
        pdf.line(x - 4, y - 6, x, y - 8)
    # Eye
    eye(pdf, cx + 32, cy - 30, 2)
    # Nostril
    pdf.circle(cx + 47, cy - 30, 0.8, style="DF")
    # Mouth
    pdf.line(cx + 50, cy - 27, cx + 45, cy - 25)
    # Ears
    pdf.polygon([(cx + 18, cy - 38), (cx + 16, cy - 50), (cx + 24, cy - 42)], style="D")
    pdf.polygon([(cx + 28, cy - 38), (cx + 30, cy - 50), (cx + 35, cy - 42)], style="D")
    # Stripes on body (vertical)
    for i in range(8):
        x = cx - 32 + i * 9
        pdf.line(x, cy - 22, x + 2, cy + 18)
        pdf.line(x + 2, cy + 18, x - 2, cy + 22)
    # Stripes on head
    for i in range(4):
        pdf.line(cx + 30 + i * 5, cy - 38, cx + 32 + i * 5, cy - 22)
    # Stripes on neck
    for i in range(3):
        pdf.line(cx + 16 + i * 4, cy - 35, cx + 22 + i * 4, cy - 18)
    # Legs
    pdf.rect(cx - 28, cy + 22, 6, 30, style="D")
    pdf.rect(cx - 12, cy + 22, 6, 30, style="D")
    pdf.rect(cx + 8, cy + 22, 6, 30, style="D")
    pdf.rect(cx + 22, cy + 22, 6, 30, style="D")
    # Hooves (filled)
    for lx in [cx - 28, cx - 12, cx + 8, cx + 22]:
        pdf.rect(lx, cy + 50, 6, 4, style="DF")
    # Stripes on legs
    for lx in [cx - 28, cx - 12, cx + 8, cx + 22]:
        for j in range(4):
            pdf.line(lx, cy + 25 + j * 6, lx + 6, cy + 25 + j * 6)
    # Tail
    pdf.line(cx - 38, cy - 5, cx - 50, cy + 5)
    # Tail tuft (filled black)
    pdf.ellipse(cx - 50, cy + 5, 8, 5, style="DF")


def draw_pig(pdf):
    cx, cy = 105, 165
    # Mud puddle
    pts = []
    for i in range(36):
        a = math.radians(i * 10)
        r = 75 + 5 * math.sin(a * 4)
        pts.append((cx + r * math.cos(a), cy + 35 + r * 0.25 * math.sin(a)))
    pdf.polygon(pts, style="D")
    # Body (round, fat)
    pdf.ellipse(cx - 35, cy - 5, 70, 50, style="D")
    # Head (round)
    pdf.circle(cx + 28, cy - 5, 25, style="D")
    # Ears (triangle floppy)
    pdf.polygon([(cx + 14, cy - 22), (cx + 18, cy - 35), (cx + 28, cy - 22)], style="D")
    pdf.polygon([(cx + 32, cy - 25), (cx + 42, cy - 35), (cx + 45, cy - 22)], style="D")
    # Snout (oval)
    pdf.ellipse(cx + 38, cy - 4, 18, 12, style="D")
    # Nostrils
    pdf.ellipse(cx + 44, cy - 2, 3, 4, style="DF")
    pdf.ellipse(cx + 50, cy - 2, 3, 4, style="DF")
    # Eyes
    eye(pdf, cx + 22, cy - 12, 2.5)
    eye(pdf, cx + 36, cy - 14, 2.5)
    # Smile
    pdf.arc(cx + 30, cy + 5, 12, 6, 0, 180, style="D")
    # Cheeks
    pdf.circle(cx + 20, cy - 2, 3, style="D")
    # Curly tail
    pts = []
    for i in range(20):
        t = i / 19
        a = math.radians(t * 540)
        x = cx - 35 - 8 + 8 * math.cos(a)
        y = cy - 8 + 4 * t * math.sin(a)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        pdf.line(*pts[i], *pts[i+1])
    # Belly
    pdf.arc(cx, cy + 15, 50, 16, 0, 180, style="D")
    # Legs (chunky)
    pdf.rect(cx - 25, cy + 30, 9, 18, style="D")
    pdf.rect(cx - 8, cy + 30, 9, 18, style="D")
    pdf.rect(cx + 8, cy + 30, 9, 18, style="D")
    pdf.rect(cx + 22, cy + 30, 9, 18, style="D")
    # Hooves
    for lx in [cx - 25, cx - 8, cx + 8, cx + 22]:
        pdf.line(lx + 4, cy + 48, lx + 4, cy + 52)
        pdf.rect(lx, cy + 46, 9, 4, style="DF")



# ─── PAGES DATA ──────────────────────────────────────────────────────────────

ANIMAL_PAGES = [
    ("Lion", "Lions are called the King of the Jungle! Their roar can be heard 5 miles away.", draw_lion),
    ("Elephant", "Elephants are the largest land animals and can drink water with their trunks.", draw_elephant),
    ("Giraffe", "Giraffes are the tallest animals on Earth - their tongue is purple-blue!", draw_giraffe),
    ("Owl", "Owls can turn their heads almost all the way around to look behind them!", draw_owl),
    ("Penguin", "Penguins cannot fly, but they are amazing swimmers in the cold ocean.", draw_penguin),
    ("Dolphin", "Dolphins are super smart and love to play and jump out of the water!", draw_dolphin),
    ("Butterfly", "Butterflies taste with their feet and start life as crawling caterpillars.", draw_butterfly),
    ("Rabbit", "Rabbits hop with their strong back legs and can jump 3 feet in the air!", draw_rabbit),
    ("Bear", "Bears can stand on two legs and love to eat honey and berries.", draw_bear),
    ("Turtle", "Turtles carry their homes on their backs and can live over 100 years!", draw_turtle),
    ("Cat", "Cats sleep up to 16 hours a day and can purr when they are happy.", draw_cat),
    ("Frog", "Frogs catch flies with their long sticky tongues - super fast!", draw_frog),
    ("Octopus", "Octopuses have 8 arms, 3 hearts, and can change color to hide!", draw_octopus),
    ("Snail", "Snails carry their shells on their backs and leave a slimy trail.", draw_snail),
    ("Bee", "Bees make yummy honey and dance to tell other bees where flowers are!", draw_bee),
    ("Crab", "Crabs walk sideways and use their big claws to grab food.", draw_crab),
    ("Peacock", "Peacocks show off their beautiful tail feathers like a giant fan!", draw_peacock),
    ("Fox", "Foxes are clever and have a big bushy tail to keep warm in winter.", draw_fox),
    ("Whale", "Whales are the biggest animals in the ocean and sing songs underwater!", draw_whale),
    ("Ladybug", "Ladybugs are tiny but very helpful - they eat bugs that hurt plants!", draw_ladybug),
    ("Kangaroo", "Kangaroos carry their babies (called joeys) in a pouch on their tummy!", draw_kangaroo),
    ("Panda", "Pandas eat bamboo all day - up to 40 pounds of it! They love climbing trees.", draw_panda),
    ("Zebra", "Every zebra has a different stripe pattern - just like fingerprints!", draw_zebra),
    ("Pig", "Pigs are very smart and clean animals - they roll in mud to stay cool!", draw_pig),
]


# ─── PDF GENERATION ──────────────────────────────────────────────────────────

def generate_pdf():
    pdf = AnimalBook(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)

    # Cover page (full color)
    pdf.add_page()
    draw_cover(pdf)

    # 20 animal coloring pages (B&W)
    for name, fact, draw_fn in ANIMAL_PAGES[:20]:
        pdf.add_page()
        page_border(pdf)
        page_header(pdf, name, fact)
        # Reset to black for animal drawing
        pdf.set_draw_color(0, 0, 0)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_line_width(0.5)
        draw_fn(pdf)

    output_path = "/projects/sandbox/new/animal_coloring_book.pdf"
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")
    print(f"Total pages: {21} (1 cover + 20 animals)")


if __name__ == "__main__":
    generate_pdf()
