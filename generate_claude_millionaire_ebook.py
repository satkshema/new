#!/usr/bin/env python3
"""
Generate a professional e-book PDF: "The Claude AI Millionaire Blueprint"
Uses fpdf2 with high-resolution graphics drawn using primitives.
"""

import math
from fpdf import FPDF


class MillionaireBook(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, "The Claude AI Millionaire Blueprint", align="C")
            self.ln(5)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f"- {self.page_no()} -", align="C")



# ─── HIGH-RESOLUTION GRAPHIC DRAWING FUNCTIONS ─────────────────────────────

def draw_gradient_rect(pdf, x, y, w, h, r1, g1, b1, r2, g2, b2, steps=40):
    """Draw a gradient rectangle from color1 to color2 (top to bottom)."""
    step_h = h / steps
    for i in range(steps):
        r = int(r1 + (r2 - r1) * i / steps)
        g = int(g1 + (g2 - g1) * i / steps)
        b = int(b1 + (b2 - b1) * i / steps)
        pdf.set_fill_color(r, g, b)
        pdf.rect(x, y + i * step_h, w, step_h + 0.5, style="F")


def draw_circle_filled(pdf, cx, cy, r, red, green, blue):
    """Draw a filled circle."""
    pdf.set_fill_color(red, green, blue)
    pdf.set_draw_color(red, green, blue)
    pdf.circle(cx, cy, r, style="FD")


def draw_gold_coin(pdf, cx, cy, r):
    """Draw a detailed gold coin graphic."""
    # Outer ring
    pdf.set_fill_color(218, 165, 32)
    pdf.set_draw_color(184, 134, 11)
    pdf.circle(cx, cy, r, style="FD")
    # Inner ring
    pdf.set_fill_color(255, 215, 0)
    pdf.set_draw_color(218, 165, 32)
    pdf.circle(cx, cy, r * 0.8, style="FD")
    # Dollar sign
    pdf.set_draw_color(184, 134, 11)
    pdf.set_line_width(0.5)
    pdf.line(cx, cy - r * 0.4, cx, cy + r * 0.4)
    # S shape approximation
    pts_top = []
    for i in range(8):
        angle = math.radians(180 + i * 22.5)
        pts_top.append((cx + r * 0.25 * math.cos(angle),
                       cy - r * 0.15 + r * 0.15 * math.sin(angle)))
    for i in range(len(pts_top) - 1):
        pdf.line(pts_top[i][0], pts_top[i][1],
                pts_top[i+1][0], pts_top[i+1][1])
    pts_bot = []
    for i in range(8):
        angle = math.radians(i * 22.5)
        pts_bot.append((cx + r * 0.25 * math.cos(angle),
                       cy + r * 0.15 + r * 0.15 * math.sin(angle)))
    for i in range(len(pts_bot) - 1):
        pdf.line(pts_bot[i][0], pts_bot[i][1],
                pts_bot[i+1][0], pts_bot[i+1][1])
    pdf.set_line_width(0.3)



def draw_brain_ai(pdf, cx, cy, size=25):
    """Draw an AI brain graphic with circuit patterns."""
    # Brain outline (two hemispheres)
    pdf.set_draw_color(75, 0, 130)
    pdf.set_line_width(0.5)
    # Left hemisphere
    pts_l = []
    for i in range(15):
        angle = math.radians(90 + i * 12)
        pts_l.append((cx + size * 0.5 * math.cos(angle),
                     cy + size * 0.6 * math.sin(angle)))
    pdf.polyline(pts_l)
    # Right hemisphere
    pts_r = []
    for i in range(15):
        angle = math.radians(-90 + i * 12)
        pts_r.append((cx + size * 0.5 * math.cos(angle),
                     cy + size * 0.6 * math.sin(angle)))
    pdf.polyline(pts_r)
    # Circuit nodes
    pdf.set_fill_color(138, 43, 226)
    for i in range(6):
        angle = math.radians(i * 60)
        nx = cx + size * 0.3 * math.cos(angle)
        ny = cy + size * 0.35 * math.sin(angle)
        pdf.circle(nx, ny, 1.5, style="FD")
    # Circuit lines
    pdf.set_draw_color(138, 43, 226)
    pdf.set_line_width(0.3)
    for i in range(6):
        angle1 = math.radians(i * 60)
        angle2 = math.radians((i + 2) * 60)
        x1 = cx + size * 0.3 * math.cos(angle1)
        y1 = cy + size * 0.35 * math.sin(angle1)
        x2 = cx + size * 0.3 * math.cos(angle2)
        y2 = cy + size * 0.35 * math.sin(angle2)
        pdf.line(x1, y1, x2, y2)
    # Outer glow dots
    pdf.set_fill_color(200, 150, 255)
    for i in range(12):
        angle = math.radians(i * 30)
        dx = cx + size * 0.7 * math.cos(angle)
        dy = cy + size * 0.7 * math.sin(angle)
        pdf.circle(dx, dy, 0.8, style="F")
    pdf.set_line_width(0.3)



def draw_rocket(pdf, cx, cy, size=20):
    """Draw a rocket ship graphic (growth/launch metaphor)."""
    pdf.set_draw_color(50, 50, 50)
    pdf.set_line_width(0.4)
    # Body
    pdf.set_fill_color(230, 230, 250)
    body_pts = [
        (cx, cy - size),
        (cx + size * 0.25, cy - size * 0.6),
        (cx + size * 0.25, cy + size * 0.4),
        (cx - size * 0.25, cy + size * 0.4),
        (cx - size * 0.25, cy - size * 0.6),
    ]
    pdf.polygon(body_pts, style="FD")
    # Nose cone
    pdf.set_fill_color(255, 100, 100)
    nose_pts = [
        (cx, cy - size),
        (cx + size * 0.25, cy - size * 0.6),
        (cx - size * 0.25, cy - size * 0.6),
    ]
    pdf.polygon(nose_pts, style="FD")
    # Fins
    pdf.set_fill_color(100, 149, 237)
    fin_l = [
        (cx - size * 0.25, cy + size * 0.2),
        (cx - size * 0.5, cy + size * 0.5),
        (cx - size * 0.25, cy + size * 0.4),
    ]
    pdf.polygon(fin_l, style="FD")
    fin_r = [
        (cx + size * 0.25, cy + size * 0.2),
        (cx + size * 0.5, cy + size * 0.5),
        (cx + size * 0.25, cy + size * 0.4),
    ]
    pdf.polygon(fin_r, style="FD")
    # Flame
    pdf.set_fill_color(255, 165, 0)
    flame_pts = [
        (cx - size * 0.15, cy + size * 0.4),
        (cx, cy + size * 0.7),
        (cx + size * 0.15, cy + size * 0.4),
    ]
    pdf.polygon(flame_pts, style="FD")
    # Window
    pdf.set_fill_color(135, 206, 235)
    pdf.circle(cx, cy - size * 0.3, size * 0.12, style="FD")


def draw_chart_up(pdf, x, y, w, h):
    """Draw an upward trending chart graphic."""
    pdf.set_draw_color(50, 50, 50)
    pdf.set_line_width(0.4)
    # Axes
    pdf.line(x, y + h, x + w, y + h)  # x-axis
    pdf.line(x, y, x, y + h)  # y-axis
    # Bars with gradient feel
    bar_w = w / 8
    heights = [0.2, 0.3, 0.28, 0.45, 0.5, 0.65, 0.85, 1.0]
    colors = [
        (100, 200, 100), (80, 190, 80), (60, 180, 60),
        (50, 170, 50), (40, 160, 40), (30, 150, 30),
        (20, 140, 20), (10, 130, 10)
    ]
    for i, ht in enumerate(heights):
        bar_h = h * ht * 0.9
        bx = x + 2 + i * bar_w
        by = y + h - bar_h
        pdf.set_fill_color(*colors[i])
        pdf.set_draw_color(20, 100, 20)
        pdf.rect(bx, by, bar_w - 2, bar_h, style="FD")
    # Trend line
    pdf.set_draw_color(255, 50, 50)
    pdf.set_line_width(0.6)
    for i in range(len(heights) - 1):
        x1 = x + 2 + i * bar_w + bar_w / 2
        y1 = y + h - h * heights[i] * 0.9
        x2 = x + 2 + (i + 1) * bar_w + bar_w / 2
        y2 = y + h - h * heights[i + 1] * 0.9
        pdf.line(x1, y1, x2, y2)
    pdf.set_line_width(0.3)
    pdf.set_draw_color(0, 0, 0)



def draw_network(pdf, cx, cy, size=30):
    """Draw a network/connection diagram."""
    pdf.set_draw_color(70, 130, 180)
    pdf.set_line_width(0.3)
    nodes = []
    for i in range(8):
        angle = math.radians(i * 45)
        nx = cx + size * math.cos(angle)
        ny = cy + size * 0.7 * math.sin(angle)
        nodes.append((nx, ny))
    # Connect nodes
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if (j - i) <= 3:
                pdf.set_draw_color(180, 200, 230)
                pdf.line(nodes[i][0], nodes[i][1],
                        nodes[j][0], nodes[j][1])
    # Draw nodes
    for nx, ny in nodes:
        pdf.set_fill_color(70, 130, 180)
        pdf.circle(nx, ny, 2.5, style="FD")
    # Center node (larger)
    pdf.set_fill_color(255, 215, 0)
    pdf.set_draw_color(218, 165, 32)
    pdf.circle(cx, cy, 4, style="FD")
    pdf.set_draw_color(0, 0, 0)


def draw_lightbulb(pdf, cx, cy, size=15):
    """Draw a lightbulb (ideas) graphic."""
    pdf.set_draw_color(218, 165, 32)
    pdf.set_fill_color(255, 255, 200)
    pdf.set_line_width(0.4)
    # Bulb
    pts = []
    for i in range(20):
        angle = math.radians(-180 + i * 18)
        if angle < math.radians(0):
            pts.append((cx + size * 0.4 * math.cos(math.radians(-180 + i * 18)),
                       cy + size * 0.5 * math.sin(math.radians(-180 + i * 18))))
    for i in range(11):
        angle = math.radians(i * 18)
        pts.append((cx + size * 0.4 * math.cos(angle),
                   cy - size * 0.1 + size * 0.5 * math.sin(angle)))
    if pts:
        pdf.polygon(pts, style="FD")
    # Base
    pdf.set_fill_color(192, 192, 192)
    pdf.rect(cx - size * 0.15, cy + size * 0.35, size * 0.3, size * 0.15, style="FD")
    # Rays
    pdf.set_draw_color(255, 200, 0)
    pdf.set_line_width(0.5)
    for i in range(8):
        angle = math.radians(i * 45 - 90)
        x1 = cx + size * 0.55 * math.cos(angle)
        y1 = cy - size * 0.1 + size * 0.55 * math.sin(angle)
        x2 = cx + size * 0.75 * math.cos(angle)
        y2 = cy - size * 0.1 + size * 0.75 * math.sin(angle)
        pdf.line(x1, y1, x2, y2)
    pdf.set_line_width(0.3)
    pdf.set_draw_color(0, 0, 0)


def draw_money_stack(pdf, x, y, layers=5):
    """Draw a stack of money/bills."""
    for i in range(layers):
        ly = y - i * 3
        # Bill
        pdf.set_fill_color(140 + i * 10, 200 + i * 5, 140 + i * 10)
        pdf.set_draw_color(50, 120, 50)
        pdf.rect(x, ly, 30, 12, style="FD")
        # Dollar symbol
        pdf.set_draw_color(30, 80, 30)
        pdf.circle(x + 15, ly + 6, 3, style="D")
    pdf.set_draw_color(0, 0, 0)



def draw_gear_system(pdf, cx, cy, size=12):
    """Draw interconnected gears (automation)."""
    def draw_gear(pdf, gx, gy, r, teeth=8):
        pdf.set_draw_color(100, 100, 120)
        pdf.set_fill_color(200, 210, 220)
        pts = []
        for i in range(teeth * 2):
            angle = math.radians(i * 180 / teeth)
            cr = r if i % 2 == 0 else r * 0.75
            pts.append((gx + cr * math.cos(angle), gy + cr * math.sin(angle)))
        pdf.polygon(pts, style="FD")
        pdf.set_fill_color(150, 160, 170)
        pdf.circle(gx, gy, r * 0.25, style="FD")

    draw_gear(pdf, cx - size, cy, size, 8)
    draw_gear(pdf, cx + size * 0.8, cy - size * 0.5, size * 0.7, 6)
    draw_gear(pdf, cx + size * 0.5, cy + size * 0.9, size * 0.5, 6)
    pdf.set_draw_color(0, 0, 0)


def draw_laptop(pdf, cx, cy, size=20):
    """Draw a laptop with code on screen."""
    pdf.set_draw_color(50, 50, 50)
    pdf.set_line_width(0.4)
    # Screen
    pdf.set_fill_color(40, 44, 52)
    pdf.rect(cx - size, cy - size * 0.6, size * 2, size * 1.1, style="FD")
    # Screen content (code lines)
    pdf.set_draw_color(97, 175, 239)
    code_lines = [0.2, 0.35, 0.5, 0.25, 0.45, 0.3, 0.4]
    for i, ln_w in enumerate(code_lines):
        ly = cy - size * 0.45 + i * size * 0.14
        colors = [(97, 175, 239), (229, 192, 123), (152, 195, 121),
                 (198, 120, 221), (86, 182, 194), (224, 108, 117), (209, 154, 102)]
        pdf.set_draw_color(*colors[i % len(colors)])
        pdf.set_line_width(1.2)
        pdf.line(cx - size * 0.8, ly, cx - size * 0.8 + size * 1.6 * ln_w, ly)
    pdf.set_line_width(0.4)
    # Base/keyboard
    pdf.set_fill_color(180, 180, 190)
    pdf.set_draw_color(50, 50, 50)
    base_pts = [
        (cx - size * 1.2, cy + size * 0.5),
        (cx + size * 1.2, cy + size * 0.5),
        (cx + size * 1.1, cy + size * 0.65),
        (cx - size * 1.1, cy + size * 0.65),
    ]
    pdf.polygon(base_pts, style="FD")
    pdf.set_line_width(0.3)
    pdf.set_draw_color(0, 0, 0)


def draw_diamond(pdf, cx, cy, size=10):
    """Draw a diamond/gem graphic."""
    pdf.set_draw_color(0, 100, 200)
    pdf.set_fill_color(180, 220, 255)
    pdf.set_line_width(0.4)
    # Top facets
    top_pts = [
        (cx, cy - size),
        (cx + size * 0.6, cy - size * 0.3),
        (cx + size, cy),
        (cx - size, cy),
        (cx - size * 0.6, cy - size * 0.3),
    ]
    pdf.polygon(top_pts, style="FD")
    # Bottom point
    pdf.set_fill_color(100, 180, 255)
    bot_pts = [
        (cx - size, cy),
        (cx + size, cy),
        (cx, cy + size * 1.2),
    ]
    pdf.polygon(bot_pts, style="FD")
    # Facet lines
    pdf.set_draw_color(60, 140, 220)
    pdf.line(cx - size * 0.6, cy - size * 0.3, cx, cy)
    pdf.line(cx + size * 0.6, cy - size * 0.3, cx, cy)
    pdf.line(cx, cy, cx, cy + size * 1.2)
    pdf.set_draw_color(0, 0, 0)



def draw_shield(pdf, cx, cy, size=15):
    """Draw a shield (security/trust) graphic."""
    pdf.set_draw_color(50, 50, 150)
    pdf.set_fill_color(70, 130, 180)
    pdf.set_line_width(0.5)
    pts = [
        (cx, cy - size),
        (cx + size * 0.8, cy - size * 0.6),
        (cx + size * 0.8, cy + size * 0.2),
        (cx, cy + size),
        (cx - size * 0.8, cy + size * 0.2),
        (cx - size * 0.8, cy - size * 0.6),
    ]
    pdf.polygon(pts, style="FD")
    # Checkmark
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(1.0)
    pdf.line(cx - size * 0.3, cy, cx - size * 0.05, cy + size * 0.3)
    pdf.line(cx - size * 0.05, cy + size * 0.3, cx + size * 0.35, cy - size * 0.3)
    pdf.set_line_width(0.3)
    pdf.set_draw_color(0, 0, 0)


def draw_target(pdf, cx, cy, size=15):
    """Draw a target/bullseye graphic."""
    colors = [(220, 50, 50), (255, 255, 255), (220, 50, 50), (255, 255, 255)]
    for i, (r, g, b) in enumerate(colors):
        radius = size * (1 - i * 0.25)
        pdf.set_fill_color(r, g, b)
        pdf.set_draw_color(180, 40, 40)
        pdf.circle(cx, cy, radius, style="FD")
    # Center dot
    pdf.set_fill_color(220, 50, 50)
    pdf.circle(cx, cy, size * 0.12, style="F")
    # Arrow
    pdf.set_draw_color(50, 50, 50)
    pdf.set_line_width(0.5)
    pdf.line(cx + size * 0.8, cy - size * 0.8, cx + size * 0.1, cy - size * 0.1)
    # Arrowhead
    pdf.set_fill_color(50, 50, 50)
    arrow_pts = [
        (cx + size * 0.1, cy - size * 0.1),
        (cx + size * 0.3, cy - size * 0.05),
        (cx + size * 0.15, cy - size * 0.3),
    ]
    pdf.polygon(arrow_pts, style="F")
    pdf.set_line_width(0.3)
    pdf.set_draw_color(0, 0, 0)


# ─── PAGE CONTENT ──────────────────────────────────────────────────────────────

CHAPTERS = [
    {
        "title": "THE CLAUDE AI\nMILLIONAIRE\nBLUEPRINT",
        "subtitle": "How to Leverage the World's Most Powerful AI\nto Build Wealth in 2026 and Beyond",
        "type": "cover"
    },
    {
        "title": "Table of Contents",
        "type": "toc"
    },
    {
        "title": "Chapter 1: The AI Wealth Revolution",
        "graphic": "brain",
        "content": [
            "We are living through the greatest wealth-creation opportunity since the internet. "
            "The global AI market reached $294 billion in 2025 and is projected to hit $1.77 trillion "
            "by 2032. Those who learn to harness AI effectively will capture an outsized share of this "
            "unprecedented growth.",
            "",
            "Claude, built by Anthropic, represents the cutting edge of AI assistants. Unlike generic "
            "tools, Claude excels at nuanced reasoning, complex code generation, strategic thinking, "
            "and creative problem-solving. It is your unfair advantage in the race to build wealth.",
            "",
            "This book will show you exactly how to use Claude to:",
            "  * Build profitable businesses from scratch",
            "  * Automate income streams that work while you sleep",
            "  * Deliver premium services at 10x speed",
            "  * Create digital products that generate passive revenue",
            "  * Scale from zero to seven figures systematically",
            "",
            "The millionaires of tomorrow are being made today. Let's begin."
        ]
    },
]



CHAPTERS += [
    {
        "title": "Chapter 2: Understanding Claude's Superpowers",
        "graphic": "laptop",
        "content": [
            "Before you can leverage Claude for wealth-building, you need to understand what makes "
            "it exceptional. Here are Claude's core capabilities that translate directly to revenue:",
            "",
            "ADVANCED REASONING & ANALYSIS",
            "Claude can analyze complex business problems, evaluate market opportunities, and provide "
            "strategic recommendations that would cost $500+/hour from a consultant.",
            "",
            "CODE GENERATION & SOFTWARE DEVELOPMENT",
            "Claude writes production-quality code in Python, JavaScript, TypeScript, and dozens of "
            "other languages. It can build full applications, APIs, automation scripts, and more.",
            "",
            "CONTENT CREATION AT SCALE",
            "From blog posts to email sequences, sales copy to technical documentation, Claude "
            "produces professional-grade content in minutes rather than hours.",
            "",
            "DATA ANALYSIS & INSIGHTS",
            "Feed Claude data and it extracts actionable insights, identifies trends, and generates "
            "reports that drive better business decisions.",
            "",
            "CLAUDE MANAGED AGENTS (2026)",
            "Anthropic's newest capability allows Claude to run autonomously in the cloud - reading "
            "files, executing code, browsing the web, and completing complex multi-step tasks without "
            "supervision. This is a game-changer for automation.",
            "",
            "MODEL CONTEXT PROTOCOL (MCP)",
            "MCP lets Claude connect to your databases, APIs, and internal tools directly - turning "
            "it into a fully integrated business automation engine."
        ]
    },
    {
        "title": "Chapter 3: The Service Arbitrage Model",
        "graphic": "chart",
        "content": [
            "The fastest path to your first $100K with Claude is service arbitrage. Here's the model:",
            "",
            "You sell high-value business services to clients at premium rates, then use Claude to "
            "deliver the work in a fraction of the time. You keep the margin.",
            "",
            "HIGH-MARGIN SERVICES YOU CAN OFFER:",
            "",
            "1. AI-Powered Copywriting Agency ($3K-$15K/month per client)",
            "   - Use Claude to write landing pages, email sequences, ad copy",
            "   - Deliver in hours what takes traditional agencies weeks",
            "   - Charge $2,000-$5,000 per project, spend 2-4 hours with Claude",
            "",
            "2. Software Development Consulting ($150-$300/hour)",
            "   - Build MVPs, automate workflows, create custom tools",
            "   - Claude handles 80% of the coding, you handle architecture",
            "   - Bill 40 hours for 10 hours of actual work",
            "",
            "3. Business Strategy & Research ($5K-$20K per engagement)",
            "   - Market analysis, competitive research, business plans",
            "   - Claude processes data and generates insights instantly",
            "   - Package as premium consulting deliverables",
            "",
            "4. AI Automation Agency ($2K-$10K/month retainer)",
            "   - Set up AI workflows for businesses using Claude's API",
            "   - Automate customer support, content, data processing",
            "   - Recurring revenue with minimal ongoing effort",
            "",
            "TARGET: 5 clients at $5K/month = $300K/year. Scale to $1M with a small team."
        ]
    },
]



CHAPTERS += [
    {
        "title": "Chapter 4: Building Micro-SaaS Products",
        "graphic": "rocket",
        "content": [
            "Micro-SaaS (Software as a Service) products are small, focused software tools that solve "
            "one specific problem. They're the perfect vehicle for AI-assisted wealth building because:",
            "",
            "  * Claude can build the entire product for you",
            "  * Low overhead (often $0-$50/month to run)",
            "  * Recurring revenue model (monthly subscriptions)",
            "  * Once built, they generate income passively",
            "",
            "THE MICRO-SAAS BLUEPRINT:",
            "",
            "Step 1: Find a Painful Problem",
            "Use Claude to research niches, analyze Reddit complaints, scan product review sites, "
            "and identify problems people will pay to solve.",
            "",
            "Step 2: Validate Before Building",
            "Have Claude create a landing page, set up a waitlist, and craft social media posts. "
            "Test demand before writing a single line of product code.",
            "",
            "Step 3: Build with Claude",
            "Use Claude to generate your entire codebase - frontend, backend, database, APIs. "
            "A tool that would take a dev team months can be built in days.",
            "",
            "Step 4: Launch and Iterate",
            "Use Claude for marketing copy, customer support templates, and feature updates.",
            "",
            "REVENUE POTENTIAL:",
            "  * 100 users at $29/month = $2,900/month",
            "  * 500 users at $49/month = $24,500/month",
            "  * 1,000 users at $99/month = $99,000/month",
            "",
            "Build 3-5 micro-SaaS products and you're well on your way to $1M/year."
        ]
    },
    {
        "title": "Chapter 5: Content Empire Building",
        "graphic": "network",
        "content": [
            "Content is the foundation of digital wealth. With Claude, you can produce more high-quality "
            "content than entire teams - creating multiple income streams simultaneously.",
            "",
            "THE CONTENT WEALTH STACK:",
            "",
            "1. Newsletter Business ($5K-$50K/month)",
            "   - Use Claude to research, write, and format newsletters",
            "   - Monetize through sponsorships, paid tiers, and affiliate links",
            "   - Publish daily with just 30 minutes of your time per issue",
            "",
            "2. YouTube & Video Scripts ($2K-$20K/month)",
            "   - Claude writes scripts optimized for engagement and retention",
            "   - Create faceless YouTube channels with AI-generated scripts",
            "   - Multiple channels = multiple revenue streams",
            "",
            "3. Digital Course Creation ($10K-$100K per launch)",
            "   - Use Claude to outline, write, and structure online courses",
            "   - Create workbooks, quizzes, and supplementary materials",
            "   - Launch on platforms or self-host for maximum profit",
            "",
            "4. Book Publishing ($1K-$10K/month passive)",
            "   - Write and publish non-fiction books with Claude's help",
            "   - Target underserved niches with consistent demand",
            "   - Build a catalog of 10-20 books for steady royalties",
            "",
            "5. SEO Content Sites ($3K-$30K/month)",
            "   - Build authority websites targeting buyer-intent keywords",
            "   - Use Claude to produce expert-level articles at scale",
            "   - Monetize with affiliate marketing and display ads",
            "",
            "The key: Treat content as a business asset, not a hobby."
        ]
    },
]



CHAPTERS += [
    {
        "title": "Chapter 6: AI Automation Agency",
        "graphic": "gears",
        "content": [
            "One of the most lucrative business models in 2026 is running an AI automation agency. "
            "Businesses desperately need help integrating AI into their operations, and most don't "
            "know where to start.",
            "",
            "WHAT YOU SELL:",
            "You help businesses automate repetitive tasks, reduce costs, and increase output "
            "using Claude's API and Managed Agents platform.",
            "",
            "COMMON AUTOMATIONS (each billable at $2K-$15K):",
            "",
            "  * Customer support automation - Claude handles 80% of tickets",
            "  * Document processing - contracts, invoices, reports analyzed instantly",
            "  * Email response systems - personalized replies generated automatically",
            "  * Content pipelines - blog posts, social media, newsletters on autopilot",
            "  * Data entry & CRM updates - eliminate manual data work",
            "  * Lead qualification - AI scores and routes leads automatically",
            "  * Report generation - weekly/monthly reports created without human effort",
            "",
            "HOW TO BUILD WITH CLAUDE:",
            "",
            "Use Claude's API to build these systems. With Managed Agents, you can deploy "
            "autonomous AI workers that run 24/7 in the cloud, connecting to clients' tools "
            "via MCP (Model Context Protocol).",
            "",
            "PRICING MODEL:",
            "  * Setup fee: $5,000-$25,000",
            "  * Monthly retainer: $2,000-$10,000",
            "  * Per-automation fee: $500-$5,000",
            "",
            "With 10 clients on $5K/month retainers = $600K/year",
            "Add setup fees and you're crossing $1M in year one."
        ]
    },
    {
        "title": "Chapter 7: Prompt Engineering as a Service",
        "graphic": "lightbulb",
        "content": [
            "Companies are spending millions on AI but getting mediocre results because they don't "
            "know how to communicate with AI effectively. This is your opportunity.",
            "",
            "WHAT PROMPT ENGINEERS DO:",
            "  * Design system prompts that make AI outputs reliable and consistent",
            "  * Create prompt libraries for enterprise teams",
            "  * Optimize AI workflows to reduce token costs by 40-70%",
            "  * Build custom GPTs, Claude projects, and agent configurations",
            "  * Train teams on effective AI communication",
            "",
            "WHY THIS IS LUCRATIVE:",
            "A well-crafted prompt can save a company thousands per month in wasted AI spend "
            "and produce dramatically better outputs. This makes your service an easy ROI sell.",
            "",
            "SERVICE PACKAGES:",
            "",
            "1. Prompt Audit ($2,500-$5,000)",
            "   - Review existing AI usage, identify optimization opportunities",
            "   - Deliver improved prompts with documentation",
            "",
            "2. Custom Prompt Library ($5,000-$15,000)",
            "   - Build a complete prompt system for their use cases",
            "   - Include training materials and best practices guide",
            "",
            "3. Ongoing Optimization ($3,000-$8,000/month)",
            "   - Continuous prompt improvement based on output quality",
            "   - New prompt development as needs emerge",
            "   - Team training and support",
            "",
            "4. AI Strategy Consulting ($10,000-$50,000)",
            "   - Full AI integration roadmap",
            "   - Tool selection, workflow design, implementation oversight",
            "",
            "USE CLAUDE TO DELIVER:",
            "Ironically, you use Claude to help you create better prompts for clients. "
            "Claude excels at meta-prompt engineering and can test/iterate rapidly."
        ]
    },
]



CHAPTERS += [
    {
        "title": "Chapter 8: Digital Products & Templates",
        "graphic": "diamond",
        "content": [
            "Digital products have near-zero marginal cost. Create once, sell forever. Claude "
            "makes creation fast, so you can build an empire of digital assets.",
            "",
            "HIGH-DEMAND DIGITAL PRODUCTS:",
            "",
            "1. Notion/Airtable Templates ($19-$199 each)",
            "   - Business dashboards, project trackers, CRM systems",
            "   - Use Claude to design the logic and documentation",
            "   - Sell on Gumroad, Etsy, or your own site",
            "",
            "2. Spreadsheet Tools ($29-$299 each)",
            "   - Financial models, calculators, trackers",
            "   - Claude writes complex formulas and macros instantly",
            "   - Target specific industries for premium pricing",
            "",
            "3. Prompt Packs ($27-$197 each)",
            "   - Curated collections of tested prompts for specific use cases",
            "   - Marketing, coding, writing, analysis prompt bundles",
            "   - Low effort to create, high perceived value",
            "",
            "4. Code Templates & Boilerplates ($49-$499 each)",
            "   - SaaS starter kits, landing page templates, API boilerplates",
            "   - Claude generates the code, you package and sell",
            "   - Developers gladly pay to save time",
            "",
            "5. AI Workflow Blueprints ($97-$497 each)",
            "   - Step-by-step systems for specific business outcomes",
            "   - Include prompts, automation configs, and instructions",
            "   - Solve one expensive problem and charge accordingly",
            "",
            "SCALING STRATEGY:",
            "  * Create 1 product per week using Claude (2-4 hours each)",
            "  * Build to 50+ products in your catalog within a year",
            "  * Average $500/month per product = $25,000/month passive",
            "  * Top performers can hit $100K/month with viral products"
        ]
    },
    {
        "title": "Chapter 9: The API Economy",
        "graphic": "shield",
        "content": [
            "Claude's API unlocks a completely different level of income potential. Instead of "
            "using Claude manually, you build systems that use Claude programmatically - serving "
            "hundreds or thousands of customers simultaneously.",
            "",
            "API-POWERED BUSINESS MODELS:",
            "",
            "1. AI-Powered Apps",
            "   - Build apps with Claude as the backend brain",
            "   - Users pay monthly subscriptions; Claude handles the intelligence",
            "   - Examples: writing assistants, code reviewers, data analyzers",
            "",
            "2. White-Label AI Solutions",
            "   - Build AI tools that other businesses rebrand and sell",
            "   - Charge per-seat licensing or revenue share",
            "   - One product, many customers paying simultaneously",
            "",
            "3. AI Marketplaces & Platforms",
            "   - Create platforms where others deploy AI workflows",
            "   - Take a percentage of every transaction",
            "   - Network effects create compounding growth",
            "",
            "TECHNICAL STACK (Claude builds all of this):",
            "  * Backend: Python/Node.js with Claude API integration",
            "  * Frontend: React/Next.js for the user interface",
            "  * Database: PostgreSQL for data persistence",
            "  * Auth: Clerk or Auth0 for user management",
            "  * Payments: Stripe for billing and subscriptions",
            "  * Hosting: Vercel/Railway for deployment",
            "",
            "Claude can generate your entire technical stack in days. You focus on "
            "the business model, marketing, and customer acquisition."
        ]
    },
]



CHAPTERS += [
    {
        "title": "Chapter 10: Scaling to Seven Figures",
        "graphic": "target",
        "content": [
            "Getting to $1,000,000 requires systematic scaling. Here's the exact roadmap:",
            "",
            "PHASE 1: Foundation ($0 to $10K/month) - Months 1-3",
            "  * Pick ONE model from this book (services recommended)",
            "  * Land your first 3 clients using cold outreach + Claude",
            "  * Deliver exceptional results to build testimonials",
            "  * Reinvest profits into tools and marketing",
            "",
            "PHASE 2: Growth ($10K to $50K/month) - Months 4-8",
            "  * Systematize your delivery with Claude automations",
            "  * Hire 1-2 people for tasks Claude can't do",
            "  * Raise prices based on proven results",
            "  * Add a second revenue stream (products or SaaS)",
            "",
            "PHASE 3: Scale ($50K to $100K+/month) - Months 9-14",
            "  * Build systems that run without you daily",
            "  * Deploy Claude Managed Agents for autonomous operations",
            "  * Focus on high-leverage activities only",
            "  * Multiple revenue streams compounding",
            "",
            "THE MILLIONAIRE MATH:",
            "  * Services: $30K/month (6 clients at $5K)",
            "  * SaaS Product: $25K/month (500 users at $49)",
            "  * Digital Products: $15K/month (catalog sales)",
            "  * Content/Affiliate: $10K/month (newsletter + courses)",
            "  * API Products: $20K/month (white-label clients)",
            "  * TOTAL: $100K/month = $1.2M/year",
            "",
            "This isn't fantasy. These are real numbers achievable by one person "
            "leveraging Claude effectively across multiple income streams."
        ]
    },
    {
        "title": "Chapter 11: Advanced Claude Techniques",
        "graphic": "brain",
        "content": [
            "To maximize your earning potential, master these advanced Claude techniques:",
            "",
            "1. CHAIN-OF-THOUGHT PROMPTING",
            "Ask Claude to think step-by-step for complex problems. This produces dramatically "
            "better business strategies, code, and analysis.",
            "",
            "2. SYSTEM PROMPTS FOR CONSISTENCY",
            "Create detailed system prompts that turn Claude into your specialized expert - "
            "a copywriter, developer, analyst, or strategist on demand.",
            "",
            "3. MULTI-TURN CONVERSATIONS",
            "Build on previous context across messages. Start broad, then drill into specifics. "
            "This mimics working with an expert consultant.",
            "",
            "4. CLAUDE PROJECTS (Knowledge Bases)",
            "Upload documents, codebases, and brand guidelines. Claude uses this context to "
            "produce perfectly tailored outputs every time.",
            "",
            "5. API BATCH PROCESSING",
            "Process hundreds of tasks simultaneously via the API. Generate 100 product "
            "descriptions, analyze 500 customer reviews, or write 50 emails in one batch.",
            "",
            "6. MANAGED AGENTS FOR AUTONOMY",
            "Deploy Claude agents that work autonomously - monitoring data, updating systems, "
            "generating reports, and handling tasks 24/7 without your input.",
            "",
            "7. MCP INTEGRATIONS",
            "Connect Claude directly to Slack, databases, CRMs, and email. It becomes an "
            "intelligent layer that understands and acts on your business data.",
            "",
            "MASTERY = LEVERAGE: The better you are with Claude, the more value you create "
            "per hour of work. Top practitioners earn $1,000+ per hour of effective output."
        ]
    },
]



CHAPTERS += [
    {
        "title": "Chapter 12: Your 90-Day Action Plan",
        "graphic": "rocket",
        "content": [
            "Knowledge without action is worthless. Here is your concrete 90-day plan to start "
            "building wealth with Claude:",
            "",
            "WEEK 1-2: FOUNDATION",
            "  [ ] Set up Claude Pro subscription ($20/month)",
            "  [ ] Complete 10 hours of Claude practice (prompting, coding, analysis)",
            "  [ ] Choose your primary business model from Chapters 3-9",
            "  [ ] Identify your target market and ideal client",
            "  [ ] Use Claude to research 50 potential clients/opportunities",
            "",
            "WEEK 3-4: BUILD",
            "  [ ] Create your service offering or product with Claude",
            "  [ ] Build a simple website/landing page (Claude writes the code)",
            "  [ ] Develop 3 case studies or sample work",
            "  [ ] Set up basic systems (invoicing, contracts, project management)",
            "  [ ] Create your outreach templates with Claude",
            "",
            "WEEK 5-8: LAUNCH & SELL",
            "  [ ] Send 20 outreach messages per day (Claude personalizes each one)",
            "  [ ] Post daily on LinkedIn/Twitter about AI insights",
            "  [ ] Offer free audits or samples to get first clients",
            "  [ ] Close your first 2-3 paying clients",
            "  [ ] Deliver exceptional results using Claude",
            "",
            "WEEK 9-12: OPTIMIZE & SCALE",
            "  [ ] Collect testimonials and refine your process",
            "  [ ] Raise prices by 25-50%",
            "  [ ] Add a second revenue stream",
            "  [ ] Automate repetitive parts with Claude API",
            "  [ ] Set monthly revenue target and track progress",
            "",
            "90-DAY GOAL: $5,000-$15,000/month in revenue",
            "",
            "Remember: Every millionaire started with their first dollar. "
            "Claude is your unfair advantage. Use it relentlessly."
        ]
    },
    {
        "title": "Final Words: Your Future Starts Now",
        "graphic": "diamond",
        "content": [
            "The opportunity before you is extraordinary. We are in the early innings of the AI "
            "revolution, and those who act now will be the millionaires and billionaires of tomorrow.",
            "",
            "Claude is not just a tool - it's a force multiplier. It turns one person into a team. "
            "It turns weeks into hours. It turns ideas into income.",
            "",
            "KEY PRINCIPLES TO REMEMBER:",
            "",
            "  1. Start before you're ready. Perfection is the enemy of profit.",
            "  2. Focus on solving real problems. Money follows value.",
            "  3. Use Claude to work ON your business, not just IN it.",
            "  4. Build systems and assets, not just income.",
            "  5. Reinvest in yourself and your tools continuously.",
            "  6. Think in terms of leverage - how can one hour produce $10K in value?",
            "  7. Be ethical. Build trust. Play long-term games.",
            "",
            "The AI wealth gap is widening every day. On one side are those who learn to leverage "
            "tools like Claude to create extraordinary value. On the other are those who wait, "
            "hesitate, and eventually get left behind.",
            "",
            "You've read this book. You have the blueprint. Now execute.",
            "",
            "Your million-dollar journey begins with a single prompt.",
            "",
            "Go make it happen.",
            "",
            "",
            "---",
            "Copyright 2026. All rights reserved.",
            "Built with the power of AI. Your future awaits."
        ]
    },
]



# ─── PDF GENERATION ────────────────────────────────────────────────────────────

def create_cover_page(pdf, chapter):
    """Create a stunning cover page with graphics."""
    pdf.add_page()
    # Dark gradient background
    draw_gradient_rect(pdf, 0, 0, 210, 297, 15, 20, 50, 40, 50, 100)

    # Decorative elements - gold coins scattered
    draw_gold_coin(pdf, 30, 40, 8)
    draw_gold_coin(pdf, 175, 55, 6)
    draw_gold_coin(pdf, 50, 250, 7)
    draw_gold_coin(pdf, 165, 240, 9)
    draw_gold_coin(pdf, 20, 180, 5)
    draw_gold_coin(pdf, 185, 160, 6)

    # Central brain AI graphic
    draw_brain_ai(pdf, 105, 80, 35)

    # Rocket on the side
    draw_rocket(pdf, 165, 110, 15)

    # Chart graphic
    draw_chart_up(pdf, 25, 100, 50, 35)

    # Title text area - dark overlay
    pdf.set_fill_color(10, 15, 35)
    pdf.set_draw_color(218, 165, 32)
    pdf.set_line_width(1.0)
    pdf.rect(20, 145, 170, 95, style="FD")

    # Gold border accent
    pdf.set_draw_color(255, 215, 0)
    pdf.set_line_width(0.5)
    pdf.rect(23, 148, 164, 89, style="D")

    # Title
    pdf.set_text_color(255, 215, 0)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_xy(25, 155)
    for line in chapter["title"].split("\n"):
        pdf.cell(160, 14, line, align="C")
        pdf.ln(14)

    # Subtitle
    pdf.set_text_color(200, 210, 230)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_xy(25, 202)
    for line in chapter["subtitle"].split("\n"):
        pdf.cell(160, 7, line, align="C")
        pdf.ln(7)

    # Bottom decorative elements
    draw_diamond(pdf, 105, 265, 8)
    draw_network(pdf, 105, 280, 20)

    # Author line
    pdf.set_text_color(180, 180, 200)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_xy(25, 285)
    pdf.cell(160, 5, "Your Complete Guide to AI-Powered Wealth Building", align="C")

    pdf.set_line_width(0.3)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_text_color(0, 0, 0)



def create_toc_page(pdf, chapter):
    """Create a table of contents page."""
    pdf.add_page()
    # Header background
    draw_gradient_rect(pdf, 0, 0, 210, 40, 25, 35, 75, 45, 55, 105)

    pdf.set_text_color(255, 215, 0)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(10, 12)
    pdf.cell(190, 12, "TABLE OF CONTENTS", align="C")

    # Decorative line
    pdf.set_draw_color(218, 165, 32)
    pdf.set_line_width(0.8)
    pdf.line(30, 38, 180, 38)

    # TOC entries
    toc_items = [
        ("Chapter 1", "The AI Wealth Revolution", "3"),
        ("Chapter 2", "Understanding Claude's Superpowers", "4"),
        ("Chapter 3", "The Service Arbitrage Model", "5"),
        ("Chapter 4", "Building Micro-SaaS Products", "6"),
        ("Chapter 5", "Content Empire Building", "7"),
        ("Chapter 6", "AI Automation Agency", "8"),
        ("Chapter 7", "Prompt Engineering as a Service", "9"),
        ("Chapter 8", "Digital Products & Templates", "10"),
        ("Chapter 9", "The API Economy", "11"),
        ("Chapter 10", "Scaling to Seven Figures", "12"),
        ("Chapter 11", "Advanced Claude Techniques", "13"),
        ("Chapter 12", "Your 90-Day Action Plan", "14"),
        ("", "Final Words: Your Future Starts Now", "15"),
    ]

    y_start = 50
    for i, (ch_num, title, page) in enumerate(toc_items):
        y = y_start + i * 17
        # Alternating background
        if i % 2 == 0:
            pdf.set_fill_color(245, 248, 255)
            pdf.rect(15, y - 2, 180, 15, style="F")

        # Chapter number
        pdf.set_text_color(70, 130, 180)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_xy(20, y)
        pdf.cell(30, 10, ch_num)

        # Title
        pdf.set_text_color(30, 30, 50)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_xy(50, y)
        pdf.cell(120, 10, title)

        # Dots
        pdf.set_text_color(150, 150, 150)
        pdf.set_font("Helvetica", "", 8)
        dot_x = 150
        while dot_x < 175:
            pdf.set_xy(dot_x, y + 2)
            pdf.cell(2, 10, ".")
            dot_x += 3

        # Page number
        pdf.set_text_color(70, 130, 180)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_xy(178, y)
        pdf.cell(10, 10, page, align="R")

    # Bottom graphic
    draw_money_stack(pdf, 85, 275, 4)

    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(0, 0, 0)



def create_chapter_page(pdf, chapter):
    """Create a chapter page with header graphic and content."""
    pdf.add_page()

    # Header area with gradient
    draw_gradient_rect(pdf, 0, 0, 210, 55, 25, 35, 75, 55, 75, 135)

    # Chapter title
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(15, 10)
    pdf.cell(180, 10, chapter["title"], align="C")

    # Gold underline
    pdf.set_draw_color(255, 215, 0)
    pdf.set_line_width(0.8)
    title_w = pdf.get_string_width(chapter["title"])
    line_x = 105 - title_w / 2
    pdf.line(line_x, 22, line_x + title_w, 22)

    # Graphic in header area
    graphic = chapter.get("graphic", "brain")
    gx, gy = 105, 40
    if graphic == "brain":
        draw_brain_ai(pdf, gx, gy, 12)
    elif graphic == "laptop":
        draw_laptop(pdf, gx, gy, 12)
    elif graphic == "chart":
        draw_chart_up(pdf, gx - 18, gy - 8, 36, 16)
    elif graphic == "rocket":
        draw_rocket(pdf, gx, gy, 12)
    elif graphic == "network":
        draw_network(pdf, gx, gy, 15)
    elif graphic == "gears":
        draw_gear_system(pdf, gx, gy, 8)
    elif graphic == "lightbulb":
        draw_lightbulb(pdf, gx, gy, 10)
    elif graphic == "diamond":
        draw_diamond(pdf, gx, gy, 8)
    elif graphic == "shield":
        draw_shield(pdf, gx, gy, 10)
    elif graphic == "target":
        draw_target(pdf, gx, gy, 10)

    # Content area
    pdf.set_text_color(30, 30, 50)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(18, 60)

    for line in chapter["content"]:
        if line == "":
            pdf.ln(4)
        elif line.startswith("  *") or line.startswith("  ["):
            # Bullet point
            pdf.set_font("Helvetica", "", 9)
            pdf.set_x(22)
            pdf.multi_cell(168, 4.5, line)
            pdf.ln(1)
        elif line.isupper() or (line.endswith(":") and not line.startswith(" ")):
            # Section header
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(70, 100, 160)
            pdf.set_x(18)
            pdf.multi_cell(174, 5, line)
            pdf.set_text_color(30, 30, 50)
            pdf.set_font("Helvetica", "", 10)
            pdf.ln(1)
        elif line.startswith("   "):
            # Indented sub-item
            pdf.set_font("Helvetica", "", 9)
            pdf.set_x(26)
            pdf.multi_cell(164, 4.5, line.strip())
            pdf.ln(1)
        elif line[0:1].isdigit() and "." in line[:3]:
            # Numbered item
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_x(20)
            pdf.multi_cell(170, 5, line)
            pdf.set_font("Helvetica", "", 10)
            pdf.ln(1)
        else:
            pdf.set_x(18)
            pdf.multi_cell(174, 4.8, line)
            pdf.ln(1)

    # Decorative bottom element
    pdf.set_draw_color(218, 165, 32)
    pdf.set_line_width(0.5)
    pdf.line(60, 284, 150, 284)
    draw_gold_coin(pdf, 105, 290, 4)

    pdf.set_draw_color(0, 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.set_line_width(0.3)



def generate_book():
    """Generate the complete e-book PDF."""
    pdf = MillionaireBook()
    pdf.set_auto_page_break(auto=True, margin=20)

    for chapter in CHAPTERS:
        ch_type = chapter.get("type", "chapter")
        if ch_type == "cover":
            create_cover_page(pdf, chapter)
        elif ch_type == "toc":
            create_toc_page(pdf, chapter)
        else:
            create_chapter_page(pdf, chapter)

    output_path = "claude_millionaire_blueprint.pdf"
    pdf.output(output_path)
    print(f"E-book generated successfully: {output_path}")
    print(f"Total pages: {pdf.page_no()}")
    return output_path


if __name__ == "__main__":
    generate_book()
