#!/usr/bin/env python3
"""
Generate a 20-page Choose Your Own Adventure coloring book PDF for kids (age 8).
Each page has: title, LINE ART coloring illustration, simple script, and coloring-activity navigation.
Uses fpdf2 drawing primitives to create kid-friendly outline illustrations.
"""

import math
from fpdf import FPDF


class AdventureBook(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_title(self, title, subtitle=""):
        self.set_font("Helvetica", "B", 18)
        self.set_xy(10, 8)
        self.cell(0, 10, title, align="C")
        if subtitle:
            self.set_font("Helvetica", "I", 10)
            self.set_xy(10, 18)
            self.cell(0, 7, subtitle, align="C")

    def add_script(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_xy(15, 135)
        self.multi_cell(180, 5.5, text)

    def add_coloring_nav(self, activities):
        self.ln(3)
        self.set_font("Helvetica", "B", 10)
        self.set_x(15)
        self.set_draw_color(0, 0, 0)
        self.cell(0, 6, "Coloring Activity - Pick your path!")
        self.ln(7)
        self.set_font("Helvetica", "", 9)
        for act in activities:
            self.set_x(20)
            self.multi_cell(170, 5, act)
            self.ln(1)


# ─── LINE ART DRAWING FUNCTIONS ───────────────────────────────────────────────
# Each function draws a coloring-style outline illustration in the image area.
# Drawing area: x=15..195, y=28..125 (roughly 180mm x 97mm)

def draw_star(pdf, cx, cy, r_outer, r_inner, points=5):
    """Draw a star outline."""
    angles = []
    for i in range(points * 2):
        angle = math.radians(-90 + i * 180 / points)
        r = r_outer if i % 2 == 0 else r_inner
        angles.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    pdf.polygon(angles, style="D")


def draw_sun(pdf, cx, cy, r):
    """Draw a sun with rays."""
    pdf.circle(cx, cy, r, style="D")
    for i in range(12):
        angle = math.radians(i * 30)
        x1 = cx + (r + 2) * math.cos(angle)
        y1 = cy + (r + 2) * math.sin(angle)
        x2 = cx + (r + 6) * math.cos(angle)
        y2 = cy + (r + 6) * math.sin(angle)
        pdf.line(x1, y1, x2, y2)


def draw_tree(pdf, x, y, trunk_h=20, crown_r=12):
    """Draw a simple tree (trunk + circle crown)."""
    pdf.rect(x - 2, y, 4, trunk_h, style="D")
    pdf.circle(x, y - crown_r + 2, crown_r, style="D")


def draw_mountain(pdf, x, y, w, h):
    """Draw a triangle mountain with snow cap."""
    pdf.polygon([(x, y), (x + w/2, y - h), (x + w, y)], style="D")
    # Snow cap
    cap_h = h * 0.25
    cap_w = w * 0.25
    mid_x = x + w/2
    top_y = y - h
    pdf.polygon([
        (mid_x - cap_w/2, top_y + cap_h),
        (mid_x, top_y),
        (mid_x + cap_w/2, top_y + cap_h)
    ], style="D")


def draw_wave(pdf, x, y, width, amplitude=4, waves=4):
    """Draw ocean waves."""
    step = width / (waves * 20)
    points = []
    for i in range(waves * 20 + 1):
        px = x + i * step
        py = y + amplitude * math.sin(i * math.pi / 10)
        points.append((px, py))
    for i in range(len(points) - 1):
        pdf.line(points[i][0], points[i][1], points[i+1][0], points[i+1][1])



def draw_fish(pdf, cx, cy, size=8):
    """Draw a simple fish outline."""
    # Body (ellipse-ish with polygon)
    pts = []
    for i in range(20):
        angle = math.radians(i * 18)
        rx = size
        ry = size * 0.5
        pts.append((cx + rx * math.cos(angle), cy + ry * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Tail
    pdf.polygon([
        (cx - size, cy),
        (cx - size - 4, cy - 3),
        (cx - size - 4, cy + 3)
    ], style="D")
    # Eye
    pdf.circle(cx + size * 0.4, cy - 1, 1, style="D")


def draw_turtle(pdf, cx, cy, size=12):
    """Draw a sea turtle outline."""
    # Shell (oval)
    pts = []
    for i in range(24):
        angle = math.radians(i * 15)
        pts.append((cx + size * math.cos(angle), cy + size * 0.7 * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Head
    pdf.circle(cx + size + 3, cy, 3, style="D")
    # Flippers
    pdf.ellipse(cx - 4, cy - size * 0.7 - 4, 8, 5, style="D")
    pdf.ellipse(cx - 4, cy + size * 0.7, 8, 5, style="D")
    # Shell pattern
    pdf.line(cx - size * 0.5, cy, cx + size * 0.5, cy)
    pdf.line(cx, cy - size * 0.5, cx, cy + size * 0.5)


def draw_ship(pdf, x, y, w=50, h=30):
    """Draw a sunken pirate ship outline."""
    # Hull
    pdf.polygon([
        (x, y), (x + 5, y + h * 0.6), (x + w - 5, y + h * 0.6), (x + w, y)
    ], style="D")
    # Mast
    mast_x = x + w * 0.5
    pdf.line(mast_x, y, mast_x, y - h * 0.8)
    # Sail (tattered)
    pdf.polygon([
        (mast_x, y - h * 0.7),
        (mast_x + 15, y - h * 0.5),
        (mast_x + 12, y - h * 0.2),
        (mast_x, y - h * 0.1)
    ], style="D")
    # Flag
    pdf.polygon([
        (mast_x, y - h * 0.8),
        (mast_x + 8, y - h * 0.75),
        (mast_x, y - h * 0.7)
    ], style="D")
    # Porthole
    pdf.circle(x + w * 0.3, y + h * 0.3, 2.5, style="D")
    pdf.circle(x + w * 0.7, y + h * 0.3, 2.5, style="D")


def draw_whale(pdf, cx, cy, size=30):
    """Draw a whale outline."""
    # Body
    pts = []
    for i in range(30):
        angle = math.radians(i * 12)
        rx = size
        ry = size * 0.45
        pts.append((cx + rx * math.cos(angle), cy + ry * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Tail
    pdf.polygon([
        (cx - size, cy),
        (cx - size - 10, cy - 8),
        (cx - size - 8, cy),
        (cx - size - 10, cy + 8)
    ], style="D")
    # Eye
    pdf.circle(cx + size * 0.5, cy - 3, 2, style="D")
    # Mouth line
    pdf.line(cx + size * 0.7, cy + 2, cx + size * 0.3, cy + 5)
    # Water spout
    pdf.line(cx + 5, cy - size * 0.45, cx + 5, cy - size * 0.45 - 8)
    pdf.line(cx + 2, cy - size * 0.45 - 8, cx + 8, cy - size * 0.45 - 8)



def draw_jellyfish(pdf, cx, cy, size=10):
    """Draw a jellyfish."""
    # Bell (half circle)
    pts = []
    for i in range(13):
        angle = math.radians(180 + i * 15)
        pts.append((cx + size * math.cos(angle), cy + size * 0.8 * math.sin(angle)))
    pdf.polyline(pts)
    # Bottom line
    pdf.line(pts[0][0], pts[0][1], pts[-1][0], pts[-1][1])
    # Tentacles
    for i in range(4):
        tx = cx - size * 0.6 + i * size * 0.4
        for j in range(3):
            y1 = cy + j * 4
            y2 = cy + j * 4 + 2
            pdf.line(tx, y1, tx + 1.5, y2)
            pdf.line(tx + 1.5, y2, tx, y2 + 2)


def draw_mushroom_house(pdf, x, y, cap_w=20, cap_h=12, stem_w=10, stem_h=15):
    """Draw a mushroom house."""
    # Stem
    pdf.rect(x + (cap_w - stem_w)/2, y, stem_w, stem_h, style="D")
    # Cap (half ellipse)
    pts = []
    for i in range(21):
        angle = math.radians(180 + i * 9)
        pts.append((x + cap_w/2 + cap_w/2 * math.cos(angle), y + cap_h * 0.8 * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Door
    pdf.rect(x + cap_w/2 - 2, y + stem_h - 7, 4, 7, style="D")
    # Window dots on cap
    pdf.circle(x + cap_w * 0.3, y - cap_h * 0.4, 2, style="D")
    pdf.circle(x + cap_w * 0.7, y - cap_h * 0.4, 2, style="D")


def draw_dragon(pdf, cx, cy, size=25):
    """Draw a friendly flower dragon."""
    # Body (oval)
    pts = []
    for i in range(24):
        angle = math.radians(i * 15)
        pts.append((cx + size * math.cos(angle), cy + size * 0.4 * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Head
    pdf.circle(cx + size + 5, cy - 3, 6, style="D")
    # Eye
    pdf.circle(cx + size + 7, cy - 5, 1.5, style="D")
    # Smile
    pdf.arc(cx + size + 5, cy - 1, 4, 4, 0, 180, style="D")
    # Wings (petal shapes)
    pdf.ellipse(cx - 5, cy - size * 0.4 - 10, 15, 10, style="D")
    pdf.ellipse(cx + 5, cy - size * 0.4 - 8, 12, 8, style="D")
    # Tail
    pdf.line(cx - size, cy, cx - size - 10, cy + 5)
    pdf.line(cx - size - 10, cy + 5, cx - size - 8, cy + 10)
    # Flower petals on body
    for i in range(4):
        px = cx - size * 0.5 + i * size * 0.35
        draw_star(pdf, px, cy, 3, 1.5, 5)


def draw_crystal(pdf, x, y, w=8, h=20):
    """Draw a crystal."""
    pdf.polygon([
        (x + w/2, y),
        (x + w, y + h * 0.3),
        (x + w * 0.8, y + h),
        (x + w * 0.2, y + h),
        (x, y + h * 0.3)
    ], style="D")
    # Inner facet lines
    pdf.line(x + w * 0.3, y + h * 0.2, x + w * 0.3, y + h * 0.8)
    pdf.line(x + w * 0.7, y + h * 0.2, x + w * 0.7, y + h * 0.8)



def draw_eagle(pdf, cx, cy, wingspan=50):
    """Draw an eagle with spread wings."""
    # Body
    pts = []
    for i in range(16):
        angle = math.radians(i * 22.5)
        pts.append((cx + 8 * math.cos(angle), cy + 5 * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Left wing
    pdf.polygon([
        (cx - 5, cy - 2),
        (cx - wingspan/2, cy - 15),
        (cx - wingspan/2 + 5, cy - 10),
        (cx - wingspan/3, cy - 12),
        (cx - 10, cy + 2)
    ], style="D")
    # Right wing
    pdf.polygon([
        (cx + 5, cy - 2),
        (cx + wingspan/2, cy - 15),
        (cx + wingspan/2 - 5, cy - 10),
        (cx + wingspan/3, cy - 12),
        (cx + 10, cy + 2)
    ], style="D")
    # Head
    pdf.circle(cx, cy - 6, 4, style="D")
    # Beak
    pdf.polygon([
        (cx, cy - 5),
        (cx + 3, cy - 4),
        (cx, cy - 2)
    ], style="D")
    # Tail
    pdf.polygon([
        (cx - 3, cy + 5),
        (cx, cy + 12),
        (cx + 3, cy + 5)
    ], style="D")


def draw_temple(pdf, x, y, w=40, h=35):
    """Draw a sky temple."""
    # Base
    pdf.rect(x, y, w, h * 0.6, style="D")
    # Roof (triangle)
    pdf.polygon([
        (x - 3, y),
        (x + w/2, y - h * 0.4),
        (x + w + 3, y)
    ], style="D")
    # Columns
    col_w = 3
    for i in range(4):
        cx = x + 5 + i * (w - 10) / 3
        pdf.rect(cx, y, col_w, h * 0.6, style="D")
    # Door
    pdf.rect(x + w/2 - 4, y + h * 0.3, 8, h * 0.3, style="D")
    # Spire
    pdf.line(x + w/2, y - h * 0.4, x + w/2, y - h * 0.55)
    draw_star(pdf, x + w/2, y - h * 0.58, 3, 1.5, 5)


def draw_cave(pdf, x, y, w=50, h=35):
    """Draw a cave entrance."""
    # Cave opening (arch)
    pts = []
    for i in range(13):
        angle = math.radians(180 + i * 15)
        pts.append((x + w/2 + w/2 * math.cos(angle), y + h + h * 0.8 * math.sin(angle)))
    pts.append((x + w, y + h))
    pts.insert(0, (x, y + h))
    pdf.polygon(pts, style="D")
    # Stalactites
    for i in range(5):
        sx = x + 8 + i * (w - 16) / 4
        pdf.polygon([
            (sx - 2, y + 5),
            (sx, y + 12),
            (sx + 2, y + 5)
        ], style="D")
    # Ground rocks
    pdf.ellipse(x + 5, y + h - 5, 8, 5, style="D")
    pdf.ellipse(x + w - 15, y + h - 4, 10, 4, style="D")


def draw_gate(pdf, x, y, w=50, h=50):
    """Draw the final magical gate with orbs."""
    # Gate frame (arch)
    pdf.rect(x, y + h * 0.3, 5, h * 0.7, style="D")
    pdf.rect(x + w - 5, y + h * 0.3, 5, h * 0.7, style="D")
    # Arch top
    pts = []
    for i in range(13):
        angle = math.radians(180 + i * 15)
        pts.append((x + w/2 + (w/2 - 2.5) * math.cos(angle), y + h * 0.3 + h * 0.3 * math.sin(angle)))
    pdf.polyline(pts)
    # Stars around gate
    for i in range(6):
        sx = x + 8 + i * (w - 16) / 5
        sy = y + 5 + (i % 2) * 5
        draw_star(pdf, sx, sy, 3, 1.5, 5)
    # Five orbs at bottom
    orb_y = y + h - 8
    for i in range(5):
        ox = x + 5 + i * (w - 10) / 4
        pdf.circle(ox, orb_y, 4, style="D")



def draw_chest(pdf, x, y, w=25, h=18):
    """Draw a treasure chest."""
    # Box
    pdf.rect(x, y + h * 0.4, w, h * 0.6, style="D")
    # Lid (rounded top)
    pts = []
    for i in range(13):
        angle = math.radians(180 + i * 15)
        pts.append((x + w/2 + w/2 * math.cos(angle), y + h * 0.4 + h * 0.3 * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Lock
    pdf.circle(x + w/2, y + h * 0.6, 2, style="D")
    # Items inside (compass, seed, feather peeking out)
    pdf.circle(x + w * 0.25, y + h * 0.2, 3, style="D")  # compass
    pdf.ellipse(x + w * 0.45, y + h * 0.15, 3, 5, style="D")  # seed
    # feather
    pdf.line(x + w * 0.7, y + h * 0.3, x + w * 0.75, y)
    pdf.line(x + w * 0.75, y, x + w * 0.8, y + h * 0.3)


def draw_fox(pdf, cx, cy, size=15):
    """Draw a two-tailed fox."""
    # Body
    pts = []
    for i in range(20):
        angle = math.radians(i * 18)
        pts.append((cx + size * math.cos(angle), cy + size * 0.5 * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Head
    pdf.circle(cx + size + 3, cy - 2, 5, style="D")
    # Ears
    pdf.polygon([(cx + size + 1, cy - 7), (cx + size + 3, cy - 12), (cx + size + 5, cy - 7)], style="D")
    pdf.polygon([(cx + size + 4, cy - 6), (cx + size + 7, cy - 11), (cx + size + 8, cy - 5)], style="D")
    # Eye
    pdf.circle(cx + size + 5, cy - 3, 1, style="D")
    # Two tails!
    pdf.line(cx - size, cy - 2, cx - size - 10, cy - 8)
    pdf.line(cx - size - 10, cy - 8, cx - size - 8, cy - 5)
    pdf.line(cx - size, cy + 2, cx - size - 10, cy + 8)
    pdf.line(cx - size - 10, cy + 8, cx - size - 8, cy + 5)
    # Legs
    for i in range(4):
        lx = cx - size * 0.5 + i * size * 0.4
        pdf.line(lx, cy + size * 0.5, lx, cy + size * 0.5 + 6)


def draw_fairy(pdf, cx, cy, size=6):
    """Draw a small fairy."""
    # Body
    pdf.circle(cx, cy, size * 0.4, style="D")
    # Head
    pdf.circle(cx, cy - size * 0.7, size * 0.3, style="D")
    # Wings
    pdf.ellipse(cx - size, cy - size * 0.5, size * 0.8, size * 0.4, style="D")
    pdf.ellipse(cx + size * 0.3, cy - size * 0.5, size * 0.8, size * 0.4, style="D")
    # Wand
    pdf.line(cx + size * 0.3, cy - size * 0.2, cx + size, cy - size)
    draw_star(pdf, cx + size + 1, cy - size - 1, 2, 1, 5)


def draw_golem(pdf, cx, cy, size=20):
    """Draw a stone golem."""
    # Body (blocky)
    pdf.rect(cx - size * 0.4, cy - size * 0.3, size * 0.8, size * 0.8, style="D")
    # Head
    pdf.rect(cx - size * 0.25, cy - size * 0.3 - size * 0.35, size * 0.5, size * 0.35, style="D")
    # Eyes
    pdf.rect(cx - size * 0.15, cy - size * 0.5, size * 0.1, size * 0.08, style="D")
    pdf.rect(cx + size * 0.05, cy - size * 0.5, size * 0.1, size * 0.08, style="D")
    # Arms
    pdf.rect(cx - size * 0.4 - size * 0.25, cy - size * 0.1, size * 0.25, size * 0.5, style="D")
    pdf.rect(cx + size * 0.4, cy - size * 0.1, size * 0.25, size * 0.5, style="D")
    # Legs
    pdf.rect(cx - size * 0.3, cy + size * 0.5, size * 0.25, size * 0.3, style="D")
    pdf.rect(cx + size * 0.05, cy + size * 0.5, size * 0.25, size * 0.3, style="D")
    # Crack lines (stone texture)
    pdf.line(cx - size * 0.2, cy - size * 0.1, cx + size * 0.1, cy + size * 0.2)
    pdf.line(cx + size * 0.2, cy, cx + size * 0.3, cy + size * 0.3)



# ─── SCENE DRAWING FUNCTIONS (one per page) ───────────────────────────────────

def scene_crossroads(pdf):
    """Page 1: Three paths with waves, trees, mountains."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Ground line
    pdf.line(15, 115, 195, 115)
    # Path splits
    pdf.line(105, 115, 60, 85)
    pdf.line(105, 115, 105, 75)
    pdf.line(105, 115, 150, 85)
    # Ocean (left)
    for i in range(3):
        draw_wave(pdf, 25, 65 + i * 8, 40, 3, 3)
    # Forest (center)
    draw_tree(pdf, 95, 75, 15, 10)
    draw_tree(pdf, 105, 70, 18, 12)
    draw_tree(pdf, 115, 75, 15, 10)
    # Mountain (right)
    draw_mountain(pdf, 135, 85, 35, 45)
    draw_mountain(pdf, 155, 85, 25, 30)
    # Character (stick figure)
    pdf.circle(105, 100, 3, style="D")
    pdf.line(105, 103, 105, 112)
    pdf.line(105, 106, 100, 110)
    pdf.line(105, 106, 110, 110)
    # Sun
    draw_sun(pdf, 170, 40, 8)


def scene_chest(pdf):
    """Page 2: Magic chest with items."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Big chest in center
    draw_chest(pdf, 80, 60, 40, 30)
    # Sparkles around
    for i in range(8):
        angle = math.radians(i * 45)
        sx = 100 + 35 * math.cos(angle)
        sy = 72 + 25 * math.sin(angle)
        draw_star(pdf, sx, sy, 3, 1.5, 4)
    # Grass
    for i in range(15):
        gx = 30 + i * 10
        pdf.line(gx, 115, gx - 2, 110)
        pdf.line(gx, 115, gx + 2, 108)
    # Compass, seed, feather labeled
    pdf.circle(55, 45, 6, style="D")
    pdf.line(55, 39, 55, 51)
    pdf.line(49, 45, 61, 45)
    pdf.ellipse(98, 40, 5, 8, style="D")
    # Feather
    pdf.line(145, 50, 150, 35)
    pdf.ellipse(146, 35, 8, 15, style="D")


def scene_coral_reef(pdf):
    """Page 3: Underwater coral reef with fish and turtle."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Water waves at top
    for i in range(3):
        draw_wave(pdf, 15, 32 + i * 4, 180, 2, 6)
    # Coral formations
    for i in range(5):
        cx = 30 + i * 35
        h = 15 + (i % 3) * 8
        pdf.polygon([
            (cx, 115), (cx + 3, 115 - h), (cx + 6, 115 - h + 5),
            (cx + 9, 115 - h - 2), (cx + 12, 115)
        ], style="D")
    # Fish
    draw_fish(pdf, 60, 65, 7)
    draw_fish(pdf, 80, 55, 5)
    draw_fish(pdf, 140, 70, 6)
    draw_fish(pdf, 160, 58, 5)
    # Turtle
    draw_turtle(pdf, 110, 80, 12)
    # Bubbles
    for i in range(6):
        pdf.circle(45 + i * 25, 45 + (i % 3) * 5, 2, style="D")


def scene_jellyfish(pdf):
    """Page 4: Glowing jellyfish and mermaid."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Jellyfish
    draw_jellyfish(pdf, 50, 55, 12)
    draw_jellyfish(pdf, 90, 45, 9)
    draw_jellyfish(pdf, 130, 60, 11)
    draw_jellyfish(pdf, 160, 50, 8)
    # Mermaid
    pdf.circle(105, 90, 5, style="D")  # head
    pdf.line(105, 95, 105, 108)  # body
    # Tail (fish tail)
    pdf.polygon([
        (105, 108), (100, 115), (105, 112), (110, 115)
    ], style="D")
    # Hair
    pdf.line(100, 88, 95, 95)
    pdf.line(110, 88, 115, 95)
    # Sparkles
    for i in range(5):
        draw_star(pdf, 35 + i * 35, 35 + (i % 2) * 10, 2, 1, 4)



def scene_talking_coral(pdf):
    """Page 5: Big brain coral with vision bubbles."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Big brain coral center
    pdf.circle(105, 85, 20, style="D")
    # Squiggly lines inside (brain pattern)
    for i in range(5):
        y = 75 + i * 5
        draw_wave(pdf, 90, y, 30, 2, 2)
    # Vision bubbles
    pdf.circle(55, 50, 15, style="D")
    pdf.circle(155, 50, 15, style="D")
    # Ship in left bubble
    draw_ship(pdf, 43, 45, 20, 12)
    # Whale in right bubble
    pts = []
    for i in range(16):
        angle = math.radians(i * 22.5)
        pts.append((155 + 10 * math.cos(angle), 50 + 5 * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Bubbles rising
    for i in range(4):
        pdf.circle(105 + i * 3, 60 - i * 5, 1.5, style="D")
    # Seabed
    pdf.line(15, 115, 195, 115)
    for i in range(8):
        cx = 25 + i * 22
        pdf.line(cx, 115, cx - 2, 108)
        pdf.line(cx, 115, cx + 3, 107)


def scene_sunken_ship(pdf):
    """Page 6: Sunken pirate ship with key."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Big ship
    draw_ship(pdf, 55, 65, 80, 45)
    # Key (highlighted)
    pdf.ellipse(135, 55, 12, 6, style="D")  # key head
    pdf.line(141, 58, 155, 58)  # key shaft
    pdf.line(155, 58, 155, 62)  # key teeth
    pdf.line(152, 58, 152, 61)
    # Fish swimming around
    draw_fish(pdf, 35, 50, 5)
    draw_fish(pdf, 170, 75, 6)
    draw_fish(pdf, 40, 90, 4)
    # Seaweed
    for i in range(4):
        sx = 20 + i * 12
        for j in range(4):
            y1 = 115 - j * 6
            pdf.line(sx, y1, sx + 2, y1 - 3)
            pdf.line(sx + 2, y1 - 3, sx, y1 - 6)
    # Bubbles
    for i in range(5):
        pdf.circle(80 + i * 8, 38 + i * 3, 1.5 + i * 0.3, style="D")


def scene_whale(pdf):
    """Page 7: Big friendly whale."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Big whale
    draw_whale(pdf, 105, 75, 40)
    # Small person on whale's back
    pdf.circle(95, 55, 3, style="D")  # head
    pdf.line(95, 58, 95, 65)  # body
    pdf.line(95, 61, 91, 64)  # arms
    pdf.line(95, 61, 99, 64)
    # Waves at top
    for i in range(2):
        draw_wave(pdf, 15, 30 + i * 5, 180, 2, 5)
    # Small fish
    draw_fish(pdf, 40, 95, 4)
    draw_fish(pdf, 165, 100, 5)
    draw_fish(pdf, 55, 105, 3)
    # Music notes (whale singing)
    for i in range(3):
        nx = 130 + i * 10
        ny = 55 - i * 5
        pdf.circle(nx, ny, 2, style="D")
        pdf.line(nx + 2, ny, nx + 2, ny - 8)


def scene_deep_abyss(pdf):
    """Page 8: Glowing underwater cave with archway."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Cave walls
    pdf.polygon([
        (15, 30), (30, 35), (20, 60), (15, 90), (20, 120), (15, 125)
    ], style="D")
    pdf.polygon([
        (195, 30), (180, 35), (190, 60), (195, 90), (190, 120), (195, 125)
    ], style="D")
    # Archway in center
    pts = []
    for i in range(13):
        angle = math.radians(180 + i * 15)
        pts.append((105 + 25 * math.cos(angle), 90 + 30 * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Glowing creatures (circles with rays)
    for i in range(10):
        cx = 40 + i * 15
        cy = 45 + (i % 3) * 15
        pdf.circle(cx, cy, 2, style="D")
        for j in range(4):
            angle = math.radians(j * 90 + i * 20)
            pdf.line(cx + 2.5 * math.cos(angle), cy + 2.5 * math.sin(angle),
                    cx + 4 * math.cos(angle), cy + 4 * math.sin(angle))
    # Stars inside archway
    for i in range(5):
        draw_star(pdf, 90 + i * 7, 75 + (i % 2) * 5, 2, 1, 5)



def scene_forest_entry(pdf):
    """Page 9: Forest entrance with fox and fairies."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Big trees
    draw_tree(pdf, 35, 80, 30, 18)
    draw_tree(pdf, 70, 75, 35, 20)
    draw_tree(pdf, 140, 75, 35, 20)
    draw_tree(pdf, 175, 80, 30, 18)
    # Path between trees
    pdf.line(85, 115, 95, 90)
    pdf.line(125, 115, 115, 90)
    # Fox
    draw_fox(pdf, 105, 100, 10)
    # Fairies
    draw_fairy(pdf, 60, 45, 5)
    draw_fairy(pdf, 150, 40, 4)
    draw_fairy(pdf, 100, 38, 5)
    # Sparkle trails
    for i in range(6):
        pdf.circle(55 + i * 8, 48 + i * 2, 0.8, style="D")


def scene_whispering_trees(pdf):
    """Page 10: Trees with faces, signpost."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Trees with faces
    for i, tx in enumerate([45, 105, 165]):
        draw_tree(pdf, tx, 75, 30, 18)
        # Face on trunk
        pdf.circle(tx - 2, 85, 1.2, style="D")
        pdf.circle(tx + 2, 85, 1.2, style="D")
        pdf.arc(tx, 89, 4, 3, 0, 180, style="D")
    # Signpost in center
    pdf.line(105, 115, 105, 95)
    # Left sign
    pdf.polygon([(80, 97), (105, 95), (105, 100), (80, 102)], style="D")
    # Right sign
    pdf.polygon([(105, 100), (130, 98), (130, 103), (105, 105)], style="D")
    # Labels
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(82, 97)
    pdf.cell(20, 5, "Mushroom", align="C")
    pdf.set_xy(107, 99)
    pdf.cell(20, 5, "Dragon", align="C")
    # Whisper lines
    for i in range(4):
        draw_wave(pdf, 55 + i * 25, 55, 15, 1.5, 2)


def scene_biggest_tree(pdf):
    """Page 11: Enormous old tree with fairy."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Massive trunk
    pdf.rect(80, 50, 40, 65, style="D")
    # Huge crown
    pts = []
    for i in range(24):
        angle = math.radians(i * 15)
        pts.append((100 + 45 * math.cos(angle), 40 + 25 * math.sin(angle)))
    pdf.polygon(pts, style="D")
    # Root arches
    pdf.arc(75, 115, 20, 15, 180, 360, style="D")
    pdf.arc(115, 115, 20, 15, 180, 360, style="D")
    # Glowing moss (dots)
    for i in range(8):
        mx = 82 + (i % 4) * 10
        my = 60 + (i // 4) * 20
        pdf.circle(mx, my, 1.5, style="D")
    # Fairy on shoulder of character
    pdf.circle(55, 95, 3, style="D")  # person head
    pdf.line(55, 98, 55, 108)
    draw_fairy(pdf, 60, 92, 4)


def scene_mushroom_village(pdf):
    """Page 12: Multiple mushroom houses."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Multiple mushroom houses
    draw_mushroom_house(pdf, 30, 80, 22, 14, 10, 18)
    draw_mushroom_house(pdf, 70, 85, 18, 11, 8, 15)
    draw_mushroom_house(pdf, 110, 75, 25, 16, 12, 20)
    draw_mushroom_house(pdf, 155, 82, 20, 12, 9, 16)
    # Rope bridge between mushrooms
    pdf.line(52, 78, 70, 80)
    pdf.line(52, 80, 70, 82)
    pdf.line(95, 73, 110, 72)
    pdf.line(95, 75, 110, 74)
    # Tiny people (circles)
    for i in range(4):
        px = 45 + i * 40
        pdf.circle(px, 108, 2, style="D")
        pdf.line(px, 110, px, 115)
    # Well
    pdf.rect(130, 100, 12, 8, style="D")
    pdf.line(133, 100, 133, 93)
    pdf.line(139, 100, 139, 93)
    pdf.line(133, 93, 139, 93)
    # Stars (magic)
    for i in range(5):
        draw_star(pdf, 35 + i * 35, 45 + (i % 2) * 8, 2.5, 1, 5)



def scene_dragon_tree(pdf):
    """Page 13: Flower dragon wrapped around tall tree."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Tall tree trunk
    pdf.rect(95, 30, 12, 85, style="D")
    # Crown at very top
    pdf.circle(101, 30, 20, style="D")
    # Dragon wrapped around tree
    draw_dragon(pdf, 75, 75, 18)
    # Flower petals on dragon (extra)
    for i in range(6):
        angle = math.radians(i * 60)
        px = 75 + 20 * math.cos(angle)
        py = 75 + 10 * math.sin(angle)
        pdf.circle(px, py, 2, style="D")
    # Person looking up
    pdf.circle(145, 95, 3, style="D")
    pdf.line(145, 98, 145, 108)
    pdf.line(145, 103, 140, 100)  # arm pointing up
    # Speech bubble for riddle
    pdf.ellipse(130, 60, 40, 15, style="D")
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(133, 63)
    pdf.cell(34, 5, "What gets bigger", align="C")
    pdf.set_xy(133, 68)
    pdf.cell(34, 5, "when you share it?", align="C")


def scene_crystal_clearing(pdf):
    """Page 14: Circle of crystals with rainbows."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Crystal circle
    for i in range(8):
        angle = math.radians(i * 45)
        cx = 105 + 35 * math.cos(angle)
        cy = 78 + 25 * math.sin(angle)
        draw_crystal(pdf, cx - 4, cy - 10, 8, 20)
    # Rainbow arcs (just curved lines)
    for i in range(4):
        r = 25 + i * 5
        pts = []
        for j in range(13):
            angle = math.radians(180 + j * 15)
            pts.append((105 + r * math.cos(angle), 55 + r * 0.5 * math.sin(angle)))
        pdf.polyline(pts)
    # Animals at bottom
    draw_fox(pdf, 50, 110, 6)
    pdf.circle(160, 108, 3, style="D")  # bunny head
    pdf.ellipse(157, 103, 3, 4, style="D")  # ear
    pdf.ellipse(161, 103, 3, 4, style="D")  # ear
    # Crystal doorway in center
    pdf.rect(95, 65, 20, 30, style="D")
    draw_star(pdf, 105, 75, 5, 2.5, 6)


def scene_storm_peaks(pdf):
    """Page 15: Mountain with lightning, temple and cave visible."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Two mountains
    draw_mountain(pdf, 30, 115, 60, 70)
    draw_mountain(pdf, 110, 115, 60, 65)
    # Temple on left peak
    draw_temple(pdf, 45, 50, 25, 20)
    # Cave on right peak
    draw_cave(pdf, 125, 55, 30, 20)
    # Lightning bolts
    pdf.polygon([
        (80, 30), (85, 42), (82, 42), (88, 55)
    ], style="D")
    pdf.polygon([
        (140, 28), (144, 38), (141, 38), (146, 48)
    ], style="D")
    # Clouds
    pdf.circle(60, 32, 8, style="D")
    pdf.circle(68, 30, 7, style="D")
    pdf.circle(76, 32, 8, style="D")
    pdf.circle(150, 30, 7, style="D")
    pdf.circle(157, 28, 6, style="D")
    # Wind lines
    for i in range(3):
        draw_wave(pdf, 20, 38 + i * 3, 30, 1.5, 2)


def scene_giant_eagle(pdf):
    """Page 16: Eagle with huge wingspan."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Giant eagle
    draw_eagle(pdf, 105, 70, 70)
    # Mountain backdrop
    draw_mountain(pdf, 15, 115, 40, 30)
    draw_mountain(pdf, 155, 115, 35, 25)
    # Clouds
    pdf.circle(40, 35, 6, style="D")
    pdf.circle(47, 33, 5, style="D")
    pdf.circle(165, 38, 5, style="D")
    pdf.circle(172, 36, 6, style="D")
    # Person below eagle
    pdf.circle(105, 105, 3, style="D")
    pdf.line(105, 108, 105, 118)
    pdf.line(105, 111, 100, 108)
    pdf.line(105, 111, 110, 108)
    # Wind swooshes
    for i in range(3):
        draw_wave(pdf, 40 + i * 40, 85 + i * 3, 25, 2, 2)



def scene_sky_temple(pdf):
    """Page 17: Floating temple with clouds and wind monks."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Floating temple
    draw_temple(pdf, 70, 50, 60, 40)
    # Clouds underneath (floating platform)
    for i in range(6):
        cx = 65 + i * 12
        pdf.circle(cx, 90, 6 + (i % 2) * 2, style="D")
    # Lightning bridge
    pdf.line(40, 110, 55, 100)
    pdf.line(55, 100, 50, 95)
    pdf.line(50, 95, 70, 88)
    # Wind monks (simple robed figures)
    for i in range(3):
        mx = 80 + i * 15
        pdf.polygon([
            (mx, 60), (mx - 4, 78), (mx + 4, 78)
        ], style="D")
        pdf.circle(mx, 57, 3, style="D")
    # Person walking on air
    pdf.circle(155, 80, 3, style="D")
    pdf.line(155, 83, 155, 92)
    pdf.line(155, 86, 150, 84)
    pdf.line(155, 86, 160, 84)
    # Dashed "air path"
    for i in range(8):
        pdf.line(135 + i * 5, 95, 137 + i * 5, 95)
    # Stars
    for i in range(5):
        draw_star(pdf, 30 + i * 38, 35 + (i % 2) * 5, 2.5, 1, 5)


def scene_cave_of_winds(pdf):
    """Page 18: Musical cave with stone golem."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Cave shape
    draw_cave(pdf, 40, 35, 120, 60)
    # Stone golem inside
    draw_golem(pdf, 110, 80, 18)
    # Wind lines (music)
    for i in range(4):
        draw_wave(pdf, 55 + i * 10, 55 + i * 5, 20, 2, 2)
    # Music notes
    for i in range(5):
        nx = 50 + i * 15
        ny = 40 + (i % 2) * 5
        pdf.circle(nx, ny, 1.5, style="D")
        pdf.line(nx + 1.5, ny, nx + 1.5, ny - 6)
        pdf.line(nx + 1.5, ny - 6, nx + 4, ny - 6)
    # Person standing strong
    pdf.circle(70, 85, 3, style="D")
    pdf.line(70, 88, 70, 100)
    pdf.line(70, 92, 65, 89)
    pdf.line(70, 92, 75, 89)
    pdf.line(70, 100, 67, 108)
    pdf.line(70, 100, 73, 108)
    # Wind blast arrows
    for i in range(3):
        ax = 95 - i * 8
        ay = 82 + i * 3
        pdf.line(ax, ay, ax - 6, ay)
        pdf.line(ax - 6, ay, ax - 4, ay - 1.5)
        pdf.line(ax - 6, ay, ax - 4, ay + 1.5)


def scene_summit(pdf):
    """Page 19: Mountain top with stone doorway and starry sky."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Mountain peak shape
    pdf.polygon([
        (15, 125), (50, 80), (105, 65), (160, 80), (195, 125)
    ], style="D")
    # Stone doorway
    pdf.rect(85, 70, 5, 40, style="D")
    pdf.rect(120, 70, 5, 40, style="D")
    # Arch
    pts = []
    for i in range(13):
        angle = math.radians(180 + i * 15)
        pts.append((105 + 17.5 * math.cos(angle), 70 + 15 * math.sin(angle)))
    pdf.polyline(pts)
    # Lightning bolt carvings on door
    pdf.line(92, 75, 95, 82)
    pdf.line(95, 82, 93, 82)
    pdf.line(93, 82, 96, 90)
    pdf.line(118, 75, 115, 82)
    pdf.line(115, 82, 117, 82)
    pdf.line(117, 82, 114, 90)
    # Stars in sky (visible in daytime!)
    for i in range(12):
        sx = 25 + i * 15
        sy = 32 + (i % 3) * 8
        draw_star(pdf, sx, sy, 2.5, 1, 5)
    # Eagle, monk, golem as witnesses
    draw_eagle(pdf, 40, 95, 20)
    # Small monk
    pdf.polygon([(160, 90), (157, 105), (163, 105)], style="D")
    pdf.circle(160, 87, 2.5, style="D")
    # Small golem
    pdf.rect(172, 92, 8, 12, style="D")
    pdf.rect(174, 86, 4, 6, style="D")


def scene_final_gate(pdf):
    """Page 20: The Final Gate with five orbs."""
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    # Grand gate
    draw_gate(pdf, 60, 35, 80, 70)
    # Extra decoration: stars and sparkles around gate
    for i in range(10):
        angle = math.radians(i * 36)
        sx = 100 + 50 * math.cos(angle)
        sy = 65 + 35 * math.sin(angle)
        draw_star(pdf, sx, sy, 2, 1, 4)
    # Five orbs with labels below
    orb_labels = ["Blue", "Green", "Rainbow", "Silver", "Amber"]
    pdf.set_font("Helvetica", "", 6)
    for i in range(5):
        ox = 68 + i * 16
        oy = 98
        pdf.circle(ox, oy, 5, style="D")
        # Inner glow lines
        for j in range(4):
            angle = math.radians(j * 90 + 45)
            pdf.line(ox + 2 * math.cos(angle), oy + 2 * math.sin(angle),
                    ox + 4 * math.cos(angle), oy + 4 * math.sin(angle))
        pdf.set_xy(ox - 8, oy + 6)
        pdf.cell(16, 4, orb_labels[i], align="C")
    # Character in awe
    pdf.circle(30, 85, 3, style="D")
    pdf.line(30, 88, 30, 98)
    pdf.line(30, 91, 35, 87)  # arm up in awe
    pdf.line(30, 91, 25, 95)



# ─── PAGE DATA ────────────────────────────────────────────────────────────────

pages = [
    {
        "title": "The Crossroads",
        "subtitle": "Page 1 - Where It All Begins",
        "script": (
            "You are standing where three paths meet. "
            "One path smells like the ocean. One path leads into a green forest. "
            "One path goes up a tall mountain. Where will you go?"
        ),
        "activities": [
            "Color the WAVES blue -> turn to Page 3 (Ocean path)",
            "Color the TREES green -> turn to Page 9 (Forest path)",
            "Color the MOUNTAIN gray -> turn to Page 15 (Mountain path)",
        ],
        "scene": scene_crossroads,
    },
    {
        "title": "The Crossroads",
        "subtitle": "Page 2 - The Magic Chest",
        "script": (
            "You find a little chest in the grass! Inside there are three things: "
            "a shiny compass, a glowing seed, and a sparkly feather. You can pick one!"
        ),
        "activities": [
            "Color the COMPASS blue -> turn to Page 3 (Ocean helper)",
            "Color the SEED green -> turn to Page 9 (Forest helper)",
            "Color the FEATHER yellow -> turn to Page 15 (Mountain helper)",
        ],
        "scene": scene_chest,
    },
    {
        "title": "Coral Reef Dive",
        "subtitle": "Page 3 - Into the Ocean!",
        "script": (
            "You jump into warm, clear water! Beautiful fish swim all around you. "
            "A friendly turtle waves its flipper. You see two paths through the coral."
        ),
        "activities": [
            "Color the SHIP brown -> turn to Page 6 (Sunken ship)",
            "Color the TURTLE green -> turn to Page 7 (Follow the turtle)",
        ],
        "scene": scene_coral_reef,
    },
    {
        "title": "Coral Reef Dive",
        "subtitle": "Page 4 - Glowing Jellyfish",
        "script": (
            "Wow! Glowing jellyfish light up the water like tiny lamps! "
            "A mermaid appears and says, 'Only brave swimmers can find the treasure below!'"
        ),
        "activities": [
            "Color the JELLYFISH purple -> turn to Page 6 (Dive to the ship)",
            "Color the MERMAID pink -> turn to Page 7 (Ask about the whale)",
        ],
        "scene": scene_jellyfish,
    },
    {
        "title": "Coral Reef Dive",
        "subtitle": "Page 5 - The Talking Coral",
        "script": (
            "You touch a big round coral and it shows you pictures in your mind! "
            "You see a secret underwater cave. There are two ways to get there."
        ),
        "activities": [
            "Color the CORAL orange -> turn to Page 6 (Go past the ship)",
            "Color the WHALE blue -> turn to Page 7 (Follow the whale)",
        ],
        "scene": scene_talking_coral,
    },
    {
        "title": "Sunken Ship",
        "subtitle": "Page 6 - The Old Pirate Ship",
        "script": (
            "A big old ship sits on the ocean floor! Fish swim in and out of the windows. "
            "Inside, you find a rusty key on the ship's wheel. It must open something special!"
        ),
        "activities": [
            "Color the KEY gold -> turn to Page 8 (Open the deep cave)",
        ],
        "scene": scene_sunken_ship,
    },
    {
        "title": "Whale Encounter",
        "subtitle": "Page 7 - The Friendly Whale",
        "script": (
            "A giant blue whale swims up to you! It sings a deep, beautiful song. "
            "'Climb on my back,' it seems to say. 'I will take you somewhere amazing!'"
        ),
        "activities": [
            "Color the WHALE blue -> turn to Page 8 (Ride to the deep cave)",
        ],
        "scene": scene_whale,
    },
    {
        "title": "The Deep Abyss",
        "subtitle": "Page 8 - The Glowing Cave",
        "script": (
            "You reach a huge underwater cave full of glowing creatures! "
            "They swirl around like stars. A big shiny doorway appears ahead. "
            "You feel brave and strong. Time to go through!"
        ),
        "activities": [
            "Color the DOORWAY blue-green -> turn to Page 20 (The Final Gate!)",
        ],
        "scene": scene_deep_abyss,
    },


    {
        "title": "Ancient Forest",
        "subtitle": "Page 9 - Into the Woods!",
        "script": (
            "You walk under giant trees with silver bark! Tiny glowing fairies fly around. "
            "A fox with TWO tails looks at you and runs down a path. What do you do?"
        ),
        "activities": [
            "Color the FOX orange -> turn to Page 12 (Follow to Mushroom Village)",
            "Color the TREE silver -> turn to Page 13 (Climb to find the dragon)",
        ],
        "scene": scene_forest_entry,
    },
    {
        "title": "Ancient Forest",
        "subtitle": "Page 10 - Whispering Trees",
        "script": (
            "The trees are whispering! They tell you about a tiny village made of mushrooms "
            "and a friendly dragon who lives in the tallest tree."
        ),
        "activities": [
            "Color the MUSHROOM red -> turn to Page 12 (Visit the village)",
            "Color the DRAGON green -> turn to Page 13 (Find the dragon)",
        ],
        "scene": scene_whispering_trees,
    },
    {
        "title": "Ancient Forest",
        "subtitle": "Page 11 - The Biggest Tree",
        "script": (
            "You find the oldest, biggest tree in the whole forest! "
            "A little fairy sits on your shoulder. 'You need wisdom or courage,' she says. "
            "'Which do you want?'"
        ),
        "activities": [
            "Color the FAIRY yellow -> turn to Page 12 (Get wisdom)",
            "Color the TREE ROOTS brown -> turn to Page 13 (Get courage)",
        ],
        "scene": scene_biggest_tree,
    },
    {
        "title": "Mushroom Village",
        "subtitle": "Page 12 - Tiny Houses!",
        "script": (
            "Giant mushrooms have been turned into little houses! Tiny people live inside. "
            "Their leader gives you a magic drink. Now you can talk to trees! Cool!"
        ),
        "activities": [
            "Color the MUSHROOM HOUSE red with white dots -> turn to Page 14 (Crystal Clearing)",
        ],
        "scene": scene_mushroom_village,
    },
    {
        "title": "Dragon's Tree",
        "subtitle": "Page 13 - The Flower Dragon",
        "script": (
            "A dragon covered in flower petals wraps around the tallest tree! "
            "It asks you a riddle: 'What gets bigger when you share it?' "
            "You answer: 'Courage!' The dragon smiles and gives you a ride!"
        ),
        "activities": [
            "Color the DRAGON'S PETALS rainbow colors -> turn to Page 14 (Crystal Clearing)",
        ],
        "scene": scene_dragon_tree,
    },
    {
        "title": "The Crystal Clearing",
        "subtitle": "Page 14 - Rainbow Crystals!",
        "script": (
            "You find a magical circle full of giant crystals! They make rainbows everywhere! "
            "All the forest animals bow to you. 'You did it!' they cheer. "
            "A crystal door appears, glowing green."
        ),
        "activities": [
            "Color the CRYSTALS in rainbow colors -> turn to Page 20 (The Final Gate!)",
        ],
        "scene": scene_crystal_clearing,
    },
    {
        "title": "Storm Peaks",
        "subtitle": "Page 15 - Up the Mountain!",
        "script": (
            "The mountain is windy and exciting! Lightning flashes in the sky. "
            "You see two places above: a golden temple and a glowing cave. "
            "Which one do you climb to?"
        ),
        "activities": [
            "Color the TEMPLE gold -> turn to Page 17 (Sky Temple)",
            "Color the CAVE orange -> turn to Page 18 (Cave of Winds)",
        ],
        "scene": scene_storm_peaks,
    },


    {
        "title": "Storm Peaks",
        "subtitle": "Page 16 - The Giant Eagle",
        "script": (
            "A huge eagle lands next to you! Its wings are bigger than a car! "
            "It looks at you with kind eyes. It can fly you to either place!"
        ),
        "activities": [
            "Color the EAGLE'S LEFT WING gold -> turn to Page 17 (Fly to temple)",
            "Color the EAGLE'S RIGHT WING orange -> turn to Page 18 (Fly to cave)",
        ],
        "scene": scene_giant_eagle,
    },
    {
        "title": "Sky Temple",
        "subtitle": "Page 17 - Walking on Clouds!",
        "script": (
            "The temple floats in the sky! Inside, wind-people teach you a secret: "
            "if you believe, you can walk on air! You close your eyes, step forward... "
            "and the wind holds you up! Amazing!"
        ),
        "activities": [
            "Color the CLOUDS white and light blue -> turn to Page 19 (The Summit)",
        ],
        "scene": scene_sky_temple,
    },
    {
        "title": "Cave of Winds",
        "subtitle": "Page 18 - The Musical Cave",
        "script": (
            "This cave makes music when the wind blows through it! Deep inside, "
            "a stone giant wakes up. 'Stand strong against my wind!' it says. "
            "You hold your ground. The giant is impressed!"
        ),
        "activities": [
            "Color the STONE GIANT gray and brown -> turn to Page 19 (The Summit)",
        ],
        "scene": scene_cave_of_winds,
    },
    {
        "title": "Summit Merge Point",
        "subtitle": "Page 19 - Top of the World!",
        "script": (
            "You made it to the very top! You can see stars even though it's daytime! "
            "A big stone door stands here. The eagle, the wind-people, and the stone giant "
            "all watch proudly. You're ready for the last adventure!"
        ),
        "activities": [
            "Color the STONE DOOR with lightning bolts -> turn to Page 20 (The Final Gate!)",
        ],
        "scene": scene_summit,
    },
    {
        "title": "The Final Gate",
        "subtitle": "Page 20 - Choose Your Destiny!",
        "script": (
            "All paths lead here! A magical gate shimmers with every color. "
            "Five glowing balls float in front of you. Each one gives you a superpower! "
            "Pick your favorite ending!"
        ),
        "activities": [
            "Color the ball BLUE -> You become the Ocean Guardian (protector of the sea!)",
            "Color the ball GREEN -> You become the Forest Spirit (friend of all plants!)",
            "Color the ball RAINBOW -> You become the Hybrid Traveler (visit all worlds!)",
            "Color the ball SILVER -> You become the Sky Wanderer (fly among the stars!)",
            "Color the ball AMBER/ORANGE -> You become the Cave Keeper (keeper of secrets!)",
        ],
        "scene": scene_final_gate,
    },
]


# ─── GENERATE PDF ─────────────────────────────────────────────────────────────

def generate_pdf():
    pdf = AdventureBook(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)

    for page in pages:
        pdf.add_page()
        pdf.add_title(page["title"], page["subtitle"])

        # Draw the line art coloring illustration
        pdf.set_line_width(0.4)
        pdf.set_draw_color(0, 0, 0)
        page["scene"](pdf)

        # Add border around illustration area
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.2)
        pdf.rect(15, 27, 180, 100, style="D")
        pdf.set_draw_color(0, 0, 0)

        # Add script and navigation
        pdf.add_script(page["script"])
        pdf.add_coloring_nav(page["activities"])

    output_path = "/projects/sandbox/new/adventure_book.pdf"
    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")
    print(f"Total pages: {len(pages)}")


if __name__ == "__main__":
    generate_pdf()
