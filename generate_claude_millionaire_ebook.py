#!/usr/bin/env python3
"""
Generate "The Claude AI Millionaire Blueprint" - 56-page e-book PDF
Uses fpdf2 with high-resolution vector graphics on every page.
"""

import math
import os
from fpdf import FPDF

# ============================================================
# CONSTANTS
# ============================================================
PAGE_W = 210  # A4 width mm
PAGE_H = 297  # A4 height mm
MARGIN = 15
CONTENT_W = PAGE_W - 2 * MARGIN

# Color palette
GOLD = (255, 215, 0)
DARK_BG = (15, 15, 35)
DEEP_BLUE = (10, 25, 80)
ACCENT_BLUE = (0, 150, 255)
ACCENT_GREEN = (0, 220, 100)
ACCENT_PURPLE = (140, 80, 255)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 210)
DARK_GRAY = (40, 40, 60)
ORANGE = (255, 140, 0)
RED = (220, 50, 50)
TEAL = (0, 200, 180)



# ============================================================
# DRAWING HELPER FUNCTIONS
# ============================================================

def draw_gradient_rect(pdf, x, y, w, h, color1, color2, steps=40):
    """Draw a gradient rectangle from color1 (top) to color2 (bottom)."""
    step_h = h / steps
    for i in range(steps):
        r = color1[0] + (color2[0] - color1[0]) * i / steps
        g = color1[1] + (color2[1] - color1[1]) * i / steps
        b = color1[2] + (color2[2] - color1[2]) * i / steps
        pdf.set_fill_color(int(r), int(g), int(b))
        pdf.rect(x, y + i * step_h, w, step_h + 0.5, 'F')


def draw_gold_coin(pdf, cx, cy, r):
    """Draw a detailed gold coin with shine and dollar sign."""
    # Outer ring
    pdf.set_fill_color(180, 140, 0)
    pdf.set_draw_color(140, 100, 0)
    for angle in range(0, 360, 5):
        x = cx + r * math.cos(math.radians(angle))
        y = cy + r * math.sin(math.radians(angle))
    pdf.ellipse(cx - r, cy - r, 2 * r, 2 * r, 'FD')
    # Inner circle
    pdf.set_fill_color(255, 215, 0)
    pdf.ellipse(cx - r * 0.8, cy - r * 0.8, r * 1.6, r * 1.6, 'F')
    # Highlight arc
    pdf.set_fill_color(255, 240, 100)
    pdf.ellipse(cx - r * 0.5, cy - r * 0.6, r * 0.8, r * 0.6, 'F')
    # Dollar sign
    pdf.set_font('Helvetica', 'B', max(6, int(r * 1.2)))
    pdf.set_text_color(140, 100, 0)
    tw = pdf.get_string_width('$')
    pdf.text(cx - tw / 2, cy + r * 0.35, '$')



def draw_brain_ai(pdf, cx, cy, size):
    """Draw an AI brain with neural network connections."""
    r = size / 2
    # Brain outline (two hemispheres)
    pdf.set_fill_color(140, 80, 255)
    pdf.set_draw_color(100, 40, 200)
    pdf.ellipse(cx - r, cy - r * 0.8, r * 1.0, r * 1.6, 'FD')
    pdf.ellipse(cx, cy - r * 0.8, r * 1.0, r * 1.6, 'FD')
    # Neural nodes
    pdf.set_fill_color(0, 220, 255)
    nodes = []
    for i in range(8):
        angle = i * 45
        nx = cx + r * 0.5 * math.cos(math.radians(angle))
        ny = cy + r * 0.5 * math.sin(math.radians(angle))
        nodes.append((nx, ny))
        pdf.ellipse(nx - 1.5, ny - 1.5, 3, 3, 'F')
    # Connections
    pdf.set_draw_color(0, 200, 255)
    pdf.set_line_width(0.3)
    for i in range(len(nodes)):
        for j in range(i + 1, min(i + 3, len(nodes))):
            pdf.line(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1])
    # Center glow
    pdf.set_fill_color(255, 255, 255)
    pdf.ellipse(cx - 2, cy - 2, 4, 4, 'F')


def draw_rocket(pdf, cx, cy, size):
    """Draw a rocket ship launching upward."""
    s = size
    # Flame
    pdf.set_fill_color(255, 100, 0)
    pdf.set_draw_color(255, 50, 0)
    pts = [(cx, cy + s * 0.8), (cx - s * 0.15, cy + s * 0.5),
           (cx + s * 0.15, cy + s * 0.5)]
    # Draw flame triangle
    with pdf.new_path(cx, cy + s * 0.8) as path:
        path.line_to(cx - s * 0.15, cy + s * 0.5)
        path.line_to(cx + s * 0.15, cy + s * 0.5)
        path.close()
    # Body
    pdf.set_fill_color(220, 230, 255)
    pdf.set_draw_color(100, 120, 200)
    pdf.ellipse(cx - s * 0.12, cy - s * 0.5, s * 0.24, s * 1.0, 'FD')
    # Nose cone
    pdf.set_fill_color(255, 80, 80)
    pdf.ellipse(cx - s * 0.08, cy - s * 0.55, s * 0.16, s * 0.2, 'F')
    # Window
    pdf.set_fill_color(0, 180, 255)
    pdf.ellipse(cx - s * 0.06, cy - s * 0.15, s * 0.12, s * 0.12, 'F')
    # Fins
    pdf.set_fill_color(255, 80, 80)
    pdf.ellipse(cx - s * 0.2, cy + s * 0.25, s * 0.1, s * 0.2, 'F')
    pdf.ellipse(cx + s * 0.1, cy + s * 0.25, s * 0.1, s * 0.2, 'F')



def draw_chart_up(pdf, cx, cy, size):
    """Draw an upward trending chart with bars."""
    s = size
    # Background panel
    pdf.set_fill_color(20, 30, 60)
    pdf.set_draw_color(0, 150, 255)
    pdf.rect(cx - s * 0.5, cy - s * 0.4, s, s * 0.8, 'FD')
    # Grid lines
    pdf.set_draw_color(40, 60, 100)
    pdf.set_line_width(0.15)
    for i in range(5):
        yy = cy - s * 0.3 + i * s * 0.15
        pdf.line(cx - s * 0.4, yy, cx + s * 0.4, yy)
    # Bars (ascending)
    colors = [(0, 150, 255), (0, 180, 200), (0, 210, 150), (0, 230, 100), (0, 255, 80)]
    bar_w = s * 0.12
    heights = [0.2, 0.35, 0.3, 0.5, 0.65]
    for i, h in enumerate(heights):
        bx = cx - s * 0.38 + i * s * 0.18
        by = cy + s * 0.3 - h * s
        pdf.set_fill_color(*colors[i])
        pdf.rect(bx, by, bar_w, h * s, 'F')
    # Trend line
    pdf.set_draw_color(255, 215, 0)
    pdf.set_line_width(0.6)
    points = [(cx - s * 0.35, cy + s * 0.15), (cx - s * 0.17, cy),
              (cx, cy + s * 0.05), (cx + s * 0.17, cy - s * 0.15),
              (cx + s * 0.35, cy - s * 0.3)]
    for i in range(len(points) - 1):
        pdf.line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])


def draw_network(pdf, cx, cy, size):
    """Draw a network/connection diagram."""
    s = size
    nodes = []
    for i in range(7):
        angle = i * (360 / 7)
        nx = cx + s * 0.4 * math.cos(math.radians(angle))
        ny = cy + s * 0.4 * math.sin(math.radians(angle))
        nodes.append((nx, ny))
    # Draw connections
    pdf.set_draw_color(0, 150, 255)
    pdf.set_line_width(0.3)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if (i + j) % 2 == 0:
                pdf.line(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1])
    # Draw nodes
    for i, (nx, ny) in enumerate(nodes):
        pdf.set_fill_color(0, 180 + i * 10, 255 - i * 20)
        pdf.ellipse(nx - 3, ny - 3, 6, 6, 'F')
    # Center hub
    pdf.set_fill_color(255, 215, 0)
    pdf.ellipse(cx - 5, cy - 5, 10, 10, 'F')
    # Hub connections
    pdf.set_draw_color(255, 215, 0)
    for nx, ny in nodes:
        pdf.line(cx, cy, nx, ny)



def draw_gear_system(pdf, cx, cy, size):
    """Draw interlocking gears for automation."""
    s = size
    def draw_single_gear(gx, gy, gr, teeth=8):
        pdf.set_fill_color(80, 100, 140)
        pdf.set_draw_color(60, 80, 120)
        pdf.ellipse(gx - gr, gy - gr, 2 * gr, 2 * gr, 'FD')
        # Teeth
        for i in range(teeth):
            angle = i * (360 / teeth)
            tx = gx + (gr + 2) * math.cos(math.radians(angle))
            ty = gy + (gr + 2) * math.sin(math.radians(angle))
            pdf.set_fill_color(100, 120, 160)
            pdf.ellipse(tx - 2, ty - 2, 4, 4, 'F')
        # Center hole
        pdf.set_fill_color(30, 40, 70)
        pdf.ellipse(gx - gr * 0.3, gy - gr * 0.3, gr * 0.6, gr * 0.6, 'F')
    draw_single_gear(cx - s * 0.2, cy, s * 0.25, 8)
    draw_single_gear(cx + s * 0.22, cy - s * 0.15, s * 0.18, 6)
    draw_single_gear(cx + s * 0.15, cy + s * 0.25, s * 0.15, 6)


def draw_lightbulb(pdf, cx, cy, size):
    """Draw a lightbulb representing ideas."""
    s = size
    # Glow effect
    pdf.set_fill_color(255, 250, 150)
    pdf.ellipse(cx - s * 0.35, cy - s * 0.4, s * 0.7, s * 0.7, 'F')
    # Bulb
    pdf.set_fill_color(255, 240, 50)
    pdf.set_draw_color(200, 180, 0)
    pdf.ellipse(cx - s * 0.25, cy - s * 0.35, s * 0.5, s * 0.55, 'FD')
    # Base
    pdf.set_fill_color(160, 160, 170)
    pdf.rect(cx - s * 0.1, cy + s * 0.15, s * 0.2, s * 0.15, 'F')
    # Filament lines
    pdf.set_draw_color(200, 150, 0)
    pdf.set_line_width(0.4)
    pdf.line(cx - s * 0.05, cy, cx, cy - s * 0.1)
    pdf.line(cx, cy - s * 0.1, cx + s * 0.05, cy)
    # Rays
    pdf.set_draw_color(255, 200, 0)
    pdf.set_line_width(0.5)
    for i in range(8):
        angle = i * 45
        x1 = cx + s * 0.32 * math.cos(math.radians(angle))
        y1 = cy - s * 0.05 + s * 0.32 * math.sin(math.radians(angle))
        x2 = cx + s * 0.42 * math.cos(math.radians(angle))
        y2 = cy - s * 0.05 + s * 0.42 * math.sin(math.radians(angle))
        pdf.line(x1, y1, x2, y2)



def draw_diamond(pdf, cx, cy, size):
    """Draw a sparkling diamond."""
    s = size
    # Glow
    pdf.set_fill_color(200, 230, 255)
    pdf.ellipse(cx - s * 0.4, cy - s * 0.4, s * 0.8, s * 0.8, 'F')
    # Diamond body using lines
    pdf.set_fill_color(100, 200, 255)
    pdf.set_draw_color(50, 150, 255)
    pdf.set_line_width(0.5)
    # Top facet
    top = cy - s * 0.35
    mid = cy - s * 0.05
    bot = cy + s * 0.35
    left = cx - s * 0.3
    right = cx + s * 0.3
    # Draw diamond shape with lines
    pdf.line(cx, top, right, mid)
    pdf.line(right, mid, cx, bot)
    pdf.line(cx, bot, left, mid)
    pdf.line(left, mid, cx, top)
    # Inner facets
    pdf.set_draw_color(150, 220, 255)
    pdf.line(cx, top, cx, bot)
    pdf.line(left, mid, right, mid)
    # Sparkles
    pdf.set_fill_color(255, 255, 255)
    sparkle_positions = [(cx + s * 0.3, cy - s * 0.3), (cx - s * 0.25, cy - s * 0.25),
                         (cx + s * 0.2, cy + s * 0.1)]
    for sx, sy in sparkle_positions:
        pdf.ellipse(sx - 1, sy - 1, 2, 2, 'F')


def draw_shield(pdf, cx, cy, size):
    """Draw a shield for security/trust."""
    s = size
    # Shield body
    pdf.set_fill_color(0, 100, 200)
    pdf.set_draw_color(0, 70, 150)
    pdf.ellipse(cx - s * 0.3, cy - s * 0.4, s * 0.6, s * 0.65, 'FD')
    # Bottom point
    pdf.set_fill_color(0, 100, 200)
    pdf.rect(cx - s * 0.3, cy, s * 0.6, s * 0.2, 'F')
    # Checkmark
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(1.0)
    pdf.line(cx - s * 0.12, cy - s * 0.05, cx - s * 0.02, cy + s * 0.08)
    pdf.line(cx - s * 0.02, cy + s * 0.08, cx + s * 0.15, cy - s * 0.15)
    # Glow ring
    pdf.set_draw_color(0, 200, 255)
    pdf.set_line_width(0.4)
    pdf.ellipse(cx - s * 0.38, cy - s * 0.38, s * 0.76, s * 0.76, 'D')


def draw_target(pdf, cx, cy, size):
    """Draw a target/bullseye for goals."""
    s = size
    rings = [(s * 0.45, (220, 50, 50)), (s * 0.35, (255, 255, 255)),
             (s * 0.25, (220, 50, 50)), (s * 0.15, (255, 255, 255)),
             (s * 0.08, (220, 50, 50))]
    for radius, color in rings:
        pdf.set_fill_color(*color)
        pdf.ellipse(cx - radius, cy - radius, 2 * radius, 2 * radius, 'F')
    # Arrow
    pdf.set_draw_color(50, 50, 50)
    pdf.set_line_width(0.7)
    pdf.line(cx - s * 0.5, cy + s * 0.3, cx, cy)
    # Arrow head
    pdf.set_fill_color(50, 50, 50)
    pdf.ellipse(cx - 2, cy - 2, 4, 4, 'F')



def draw_laptop(pdf, cx, cy, size):
    """Draw a laptop with code on screen."""
    s = size
    # Screen
    pdf.set_fill_color(20, 25, 50)
    pdf.set_draw_color(80, 80, 100)
    pdf.rect(cx - s * 0.35, cy - s * 0.35, s * 0.7, s * 0.5, 'FD')
    # Code lines on screen
    colors = [(0, 255, 150), (0, 180, 255), (255, 200, 0), (200, 100, 255)]
    for i in range(4):
        pdf.set_fill_color(*colors[i])
        w = s * (0.2 + (i % 3) * 0.12)
        pdf.rect(cx - s * 0.28, cy - s * 0.25 + i * s * 0.1, w, s * 0.04, 'F')
    # Base/keyboard
    pdf.set_fill_color(60, 65, 80)
    pdf.rect(cx - s * 0.4, cy + s * 0.15, s * 0.8, s * 0.08, 'F')
    # Keyboard dots
    pdf.set_fill_color(90, 95, 110)
    for i in range(8):
        for j in range(2):
            pdf.rect(cx - s * 0.3 + i * s * 0.08, cy + s * 0.16 + j * s * 0.03, s * 0.05, s * 0.02, 'F')


def draw_money_stack(pdf, cx, cy, size):
    """Draw a stack of money/bills."""
    s = size
    # Bills stacked
    for i in range(5):
        offset = i * 3
        # Bill shadow
        pdf.set_fill_color(0, 100 + i * 20, 0)
        pdf.rect(cx - s * 0.3 + 1, cy + s * 0.2 - offset + 1, s * 0.6, s * 0.12, 'F')
        # Bill
        pdf.set_fill_color(50, 160 + i * 15, 50)
        pdf.set_draw_color(30, 100, 30)
        pdf.rect(cx - s * 0.3, cy + s * 0.2 - offset, s * 0.6, s * 0.12, 'FD')
        # Dollar symbol on bill
        pdf.set_font('Helvetica', 'B', 6)
        pdf.set_text_color(200, 255, 200)
        pdf.text(cx - 2, cy + s * 0.28 - offset, '$')
    # Floating coins on top
    draw_gold_coin(pdf, cx - s * 0.15, cy - s * 0.15, s * 0.1)
    draw_gold_coin(pdf, cx + s * 0.15, cy - s * 0.2, s * 0.08)


def draw_page_decoration(pdf, page_num):
    """Add subtle decorative elements to page borders."""
    # Top accent line
    pdf.set_draw_color(*ACCENT_BLUE)
    pdf.set_line_width(0.5)
    pdf.line(MARGIN, 8, PAGE_W - MARGIN, 8)
    # Bottom accent line with gradient dots
    pdf.set_line_width(0.3)
    pdf.line(MARGIN, PAGE_H - 10, PAGE_W - MARGIN, PAGE_H - 10)
    # Corner decorations
    pdf.set_fill_color(*GOLD)
    pdf.ellipse(MARGIN - 2, 6, 4, 4, 'F')
    pdf.ellipse(PAGE_W - MARGIN - 2, 6, 4, 4, 'F')
    # Page number
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(*LIGHT_GRAY)
    pdf.text(PAGE_W / 2 - 3, PAGE_H - 12, str(page_num))



def draw_prompt_box(pdf, y_start, title, prompt_text, color=ACCENT_BLUE):
    """Draw a formatted prompt example box with dark background."""
    box_x = MARGIN + 5
    box_w = CONTENT_W - 10
    # Calculate height based on text
    lines = prompt_text.split('\n')
    box_h = 12 + len(lines) * 4.5 + 8
    # Dark background
    pdf.set_fill_color(20, 22, 40)
    pdf.set_draw_color(*color)
    pdf.set_line_width(0.8)
    pdf.rect(box_x, y_start, box_w, box_h, 'FD')
    # Title bar
    pdf.set_fill_color(color[0] // 3, color[1] // 3, color[2] // 3)
    pdf.rect(box_x, y_start, box_w, 10, 'F')
    # Title text
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(*color)
    pdf.text(box_x + 4, y_start + 7, f"PROMPT: {title}")
    # Copy indicator
    pdf.set_font('Helvetica', '', 6)
    pdf.set_text_color(150, 150, 170)
    pdf.text(box_x + box_w - 25, y_start + 7, "[COPY & USE]")
    # Prompt text
    pdf.set_font('Courier', '', 7)
    pdf.set_text_color(0, 255, 150)
    for i, line in enumerate(lines):
        pdf.text(box_x + 6, y_start + 15 + i * 4.5, line[:85])
    return y_start + box_h + 3


def draw_case_study_box(pdf, y_start, title, revenue, description, timeline):
    """Draw a case study results box."""
    box_x = MARGIN + 3
    box_w = CONTENT_W - 6
    box_h = 35
    # Background
    pdf.set_fill_color(15, 25, 50)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.6)
    pdf.rect(box_x, y_start, box_w, box_h, 'FD')
    # Revenue badge
    pdf.set_fill_color(255, 215, 0)
    pdf.rect(box_x + box_w - 40, y_start + 2, 38, 12, 'F')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(0, 0, 0)
    pdf.text(box_x + box_w - 38, y_start + 10, revenue)
    # Title
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*WHITE)
    pdf.text(box_x + 5, y_start + 10, title)
    # Timeline
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(*TEAL)
    pdf.text(box_x + 5, y_start + 17, f"Timeline: {timeline}")
    # Description
    pdf.set_font('Helvetica', '', 7)
    pdf.set_text_color(*LIGHT_GRAY)
    desc_lines = [description[i:i+90] for i in range(0, len(description), 90)]
    for i, line in enumerate(desc_lines[:2]):
        pdf.text(box_x + 5, y_start + 24 + i * 4, line)
    return y_start + box_h + 4



def add_chapter_header(pdf, chapter_num, title, subtitle="", graphic_func=None):
    """Add a chapter header page with gradient and graphic."""
    # Full page gradient background
    draw_gradient_rect(pdf, 0, 0, PAGE_W, PAGE_H, DEEP_BLUE, DARK_BG, 60)
    # Decorative side bar
    pdf.set_fill_color(*GOLD)
    pdf.rect(0, 0, 4, PAGE_H, 'F')
    # Chapter number circle
    pdf.set_fill_color(*ACCENT_BLUE)
    pdf.ellipse(PAGE_W / 2 - 15, 30, 30, 30, 'F')
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(*WHITE)
    tw = pdf.get_string_width(str(chapter_num))
    pdf.text(PAGE_W / 2 - tw / 2, 50, str(chapter_num))
    # Chapter label
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*GOLD)
    tw = pdf.get_string_width('CHAPTER')
    pdf.text(PAGE_W / 2 - tw / 2, 25, 'CHAPTER')
    # Title
    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(*WHITE)
    tw = pdf.get_string_width(title)
    if tw > CONTENT_W:
        pdf.set_font('Helvetica', 'B', 18)
        tw = pdf.get_string_width(title)
    pdf.text(PAGE_W / 2 - tw / 2, 80, title)
    # Subtitle
    if subtitle:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(*LIGHT_GRAY)
        tw = pdf.get_string_width(subtitle)
        pdf.text(PAGE_W / 2 - tw / 2, 90, subtitle)
    # Graphic
    if graphic_func:
        graphic_func(pdf, PAGE_W / 2, 150, 60)
    # Decorative bottom elements
    draw_gold_coin(pdf, 30, PAGE_H - 40, 8)
    draw_gold_coin(pdf, PAGE_W - 30, PAGE_H - 40, 8)
    # Bottom line
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.5)
    pdf.line(MARGIN, PAGE_H - 25, PAGE_W - MARGIN, PAGE_H - 25)


def write_body_text(pdf, text, y_pos, font_size=9):
    """Write body text with automatic wrapping."""
    pdf.set_font('Helvetica', '', font_size)
    pdf.set_text_color(50, 50, 70)
    words = text.split()
    line = ""
    x = MARGIN
    max_w = CONTENT_W
    line_height = font_size * 0.45
    for word in words:
        test = line + " " + word if line else word
        if pdf.get_string_width(test) < max_w:
            line = test
        else:
            pdf.text(x, y_pos, line)
            y_pos += line_height
            line = word
            if y_pos > PAGE_H - 25:
                return y_pos
    if line:
        pdf.text(x, y_pos, line)
        y_pos += line_height
    return y_pos


def write_bullet_point(pdf, text, y_pos, bullet_color=ACCENT_BLUE):
    """Write a bullet point with colored bullet."""
    pdf.set_fill_color(*bullet_color)
    pdf.ellipse(MARGIN + 2, y_pos - 2.5, 3, 3, 'F')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(50, 50, 70)
    pdf.text(MARGIN + 8, y_pos, text[:90])
    return y_pos + 5.5



# ============================================================
# MAIN PDF GENERATION
# ============================================================

def generate_ebook():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)
    page_count = 0

    # ========================================================
    # PAGE 1: COVER
    # ========================================================
    pdf.add_page()
    page_count += 1
    # Full gradient background
    draw_gradient_rect(pdf, 0, 0, PAGE_W, PAGE_H, (5, 5, 30), (0, 0, 0), 80)
    # Gold border frame
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(2)
    pdf.rect(8, 8, PAGE_W - 16, PAGE_H - 16, 'D')
    pdf.set_line_width(0.5)
    pdf.rect(12, 12, PAGE_W - 24, PAGE_H - 24, 'D')
    # Top decorative coins
    for i in range(5):
        draw_gold_coin(pdf, 30 + i * 38, 25, 10)
    # AI Brain - large centered
    draw_brain_ai(pdf, PAGE_W / 2, 75, 45)
    # Title
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(*GOLD)
    title = "THE CLAUDE AI"
    tw = pdf.get_string_width(title)
    pdf.text(PAGE_W / 2 - tw / 2, 120, title)
    pdf.set_font('Helvetica', 'B', 32)
    title2 = "MILLIONAIRE"
    tw = pdf.get_string_width(title2)
    pdf.text(PAGE_W / 2 - tw / 2, 135, title2)
    pdf.set_font('Helvetica', 'B', 28)
    title3 = "BLUEPRINT"
    tw = pdf.get_string_width(title3)
    pdf.text(PAGE_W / 2 - tw / 2, 150, title3)
    # Subtitle
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(*WHITE)
    sub = "Your Complete Guide to Building Wealth with AI"
    tw = pdf.get_string_width(sub)
    pdf.text(PAGE_W / 2 - tw / 2, 165, sub)
    # Central graphics row
    draw_rocket(pdf, 40, 200, 35)
    draw_chart_up(pdf, PAGE_W / 2, 200, 50)
    draw_money_stack(pdf, PAGE_W - 45, 200, 35)
    # Network at bottom
    draw_network(pdf, PAGE_W / 2, 255, 40)
    # Bottom text
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*ACCENT_GREEN)
    bot_text = "20+ Live Prompts | Real Case Studies | 90-Day Plan"
    tw = pdf.get_string_width(bot_text)
    pdf.text(PAGE_W / 2 - tw / 2, 280, bot_text)



    # ========================================================
    # PAGE 2: TABLE OF CONTENTS
    # ========================================================
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 50, DEEP_BLUE, DARK_BG, 20)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(*WHITE)
    pdf.text(MARGIN, 35, "TABLE OF CONTENTS")
    draw_page_decoration(pdf, page_count)
    # Decorative element
    draw_diamond(pdf, PAGE_W - 35, 30, 25)

    chapters = [
        ("1", "The AI Wealth Revolution", "3"),
        ("2", "Understanding Claude's Superpowers", "6"),
        ("3", "Service Arbitrage Model", "9"),
        ("4", "Building Micro-SaaS", "13"),
        ("5", "Content Empire Building", "17"),
        ("6", "AI Automation Agency", "21"),
        ("7", "Prompt Engineering as a Service", "25"),
        ("8", "Digital Products & Templates", "29"),
        ("9", "The API Economy", "32"),
        ("10", "Scaling to Seven Figures", "35"),
        ("11", "Advanced Claude Techniques", "38"),
        ("12", "Live Prompt Library", "42"),
        ("13", "Case Studies", "48"),
        ("14", "Your 90-Day Action Plan", "52"),
        ("", "Final Words", "55"),
    ]
    y = 60
    for num, title, pg in chapters:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(*DARK_BG)
        label = f"Chapter {num}: {title}" if num else title
        pdf.text(MARGIN + 5, y, label)
        # Dots
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(*LIGHT_GRAY)
        dots = '.' * 60
        pdf.text(MARGIN + 80, y, dots[:40])
        # Page number
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(*ACCENT_BLUE)
        pdf.text(PAGE_W - MARGIN - 10, y, pg)
        y += 14
    # Bottom graphic
    draw_chart_up(pdf, PAGE_W / 2, PAGE_H - 50, 40)



    # ========================================================
    # CHAPTER 1: The AI Wealth Revolution (3 pages)
    # ========================================================
    # Page 3 - Chapter header
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 1, "The AI Wealth Revolution",
                       "Why NOW is the greatest wealth opportunity in history", draw_chart_up)

    # Page 4
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, DEEP_BLUE, (240, 240, 250), 15)
    draw_page_decoration(pdf, page_count)
    draw_money_stack(pdf, PAGE_W - 40, 45, 30)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "The $15.7 Trillion AI Opportunity")
    y += 10
    text = ("The artificial intelligence market is projected to reach $15.7 trillion by 2030. "
            "This isn't just a tech trend - it's the biggest wealth transfer in human history. "
            "Those who position themselves now will capture disproportionate value. Claude AI, "
            "developed by Anthropic, represents the most capable AI assistant available today, "
            "and smart entrepreneurs are already using it to build six and seven-figure businesses.")
    y = write_body_text(pdf, text, y)
    y += 5
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*ACCENT_BLUE)
    pdf.text(MARGIN, y, "Key Market Statistics:")
    y += 7
    stats = [
        "AI market growing at 37.3% CAGR through 2030",
        "74% of businesses plan to increase AI spending in 2025",
        "Average AI-powered business sees 40% productivity gains",
        "Solo AI entrepreneurs earning $10K-$100K/month within 6 months",
        "AI services market worth $200B+ by 2026",
        "Companies paying $150-500/hour for AI consulting",
    ]
    for stat in stats:
        y = write_bullet_point(pdf, stat, y, ACCENT_GREEN)
    y += 5
    text2 = ("The window of opportunity is NOW. Early movers in AI-powered businesses are "
             "building moats that will be nearly impossible to replicate in 2-3 years. "
             "This blueprint gives you the exact roadmap to capitalize on this revolution.")
    y = write_body_text(pdf, text2, y)
    # Bottom chart graphic
    draw_chart_up(pdf, PAGE_W / 2, PAGE_H - 55, 45)

    # Page 5
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, DEEP_BLUE, (240, 240, 250), 15)
    draw_page_decoration(pdf, page_count)
    draw_rocket(pdf, PAGE_W - 35, 50, 30)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Why Claude Changes Everything")
    y += 10
    text = ("Unlike previous AI tools, Claude offers unprecedented capabilities: nuanced "
            "understanding, complex reasoning, code generation, creative writing, data analysis, "
            "and strategic thinking. This means a single person with Claude can now deliver "
            "work that previously required a team of 5-10 specialists.")
    y = write_body_text(pdf, text, y)
    y += 5
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*ACCENT_PURPLE)
    pdf.text(MARGIN, y, "The Leverage Equation:")
    y += 8
    items = [
        "1 Person + Claude = Output of 5-10 people",
        "Zero employees needed to start",
        "Minimal capital required ($20/month for Claude Pro)",
        "Infinite scalability - no inventory, no overhead",
        "Global market access from day one",
        "Multiple revenue streams simultaneously",
    ]
    for item in items:
        y = write_bullet_point(pdf, item, y, ACCENT_PURPLE)
    y += 5
    text3 = ("This blueprint will show you exactly how to leverage Claude across 7 proven "
             "business models, with real prompts you can copy and use today.")
    y = write_body_text(pdf, text3, y)
    draw_brain_ai(pdf, PAGE_W / 2, PAGE_H - 55, 40)



    # ========================================================
    # CHAPTER 2: Understanding Claude's Superpowers (3 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 2, "Understanding Claude's", "Superpowers", draw_brain_ai)

    # Page 7
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, ACCENT_PURPLE, (245, 240, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_brain_ai(pdf, PAGE_W - 35, 40, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Claude's Core Capabilities")
    y += 10
    text = ("Claude is not just another chatbot. It's a reasoning engine that can handle "
            "complex multi-step tasks with human-level quality. Understanding its capabilities "
            "is the foundation of building profitable AI businesses.")
    y = write_body_text(pdf, text, y)
    y += 5
    capabilities = [
        ("Advanced Reasoning", "Breaks down complex problems, analyzes data, creates strategies"),
        ("Code Generation", "Writes production-ready code in 20+ languages, debugs, optimizes"),
        ("Creative Writing", "Blog posts, emails, scripts, copy that converts at 2-5x industry avg"),
        ("Data Analysis", "Processes CSV, JSON, extracts insights, builds financial models"),
        ("Research & Synthesis", "Analyzes markets, competitors, trends with actionable insights"),
        ("Conversation Design", "Creates chatbot flows, customer service scripts, sales funnels"),
    ]
    for cap_title, cap_desc in capabilities:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(*ACCENT_BLUE)
        pdf.text(MARGIN + 5, y, f">> {cap_title}")
        y += 4.5
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(60, 60, 80)
        pdf.text(MARGIN + 10, y, cap_desc)
        y += 6
    draw_network(pdf, PAGE_W / 2, PAGE_H - 50, 35)

    # Page 8
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, ACCENT_PURPLE, (245, 240, 255), 15)
    draw_page_decoration(pdf, page_count)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "The Prompt Engineering Advantage")
    y += 10
    text = ("The difference between mediocre AI output and exceptional results lies in "
            "how you communicate with Claude. Master prompt engineers earn $100-500/hour "
            "because they know how to extract maximum value from every interaction.")
    y = write_body_text(pdf, text, y)
    y += 3
    # Example prompt
    prompt = ("You are an expert [ROLE]. I need you to [TASK].\n"
              "Context: [BACKGROUND INFORMATION]\n"
              "Requirements:\n"
              "- [SPECIFIC REQUIREMENT 1]\n"
              "- [SPECIFIC REQUIREMENT 2]\n"
              "Output format: [DESIRED FORMAT]\n"
              "Tone: [PROFESSIONAL/CASUAL/TECHNICAL]\n"
              "Please think step-by-step before responding.")
    y = draw_prompt_box(pdf, y, "Universal Prompt Framework", prompt, ACCENT_PURPLE)
    y += 3
    text2 = ("This framework alone will improve your Claude outputs by 10x. Each chapter "
             "in this book provides specialized prompts built on this foundation.")
    y = write_body_text(pdf, text2, y)
    draw_lightbulb(pdf, PAGE_W - 35, PAGE_H - 50, 30)



    # ========================================================
    # CHAPTER 3: Service Arbitrage Model (4 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 3, "Service Arbitrage Model",
                       "Sell human services, deliver with AI", draw_money_stack)

    # Page 10
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 80, 0), (240, 255, 240), 15)
    draw_page_decoration(pdf, page_count)
    draw_money_stack(pdf, PAGE_W - 40, 45, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "The Arbitrage Opportunity")
    y += 10
    text = ("Service arbitrage is the fastest path to $10K/month. You sell writing, coding, "
            "consulting, or design services at market rates ($50-200/hour), then use Claude "
            "to deliver 10x faster. Your effective hourly rate becomes $500-2000/hour.")
    y = write_body_text(pdf, text, y)
    y += 5
    services = [
        "Copywriting & Content: Charge $500-2000/article, deliver in 30 min",
        "Web Development: Charge $3000-10000/site, build in 2-3 days",
        "Business Consulting: Charge $200/hr, deliver reports in minutes",
        "Email Marketing: Charge $1500/month per client, 2 hours/week actual work",
        "SEO Services: Charge $2000/month, use Claude for content & analysis",
        "Social Media Management: $1500/month per client, batch in 1 hour",
    ]
    for s in services:
        y = write_bullet_point(pdf, s, y, ACCENT_GREEN)
    y += 3
    prompt = ("You are an expert cold email copywriter. Write a personalized\n"
              "outreach email to [PROSPECT NAME] at [COMPANY].\n"
              "Their pain point: [PAIN POINT from LinkedIn research]\n"
              "My service: [YOUR SERVICE]\n"
              "Goal: Book a 15-min discovery call.\n"
              "Tone: Professional but conversational. Use their name.\n"
              "Length: 4-5 sentences max. Include a specific insight about\n"
              "their business to show I've done research.")
    y = draw_prompt_box(pdf, y, "Client Outreach Prompt", prompt, ACCENT_GREEN)

    # Page 11
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 80, 0), (240, 255, 240), 15)
    draw_page_decoration(pdf, page_count)
    draw_target(pdf, PAGE_W - 35, 40, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Setting Up Your Service Business")
    y += 10
    text = ("Here's the exact step-by-step process to go from zero to $10K/month "
            "with service arbitrage using Claude:")
    y = write_body_text(pdf, text, y)
    y += 3
    steps = [
        "Week 1: Choose your service niche (copywriting is easiest to start)",
        "Week 2: Create portfolio samples using Claude (5-10 pieces)",
        "Week 3: Set up profiles on Upwork, Fiverr, and your own website",
        "Week 4: Begin outreach - 20 personalized emails per day",
        "Week 5-8: Deliver exceptional work, collect testimonials",
        "Week 9-12: Raise prices, get referrals, hire VA for admin",
    ]
    for step in steps:
        y = write_bullet_point(pdf, step, y, TEAL)
    y += 5
    prompt2 = ("Create a compelling freelance portfolio description for a\n"
               "[SERVICE TYPE] specialist. Include:\n"
               "- A hook that addresses the client's main pain point\n"
               "- 3 bullet points of unique value propositions\n"
               "- Social proof placeholder (results you've achieved)\n"
               "- Clear CTA for booking a consultation\n"
               "Tone: Confident, results-focused, specific numbers.")
    y = draw_prompt_box(pdf, y, "Portfolio Builder Prompt", prompt2, TEAL)
    draw_chart_up(pdf, PAGE_W / 2, PAGE_H - 45, 35)

    # Page 12
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 80, 0), (240, 255, 240), 15)
    draw_page_decoration(pdf, page_count)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Scaling Your Service Revenue")
    y += 10
    text = ("Once you've validated your service model, here's how to scale rapidly:")
    y = write_body_text(pdf, text, y)
    y += 3
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_BLUE)
    pdf.text(MARGIN, y, "Revenue Milestones:")
    y += 7
    milestones = [
        "Month 1: $1,000-3,000 (3-5 clients at $300-600 each)",
        "Month 2: $3,000-5,000 (raise prices, 5-8 clients)",
        "Month 3: $5,000-10,000 (premium pricing, referrals flowing)",
        "Month 4-6: $10,000-20,000 (retainer clients, systems built)",
        "Month 6-12: $20,000-50,000 (team of VAs, premium positioning)",
    ]
    for m in milestones:
        y = write_bullet_point(pdf, m, y, GOLD)
    y += 5
    prompt3 = ("You are a pricing strategist. Help me create a 3-tier\n"
               "pricing structure for my [SERVICE] business.\n"
               "Tier 1 (Basic): Entry-level package for budget clients\n"
               "Tier 2 (Professional): Most popular, best value\n"
               "Tier 3 (Premium): High-touch, maximum results\n"
               "For each tier, suggest: name, price, deliverables,\n"
               "turnaround time, and positioning strategy.")
    y = draw_prompt_box(pdf, y, "Pricing Strategy Prompt", prompt3, GOLD)
    draw_money_stack(pdf, PAGE_W / 2, PAGE_H - 45, 30)
    draw_gold_coin(pdf, 30, PAGE_H - 40, 10)
    draw_gold_coin(pdf, PAGE_W - 30, PAGE_H - 40, 10)



    # ========================================================
    # CHAPTER 4: Building Micro-SaaS (4 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 4, "Building Micro-SaaS",
                       "Launch profitable software products with Claude", draw_laptop)

    # Page 14
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 50, 100), (235, 245, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_laptop(pdf, PAGE_W - 40, 45, 30)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "The Micro-SaaS Revolution")
    y += 10
    text = ("Micro-SaaS products generate $1K-$50K/month in recurring revenue with "
            "minimal maintenance. Claude can help you build, launch, and iterate on "
            "software products 10x faster than traditional development.")
    y = write_body_text(pdf, text, y)
    y += 4
    ideas = [
        "AI Writing Assistant Chrome Extension - $29/month",
        "Automated Invoice Generator for Freelancers - $19/month",
        "Social Media Scheduler with AI Captions - $39/month",
        "Customer Feedback Analyzer Dashboard - $49/month",
        "Email Template Builder with AI Personalization - $25/month",
        "Meeting Notes Summarizer Tool - $15/month",
    ]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_BLUE)
    pdf.text(MARGIN, y, "Validated Micro-SaaS Ideas:")
    y += 6
    for idea in ideas:
        y = write_bullet_point(pdf, idea, y, ACCENT_BLUE)
    y += 3
    prompt = ("You are a SaaS product strategist. Validate this idea:\n"
              "[YOUR IDEA]\n"
              "Analyze: 1) Target market size and willingness to pay\n"
              "2) Existing competitors and their weaknesses\n"
              "3) Minimum viable feature set for launch\n"
              "4) Pricing strategy (freemium vs paid)\n"
              "5) Customer acquisition channels\n"
              "6) Technical feasibility for a solo developer\n"
              "Give a 1-10 viability score with reasoning.")
    y = draw_prompt_box(pdf, y, "SaaS Idea Validator", prompt, ACCENT_BLUE)

    # Page 15
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 50, 100), (235, 245, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_gear_system(pdf, PAGE_W - 40, 45, 30)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Building Your MVP with Claude")
    y += 10
    text = ("Claude can generate entire codebases. Here's the process: "
            "1) Define your core feature set, 2) Use Claude to generate the code, "
            "3) Test and iterate, 4) Deploy to production. Most MVPs can be built in "
            "a single weekend using this approach.")
    y = write_body_text(pdf, text, y)
    y += 3
    prompt2 = ("Build a complete [APP TYPE] using [TECH STACK].\n"
               "Requirements:\n"
               "- User authentication (email + Google OAuth)\n"
               "- Dashboard with [CORE FEATURE]\n"
               "- Stripe integration for $[PRICE]/month billing\n"
               "- Database schema for [DATA MODELS]\n"
               "- REST API endpoints\n"
               "- Responsive UI with Tailwind CSS\n"
               "Generate the full code with file structure.\n"
               "Include error handling and input validation.")
    y = draw_prompt_box(pdf, y, "Code Generator - Full MVP", prompt2, TEAL)
    y += 3
    text2 = ("Pro tip: Break your app into modules and have Claude generate each one "
             "separately. This produces better code quality and makes debugging easier.")
    y = write_body_text(pdf, text2, y)
    draw_laptop(pdf, PAGE_W / 2, PAGE_H - 50, 35)

    # Page 16
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 50, 100), (235, 245, 255), 15)
    draw_page_decoration(pdf, page_count)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Launch & Growth Strategy")
    y += 10
    text = ("Your MVP is built - now it's time to get paying customers. Here's the "
            "proven launch playbook for micro-SaaS products:")
    y = write_body_text(pdf, text, y)
    y += 3
    steps = [
        "Pre-launch: Build email list of 100+ with landing page",
        "Beta: Give 20 users free access for feedback",
        "Launch: Product Hunt, Hacker News, relevant subreddits",
        "Growth: Content marketing + SEO with Claude-generated articles",
        "Optimize: Use Claude to analyze churn and improve retention",
        "Scale: Affiliate program, integrations, enterprise tier",
    ]
    for step in steps:
        y = write_bullet_point(pdf, step, y, ORANGE)
    y += 5
    prompt3 = ("Create a Product Hunt launch strategy for my SaaS:\n"
               "[PRODUCT DESCRIPTION]\n"
               "Include: tagline options (5), first comment text,\n"
               "maker's story, key features to highlight,\n"
               "timing strategy, and community engagement plan.\n"
               "Also create 5 tweet templates for launch day.")
    y = draw_prompt_box(pdf, y, "Product Launch Prompt", prompt3, ORANGE)
    draw_rocket(pdf, PAGE_W / 2, PAGE_H - 50, 35)
    draw_chart_up(pdf, 35, PAGE_H - 45, 28)



    # ========================================================
    # CHAPTER 5: Content Empire Building (4 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 5, "Content Empire Building",
                       "Build audiences and monetize with AI content", draw_lightbulb)

    # Page 18
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (100, 0, 100), (255, 240, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_lightbulb(pdf, PAGE_W - 35, 40, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "The Content Money Machine")
    y += 10
    text = ("Content is the ultimate leverage. One person with Claude can produce more "
            "high-quality content than a team of 10 writers. Newsletters, blogs, YouTube "
            "scripts, social posts - all generating passive income while you sleep.")
    y = write_body_text(pdf, text, y)
    y += 4
    models = [
        "Newsletter Empire: 50K subscribers = $25K-$100K/month (ads + sponsorships)",
        "Blog Network: 10 niche sites = $5K-$30K/month (affiliate + ads)",
        "YouTube Channel: AI-scripted videos = $10K-$50K/month",
        "Twitter/X Growth: Build authority = consulting leads at $500/hr",
        "Podcast Production: AI-researched episodes = sponsorship revenue",
    ]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_PURPLE)
    pdf.text(MARGIN, y, "Revenue Models:")
    y += 6
    for model in models:
        y = write_bullet_point(pdf, model, y, ACCENT_PURPLE)
    y += 3
    prompt = ("Create a 30-day content calendar for a [NICHE] brand.\n"
              "Platform: [PLATFORM]\n"
              "Posting frequency: [X times per day/week]\n"
              "Content pillars: [PILLAR 1], [PILLAR 2], [PILLAR 3]\n"
              "For each post include: topic, hook, key points,\n"
              "hashtags, best posting time, and content format.\n"
              "Mix educational (40%), entertaining (30%), promotional (30%).\n"
              "Include viral content formulas for maximum engagement.")
    y = draw_prompt_box(pdf, y, "Content Calendar Generator", prompt, ACCENT_PURPLE)

    # Page 19
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (100, 0, 100), (255, 240, 255), 15)
    draw_page_decoration(pdf, page_count)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "SEO Content at Scale")
    y += 10
    text = ("Search engine optimization is a goldmine for passive income. With Claude, "
            "you can produce 50-100 SEO-optimized articles per month that rank on Google "
            "and generate traffic, leads, and affiliate revenue indefinitely.")
    y = write_body_text(pdf, text, y)
    y += 3
    prompt2 = ("Write a comprehensive 2000-word SEO article on:\n"
               "Topic: [KEYWORD/TOPIC]\n"
               "Target keyword: [PRIMARY KEYWORD]\n"
               "Secondary keywords: [KW1], [KW2], [KW3]\n"
               "Search intent: [informational/commercial/transactional]\n"
               "Include: compelling title (60 chars), meta description\n"
               "(155 chars), H2/H3 structure, internal link suggestions,\n"
               "FAQ section (5 questions), and a call-to-action.\n"
               "Tone: Expert but accessible. Include data and examples.\n"
               "Optimize for featured snippets and People Also Ask.")
    y = draw_prompt_box(pdf, y, "SEO Article Writer", prompt2, ACCENT_GREEN)
    y += 3
    text2 = ("Results: Our case study shows 100 AI-written articles generating "
             "150,000 monthly visitors and $8,500/month in ad + affiliate revenue.")
    y = write_body_text(pdf, text2, y)
    draw_chart_up(pdf, PAGE_W / 2, PAGE_H - 50, 35)

    # Page 20
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (100, 0, 100), (255, 240, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_network(pdf, PAGE_W - 40, 45, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Email Marketing & Newsletters")
    y += 10
    text = ("Email is where content converts to cash. A well-crafted newsletter with "
            "10,000 subscribers can generate $5,000-$20,000/month through sponsorships, "
            "affiliate links, and digital product sales.")
    y = write_body_text(pdf, text, y)
    y += 3
    prompt3 = ("Write a high-converting email sequence (5 emails) for:\n"
               "Product: [PRODUCT/SERVICE]\n"
               "Audience: [TARGET AUDIENCE]\n"
               "Goal: Convert free subscribers to $[PRICE] purchase\n"
               "Email 1: Value-first welcome (build trust)\n"
               "Email 2: Problem agitation (highlight pain)\n"
               "Email 3: Social proof (case studies/testimonials)\n"
               "Email 4: Overcome objections (FAQ style)\n"
               "Email 5: Urgency close (limited offer)\n"
               "Include subject lines with 40%+ open rate potential.")
    y = draw_prompt_box(pdf, y, "Email Sequence Writer", prompt3, ORANGE)
    draw_money_stack(pdf, 35, PAGE_H - 45, 25)
    draw_lightbulb(pdf, PAGE_W - 35, PAGE_H - 45, 25)



    # ========================================================
    # CHAPTER 6: AI Automation Agency (4 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 6, "AI Automation Agency",
                       "Build systems that make businesses run on autopilot", draw_gear_system)

    # Page 22
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 60, 80), (235, 250, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_gear_system(pdf, PAGE_W - 40, 45, 30)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "The $10B Automation Market")
    y += 10
    text = ("Businesses waste 30-40% of their time on repetitive tasks. An AI automation "
            "agency helps companies eliminate this waste using Claude-powered workflows. "
            "Typical retainers: $5,000-$25,000/month per client.")
    y = write_body_text(pdf, text, y)
    y += 4
    services = [
        "Customer Support Automation: Reduce ticket volume by 80%",
        "Sales Pipeline Automation: Auto-qualify and nurture leads",
        "Content Repurposing: Turn 1 piece into 20 across platforms",
        "Report Generation: Auto-create weekly business reports",
        "Employee Onboarding: Automated training sequences",
        "Invoice & Payment Processing: Zero-touch accounting",
    ]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*TEAL)
    pdf.text(MARGIN, y, "High-Value Automation Services:")
    y += 6
    for svc in services:
        y = write_bullet_point(pdf, svc, y, TEAL)
    y += 3
    prompt = ("Design a customer support automation system for a\n"
              "[BUSINESS TYPE] with [X] daily support tickets.\n"
              "Current pain points: [LIST PAIN POINTS]\n"
              "Create: 1) Ticket classification system (categories)\n"
              "2) Auto-response templates for top 10 questions\n"
              "3) Escalation rules for complex issues\n"
              "4) Customer satisfaction follow-up sequence\n"
              "5) Weekly performance reporting dashboard\n"
              "Goal: Handle 80% of tickets without human intervention.")
    y = draw_prompt_box(pdf, y, "Customer Support Bot Builder", prompt, TEAL)

    # Page 23
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 60, 80), (235, 250, 255), 15)
    draw_page_decoration(pdf, page_count)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Building Your Agency")
    y += 10
    text = ("An automation agency is one of the highest-leverage business models because "
            "once you build a system for one client, you can replicate it for dozens of "
            "similar businesses with minimal additional work.")
    y = write_body_text(pdf, text, y)
    y += 3
    steps = [
        "Step 1: Pick a niche (e-commerce, real estate, SaaS companies)",
        "Step 2: Build a case study by automating your own processes",
        "Step 3: Create a 'before/after' demonstration showing time saved",
        "Step 4: Reach out to businesses in your niche (LinkedIn + email)",
        "Step 5: Offer a free automation audit (2-3 quick wins identified)",
        "Step 6: Close $3K-10K setup fee + $2K-5K monthly retainer",
        "Step 7: Deliver using Claude + Zapier/Make + custom scripts",
        "Step 8: Document everything and build SOPs for scaling",
    ]
    for step in steps:
        y = write_bullet_point(pdf, step, y, ACCENT_BLUE)
    y += 3
    prompt2 = ("Analyze this business process and identify automation\n"
               "opportunities:\n"
               "Business: [TYPE] with [X] employees\n"
               "Current process: [DESCRIBE MANUAL WORKFLOW]\n"
               "Time spent: [X hours/week]\n"
               "For each automation opportunity, provide:\n"
               "1) Description of automated workflow\n"
               "2) Tools needed (Claude API, Zapier, etc.)\n"
               "3) Estimated time savings per week\n"
               "4) Implementation complexity (1-10)\n"
               "5) ROI calculation (cost vs time saved)")
    y = draw_prompt_box(pdf, y, "Automation Audit Prompt", prompt2, ACCENT_BLUE)

    # Page 24
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 60, 80), (235, 250, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_shield(pdf, PAGE_W - 35, 40, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Client Management & Delivery")
    y += 10
    text = ("The key to a sustainable automation agency is systematized delivery. "
            "Use Claude to help manage client relationships, create reports, and "
            "continuously optimize their systems.")
    y = write_body_text(pdf, text, y)
    y += 3
    prompt3 = ("Create a weekly client report for [CLIENT NAME].\n"
               "Metrics this week:\n"
               "- Tickets automated: [X] out of [Y] total\n"
               "- Time saved: [X hours]\n"
               "- Customer satisfaction: [X]%\n"
               "- Cost savings: $[X]\n"
               "Format: Executive summary (3 sentences),\n"
               "key metrics dashboard, wins this week,\n"
               "optimization recommendations for next week,\n"
               "and ROI calculation since engagement started.")
    y = draw_prompt_box(pdf, y, "Client Report Generator", prompt3, GOLD)
    y += 5
    text2 = ("Pro tip: Set up automated weekly reports that Claude generates from your "
             "tracking data. Clients love seeing consistent ROI proof, and it reduces "
             "churn significantly. Aim for 95%+ client retention rate.")
    y = write_body_text(pdf, text2, y)
    draw_gear_system(pdf, PAGE_W / 2, PAGE_H - 50, 35)
    draw_gold_coin(pdf, 30, PAGE_H - 35, 8)
    draw_gold_coin(pdf, PAGE_W - 30, PAGE_H - 35, 8)



    # ========================================================
    # CHAPTER 7: Prompt Engineering as a Service (4 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 7, "Prompt Engineering", "as a Service", draw_lightbulb)

    # Page 26
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (80, 0, 120), (250, 240, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_lightbulb(pdf, PAGE_W - 35, 40, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "The $200/Hour Prompt Engineer")
    y += 10
    text = ("Companies are desperate for prompt engineers who can make AI work reliably. "
            "Most people get mediocre results from AI because they don't know how to "
            "communicate effectively. You can charge $100-500/hour to write optimized "
            "prompts that 10x their AI ROI.")
    y = write_body_text(pdf, text, y)
    y += 4
    services = [
        "Custom prompt libraries for sales teams: $2K-$5K per set",
        "AI workflow design for operations: $5K-$15K per project",
        "Chatbot personality & response engineering: $3K-$10K",
        "Enterprise prompt templates: $500-$2K per template set",
        "AI training workshops: $2K-$5K per session",
        "Ongoing prompt optimization retainer: $3K-$8K/month",
    ]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_PURPLE)
    pdf.text(MARGIN, y, "Service Offerings & Pricing:")
    y += 6
    for svc in services:
        y = write_bullet_point(pdf, svc, y, ACCENT_PURPLE)
    y += 3
    prompt = ("You are a meta-prompt engineer. Take this basic prompt:\n"
              "[ORIGINAL PROMPT]\n"
              "And optimize it for maximum output quality by:\n"
              "1) Adding role/persona specification\n"
              "2) Providing structured context\n"
              "3) Defining explicit output format\n"
              "4) Including quality criteria\n"
              "5) Adding chain-of-thought instructions\n"
              "6) Including examples (few-shot learning)\n"
              "Show the before/after with explanation of changes.")
    y = draw_prompt_box(pdf, y, "Prompt Optimizer (Meta-Prompt)", prompt, ACCENT_PURPLE)

    # Page 27
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (80, 0, 120), (250, 240, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_diamond(pdf, PAGE_W - 35, 40, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Advanced Prompting Techniques")
    y += 10
    text = ("These advanced techniques separate $50/hour prompt writers from "
            "$500/hour prompt engineers:")
    y = write_body_text(pdf, text, y)
    y += 3
    techniques = [
        "Chain-of-Thought: Force step-by-step reasoning for complex tasks",
        "Few-Shot Learning: Provide 2-3 examples of desired output format",
        "Role Stacking: Assign multiple expert personas for comprehensive answers",
        "Constraint Engineering: Use specific boundaries to control output quality",
        "Output Templating: Pre-define exact structure for consistent results",
        "Iterative Refinement: Build prompts that self-improve through feedback",
        "Context Windows: Strategically manage context for long-form projects",
    ]
    for tech in techniques:
        y = write_bullet_point(pdf, tech, y, TEAL)
    y += 3
    prompt2 = ("Create a prompt library for a [INDUSTRY] sales team.\n"
               "They need prompts for:\n"
               "1) Lead qualification (scoring criteria)\n"
               "2) Personalized outreach (email + LinkedIn)\n"
               "3) Objection handling (top 10 objections)\n"
               "4) Proposal generation (template)\n"
               "5) Follow-up sequences (3-5-7 day cadence)\n"
               "Each prompt should include: role, context placeholders,\n"
               "output format, quality criteria, and example output.")
    y = draw_prompt_box(pdf, y, "Sales Prompt Library Builder", prompt2, TEAL)

    # Page 28
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (80, 0, 120), (250, 240, 255), 15)
    draw_page_decoration(pdf, page_count)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Selling Your Prompt Services")
    y += 10
    text = ("The market for prompt engineering is exploding. Here's how to position "
            "yourself and attract high-paying clients:")
    y = write_body_text(pdf, text, y)
    y += 3
    strategies = [
        "Create a portfolio of before/after prompt transformations",
        "Share prompt tips on LinkedIn and Twitter (builds authority fast)",
        "Offer free 'prompt audits' to prospects - show them what's possible",
        "Partner with AI tool companies for referral revenue",
        "Create a 'Prompt ROI Calculator' showing time/money saved",
        "Target companies already using AI but getting poor results",
        "Offer workshops at $2K-5K for teams of 10-20 people",
    ]
    for strat in strategies:
        y = write_bullet_point(pdf, strat, y, ORANGE)
    y += 3
    text2 = ("Your unique advantage: you're not just writing prompts, you're designing "
             "AI workflows that transform entire business processes. Position yourself "
             "as an 'AI Transformation Consultant' and command premium pricing.")
    y = write_body_text(pdf, text2, y)
    draw_lightbulb(pdf, 35, PAGE_H - 50, 28)
    draw_brain_ai(pdf, PAGE_W / 2, PAGE_H - 50, 30)
    draw_diamond(pdf, PAGE_W - 35, PAGE_H - 50, 25)



    # ========================================================
    # CHAPTER 8: Digital Products & Templates (3 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 8, "Digital Products &", "Templates", draw_diamond)

    # Page 30
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (100, 50, 0), (255, 248, 235), 15)
    draw_page_decoration(pdf, page_count)
    draw_diamond(pdf, PAGE_W - 35, 40, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Passive Income with Digital Products")
    y += 10
    text = ("Digital products are the holy grail: create once, sell forever. Claude "
            "helps you create premium digital products in hours instead of weeks. "
            "Templates, courses, ebooks, swipe files - all with zero marginal cost.")
    y = write_body_text(pdf, text, y)
    y += 4
    products = [
        "Notion Template Packs: $27-97 each, sell 100+/month = $2.7K-$9.7K",
        "Online Courses: $197-997 each, 20 sales/month = $4K-$20K",
        "Prompt Libraries: $47-197 each, sell on Gumroad = $2K-$10K/month",
        "Business Templates: $37-147 (proposals, contracts, SOPs)",
        "AI Workflow Guides: $27-67 each, bundle for $197",
        "Swipe Files: $17-47 (email, ad copy, landing page collections)",
    ]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ORANGE)
    pdf.text(MARGIN, y, "High-Margin Digital Products:")
    y += 6
    for product in products:
        y = write_bullet_point(pdf, product, y, ORANGE)
    y += 3
    prompt = ("Create a comprehensive online course outline for:\n"
              "Topic: [COURSE TOPIC]\n"
              "Target student: [WHO IS THIS FOR]\n"
              "Desired outcome: [WHAT THEY'LL ACHIEVE]\n"
              "Course length: 6-8 modules\n"
              "For each module provide: title, learning objectives,\n"
              "3-5 lessons, assignments, and resources.\n"
              "Include a bonus module and upsell opportunity.\n"
              "Pricing strategy: $197 self-paced, $497 with coaching.")
    y = draw_prompt_box(pdf, y, "Course Outline Creator", prompt, ORANGE)

    # Page 31
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (100, 50, 0), (255, 248, 235), 15)
    draw_page_decoration(pdf, page_count)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Product Creation Workflow")
    y += 10
    text = ("Here's the 48-hour digital product creation framework using Claude:")
    y = write_body_text(pdf, text, y)
    y += 3
    workflow = [
        "Hour 1-2: Market research - find gaps using Claude analysis",
        "Hour 3-4: Outline creation - structure the product content",
        "Hour 5-12: Content generation - Claude writes 80% of material",
        "Hour 13-16: Design & formatting - professional presentation",
        "Hour 17-20: Sales page - Claude writes high-converting copy",
        "Hour 21-24: Email sequence - 5 emails for launch",
        "Hour 25-30: Landing page + payment setup (Gumroad/Teachable)",
        "Hour 31-48: Launch preparation - social proof, early reviews",
    ]
    for w in workflow:
        y = write_bullet_point(pdf, w, y, ACCENT_BLUE)
    y += 3
    prompt2 = ("Write a high-converting sales page for my digital product:\n"
               "Product: [NAME AND DESCRIPTION]\n"
               "Price: $[PRICE]\n"
               "Target buyer: [IDEAL CUSTOMER]\n"
               "Include: headline (benefit-focused), subheadline,\n"
               "3 pain points, 5 benefits, social proof section,\n"
               "FAQ (5 questions), guarantee, and CTA.\n"
               "Use proven copywriting frameworks (PAS, AIDA).\n"
               "Tone: Authoritative but friendly. Use power words.")
    y = draw_prompt_box(pdf, y, "Sales Page Writer", prompt2, RED)
    draw_money_stack(pdf, PAGE_W / 2, PAGE_H - 45, 30)



    # ========================================================
    # CHAPTER 9: The API Economy (3 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 9, "The API Economy",
                       "Build and monetize AI-powered APIs", draw_network)

    # Page 33
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 40, 80), (235, 245, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_network(pdf, PAGE_W - 40, 45, 30)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Monetizing the Claude API")
    y += 10
    text = ("The Claude API lets you build products that serve thousands of customers "
            "simultaneously. Create API endpoints that solve specific problems, charge "
            "per use or monthly, and scale to millions in revenue.")
    y = write_body_text(pdf, text, y)
    y += 4
    api_ideas = [
        "Content Generation API: Businesses pay per article generated",
        "Email Personalization API: E-commerce stores auto-personalize",
        "Document Summarizer API: Legal/medical document processing",
        "Code Review API: Automated PR reviews for dev teams",
        "Customer Sentiment API: Real-time brand monitoring",
        "Translation + Localization API: Context-aware translations",
    ]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_BLUE)
    pdf.text(MARGIN, y, "API Business Ideas:")
    y += 6
    for idea in api_ideas:
        y = write_bullet_point(pdf, idea, y, ACCENT_BLUE)
    y += 3
    prompt = ("Generate API documentation for my [SERVICE] API.\n"
              "Endpoints to document:\n"
              "- POST /generate: [DESCRIPTION]\n"
              "- GET /status: [DESCRIPTION]\n"
              "- POST /batch: [DESCRIPTION]\n"
              "For each endpoint include: description, parameters,\n"
              "request/response examples (JSON), error codes,\n"
              "rate limits, and authentication requirements.\n"
              "Format: OpenAPI 3.0 compatible documentation.\n"
              "Include a quick-start guide and code examples in\n"
              "Python, JavaScript, and cURL.")
    y = draw_prompt_box(pdf, y, "API Documentation Writer", prompt, ACCENT_BLUE)

    # Page 34
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 40, 80), (235, 245, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_laptop(pdf, PAGE_W - 40, 45, 30)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "API Business Architecture")
    y += 10
    text = ("Building a profitable API business requires the right architecture. "
            "Here's the stack that lets you scale to thousands of requests while "
            "keeping costs manageable:")
    y = write_body_text(pdf, text, y)
    y += 3
    stack = [
        "Frontend: Next.js dashboard for customer management",
        "API Gateway: FastAPI or Express with rate limiting",
        "AI Layer: Claude API with intelligent caching",
        "Database: PostgreSQL for users + Redis for caching",
        "Billing: Stripe metered billing per API call",
        "Monitoring: Track usage, costs, and quality metrics",
        "Documentation: Auto-generated with Swagger/OpenAPI",
    ]
    for item in stack:
        y = write_bullet_point(pdf, item, y, TEAL)
    y += 3
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*GOLD)
    pdf.text(MARGIN, y, "Revenue Model Example:")
    y += 6
    revenue_items = [
        "1,000 API calls/day x $0.05/call = $1,500/month",
        "Your Claude API cost: ~$300/month (with caching)",
        "Infrastructure: ~$100/month",
        "Net profit: $1,100/month from ONE customer",
        "Scale to 50 customers = $55,000/month profit",
    ]
    for item in revenue_items:
        y = write_bullet_point(pdf, item, y, GOLD)
    draw_chart_up(pdf, PAGE_W / 2, PAGE_H - 50, 38)
    draw_network(pdf, 35, PAGE_H - 45, 25)



    # ========================================================
    # CHAPTER 10: Scaling to Seven Figures (3 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 10, "Scaling to Seven Figures",
                       "The roadmap from $10K to $100K/month", draw_rocket)

    # Page 36
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (80, 0, 0), (255, 240, 240), 15)
    draw_page_decoration(pdf, page_count)
    draw_rocket(pdf, PAGE_W - 35, 50, 30)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "The Seven-Figure Scaling Framework")
    y += 10
    text = ("Getting to $10K/month is about hustle. Getting to $100K/month is about "
            "systems. Here's the exact framework for scaling your AI business to "
            "seven figures annually:")
    y = write_body_text(pdf, text, y)
    y += 4
    phases = [
        "Phase 1 ($0-10K): Validate one business model, land first clients",
        "Phase 2 ($10K-30K): Systematize delivery, build SOPs with Claude",
        "Phase 3 ($30K-50K): Hire VAs, automate client onboarding",
        "Phase 4 ($50K-80K): Add revenue streams, productize services",
        "Phase 5 ($80K-100K+): Build team, create leveraged offerings",
    ]
    for phase in phases:
        y = write_bullet_point(pdf, phase, y, RED)
    y += 4
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_BLUE)
    pdf.text(MARGIN, y, "Key Scaling Levers:")
    y += 6
    levers = [
        "Productize your service into repeatable packages",
        "Create systems documentation (Claude writes your SOPs)",
        "Build templates that VAs can execute without you",
        "Automate 80% of client communication",
        "Launch a complementary digital product for passive income",
        "Build referral systems that generate leads on autopilot",
    ]
    for lever in levers:
        y = write_bullet_point(pdf, lever, y, ACCENT_BLUE)
    draw_chart_up(pdf, PAGE_W / 2, PAGE_H - 50, 40)

    # Page 37
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (80, 0, 0), (255, 240, 240), 15)
    draw_page_decoration(pdf, page_count)
    draw_target(pdf, PAGE_W - 35, 40, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Building Your Revenue Stack")
    y += 10
    text = ("The fastest path to seven figures combines multiple revenue streams. "
            "Each stream reinforces the others, creating a compounding effect:")
    y = write_body_text(pdf, text, y)
    y += 3
    prompt = ("Create a financial model for my AI business:\n"
              "Current revenue: $[X]/month\n"
              "Business model: [DESCRIPTION]\n"
              "Target: $100K/month in 12 months\n"
              "Calculate: monthly growth rate needed, number of\n"
              "clients/products at each price point, team costs,\n"
              "tool costs, marketing budget, and profit margins.\n"
              "Present as a 12-month projection table with:\n"
              "Revenue | Costs | Profit | Growth Rate | Clients\n"
              "Include 3 scenarios: conservative, moderate, aggressive.")
    y = draw_prompt_box(pdf, y, "Financial Model Builder", prompt, GOLD)
    y += 3
    text2 = ("Stack these revenue streams: 1) Done-for-you services ($5K-15K/month), "
             "2) Group coaching ($3K-8K/month), 3) Digital products ($2K-5K/month), "
             "4) SaaS tools ($5K-20K/month), 5) Affiliate income ($1K-3K/month).")
    y = write_body_text(pdf, text2, y)
    draw_money_stack(pdf, 35, PAGE_H - 45, 28)
    draw_rocket(pdf, PAGE_W / 2, PAGE_H - 50, 30)
    draw_gold_coin(pdf, PAGE_W - 30, PAGE_H - 35, 10)



    # ========================================================
    # CHAPTER 11: Advanced Claude Techniques (4 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 11, "Advanced Claude Techniques",
                       "Master-level prompting for maximum output", draw_brain_ai)

    # Page 39
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 0, 80), (235, 235, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_brain_ai(pdf, PAGE_W - 35, 45, 28)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Chain-of-Thought Mastery")
    y += 10
    text = ("Chain-of-thought prompting forces Claude to show its reasoning, "
            "producing dramatically better outputs for complex tasks. This is "
            "the single most powerful technique for business applications.")
    y = write_body_text(pdf, text, y)
    y += 3
    prompt = ("You are a senior market research analyst.\n"
              "Task: Analyze the [MARKET] for a new [PRODUCT].\n"
              "\n"
              "Think step by step:\n"
              "Step 1: Identify the total addressable market (TAM)\n"
              "Step 2: Map the competitive landscape (top 5 players)\n"
              "Step 3: Identify underserved segments\n"
              "Step 4: Analyze pricing models in the market\n"
              "Step 5: Identify distribution channels\n"
              "Step 6: Assess barriers to entry\n"
              "Step 7: Synthesize into a go/no-go recommendation\n"
              "\n"
              "For each step, show your reasoning before concluding.")
    y = draw_prompt_box(pdf, y, "Market Research Analyst", prompt, ACCENT_BLUE)
    y += 3
    text2 = ("This structured approach consistently produces consultant-quality "
             "analysis that you can deliver to clients or use for your own decisions.")
    y = write_body_text(pdf, text2, y)
    draw_network(pdf, PAGE_W / 2, PAGE_H - 45, 30)

    # Page 40
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 0, 80), (235, 235, 255), 15)
    draw_page_decoration(pdf, page_count)
    draw_gear_system(pdf, PAGE_W - 40, 45, 30)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Multi-Agent Workflows")
    y += 10
    text = ("The most powerful technique is using Claude in multiple 'roles' within "
            "a single workflow. Each role specializes in one aspect, producing "
            "outputs that rival entire consulting teams.")
    y = write_body_text(pdf, text, y)
    y += 3
    prompt2 = ("I need you to analyze my business plan from 3 perspectives.\n"
               "\n"
               "ROLE 1 - Optimistic Investor:\n"
               "Evaluate [BUSINESS PLAN] as a VC looking for upside.\n"
               "Focus on: market opportunity, growth potential, moat.\n"
               "\n"
               "ROLE 2 - Devil's Advocate:\n"
               "Challenge every assumption. What could go wrong?\n"
               "Focus on: risks, weaknesses, competitive threats.\n"
               "\n"
               "ROLE 3 - Operations Expert:\n"
               "How would you execute this plan practically?\n"
               "Focus on: timeline, resources, milestones, KPIs.\n"
               "\n"
               "End with a synthesis combining all three perspectives.")
    y = draw_prompt_box(pdf, y, "Multi-Perspective Analyzer", prompt2, ACCENT_PURPLE)
    draw_brain_ai(pdf, 35, PAGE_H - 45, 25)
    draw_lightbulb(pdf, PAGE_W - 35, PAGE_H - 45, 25)

    # Page 41
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 0, 80), (235, 235, 255), 15)
    draw_page_decoration(pdf, page_count)
    y = 25
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Data Analysis & Insights")
    y += 10
    text = ("Claude excels at turning raw data into actionable business intelligence. "
            "Combine this with the API to create automated reporting systems that "
            "clients pay $3K-$10K/month for.")
    y = write_body_text(pdf, text, y)
    y += 3
    prompt3 = ("Analyze this dataset and provide business insights:\n"
               "[PASTE CSV DATA OR DESCRIBE DATASET]\n"
               "\n"
               "Provide:\n"
               "1) Executive Summary (3 key findings)\n"
               "2) Trend Analysis (what's improving/declining)\n"
               "3) Anomaly Detection (unusual patterns)\n"
               "4) Correlation Analysis (what factors relate)\n"
               "5) Predictive Insights (what's likely next)\n"
               "6) Actionable Recommendations (3-5 specific actions)\n"
               "\n"
               "Format as a board-ready report with clear headings.\n"
               "Include suggested visualizations for each insight.")
    y = draw_prompt_box(pdf, y, "Data Analyzer", prompt3, TEAL)
    y += 3
    text2 = ("Pro tip: Pair this with Python data processing to handle large datasets. "
             "Claude can write the analysis code AND interpret the results.")
    y = write_body_text(pdf, text2, y)
    draw_chart_up(pdf, PAGE_W / 2, PAGE_H - 50, 38)
    draw_laptop(pdf, 35, PAGE_H - 45, 25)



    # ========================================================
    # CHAPTER 12: Live Prompt Library (6 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 12, "Live Prompt Library",
                       "20+ ready-to-use prompts for every business model", draw_lightbulb)

    # Page 43 - Prompts 1-4
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 80, 50), (235, 255, 245), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Business Growth Prompts")
    y += 8
    draw_gold_coin(pdf, PAGE_W - 25, 18, 8)

    p1 = ("Write a business plan executive summary for [BUSINESS].\n"
           "Include: value proposition, target market ($TAM),\n"
           "revenue model, competitive advantage, 3-year projection,\n"
           "funding requirements, and team overview.\n"
           "Format: Investor-ready, 2 pages, data-driven.")
    y = draw_prompt_box(pdf, y, "Business Plan Writer", p1, ACCENT_GREEN)
    y += 2

    p2 = ("Generate a legal contract template for [SERVICE TYPE].\n"
           "Include: scope of work, payment terms, deliverables,\n"
           "timeline, revision policy, IP ownership, termination\n"
           "clause, liability limits, and confidentiality agreement.\n"
           "Note: For reference only - have lawyer review before use.")
    y = draw_prompt_box(pdf, y, "Contract Generator", p2, ACCENT_BLUE)
    y += 2

    p3 = ("Write a YouTube video script for a [NICHE] channel.\n"
           "Topic: [VIDEO TOPIC]\n"
           "Length: 10-12 minutes (aim for 1500-1800 words)\n"
           "Include: attention hook (first 30 sec), pattern interrupt\n"
           "every 2 min, storytelling elements, CTA, end screen pitch.\n"
           "Optimize for retention: open loops, curiosity gaps.")
    y = draw_prompt_box(pdf, y, "YouTube Script Writer", p3, RED)

    # Page 44 - Prompts 5-8
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 80, 50), (235, 255, 245), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Content & Marketing Prompts")
    y += 8
    draw_lightbulb(pdf, PAGE_W - 30, 20, 20)

    p4 = ("Write a weekly newsletter edition that converts readers.\n"
           "Topic: [THIS WEEK'S TOPIC]\n"
           "Audience: [TARGET READER PROFILE]\n"
           "Structure: Hook story (2-3 sentences), main insight,\n"
           "3 actionable takeaways, resource recommendation,\n"
           "soft CTA for [PRODUCT/SERVICE].\n"
           "Tone: Like a smart friend sharing insider knowledge.")
    y = draw_prompt_box(pdf, y, "Newsletter Writer", p4, ACCENT_PURPLE)
    y += 2

    p5 = ("Write 5 product descriptions for my e-commerce store.\n"
           "Product: [PRODUCT NAME AND DETAILS]\n"
           "Target buyer: [CUSTOMER AVATAR]\n"
           "For each: benefit-focused headline, 3-sentence description,\n"
           "5 bullet points (features as benefits), SEO keywords.\n"
           "Tone: Premium, desire-inducing, urgency elements.\n"
           "Include social proof placeholder and size/spec details.")
    y = draw_prompt_box(pdf, y, "Product Description Writer", p5, ORANGE)
    y += 2

    p6 = ("Create a social media content plan for [BRAND] across\n"
           "Instagram, Twitter/X, LinkedIn, and TikTok.\n"
           "Brand voice: [DESCRIBE PERSONALITY]\n"
           "Goals: [AWARENESS/ENGAGEMENT/CONVERSIONS]\n"
           "Create 7 days of posts: caption, hashtags, visual\n"
           "description, best time to post, engagement hooks.\n"
           "Mix: educational, entertaining, promotional, UGC prompts.")
    y = draw_prompt_box(pdf, y, "Social Media Manager", p6, TEAL)

    # Page 45 - Prompts 9-12
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 80, 50), (235, 255, 245), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Technical & Operations Prompts")
    y += 8
    draw_laptop(pdf, PAGE_W - 30, 20, 22)

    p7 = ("Analyze this meeting transcript and extract:\n"
           "[PASTE TRANSCRIPT OR KEY POINTS]\n"
           "1) Key decisions made (numbered list)\n"
           "2) Action items (who, what, deadline)\n"
           "3) Open questions requiring follow-up\n"
           "4) Risks or concerns raised\n"
           "5) Next meeting agenda suggestions\n"
           "Format as a 1-page executive summary email\n"
           "that I can send to all stakeholders.")
    y = draw_prompt_box(pdf, y, "Meeting Summarizer", p7, ACCENT_BLUE)
    y += 2

    p8 = ("Create a competitive analysis for [MY PRODUCT] vs:\n"
           "Competitor 1: [NAME]\n"
           "Competitor 2: [NAME]\n"
           "Competitor 3: [NAME]\n"
           "Compare: pricing, features, target market, strengths,\n"
           "weaknesses, market positioning, customer reviews.\n"
           "Identify: gaps we can exploit, threats to address,\n"
           "differentiation opportunities. End with strategy rec.")
    y = draw_prompt_box(pdf, y, "Competitive Analysis Prompt", p8, RED)
    y += 2

    p9 = ("Design a customer onboarding email sequence (7 emails)\n"
           "for my [PRODUCT TYPE] priced at $[PRICE]/month.\n"
           "Day 1: Welcome + quick start guide\n"
           "Day 2: Core feature tutorial\n"
           "Day 3: Success story / case study\n"
           "Day 5: Advanced tips + integration guide\n"
           "Day 7: Check-in + offer help\n"
           "Day 10: Feature highlight they haven't used\n"
           "Day 14: Testimonial request + referral ask")
    y = draw_prompt_box(pdf, y, "Onboarding Sequence Builder", p9, ACCENT_GREEN)



    # Page 46 - Prompts 13-16
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 80, 50), (235, 255, 245), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Revenue & Automation Prompts")
    y += 8
    draw_money_stack(pdf, PAGE_W - 30, 25, 22)

    p10 = ("Build a complete sales funnel strategy for [PRODUCT].\n"
            "Price point: $[PRICE]\n"
            "Traffic source: [PAID/ORGANIC/BOTH]\n"
            "Map out: lead magnet, tripwire offer ($7-27),\n"
            "core offer, upsell, downsell, and backend offer.\n"
            "For each stage: conversion rate targets, copy hooks,\n"
            "email sequences, and retargeting strategy.")
    y = draw_prompt_box(pdf, y, "Sales Funnel Architect", p10, GOLD)
    y += 2

    p11 = ("Create a podcast episode outline and script notes.\n"
            "Topic: [EPISODE TOPIC]\n"
            "Guest: [GUEST NAME AND BACKGROUND] (or solo ep)\n"
            "Length: 30-45 minutes\n"
            "Structure: Cold open hook, intro, 3 main segments,\n"
            "listener Q&A segment, key takeaways, CTA.\n"
            "Include: 10 interview questions that create great\n"
            "soundbites, and transition phrases between segments.")
    y = draw_prompt_box(pdf, y, "Podcast Producer", p11, ACCENT_PURPLE)
    y += 2

    p12 = ("Create a webinar presentation outline + script for\n"
            "selling [PRODUCT/SERVICE] at $[PRICE].\n"
            "Webinar length: 60 minutes\n"
            "Structure: 0-5 min hook, 5-15 story, 15-40 content,\n"
            "40-50 transition to offer, 50-60 close + Q&A.\n"
            "Include: slide titles, key points per slide,\n"
            "objection handling, scarcity elements, bonuses stack.\n"
            "Target conversion rate: 5-15% of attendees.")
    y = draw_prompt_box(pdf, y, "Webinar Script Creator", p12, ORANGE)

    # Page 47 - Prompts 17-20
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 80, 50), (235, 255, 245), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Advanced Business Prompts")
    y += 8
    draw_diamond(pdf, PAGE_W - 25, 18, 18)

    p13 = ("Create an affiliate program structure for [PRODUCT].\n"
            "Product price: $[PRICE]\n"
            "Commission structure, tier system, recruitment\n"
            "email templates, affiliate onboarding sequence,\n"
            "swipe copy for affiliates, tracking KPIs,\n"
            "and a 90-day affiliate recruitment strategy.\n"
            "Include: top 10 affiliate outreach messages.")
    y = draw_prompt_box(pdf, y, "Affiliate Program Builder", p13, ACCENT_GREEN)
    y += 2

    p14 = ("Design a customer retention strategy for my\n"
            "[SaaS/SERVICE] with [X] monthly churn rate.\n"
            "Current MRR: $[X]\n"
            "Analyze: churn causes, retention hooks to add,\n"
            "re-engagement campaigns, loyalty program design,\n"
            "NPS improvement tactics, success milestones,\n"
            "and an early warning system for at-risk accounts.\n"
            "Target: reduce churn from [X]% to [Y]% in 90 days.")
    y = draw_prompt_box(pdf, y, "Retention Strategy Designer", p14, TEAL)
    y += 2

    p15 = ("Create a hiring and delegation framework for my\n"
            "[BUSINESS TYPE] currently at $[X]/month revenue.\n"
            "I work [X] hours/week. Identify:\n"
            "1) Tasks to delegate immediately (VA-level)\n"
            "2) Tasks to automate with AI\n"
            "3) Tasks that require skilled contractors\n"
            "4) Tasks only I should do (zone of genius)\n"
            "For each hire: role, job description, where to find,\n"
            "compensation range, and onboarding checklist.")
    y = draw_prompt_box(pdf, y, "Delegation Framework", p15, ACCENT_BLUE)
    draw_gear_system(pdf, PAGE_W / 2, PAGE_H - 40, 30)



    # ========================================================
    # CHAPTER 13: Case Studies (4 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 13, "Case Studies",
                       "Real-world success stories with real numbers", draw_chart_up)

    # Page 49 - Case Studies 1 & 2
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 60, 0), (240, 255, 240), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "From Zero to Life-Changing Income")
    y += 10
    draw_chart_up(pdf, PAGE_W - 35, 25, 25)

    y = draw_case_study_box(pdf, y,
        "Solo Dev to $50K/month",
        "$50K/mo",
        "Marcus built 3 micro-SaaS tools using Claude for code generation. Tool 1: AI email warmup ($19/mo, 800 users). Tool 2: Meeting summarizer ($15/mo, 1200 users). Tool 3: Proposal generator ($49/mo, 400 users). Total build time: 6 weekends. Monthly revenue: $51,400.",
        "6 months from first line of code to $50K MRR")
    y += 3

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_BLUE)
    pdf.text(MARGIN + 5, y, "Key Strategies Used:")
    y += 5
    strategies1 = [
        "Used Claude to generate 90% of codebase, focused on product decisions",
        "Launched each tool on Product Hunt (top 5 of the day for all 3)",
        "SEO content strategy: 30 articles/month driving 50K organic visits",
        "Built in public on Twitter - grew to 15K followers who became early users",
        "Offered lifetime deals at launch for initial cash flow + testimonials",
    ]
    for s in strategies1:
        y = write_bullet_point(pdf, s, y, ACCENT_GREEN)
    y += 5

    y = draw_case_study_box(pdf, y,
        "Agency Owner: $0 to $30K in 90 Days",
        "$30K/mo",
        "Sarah launched an AI copywriting agency with zero experience. Used Claude to deliver blog posts, email sequences, and ad copy for e-commerce brands. Started with $500 clients on Upwork, scaled to $5K retainer clients through LinkedIn outreach. Now manages 8 clients with 2 VAs.",
        "90 days from launch to $30K monthly revenue")
    y += 3

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_BLUE)
    pdf.text(MARGIN + 5, y, "Key Strategies Used:")
    y += 5
    strategies2 = [
        "Specialized in e-commerce email marketing (high-value niche)",
        "Created portfolio samples in day 1 using Claude",
        "Cold DM'd 50 e-commerce founders daily on LinkedIn",
        "Offered free 'email audit' as lead magnet - converted 20% to clients",
        "Systemized delivery: each client takes 3 hours/week with Claude",
    ]
    for s in strategies2:
        y = write_bullet_point(pdf, s, y, ACCENT_GREEN)

    # Page 50 - Case Studies 3 & 4
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 60, 0), (240, 255, 240), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "More Success Stories")
    y += 10
    draw_rocket(pdf, PAGE_W - 35, 25, 25)

    y = draw_case_study_box(pdf, y,
        "Content Creator: 100K Subscribers in 6 Months",
        "$25K/mo",
        "Jake started a daily newsletter about AI business opportunities. Used Claude to research, write, and optimize every edition. Grew from 0 to 100K subscribers in 6 months. Revenue: $15K/month sponsorships + $10K/month from digital product recommendations. Works 2 hours/day.",
        "6 months from first newsletter to 100K subscribers")
    y += 3

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_BLUE)
    pdf.text(MARGIN + 5, y, "Growth Tactics:")
    y += 5
    strategies3 = [
        "Published daily (Claude generated 80% of each edition)",
        "Cross-promoted with 20 other newsletters in AI/business space",
        "Twitter thread strategy: 3 viral threads/week driving signups",
        "Referral program: subscribers get bonus content for sharing",
        "Monetized at 10K subscribers with first sponsor ($2K/edition)",
    ]
    for s in strategies3:
        y = write_bullet_point(pdf, s, y, ACCENT_PURPLE)
    y += 5

    y = draw_case_study_box(pdf, y,
        "Automation Consultant: $15K/month Retainer",
        "$15K/mo",
        "David positioned himself as an 'AI Workflow Architect' for real estate companies. Built custom automation systems using Claude API + Zapier + custom scripts. One flagship client pays $15K/month retainer for ongoing optimization. Total time: 20 hours/week across 3 clients ($45K/month total).",
        "4 months from first client to $15K/month single retainer")
    y += 3

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*ACCENT_BLUE)
    pdf.text(MARGIN + 5, y, "Key Strategies:")
    y += 5
    strategies4 = [
        "Hyper-niched into real estate (high budgets, tech-unsavvy clients)",
        "Created a 'free automation audit' that identifies $50K+ in savings",
        "Built demo automations that wow prospects in 15-min calls",
        "Charges setup fee ($10K) + monthly retainer ($5K-15K)",
        "Documented all systems so VAs can maintain while he sells",
    ]
    for s in strategies4:
        y = write_bullet_point(pdf, s, y, ACCENT_PURPLE)
    draw_money_stack(pdf, PAGE_W / 2, PAGE_H - 45, 30)

    # Page 51 - Lessons Learned
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (0, 60, 0), (240, 255, 240), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Common Patterns of Success")
    y += 10
    draw_target(pdf, PAGE_W - 35, 30, 25)

    text = ("After analyzing dozens of successful AI entrepreneurs, these patterns "
            "emerge consistently:")
    y = write_body_text(pdf, text, y)
    y += 4
    patterns = [
        "Start with services (immediate revenue) then productize",
        "Niche down aggressively - generalists struggle, specialists thrive",
        "Build in public - share your journey to attract clients and partners",
        "Speed over perfection - launch fast, iterate based on feedback",
        "Stack multiple revenue streams - don't rely on a single income source",
        "Invest in relationships - partnerships accelerate growth 10x",
        "Document everything - SOPs enable delegation and scaling",
        "Reinvest 30% of revenue into tools, education, and marketing",
        "Focus on high-value clients - 5 clients at $10K > 50 at $1K",
        "Use AI for delivery AND for business development",
    ]
    for p in patterns:
        y = write_bullet_point(pdf, p, y, GOLD)
    y += 5
    text2 = ("The biggest lesson: speed of implementation matters more than perfection. "
             "Those who take action within 48 hours of learning a strategy outperform "
             "those who spend weeks planning by 10x.")
    y = write_body_text(pdf, text2, y)
    draw_rocket(pdf, 35, PAGE_H - 50, 28)
    draw_chart_up(pdf, PAGE_W / 2, PAGE_H - 50, 35)
    draw_diamond(pdf, PAGE_W - 35, PAGE_H - 50, 25)



    # ========================================================
    # CHAPTER 14: Your 90-Day Action Plan (3 pages)
    # ========================================================
    pdf.add_page()
    page_count += 1
    add_chapter_header(pdf, 14, "Your 90-Day Action Plan",
                       "Week-by-week roadmap to your first $10K month", draw_target)

    # Page 53
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (80, 40, 0), (255, 248, 235), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Weeks 1-6: Foundation & First Revenue")
    y += 10
    draw_target(pdf, PAGE_W - 35, 25, 22)

    text = ("This is your detailed week-by-week plan. Follow it exactly and you'll "
            "have revenue within 30 days and momentum that compounds.")
    y = write_body_text(pdf, text, y)
    y += 3

    weeks_1_6 = [
        ("Week 1", "Choose your primary model (Chapter 3-9). Set up Claude Pro. "
         "Create 5 portfolio samples. Set up basic website/profile."),
        ("Week 2", "Build your outreach system. Write 10 cold email templates with Claude. "
         "Identify 100 potential clients. Begin daily outreach (20/day)."),
        ("Week 3", "Land your first client (even at a discount). Deliver exceptional work. "
         "Document your process. Get a testimonial and case study."),
        ("Week 4", "Raise your prices 50%. Continue outreach. Optimize your delivery "
         "workflow. Start creating content about your expertise."),
        ("Week 5", "Add a second service offering. Cross-sell existing clients. "
         "Build your email list. Create a lead magnet with Claude."),
        ("Week 6", "Systematize: create SOPs for every task. Test delegating one task "
         "to a VA. Revenue target: $3,000-$5,000/month."),
    ]
    for week, desc in weeks_1_6:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(*ORANGE)
        pdf.text(MARGIN + 3, y, week)
        y += 4
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(50, 50, 70)
        # Wrap description
        lines = [desc[i:i+85] for i in range(0, len(desc), 85)]
        for line in lines:
            pdf.text(MARGIN + 8, y, line)
            y += 3.8
        y += 2.5
    draw_chart_up(pdf, PAGE_W / 2, PAGE_H - 40, 32)

    # Page 54
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, 15, (80, 40, 0), (255, 248, 235), 15)
    draw_page_decoration(pdf, page_count)
    y = 20
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DEEP_BLUE)
    pdf.text(MARGIN, y, "Weeks 7-12: Scale & Systemize")
    y += 10
    draw_rocket(pdf, PAGE_W - 35, 25, 22)

    weeks_7_12 = [
        ("Week 7", "Launch a digital product using Chapter 8. Use existing client work "
         "as templates. Price at $47-197. Goal: 10 sales in first week."),
        ("Week 8", "Implement automation from Chapter 6 in your own business. "
         "Reduce your delivery time by 50%. Take on more clients."),
        ("Week 9", "Start content marketing engine. Publish 3 pieces/week with Claude. "
         "Build authority. Begin getting inbound leads."),
        ("Week 10", "Raise prices again (premium positioning). Fire bottom 20% of clients. "
         "Implement retainer model for stability."),
        ("Week 11", "Add passive income stream: course, templates, or SaaS. "
         "Use everything you've learned to create a scalable product."),
        ("Week 12", "Hire additional VA support. Create your 'CEO dashboard' for tracking. "
         "Revenue target: $8,000-$12,000/month."),
    ]
    for week, desc in weeks_7_12:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(*ORANGE)
        pdf.text(MARGIN + 3, y, week)
        y += 4
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(50, 50, 70)
        lines = [desc[i:i+85] for i in range(0, len(desc), 85)]
        for line in lines:
            pdf.text(MARGIN + 8, y, line)
            y += 3.8
        y += 2.5
    y += 3
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*ACCENT_GREEN)
    pdf.text(MARGIN, y, "90-Day Target: $10,000-$15,000/month in combined revenue")
    y += 6
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(50, 50, 70)
    text = ("After 90 days, you'll have: proven revenue model, systematized delivery, "
            "growing content presence, passive income stream in development, and a clear "
            "path to $30K-50K/month within 6 months.")
    y = write_body_text(pdf, text, y)
    draw_money_stack(pdf, 35, PAGE_H - 40, 25)
    draw_target(pdf, PAGE_W / 2, PAGE_H - 40, 25)
    draw_gold_coin(pdf, PAGE_W - 30, PAGE_H - 35, 10)



    # ========================================================
    # FINAL WORDS (2 pages)
    # ========================================================
    # Page 55
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, PAGE_H, DEEP_BLUE, DARK_BG, 60)
    # Gold border
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(1.5)
    pdf.rect(10, 10, PAGE_W - 20, PAGE_H - 20, 'D')

    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(*GOLD)
    title = "Final Words"
    tw = pdf.get_string_width(title)
    pdf.text(PAGE_W / 2 - tw / 2, 40, title)

    # Decorative elements
    draw_brain_ai(pdf, PAGE_W / 2, 75, 35)

    y = 105
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*WHITE)
    paragraphs = [
        "You now have everything you need to build a six or seven-figure income with Claude AI.",
        "",
        "The prompts in this book are not theoretical - they are battle-tested by real",
        "entrepreneurs generating real revenue. The case studies are based on documented",
        "results from people who started exactly where you are now.",
        "",
        "The difference between those who succeed and those who don't is simple: ACTION.",
        "Don't just read this book - USE it. Open Claude right now and try your first prompt.",
        "",
        "Here's your immediate next step:",
        "1. Choose ONE business model from Chapters 3-9",
        "2. Copy the relevant prompts from Chapter 12",
        "3. Generate your first piece of client-ready work TODAY",
        "4. Follow the 90-Day Plan in Chapter 14",
        "",
        "The AI wealth revolution is happening NOW. Every day you wait is a day your",
        "future competitors are building their businesses. You have the blueprint.",
        "You have the tools. The only variable is YOU.",
    ]
    for line in paragraphs:
        pdf.text(MARGIN + 10, y, line)
        y += 5.5

    # Bottom decorations
    draw_gold_coin(pdf, 30, PAGE_H - 45, 10)
    draw_gold_coin(pdf, 55, PAGE_H - 40, 8)
    draw_rocket(pdf, PAGE_W / 2, PAGE_H - 45, 28)
    draw_gold_coin(pdf, PAGE_W - 55, PAGE_H - 40, 8)
    draw_gold_coin(pdf, PAGE_W - 30, PAGE_H - 45, 10)

    # Page 56 - Back cover
    pdf.add_page()
    page_count += 1
    draw_gradient_rect(pdf, 0, 0, PAGE_W, PAGE_H, (0, 0, 0), DEEP_BLUE, 80)
    # Gold frame
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(2)
    pdf.rect(8, 8, PAGE_W - 16, PAGE_H - 16, 'D')

    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(*GOLD)
    title = "THE CLAUDE AI MILLIONAIRE BLUEPRINT"
    tw = pdf.get_string_width(title)
    pdf.text(PAGE_W / 2 - tw / 2, 40, title)

    # What's inside summary
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*WHITE)
    pdf.text(PAGE_W / 2 - 30, 60, "What's Inside:")

    y = 72
    items = [
        "7 Proven Business Models",
        "20+ Copy-Paste Prompts",
        "4 Detailed Case Studies",
        "90-Day Action Plan",
        "Scaling Framework to $100K/month",
        "Advanced AI Techniques",
        "Financial Modeling Templates",
    ]
    for item in items:
        pdf.set_fill_color(*GOLD)
        pdf.ellipse(MARGIN + 20, y - 2, 3, 3, 'F')
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(*WHITE)
        pdf.text(MARGIN + 27, y, item)
        y += 10

    # Central graphic
    draw_brain_ai(pdf, PAGE_W / 2, 180, 45)

    # Bottom graphics row
    draw_gold_coin(pdf, 35, 240, 12)
    draw_chart_up(pdf, 80, 240, 30)
    draw_rocket(pdf, PAGE_W / 2, 240, 30)
    draw_money_stack(pdf, PAGE_W - 80, 240, 28)
    draw_diamond(pdf, PAGE_W - 35, 240, 20)

    # Final tagline
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*ACCENT_GREEN)
    tagline = "Your AI-Powered Path to Financial Freedom Starts Today"
    tw = pdf.get_string_width(tagline)
    pdf.text(PAGE_W / 2 - tw / 2, 275, tagline)

    # ========================================================
    # SAVE PDF
    # ========================================================
    output_path = '/projects/sandbox/new/claude_millionaire_blueprint.pdf'
    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")
    print(f"Total pages: {page_count}")
    return output_path, page_count


if __name__ == "__main__":
    path, pages = generate_ebook()
    print(f"\nGenerated: {path}")
    print(f"Pages: {pages}")
