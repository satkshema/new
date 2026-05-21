#!/usr/bin/env python3
"""
Generate a 20-page Choose Your Own Adventure PDF book for kids (age 8).
Each page has: title, image placeholder, simple script, and coloring-activity-based navigation.
"""

from fpdf import FPDF


class AdventureBook(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_image_placeholder(self):
        x, y = 20, 30
        w, h = 170, 90
        self.set_draw_color(180, 180, 180)
        self.set_fill_color(245, 245, 245)
        self.rect(x, y, w, h, style="DF")
        self.set_font("Helvetica", "I", 12)
        self.set_text_color(150, 150, 150)
        self.set_xy(x, y + 35)
        self.cell(w, 10, "[  COLOR THIS PICTURE  ]", align="C")
        self.set_text_color(0, 0, 0)

    def add_title(self, title, subtitle=""):
        self.set_font("Helvetica", "B", 18)
        self.set_xy(10, 10)
        self.cell(0, 10, title, align="C")
        if subtitle:
            self.set_font("Helvetica", "I", 11)
            self.set_xy(10, 20)
            self.cell(0, 8, subtitle, align="C")

    def add_script(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_xy(20, 125)
        self.multi_cell(170, 6, text)

    def add_coloring_nav(self, activities):
        self.ln(4)
        self.set_font("Helvetica", "B", 11)
        self.set_x(20)
        self.cell(0, 7, "Coloring Activity - Pick your path!")
        self.ln(8)
        self.set_font("Helvetica", "", 10)
        for act in activities:
            self.set_x(25)
            self.multi_cell(165, 5, act)
            self.ln(2)


# ─── PAGE DATA ────────────────────────────────────────────────────────────────

pages = [
    # PAGE 1
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
    },
    # PAGE 2
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
    },
    # PAGE 3
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
    },
    # PAGE 4
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
    },
    # PAGE 5
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
    },
    # PAGE 6
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
    },
    # PAGE 7
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
    },
    # PAGE 8
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
    },
    # PAGE 9
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
    },
    # PAGE 10
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
    },
    # PAGE 11
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
    },
    # PAGE 12
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
    },
    # PAGE 13
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
    },
    # PAGE 14
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
    },
    # PAGE 15
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
    },
    # PAGE 16
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
    },
    # PAGE 17
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
    },
    # PAGE 18
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
    },
    # PAGE 19
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
    },
    # PAGE 20
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
    },
]


# ─── GENERATE PDF ─────────────────────────────────────────────────────────────

def generate_pdf():
    pdf = AdventureBook(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    for page in pages:
        pdf.add_page()
        pdf.add_title(page["title"], page["subtitle"])
        pdf.add_image_placeholder()
        pdf.add_script(page["script"])
        pdf.add_coloring_nav(page["activities"])

    output_path = "/projects/sandbox/new/adventure_book.pdf"
    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")
    print(f"Total pages: {len(pages)}")


if __name__ == "__main__":
    generate_pdf()
