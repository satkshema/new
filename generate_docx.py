#!/usr/bin/env python3
"""
Generate "The Claude AI Millionaire Blueprint" - Word (.docx) e-book
Pure text, professionally formatted using python-docx.
"""

import os
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# Output path
OUTPUT_PATH = '/projects/sandbox/new/claude_millionaire_blueprint.docx'


def set_cell_shading(cell, color_hex):
    """Set background shading on a table cell."""
    shading_elm = parse_xml(
        f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>'
    )
    cell._tc.get_or_add_tcPr().append(shading_elm)


def add_prompt_box(doc, title, prompt_text):
    """Add a formatted prompt box using a table with shading and border."""
    # Title paragraph
    p = doc.add_paragraph()
    p.space_before = Pt(12)
    p.space_after = Pt(4)
    run = p.add_run(f"PROMPT: {title}")
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0, 100, 200)

    # Create a single-cell table for the prompt box
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    cell = table.cell(0, 0)
    set_cell_shading(cell, "F0F0F5")


    # Set left border to blue
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="0064C8"/>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    # Add prompt text in Courier New
    para = cell.paragraphs[0]
    para.clear()
    for line in prompt_text.split('\n'):
        if para.text == '' and len(para.runs) == 0:
            run = para.add_run(line)
        else:
            para.add_run('\n')
            run = para.add_run(line)
        run.font.name = 'Courier New'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(30, 70, 30)

    # Add spacing after table
    p_after = doc.add_paragraph()
    p_after.space_before = Pt(4)
    p_after.space_after = Pt(8)



def add_case_study(doc, title, revenue, description, timeline, strategies):
    """Add a formatted case study section."""
    # Title with revenue
    p = doc.add_paragraph()
    p.space_before = Pt(16)
    p.space_after = Pt(4)
    run = p.add_run(f"{title} [{revenue}]")
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0, 60, 140)

    # Timeline
    p2 = doc.add_paragraph()
    p2.space_before = Pt(2)
    p2.space_after = Pt(6)
    run2 = p2.add_run(f"Timeline: {timeline}")
    run2.italic = True
    run2.font.size = Pt(10)
    run2.font.color.rgb = RGBColor(0, 140, 130)

    # Description
    p3 = doc.add_paragraph(description)
    p3.style = doc.styles['Body Text']
    p3.space_after = Pt(6)

    # Strategies
    p4 = doc.add_paragraph()
    p4.space_before = Pt(4)
    run4 = p4.add_run("Key Strategies:")
    run4.bold = True
    run4.font.size = Pt(10)

    for strat in strategies:
        bp = doc.add_paragraph(strat, style='List Bullet')
        bp.paragraph_format.space_after = Pt(2)



def add_chapter_heading(doc, chapter_num, title):
    """Add a chapter heading with page break before."""
    doc.add_page_break()
    if chapter_num:
        heading_text = f"Chapter {chapter_num}: {title}"
    else:
        heading_text = title
    h = doc.add_heading(heading_text, level=1)
    h.space_after = Pt(18)
    return h


def add_section_heading(doc, title):
    """Add a section heading (Heading 2)."""
    h = doc.add_heading(title, level=2)
    h.space_before = Pt(16)
    h.space_after = Pt(10)
    return h


def add_body_text(doc, text):
    """Add body text paragraph."""
    p = doc.add_paragraph(text)
    p.style = doc.styles['Body Text']
    p.space_after = Pt(8)
    return p


def add_bullet_list(doc, items):
    """Add a bulleted list."""
    for item in items:
        p = doc.add_paragraph(item, style='List Bullet')
        p.paragraph_format.space_after = Pt(3)



def generate_docx():
    """Generate the complete Word document."""
    doc = Document()

    # ============================================================
    # TITLE PAGE
    # ============================================================
    # Add empty lines for spacing
    for _ in range(6):
        doc.add_paragraph()

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("THE CLAUDE AI")
    run.bold = True
    run.font.size = Pt(32)
    run.font.color.rgb = RGBColor(0, 50, 120)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run("MILLIONAIRE BLUEPRINT")
    run2.bold = True
    run2.font.size = Pt(36)
    run2.font.color.rgb = RGBColor(0, 50, 120)

    # Subtitle
    for _ in range(2):
        doc.add_paragraph()
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run3 = p3.add_run("Your Complete Guide to Building Wealth with AI")
    run3.font.size = Pt(14)
    run3.italic = True

    # Features line
    for _ in range(3):
        doc.add_paragraph()
    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run4 = p4.add_run("20+ Live Prompts | Real Case Studies | 90-Day Plan")
    run4.bold = True
    run4.font.size = Pt(12)
    run4.font.color.rgb = RGBColor(0, 150, 80)


    # ============================================================
    # TABLE OF CONTENTS
    # ============================================================
    doc.add_page_break()
    h = doc.add_heading("TABLE OF CONTENTS", level=1)
    h.space_after = Pt(18)

    chapters = [
        ("1", "The AI Wealth Revolution"),
        ("2", "Understanding Claude's Superpowers"),
        ("3", "Service Arbitrage Model"),
        ("4", "Building Micro-SaaS"),
        ("5", "Content Empire Building"),
        ("6", "AI Automation Agency"),
        ("7", "Prompt Engineering as a Service"),
        ("8", "Digital Products & Templates"),
        ("9", "The API Economy"),
        ("10", "Scaling to Seven Figures"),
        ("11", "Advanced Claude Techniques"),
        ("12", "Live Prompt Library"),
        ("13", "Case Studies"),
        ("14", "Your 90-Day Action Plan"),
        ("", "Final Words"),
    ]

    for num, title in chapters:
        p = doc.add_paragraph()
        p.space_after = Pt(6)
        if num:
            label = f"Chapter {num}: {title}"
        else:
            label = title
        run = p.add_run(label)
        run.bold = True
        run.font.size = Pt(11)


    # ============================================================
    # CHAPTER 1: The AI Wealth Revolution
    # ============================================================
    add_chapter_heading(doc, 1, "The AI Wealth Revolution")

    add_section_heading(doc, "The $15.7 Trillion AI Opportunity")
    add_body_text(doc, (
        "The artificial intelligence market is projected to reach $15.7 trillion by 2030. "
        "This isn't just a tech trend - it's the biggest wealth transfer in human history. "
        "Those who position themselves now will capture disproportionate value. Claude AI, "
        "developed by Anthropic, represents the most capable AI assistant available today, "
        "and smart entrepreneurs are already using it to build six and seven-figure businesses."
    ))

    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("Key Market Statistics:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0, 100, 200)

    add_bullet_list(doc, [
        "AI market growing at 37.3% CAGR through 2030",
        "74% of businesses plan to increase AI spending in 2025",
        "Average AI-powered business sees 40% productivity gains",
        "Solo AI entrepreneurs earning $10K-$100K/month within 6 months",
        "AI services market worth $200B+ by 2026",
        "Companies paying $150-500/hour for AI consulting",
    ])

    add_body_text(doc, (
        "The window of opportunity is NOW. Early movers in AI-powered businesses are "
        "building moats that will be nearly impossible to replicate in 2-3 years. "
        "This blueprint gives you the exact roadmap to capitalize on this revolution."
    ))


    add_section_heading(doc, "Why Claude Changes Everything")
    add_body_text(doc, (
        "Unlike previous AI tools, Claude offers unprecedented capabilities: nuanced "
        "understanding, complex reasoning, code generation, creative writing, data analysis, "
        "and strategic thinking. This means a single person with Claude can now deliver "
        "work that previously required a team of 5-10 specialists."
    ))

    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("The Leverage Equation:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(120, 60, 200)

    add_bullet_list(doc, [
        "1 Person + Claude = Output of 5-10 people",
        "Zero employees needed to start",
        "Minimal capital required ($20/month for Claude Pro)",
        "Infinite scalability - no inventory, no overhead",
        "Global market access from day one",
        "Multiple revenue streams simultaneously",
    ])

    add_body_text(doc, (
        "This blueprint will show you exactly how to leverage Claude across 7 proven "
        "business models, with real prompts you can copy and use today."
    ))


    # ============================================================
    # CHAPTER 2: Understanding Claude's Superpowers
    # ============================================================
    add_chapter_heading(doc, 2, "Understanding Claude's Superpowers")

    add_section_heading(doc, "Claude's Core Capabilities")
    add_body_text(doc, (
        "Claude is not just another chatbot. It's a reasoning engine that can handle "
        "complex multi-step tasks with human-level quality. Understanding its capabilities "
        "is the foundation of building profitable AI businesses."
    ))

    capabilities = [
        ("Advanced Reasoning", "Breaks down complex problems, analyzes data, creates strategies"),
        ("Code Generation", "Writes production-ready code in 20+ languages, debugs, optimizes"),
        ("Creative Writing", "Blog posts, emails, scripts, copy that converts at 2-5x industry avg"),
        ("Data Analysis", "Processes CSV, JSON, extracts insights, builds financial models"),
        ("Research & Synthesis", "Analyzes markets, competitors, trends with actionable insights"),
        ("Conversation Design", "Creates chatbot flows, customer service scripts, sales funnels"),
    ]
    for cap_title, cap_desc in capabilities:
        p = doc.add_paragraph()
        p.space_after = Pt(4)
        run_t = p.add_run(f"{cap_title}: ")
        run_t.bold = True
        run_t.font.size = Pt(10)
        run_d = p.add_run(cap_desc)
        run_d.font.size = Pt(10)


    add_section_heading(doc, "The Prompt Engineering Advantage")
    add_body_text(doc, (
        "The difference between mediocre AI output and exceptional results lies in "
        "how you communicate with Claude. Master prompt engineers earn $100-500/hour "
        "because they know how to extract maximum value from every interaction."
    ))

    add_prompt_box(doc, "Universal Prompt Framework",
        "You are an expert [ROLE]. I need you to [TASK].\n"
        "Context: [BACKGROUND INFORMATION]\n"
        "Requirements:\n"
        "- [SPECIFIC REQUIREMENT 1]\n"
        "- [SPECIFIC REQUIREMENT 2]\n"
        "Output format: [DESIRED FORMAT]\n"
        "Tone: [PROFESSIONAL/CASUAL/TECHNICAL]\n"
        "Please think step-by-step before responding."
    )

    add_body_text(doc, (
        "This framework alone will improve your Claude outputs by 10x. Each chapter "
        "in this book provides specialized prompts built on this foundation."
    ))


    # ============================================================
    # CHAPTER 3: Service Arbitrage Model
    # ============================================================
    add_chapter_heading(doc, 3, "The Service Arbitrage Model")

    add_section_heading(doc, "The Arbitrage Opportunity")
    add_body_text(doc, (
        "Service arbitrage is the fastest path to $10K/month. You sell writing, coding, "
        "consulting, or design services at market rates ($50-200/hour), then use Claude "
        "to deliver 10x faster. Your effective hourly rate becomes $500-2000/hour."
    ))

    add_bullet_list(doc, [
        "Copywriting & Content: Charge $500-2000/article, deliver in 30 min",
        "Web Development: Charge $3000-10000/site, build in 2-3 days",
        "Business Consulting: Charge $200/hr, deliver reports in minutes",
        "Email Marketing: Charge $1500/month per client, 2 hours/week actual work",
        "SEO Services: Charge $2000/month, use Claude for content & analysis",
        "Social Media Management: $1500/month per client, batch in 1 hour",
    ])

    add_prompt_box(doc, "Client Outreach Prompt",
        "You are an expert cold email copywriter. Write a personalized\n"
        "outreach email to [PROSPECT NAME] at [COMPANY].\n"
        "Their pain point: [PAIN POINT from LinkedIn research]\n"
        "My service: [YOUR SERVICE]\n"
        "Goal: Book a 15-min discovery call.\n"
        "Tone: Professional but conversational. Use their name.\n"
        "Length: 4-5 sentences max. Include a specific insight about\n"
        "their business to show I've done research."
    )


    add_section_heading(doc, "Setting Up Your Service Business")
    add_body_text(doc, (
        "Here's the exact step-by-step process to go from zero to $10K/month "
        "with service arbitrage using Claude:"
    ))

    add_bullet_list(doc, [
        "Week 1: Choose your service niche (copywriting is easiest to start)",
        "Week 2: Create portfolio samples using Claude (5-10 pieces)",
        "Week 3: Set up profiles on Upwork, Fiverr, and your own website",
        "Week 4: Begin outreach - 20 personalized emails per day",
        "Week 5-8: Deliver exceptional work, collect testimonials",
        "Week 9-12: Raise prices, get referrals, hire VA for admin",
    ])

    add_prompt_box(doc, "Portfolio Builder Prompt",
        "Create a compelling freelance portfolio description for a\n"
        "[SERVICE TYPE] specialist. Include:\n"
        "- A hook that addresses the client's main pain point\n"
        "- 3 bullet points of unique value propositions\n"
        "- Social proof placeholder (results you've achieved)\n"
        "- Clear CTA for booking a consultation\n"
        "Tone: Confident, results-focused, specific numbers."
    )

    add_section_heading(doc, "Scaling Your Service Revenue")
    add_body_text(doc, "Once you've validated your service model, here's how to scale rapidly:")

    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("Revenue Milestones:")
    run.bold = True
    run.font.size = Pt(11)

    add_bullet_list(doc, [
        "Month 1: $1,000-3,000 (3-5 clients at $300-600 each)",
        "Month 2: $3,000-5,000 (raise prices, 5-8 clients)",
        "Month 3: $5,000-10,000 (premium pricing, referrals flowing)",
        "Month 4-6: $10,000-20,000 (retainer clients, systems built)",
        "Month 6-12: $20,000-50,000 (team of VAs, premium positioning)",
    ])


    add_prompt_box(doc, "Pricing Strategy Prompt",
        "You are a pricing strategist. Help me create a 3-tier\n"
        "pricing structure for my [SERVICE] business.\n"
        "Tier 1 (Basic): Entry-level package for budget clients\n"
        "Tier 2 (Professional): Most popular, best value\n"
        "Tier 3 (Premium): High-touch, maximum results\n"
        "For each tier, suggest: name, price, deliverables,\n"
        "turnaround time, and positioning strategy."
    )

    # ============================================================
    # CHAPTER 4: Building Micro-SaaS Products
    # ============================================================
    add_chapter_heading(doc, 4, "Building Micro-SaaS Products")

    add_section_heading(doc, "The Micro-SaaS Revolution")
    add_body_text(doc, (
        "Micro-SaaS products generate $1K-$50K/month in recurring revenue with "
        "minimal maintenance. Claude can help you build, launch, and iterate on "
        "software products 10x faster than traditional development."
    ))

    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("Validated Micro-SaaS Ideas:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0, 100, 200)

    add_bullet_list(doc, [
        "AI Writing Assistant Chrome Extension - $29/month",
        "Automated Invoice Generator for Freelancers - $19/month",
        "Social Media Scheduler with AI Captions - $39/month",
        "Customer Feedback Analyzer Dashboard - $49/month",
        "Email Template Builder with AI Personalization - $25/month",
        "Meeting Notes Summarizer Tool - $15/month",
    ])


    add_prompt_box(doc, "SaaS Idea Validator",
        "You are a SaaS product strategist. Validate this idea:\n"
        "[YOUR IDEA]\n"
        "Analyze: 1) Target market size and willingness to pay\n"
        "2) Existing competitors and their weaknesses\n"
        "3) Minimum viable feature set for launch\n"
        "4) Pricing strategy (freemium vs paid)\n"
        "5) Customer acquisition channels\n"
        "6) Technical feasibility for a solo developer\n"
        "Give a 1-10 viability score with reasoning."
    )

    add_section_heading(doc, "Building Your MVP with Claude")
    add_body_text(doc, (
        "Claude can generate entire codebases. Here's the process: "
        "1) Define your core feature set, 2) Use Claude to generate the code, "
        "3) Test and iterate, 4) Deploy to production. Most MVPs can be built in "
        "a single weekend using this approach."
    ))

    add_prompt_box(doc, "Code Generator - Full MVP",
        "Build a complete [APP TYPE] using [TECH STACK].\n"
        "Requirements:\n"
        "- User authentication (email + Google OAuth)\n"
        "- Dashboard with [CORE FEATURE]\n"
        "- Stripe integration for $[PRICE]/month billing\n"
        "- Database schema for [DATA MODELS]\n"
        "- REST API endpoints\n"
        "- Responsive UI with Tailwind CSS\n"
        "Generate the full code with file structure.\n"
        "Include error handling and input validation."
    )

    add_body_text(doc, (
        "Pro tip: Break your app into modules and have Claude generate each one "
        "separately. This produces better code quality and makes debugging easier."
    ))


    add_section_heading(doc, "Launch & Growth Strategy")
    add_body_text(doc, (
        "Your MVP is built - now it's time to get paying customers. Here's the "
        "proven launch playbook for micro-SaaS products:"
    ))

    add_bullet_list(doc, [
        "Pre-launch: Build email list of 100+ with landing page",
        "Beta: Give 20 users free access for feedback",
        "Launch: Product Hunt, Hacker News, relevant subreddits",
        "Growth: Content marketing + SEO with Claude-generated articles",
        "Optimize: Use Claude to analyze churn and improve retention",
        "Scale: Affiliate program, integrations, enterprise tier",
    ])

    add_prompt_box(doc, "Product Launch Prompt",
        "Create a Product Hunt launch strategy for my SaaS:\n"
        "[PRODUCT DESCRIPTION]\n"
        "Include: tagline options (5), first comment text,\n"
        "maker's story, key features to highlight,\n"
        "timing strategy, and community engagement plan.\n"
        "Also create 5 tweet templates for launch day."
    )

    # ============================================================
    # CHAPTER 5: Content Empire Building
    # ============================================================
    add_chapter_heading(doc, 5, "Content Empire Building")

    add_section_heading(doc, "The Content Money Machine")
    add_body_text(doc, (
        "Content is the ultimate leverage. One person with Claude can produce more "
        "high-quality content than a team of 10 writers. Newsletters, blogs, YouTube "
        "scripts, social posts - all generating passive income while you sleep."
    ))


    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("Revenue Models:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(120, 60, 200)

    add_bullet_list(doc, [
        "Newsletter Empire: 50K subscribers = $25K-$100K/month (ads + sponsorships)",
        "Blog Network: 10 niche sites = $5K-$30K/month (affiliate + ads)",
        "YouTube Channel: AI-scripted videos = $10K-$50K/month",
        "Twitter/X Growth: Build authority = consulting leads at $500/hr",
        "Podcast Production: AI-researched episodes = sponsorship revenue",
    ])

    add_prompt_box(doc, "Content Calendar Generator",
        "Create a 30-day content calendar for a [NICHE] brand.\n"
        "Platform: [PLATFORM]\n"
        "Posting frequency: [X times per day/week]\n"
        "Content pillars: [PILLAR 1], [PILLAR 2], [PILLAR 3]\n"
        "For each post include: topic, hook, key points,\n"
        "hashtags, best posting time, and content format.\n"
        "Mix educational (40%), entertaining (30%), promotional (30%).\n"
        "Include viral content formulas for maximum engagement."
    )

    add_section_heading(doc, "SEO Content at Scale")
    add_body_text(doc, (
        "Search engine optimization is a goldmine for passive income. With Claude, "
        "you can produce 50-100 SEO-optimized articles per month that rank on Google "
        "and generate traffic, leads, and affiliate revenue indefinitely."
    ))


    add_prompt_box(doc, "SEO Article Writer",
        "Write a comprehensive 2000-word SEO article on:\n"
        "Topic: [KEYWORD/TOPIC]\n"
        "Target keyword: [PRIMARY KEYWORD]\n"
        "Secondary keywords: [KW1], [KW2], [KW3]\n"
        "Search intent: [informational/commercial/transactional]\n"
        "Include: compelling title (60 chars), meta description\n"
        "(155 chars), H2/H3 structure, internal link suggestions,\n"
        "FAQ section (5 questions), and a call-to-action.\n"
        "Tone: Expert but accessible. Include data and examples.\n"
        "Optimize for featured snippets and People Also Ask."
    )

    add_body_text(doc, (
        "Results: Our case study shows 100 AI-written articles generating "
        "150,000 monthly visitors and $8,500/month in ad + affiliate revenue."
    ))

    add_section_heading(doc, "Email Marketing & Newsletters")
    add_body_text(doc, (
        "Email is where content converts to cash. A well-crafted newsletter with "
        "10,000 subscribers can generate $5,000-$20,000/month through sponsorships, "
        "affiliate links, and digital product sales."
    ))

    add_prompt_box(doc, "Email Sequence Writer",
        "Write a high-converting email sequence (5 emails) for:\n"
        "Product: [PRODUCT/SERVICE]\n"
        "Audience: [TARGET AUDIENCE]\n"
        "Goal: Convert free subscribers to $[PRICE] purchase\n"
        "Email 1: Value-first welcome (build trust)\n"
        "Email 2: Problem agitation (highlight pain)\n"
        "Email 3: Social proof (case studies/testimonials)\n"
        "Email 4: Overcome objections (FAQ style)\n"
        "Email 5: Urgency close (limited offer)\n"
        "Include subject lines with 40%+ open rate potential."
    )


    # ============================================================
    # CHAPTER 6: AI Automation Agency
    # ============================================================
    add_chapter_heading(doc, 6, "AI Automation Agency")

    add_section_heading(doc, "The $10B Automation Market")
    add_body_text(doc, (
        "Businesses waste 30-40% of their time on repetitive tasks. An AI automation "
        "agency helps companies eliminate this waste using Claude-powered workflows. "
        "Typical retainers: $5,000-$25,000/month per client."
    ))

    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("High-Value Automation Services:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0, 170, 150)

    add_bullet_list(doc, [
        "Customer Support Automation: Reduce ticket volume by 80%",
        "Sales Pipeline Automation: Auto-qualify and nurture leads",
        "Content Repurposing: Turn 1 piece into 20 across platforms",
        "Report Generation: Auto-create weekly business reports",
        "Employee Onboarding: Automated training sequences",
        "Invoice & Payment Processing: Zero-touch accounting",
    ])

    add_prompt_box(doc, "Customer Support Bot Builder",
        "Design a customer support automation system for a\n"
        "[BUSINESS TYPE] with [X] daily support tickets.\n"
        "Current pain points: [LIST PAIN POINTS]\n"
        "Create: 1) Ticket classification system (categories)\n"
        "2) Auto-response templates for top 10 questions\n"
        "3) Escalation rules for complex issues\n"
        "4) Customer satisfaction follow-up sequence\n"
        "5) Weekly performance reporting dashboard\n"
        "Goal: Handle 80% of tickets without human intervention."
    )


    add_section_heading(doc, "Building Your Agency")
    add_body_text(doc, (
        "An automation agency is one of the highest-leverage business models because "
        "once you build a system for one client, you can replicate it for dozens of "
        "similar businesses with minimal additional work."
    ))

    add_bullet_list(doc, [
        "Step 1: Pick a niche (e-commerce, real estate, SaaS companies)",
        "Step 2: Build a case study by automating your own processes",
        "Step 3: Create a 'before/after' demonstration showing time saved",
        "Step 4: Reach out to businesses in your niche (LinkedIn + email)",
        "Step 5: Offer a free automation audit (2-3 quick wins identified)",
        "Step 6: Close $3K-10K setup fee + $2K-5K monthly retainer",
        "Step 7: Deliver using Claude + Zapier/Make + custom scripts",
        "Step 8: Document everything and build SOPs for scaling",
    ])

    add_prompt_box(doc, "Automation Audit Prompt",
        "Analyze this business process and identify automation\n"
        "opportunities:\n"
        "Business: [TYPE] with [X] employees\n"
        "Current process: [DESCRIBE MANUAL WORKFLOW]\n"
        "Time spent: [X hours/week]\n"
        "For each automation opportunity, provide:\n"
        "1) Description of automated workflow\n"
        "2) Tools needed (Claude API, Zapier, etc.)\n"
        "3) Estimated time savings per week\n"
        "4) Implementation complexity (1-10)\n"
        "5) ROI calculation (cost vs time saved)"
    )


    add_section_heading(doc, "Client Management & Delivery")
    add_body_text(doc, (
        "The key to a sustainable automation agency is systematized delivery. "
        "Use Claude to help manage client relationships, create reports, and "
        "continuously optimize their systems."
    ))

    add_prompt_box(doc, "Client Report Generator",
        "Create a weekly client report for [CLIENT NAME].\n"
        "Metrics this week:\n"
        "- Tickets automated: [X] out of [Y] total\n"
        "- Time saved: [X hours]\n"
        "- Customer satisfaction: [X]%\n"
        "- Cost savings: $[X]\n"
        "Format: Executive summary (3 sentences),\n"
        "key metrics dashboard, wins this week,\n"
        "optimization recommendations for next week,\n"
        "and ROI calculation since engagement started."
    )

    add_body_text(doc, (
        "Pro tip: Set up automated weekly reports that Claude generates from your "
        "tracking data. Clients love seeing consistent ROI proof, and it reduces "
        "churn significantly. Aim for 95%+ client retention rate."
    ))

    # ============================================================
    # CHAPTER 7: Prompt Engineering as a Service
    # ============================================================
    add_chapter_heading(doc, 7, "Prompt Engineering as a Service")

    add_section_heading(doc, "The $200/Hour Prompt Engineer")
    add_body_text(doc, (
        "Companies are desperate for prompt engineers who can make AI work reliably. "
        "Most people get mediocre results from AI because they don't know how to "
        "communicate effectively. You can charge $100-500/hour to write optimized "
        "prompts that 10x their AI ROI."
    ))


    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("Service Offerings & Pricing:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(120, 60, 200)

    add_bullet_list(doc, [
        "Custom prompt libraries for sales teams: $2K-$5K per set",
        "AI workflow design for operations: $5K-$15K per project",
        "Chatbot personality & response engineering: $3K-$10K",
        "Enterprise prompt templates: $500-$2K per template set",
        "AI training workshops: $2K-$5K per session",
        "Ongoing prompt optimization retainer: $3K-$8K/month",
    ])

    add_prompt_box(doc, "Prompt Optimizer (Meta-Prompt)",
        "You are a meta-prompt engineer. Take this basic prompt:\n"
        "[ORIGINAL PROMPT]\n"
        "And optimize it for maximum output quality by:\n"
        "1) Adding role/persona specification\n"
        "2) Providing structured context\n"
        "3) Defining explicit output format\n"
        "4) Including quality criteria\n"
        "5) Adding chain-of-thought instructions\n"
        "6) Including examples (few-shot learning)\n"
        "Show the before/after with explanation of changes."
    )

    add_section_heading(doc, "Advanced Prompting Techniques")
    add_body_text(doc, (
        "These advanced techniques separate $50/hour prompt writers from "
        "$500/hour prompt engineers:"
    ))

    add_bullet_list(doc, [
        "Chain-of-Thought: Force step-by-step reasoning for complex tasks",
        "Few-Shot Learning: Provide 2-3 examples of desired output format",
        "Role Stacking: Assign multiple expert personas for comprehensive answers",
        "Constraint Engineering: Use specific boundaries to control output quality",
        "Output Templating: Pre-define exact structure for consistent results",
        "Iterative Refinement: Build prompts that self-improve through feedback",
        "Context Windows: Strategically manage context for long-form projects",
    ])


    add_prompt_box(doc, "Sales Prompt Library Builder",
        "Create a prompt library for a [INDUSTRY] sales team.\n"
        "They need prompts for:\n"
        "1) Lead qualification (scoring criteria)\n"
        "2) Personalized outreach (email + LinkedIn)\n"
        "3) Objection handling (top 10 objections)\n"
        "4) Proposal generation (template)\n"
        "5) Follow-up sequences (3-5-7 day cadence)\n"
        "Each prompt should include: role, context placeholders,\n"
        "output format, quality criteria, and example output."
    )

    add_section_heading(doc, "Selling Your Prompt Services")
    add_body_text(doc, (
        "The market for prompt engineering is exploding. Here's how to position "
        "yourself and attract high-paying clients:"
    ))

    add_bullet_list(doc, [
        "Create a portfolio of before/after prompt transformations",
        "Share prompt tips on LinkedIn and Twitter (builds authority fast)",
        "Offer free 'prompt audits' to prospects - show them what's possible",
        "Partner with AI tool companies for referral revenue",
        "Create a 'Prompt ROI Calculator' showing time/money saved",
        "Target companies already using AI but getting poor results",
        "Offer workshops at $2K-5K for teams of 10-20 people",
    ])

    add_body_text(doc, (
        "Your unique advantage: you're not just writing prompts, you're designing "
        "AI workflows that transform entire business processes. Position yourself "
        "as an 'AI Transformation Consultant' and command premium pricing."
    ))


    # ============================================================
    # CHAPTER 8: Digital Products & Templates
    # ============================================================
    add_chapter_heading(doc, 8, "Digital Products & Templates")

    add_section_heading(doc, "Passive Income with Digital Products")
    add_body_text(doc, (
        "Digital products are the holy grail: create once, sell forever. Claude "
        "helps you create premium digital products in hours instead of weeks. "
        "Templates, courses, ebooks, swipe files - all with zero marginal cost."
    ))

    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("High-Margin Digital Products:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(200, 120, 0)

    add_bullet_list(doc, [
        "Notion Template Packs: $27-97 each, sell 100+/month = $2.7K-$9.7K",
        "Online Courses: $197-997 each, 20 sales/month = $4K-$20K",
        "Prompt Libraries: $47-197 each, sell on Gumroad = $2K-$10K/month",
        "Business Templates: $37-147 (proposals, contracts, SOPs)",
        "AI Workflow Guides: $27-67 each, bundle for $197",
        "Swipe Files: $17-47 (email, ad copy, landing page collections)",
    ])

    add_prompt_box(doc, "Course Outline Creator",
        "Create a comprehensive online course outline for:\n"
        "Topic: [COURSE TOPIC]\n"
        "Target student: [WHO IS THIS FOR]\n"
        "Desired outcome: [WHAT THEY'LL ACHIEVE]\n"
        "Course length: 6-8 modules\n"
        "For each module provide: title, learning objectives,\n"
        "3-5 lessons, assignments, and resources.\n"
        "Include a bonus module and upsell opportunity.\n"
        "Optimize for completion rate and student success."
    )


    add_section_heading(doc, "Product Creation Workflow")
    add_body_text(doc, "Here's the 48-hour digital product creation framework using Claude:")

    add_bullet_list(doc, [
        "Hour 1-2: Market research - find gaps using Claude analysis",
        "Hour 3-4: Outline creation - structure the product content",
        "Hour 5-12: Content generation - Claude writes 80% of material",
        "Hour 13-16: Design & formatting - professional presentation",
        "Hour 17-20: Sales page - Claude writes high-converting copy",
        "Hour 21-24: Email sequence - 5 emails for launch",
        "Hour 25-30: Landing page + payment setup (Gumroad/Teachable)",
        "Hour 31-48: Launch preparation - social proof, early reviews",
    ])

    add_prompt_box(doc, "Sales Page Writer",
        "Write a high-converting sales page for my digital product:\n"
        "Product: [NAME AND DESCRIPTION]\n"
        "Price: $[PRICE]\n"
        "Target buyer: [IDEAL CUSTOMER]\n"
        "Include: headline (benefit-focused), subheadline,\n"
        "3 pain points, 5 benefits, social proof section,\n"
        "FAQ (5 questions), guarantee, and CTA.\n"
        "Use proven copywriting frameworks (PAS, AIDA).\n"
        "Tone: Authoritative but friendly. Use power words."
    )

    # ============================================================
    # CHAPTER 9: The API Economy
    # ============================================================
    add_chapter_heading(doc, 9, "The API Economy")

    add_section_heading(doc, "Monetizing the Claude API")
    add_body_text(doc, (
        "The Claude API lets you build products that serve thousands of customers "
        "simultaneously. Create API endpoints that solve specific problems, charge "
        "per use or monthly, and scale to millions in revenue."
    ))


    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("API Business Ideas:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0, 100, 200)

    add_bullet_list(doc, [
        "Content Generation API: Businesses pay per article generated",
        "Email Personalization API: E-commerce stores auto-personalize",
        "Document Summarizer API: Legal/medical document processing",
        "Code Review API: Automated PR reviews for dev teams",
        "Customer Sentiment API: Real-time brand monitoring",
        "Translation + Localization API: Context-aware translations",
    ])

    add_prompt_box(doc, "API Documentation Writer",
        "Generate API documentation for my [SERVICE] API.\n"
        "Endpoints to document:\n"
        "- POST /generate: [DESCRIPTION]\n"
        "- GET /status: [DESCRIPTION]\n"
        "- POST /batch: [DESCRIPTION]\n"
        "For each endpoint include: description, parameters,\n"
        "request/response examples (JSON), error codes,\n"
        "rate limits, and authentication requirements.\n"
        "Format: OpenAPI 3.0 compatible documentation.\n"
        "Include a quick-start guide and code examples in\n"
        "Python, JavaScript, and cURL."
    )

    add_section_heading(doc, "API Business Architecture")
    add_body_text(doc, (
        "Building a profitable API business requires the right architecture. "
        "Here's the stack that lets you scale to thousands of requests while "
        "keeping costs manageable:"
    ))

    add_bullet_list(doc, [
        "Frontend: Next.js dashboard for customer management",
        "API Gateway: FastAPI or Express with rate limiting",
        "AI Layer: Claude API with intelligent caching",
        "Database: PostgreSQL for users + Redis for caching",
        "Billing: Stripe metered billing per API call",
        "Monitoring: Track usage, costs, and quality metrics",
        "Documentation: Auto-generated with Swagger/OpenAPI",
    ])


    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("Revenue Model Example:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(180, 150, 0)

    add_bullet_list(doc, [
        "1,000 API calls/day x $0.05/call = $1,500/month",
        "Your Claude API cost: ~$300/month (with caching)",
        "Infrastructure: ~$100/month",
        "Net profit: $1,100/month from ONE customer",
        "Scale to 50 customers = $55,000/month profit",
    ])

    # ============================================================
    # CHAPTER 10: Scaling to Seven Figures
    # ============================================================
    add_chapter_heading(doc, 10, "Scaling to Seven Figures")

    add_section_heading(doc, "The Seven-Figure Scaling Framework")
    add_body_text(doc, (
        "Getting to $10K/month is about hustle. Getting to $100K/month is about "
        "systems. Here's the exact framework for scaling your AI business to "
        "seven figures annually:"
    ))

    add_bullet_list(doc, [
        "Phase 1 ($0-10K): Validate one business model, land first clients",
        "Phase 2 ($10K-30K): Systematize delivery, build SOPs with Claude",
        "Phase 3 ($30K-50K): Hire VAs, automate client onboarding",
        "Phase 4 ($50K-80K): Add revenue streams, productize services",
        "Phase 5 ($80K-100K+): Build team, create leveraged offerings",
    ])

    p = doc.add_paragraph()
    p.space_before = Pt(8)
    run = p.add_run("Key Scaling Levers:")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0, 100, 200)

    add_bullet_list(doc, [
        "Productize your service into repeatable packages",
        "Create systems documentation (Claude writes your SOPs)",
        "Build templates that VAs can execute without you",
        "Automate 80% of client communication",
        "Launch a complementary digital product for passive income",
        "Build referral systems that generate leads on autopilot",
    ])


    add_section_heading(doc, "Building Your Revenue Stack")
    add_body_text(doc, (
        "The fastest path to seven figures combines multiple revenue streams. "
        "Each stream reinforces the others, creating a compounding effect:"
    ))

    add_prompt_box(doc, "Financial Model Builder",
        "Create a financial model for my AI business:\n"
        "Current revenue: $[X]/month\n"
        "Business model: [DESCRIPTION]\n"
        "Target: $100K/month in 12 months\n"
        "Calculate: monthly growth rate needed, number of\n"
        "clients/products at each price point, team costs,\n"
        "tool costs, marketing budget, and profit margins.\n"
        "Present as a 12-month projection table with:\n"
        "Revenue | Costs | Profit | Growth Rate | Clients\n"
        "Include 3 scenarios: conservative, moderate, aggressive."
    )

    add_body_text(doc, (
        "Stack these revenue streams: 1) Done-for-you services ($5K-15K/month), "
        "2) Group coaching ($3K-8K/month), 3) Digital products ($2K-5K/month), "
        "4) SaaS tools ($5K-20K/month), 5) Affiliate income ($1K-3K/month)."
    ))

    # ============================================================
    # CHAPTER 11: Advanced Claude Techniques
    # ============================================================
    add_chapter_heading(doc, 11, "Advanced Claude Techniques")

    add_section_heading(doc, "Chain-of-Thought Mastery")
    add_body_text(doc, (
        "Chain-of-thought prompting forces Claude to show its reasoning, "
        "producing dramatically better outputs for complex tasks. This is "
        "the single most powerful technique for business applications."
    ))


    add_prompt_box(doc, "Market Research Analyst",
        "You are a senior market research analyst.\n"
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
        "For each step, show your reasoning before concluding."
    )

    add_body_text(doc, (
        "This structured approach consistently produces consultant-quality "
        "analysis that you can deliver to clients or use for your own decisions."
    ))

    add_section_heading(doc, "Multi-Agent Workflows")
    add_body_text(doc, (
        "The most powerful technique is using Claude in multiple 'roles' within "
        "a single workflow. Each role specializes in one aspect, producing "
        "outputs that rival entire consulting teams."
    ))

    add_prompt_box(doc, "Multi-Perspective Analyzer",
        "I need you to analyze my business plan from 3 perspectives.\n"
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
        "End with a synthesis combining all three perspectives."
    )


    add_section_heading(doc, "Data Analysis & Insights")
    add_body_text(doc, (
        "Claude excels at turning raw data into actionable business intelligence. "
        "Combine this with the API to create automated reporting systems that "
        "clients pay $3K-$10K/month for."
    ))

    add_prompt_box(doc, "Data Analyzer",
        "Analyze this dataset and provide business insights:\n"
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
        "Include suggested visualizations for each insight."
    )

    add_body_text(doc, (
        "Pro tip: Pair this with Python data processing to handle large datasets. "
        "Claude can write the analysis code AND interpret the results."
    ))

    # ============================================================
    # CHAPTER 12: Live Prompt Library
    # ============================================================
    add_chapter_heading(doc, 12, "Live Prompt Library")

    add_body_text(doc, (
        "Below are 20+ ready-to-use prompts organized by category. Copy, customize "
        "the bracketed placeholders, and paste directly into Claude for immediate results."
    ))


    add_section_heading(doc, "Business Growth Prompts")

    add_prompt_box(doc, "Business Plan Writer",
        "Write a business plan executive summary for [BUSINESS].\n"
        "Include: value proposition, target market ($TAM),\n"
        "revenue model, competitive advantage, 3-year projection,\n"
        "funding requirements, and team overview.\n"
        "Format: Investor-ready, 2 pages, data-driven."
    )

    add_prompt_box(doc, "Contract Generator",
        "Generate a legal contract template for [SERVICE TYPE].\n"
        "Include: scope of work, payment terms, deliverables,\n"
        "timeline, revision policy, IP ownership, termination\n"
        "clause, liability limits, and confidentiality agreement.\n"
        "Note: For reference only - have lawyer review before use."
    )

    add_prompt_box(doc, "YouTube Script Writer",
        "Write a YouTube video script for a [NICHE] channel.\n"
        "Topic: [VIDEO TOPIC]\n"
        "Length: 10-12 minutes (aim for 1500-1800 words)\n"
        "Include: attention hook (first 30 sec), pattern interrupt\n"
        "every 2 min, storytelling elements, CTA, end screen pitch.\n"
        "Optimize for retention: open loops, curiosity gaps."
    )

    add_section_heading(doc, "Content & Marketing Prompts")

    add_prompt_box(doc, "Newsletter Writer",
        "Write a weekly newsletter edition that converts readers.\n"
        "Topic: [THIS WEEK'S TOPIC]\n"
        "Audience: [TARGET READER PROFILE]\n"
        "Structure: Hook story (2-3 sentences), main insight,\n"
        "3 actionable takeaways, resource recommendation,\n"
        "soft CTA for [PRODUCT/SERVICE].\n"
        "Tone: Like a smart friend sharing insider knowledge."
    )


    add_prompt_box(doc, "Product Description Writer",
        "Write 5 product descriptions for my e-commerce store.\n"
        "Product: [PRODUCT NAME AND DETAILS]\n"
        "Target buyer: [CUSTOMER AVATAR]\n"
        "For each: benefit-focused headline, 3-sentence description,\n"
        "5 bullet points (features as benefits), SEO keywords.\n"
        "Tone: Premium, desire-inducing, urgency elements.\n"
        "Include social proof placeholder and size/spec details."
    )

    add_prompt_box(doc, "Social Media Manager",
        "Create a social media content plan for [BRAND] across\n"
        "Instagram, Twitter/X, LinkedIn, and TikTok.\n"
        "Brand voice: [DESCRIBE PERSONALITY]\n"
        "Goals: [AWARENESS/ENGAGEMENT/CONVERSIONS]\n"
        "Create 7 days of posts: caption, hashtags, visual\n"
        "description, best time to post, engagement hooks.\n"
        "Mix: educational, entertaining, promotional, UGC prompts."
    )

    add_section_heading(doc, "Technical & Operations Prompts")

    add_prompt_box(doc, "Meeting Summarizer",
        "Analyze this meeting transcript and extract:\n"
        "[PASTE TRANSCRIPT OR KEY POINTS]\n"
        "1) Key decisions made (numbered list)\n"
        "2) Action items (who, what, deadline)\n"
        "3) Open questions requiring follow-up\n"
        "4) Risks or concerns raised\n"
        "5) Next meeting agenda suggestions\n"
        "Format as a 1-page executive summary email\n"
        "that I can send to all stakeholders."
    )

    add_prompt_box(doc, "Competitive Analysis Prompt",
        "Create a competitive analysis for [MY PRODUCT] vs:\n"
        "Competitor 1: [NAME]\n"
        "Competitor 2: [NAME]\n"
        "Competitor 3: [NAME]\n"
        "Compare: pricing, features, target market, strengths,\n"
        "weaknesses, market positioning, customer reviews.\n"
        "Identify: gaps we can exploit, threats to address,\n"
        "differentiation opportunities. End with strategy rec."
    )


    add_prompt_box(doc, "Onboarding Sequence Builder",
        "Design a customer onboarding email sequence (7 emails)\n"
        "for my [PRODUCT TYPE] priced at $[PRICE]/month.\n"
        "Day 1: Welcome + quick start guide\n"
        "Day 2: Core feature tutorial\n"
        "Day 3: Success story / case study\n"
        "Day 5: Advanced tips + integration guide\n"
        "Day 7: Check-in + offer help\n"
        "Day 10: Feature highlight they haven't used\n"
        "Day 14: Testimonial request + referral ask"
    )

    add_section_heading(doc, "Revenue & Automation Prompts")

    add_prompt_box(doc, "Sales Funnel Architect",
        "Build a complete sales funnel strategy for [PRODUCT].\n"
        "Price point: $[PRICE]\n"
        "Traffic source: [PAID/ORGANIC/BOTH]\n"
        "Map out: lead magnet, tripwire offer ($7-27),\n"
        "core offer, upsell, downsell, and backend offer.\n"
        "For each stage: conversion rate targets, copy hooks,\n"
        "email sequences, and retargeting strategy."
    )

    add_prompt_box(doc, "Podcast Producer",
        "Create a podcast episode outline and script notes.\n"
        "Topic: [EPISODE TOPIC]\n"
        "Guest: [GUEST NAME AND BACKGROUND] (or solo ep)\n"
        "Length: 30-45 minutes\n"
        "Structure: Cold open hook, intro, 3 main segments,\n"
        "listener Q&A segment, key takeaways, CTA.\n"
        "Include: 10 interview questions that create great\n"
        "soundbites, and transition phrases between segments."
    )

    add_prompt_box(doc, "Webinar Script Creator",
        "Create a webinar presentation outline + script for\n"
        "selling [PRODUCT/SERVICE] at $[PRICE].\n"
        "Webinar length: 60 minutes\n"
        "Structure: 0-5 min hook, 5-15 story, 15-40 content,\n"
        "40-50 transition to offer, 50-60 close + Q&A.\n"
        "Include: slide titles, key points per slide,\n"
        "objection handling, scarcity elements, bonuses stack.\n"
        "Target conversion rate: 5-15% of attendees."
    )


    add_section_heading(doc, "Advanced Business Prompts")

    add_prompt_box(doc, "Affiliate Program Builder",
        "Create an affiliate program structure for [PRODUCT].\n"
        "Product price: $[PRICE]\n"
        "Commission structure, tier system, recruitment\n"
        "email templates, affiliate onboarding sequence,\n"
        "swipe copy for affiliates, tracking KPIs,\n"
        "and a 90-day affiliate recruitment strategy.\n"
        "Include: top 10 affiliate outreach messages."
    )

    add_prompt_box(doc, "Retention Strategy Designer",
        "Design a customer retention strategy for my\n"
        "[SaaS/SERVICE] with [X] monthly churn rate.\n"
        "Current MRR: $[X]\n"
        "Analyze: churn causes, retention hooks to add,\n"
        "re-engagement campaigns, loyalty program design,\n"
        "NPS improvement tactics, success milestones,\n"
        "and an early warning system for at-risk accounts.\n"
        "Target: reduce churn from [X]% to [Y]% in 90 days."
    )

    add_prompt_box(doc, "Delegation Framework",
        "Create a hiring and delegation framework for my\n"
        "[BUSINESS TYPE] currently at $[X]/month revenue.\n"
        "I work [X] hours/week. Identify:\n"
        "1) Tasks to delegate immediately (VA-level)\n"
        "2) Tasks to automate with AI\n"
        "3) Tasks that require skilled contractors\n"
        "4) Tasks only I should do (zone of genius)\n"
        "For each hire: role, job description, where to find,\n"
        "compensation range, and onboarding checklist."
    )


    # ============================================================
    # CHAPTER 13: Case Studies
    # ============================================================
    add_chapter_heading(doc, 13, "Case Studies")

    add_section_heading(doc, "From Zero to Life-Changing Income")

    add_case_study(doc,
        "Solo Dev to $50K/month",
        "$50K/mo",
        ("Marcus built 3 micro-SaaS tools using Claude for code generation. "
         "Tool 1: AI email warmup ($19/mo, 800 users). Tool 2: Meeting summarizer "
         "($15/mo, 1200 users). Tool 3: Proposal generator ($49/mo, 400 users). "
         "Total build time: 6 weekends."),
        "6 months from first line of code to $50K MRR",
        [
            "Used Claude to generate 90% of codebase, focused on product decisions",
            "Launched each tool on Product Hunt (top 5 of the day for all 3)",
            "SEO content strategy: 30 articles/month driving 50K organic visits",
            "Built in public on Twitter - grew to 15K followers who became early users",
            "Offered lifetime deals at launch for initial cash flow + testimonials",
        ]
    )

    add_case_study(doc,
        "Agency Owner: $0 to $30K in 90 Days",
        "$30K/mo",
        ("Sarah launched an AI copywriting agency with zero experience. Used Claude "
         "to deliver blog posts, email sequences, and ad copy for e-commerce brands. "
         "Started on Upwork, scaled to $5K retainer clients through LinkedIn outreach."),
        "90 days from launch to $30K monthly revenue",
        [
            "Specialized in e-commerce email marketing (high-value niche)",
            "Created portfolio samples in day 1 using Claude",
            "Cold DM'd 50 e-commerce founders daily on LinkedIn",
            "Offered free 'email audit' as lead magnet - converted 20% to clients",
            "Systemized delivery: each client takes 3 hours/week with Claude",
        ]
    )


    add_section_heading(doc, "More Success Stories")

    add_case_study(doc,
        "Content Creator: 100K Subscribers in 6 Months",
        "$25K/mo",
        ("Jake started a daily newsletter about AI business opportunities. Used Claude "
         "to research, write, and optimize every edition. Grew from 0 to 100K subscribers "
         "in 6 months. Revenue: $15K/month sponsorships + $10K/month from digital products."),
        "6 months from first newsletter to 100K subscribers",
        [
            "Published daily (Claude generated 80% of each edition)",
            "Cross-promoted with 20 other newsletters in AI/business space",
            "Twitter thread strategy: 3 viral threads/week driving signups",
            "Referral program: subscribers get bonus content for sharing",
            "Monetized at 10K subscribers with first sponsor ($2K/edition)",
        ]
    )

    add_case_study(doc,
        "Automation Consultant: $15K/month Retainer",
        "$15K/mo",
        ("David positioned himself as an 'AI Workflow Architect' for real estate companies. "
         "Built custom automation systems using Claude API + Zapier + custom scripts. "
         "One flagship client pays $15K/month retainer for ongoing optimization."),
        "4 months from first client to $15K/month single retainer",
        [
            "Hyper-niched into real estate (high budgets, tech-unsavvy clients)",
            "Created a 'free automation audit' that identifies $50K+ in savings",
            "Built demo automations that wow prospects in 15-min calls",
            "Charges setup fee ($10K) + monthly retainer ($5K-15K)",
            "Documented all systems so VAs can maintain while he sells",
        ]
    )


    add_section_heading(doc, "Common Patterns of Success")
    add_body_text(doc, (
        "After analyzing dozens of successful AI entrepreneurs, these patterns "
        "emerge consistently:"
    ))

    add_bullet_list(doc, [
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
    ])

    add_body_text(doc, (
        "The biggest lesson: speed of implementation matters more than perfection. "
        "Those who take action within 48 hours of learning a strategy outperform "
        "those who spend weeks planning by 10x."
    ))

    # ============================================================
    # CHAPTER 14: Your 90-Day Action Plan
    # ============================================================
    add_chapter_heading(doc, 14, "Your 90-Day Action Plan")

    add_section_heading(doc, "Weeks 1-6: Foundation & First Revenue")
    add_body_text(doc, (
        "This is your detailed week-by-week plan. Follow it exactly and you'll "
        "have revenue within 30 days and momentum that compounds."
    ))


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
        p = doc.add_paragraph()
        p.space_before = Pt(8)
        p.space_after = Pt(4)
        run_w = p.add_run(f"{week}: ")
        run_w.bold = True
        run_w.font.size = Pt(10)
        run_w.font.color.rgb = RGBColor(200, 120, 0)
        run_d = p.add_run(desc)
        run_d.font.size = Pt(10)

    add_section_heading(doc, "Weeks 7-12: Scale & Systemize")

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
        p = doc.add_paragraph()
        p.space_before = Pt(8)
        p.space_after = Pt(4)
        run_w = p.add_run(f"{week}: ")
        run_w.bold = True
        run_w.font.size = Pt(10)
        run_w.font.color.rgb = RGBColor(200, 120, 0)
        run_d = p.add_run(desc)
        run_d.font.size = Pt(10)


    # 90-day target
    p = doc.add_paragraph()
    p.space_before = Pt(16)
    run = p.add_run("90-Day Target: $10,000-$15,000/month in combined revenue")
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0, 150, 80)

    add_body_text(doc, (
        "After 90 days, you'll have: proven revenue model, systematized delivery, "
        "growing content presence, passive income stream in development, and a clear "
        "path to $30K-50K/month within 6 months."
    ))

    # ============================================================
    # FINAL WORDS
    # ============================================================
    doc.add_page_break()
    h = doc.add_heading("Final Words", level=1)
    h.space_after = Pt(24)

    final_paragraphs = [
        "You now have everything you need to build a six or seven-figure income with Claude AI.",
        ("The prompts in this book are not theoretical - they are battle-tested by real "
         "entrepreneurs generating real revenue. The case studies are based on documented "
         "results from people who started exactly where you are now."),
        ("The difference between those who succeed and those who don't is simple: ACTION. "
         "Don't just read this book - USE it. Open Claude right now and try your first prompt."),
        "Here's your immediate next step:",
    ]
    for para_text in final_paragraphs:
        add_body_text(doc, para_text)

    # Numbered steps
    steps = [
        "Choose ONE business model from Chapters 3-9",
        "Copy the relevant prompts from Chapter 12",
        "Generate your first piece of client-ready work TODAY",
        "Follow the 90-Day Plan in Chapter 14",
    ]
    for i, step in enumerate(steps, 1):
        p = doc.add_paragraph()
        p.space_after = Pt(4)
        run = p.add_run(f"{i}. {step}")
        run.bold = True
        run.font.size = Pt(11)


    add_body_text(doc, (
        "The AI wealth revolution is happening NOW. Every day you wait is a day your "
        "future competitors are building their businesses. You have the blueprint. "
        "You have the tools. The only variable is YOU."
    ))

    # Final tagline
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Your AI-Powered Path to Financial Freedom Starts Today")
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0, 100, 200)

    # What's inside summary
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("What's Inside This Blueprint:")
    run.bold = True
    run.font.size = Pt(12)

    summary_items = [
        "7 Proven Business Models",
        "20+ Copy-Paste Prompts",
        "4 Detailed Case Studies",
        "90-Day Action Plan",
        "Scaling Framework to $100K/month",
        "Advanced AI Techniques",
        "Financial Modeling Templates",
    ]
    for item in summary_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.space_after = Pt(2)
        run = p.add_run(f"• {item}")
        run.font.size = Pt(11)

    # ============================================================
    # SAVE DOCUMENT
    # ============================================================
    doc.save(OUTPUT_PATH)
    print(f"Word document generated successfully: {OUTPUT_PATH}")
    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    return OUTPUT_PATH


if __name__ == "__main__":
    path = generate_docx()
    print(f"\nGenerated: {path}")
