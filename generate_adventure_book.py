#!/usr/bin/env python3
"""
Generate a 20-page Choose Your Own Adventure PDF book.
Based on the flowchart: The Crossroads adventure with Ocean, Forest, and Mountain paths.
Each page has an image placeholder and a narrative script.
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
        """Draw a large image placeholder box."""
        x, y = 20, 30
        w, h = 170, 100
        self.set_draw_color(180, 180, 180)
        self.set_fill_color(240, 240, 240)
        self.rect(x, y, w, h, style="DF")
        self.set_font("Helvetica", "I", 14)
        self.set_text_color(150, 150, 150)
        self.set_xy(x, y + 40)
        self.cell(w, 20, "[  IMAGE PLACEHOLDER  ]", align="C")
        self.set_text_color(0, 0, 0)

    def add_title(self, title, subtitle=""):
        self.set_font("Helvetica", "B", 20)
        self.set_xy(10, 10)
        self.cell(0, 12, title, align="C")
        if subtitle:
            self.set_font("Helvetica", "I", 12)
            self.set_xy(10, 22)
            self.cell(0, 8, subtitle, align="C")

    def add_script(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_xy(20, 138)
        self.multi_cell(170, 6, text)

    def add_choices(self, choices):
        self.set_font("Helvetica", "B", 11)
        self.ln(4)
        self.set_x(25)
        self.cell(0, 7, "What do you do?")
        self.ln(8)
        self.set_font("Helvetica", "", 11)
        for choice in choices:
            self.set_x(30)
            self.cell(0, 7, choice)
            self.ln(7)



# ─── PAGE DATA ────────────────────────────────────────────────────────────────
pages = [
    {
        "title": "The Crossroads",
        "subtitle": "Page 1 - The Beginning",
        "script": (
            "You stand at the ancient Crossroads, where three weathered paths diverge into the unknown. "
            "The air hums with magic. To the west, you hear the crash of ocean waves and smell salt on the breeze. "
            "Ahead, a dense canopy of emerald leaves blocks the sky, and the chirping of strange creatures echoes "
            "from within. To the east, jagged mountain peaks pierce the clouds, crackling with distant thunder.\n\n"
            "A stone tablet at your feet reads: 'Choose wisely, traveler. Each path leads to a different destiny.'"
        ),
        "choices": [
            "-> Take the Ocean path (go to Page 3)",
            "-> Take the Forest path (go to Page 9)",
            "-> Take the Mountain path (go to Page 15)",
        ],
    },
    {
        "title": "The Crossroads (continued)",
        "subtitle": "Page 2 - Preparations",
        "script": (
            "Before you choose, you notice a small chest half-buried in the moss beside the tablet. "
            "Inside, you find three items: a glowing compass that points toward water, a seed that pulses "
            "with green light, and a feather that crackles with static electricity.\n\n"
            "You may take ONE item with you. The compass will aid you in the ocean, the seed in the forest, "
            "and the feather in the mountains. Or you may leave them all and trust in your own courage."
        ),
        "choices": [
            "-> Take the compass and head to the Ocean (go to Page 3)",
            "-> Take the seed and enter the Forest (go to Page 9)",
            "-> Take the feather and climb the Mountain (go to Page 15)",
        ],
    },
    {
        "title": "Coral Reef Dive",
        "subtitle": "Page 3 - Ocean Path Begins",
        "script": (
            "You follow the Ocean path down steep cliffs until you reach a crystalline lagoon. "
            "The water is impossibly clear - you can see colorful coral formations hundreds of feet below. "
            "A friendly sea turtle surfaces and seems to beckon you forward.\n\n"
            "You dive in. The water is warm and welcoming. Schools of iridescent fish part around you "
            "as you descend into the reef. Ahead, you see two passages through the coral wall."
        ),
        "choices": [
            "-> Swim through the narrow passage toward the sunken ship (go to Page 6)",
            "-> Follow the turtle through the wide arch toward open water (go to Page 7)",
        ],
    },
]


pages += [
    {
        "title": "Coral Reef Dive (continued)",
        "subtitle": "Page 4 - Deeper Waters",
        "script": (
            "As you swim deeper, bioluminescent jellyfish illuminate your path with soft blue and purple light. "
            "The coral here is ancient - towering pillars covered in centuries of growth. You spot a golden "
            "trident wedged into a rock formation.\n\n"
            "A mermaid appears from behind a coral fan. 'That trident belongs to the Ocean Guardian,' she warns. "
            "'Only the worthy may claim it. Prove yourself in the depths below.'"
        ),
        "choices": [
            "-> Descend toward the sunken ship to prove your worth (go to Page 6)",
            "-> Ask the mermaid about the whale in the distance (go to Page 7)",
        ],
    },
    {
        "title": "Coral Reef Dive (continued)",
        "subtitle": "Page 5 - The Living Reef",
        "script": (
            "The reef itself seems alive with intelligence. Coral polyps open and close in patterns that "
            "look almost like communication. A massive brain coral pulses with a warm glow, and when you "
            "touch it, images flood your mind: an ancient civilization that once lived beneath these waves.\n\n"
            "You see visions of the Deep Abyss - a place where all ocean paths converge. The brain coral "
            "shows you two routes to reach it."
        ),
        "choices": [
            "-> Take the route past the sunken ship (go to Page 6)",
            "-> Take the route through whale territory (go to Page 7)",
        ],
    },
    {
        "title": "Sunken Ship",
        "subtitle": "Page 6 - Ocean Sub-path A",
        "script": (
            "The sunken ship looms before you - a magnificent galleon resting on the ocean floor, its masts "
            "draped with kelp like ghostly sails. Schools of angelfish dart through broken portholes.\n\n"
            "Inside the captain's cabin, you find a waterlogged journal. The last entry reads: "
            "'The Deep Abyss called to us. We sailed too far and found what sleeps below. "
            "If you read this, brave one, take the captain's key and descend. The Guardian awaits.'\n\n"
            "You find the rusted key hanging from the ship's wheel."
        ),
        "choices": [
            "-> Take the key and descend to the Deep Abyss (go to Page 8)",
        ],
    },
    {
        "title": "Whale Encounter",
        "subtitle": "Page 7 - Ocean Sub-path B",
        "script": (
            "A colossal blue whale glides through the open water, its eye - ancient and knowing - fixes on you. "
            "It sings a low, resonant note that vibrates through your entire body. You understand its meaning: "
            "'Little land-walker, you seek the deep places.'\n\n"
            "The whale offers to carry you down to the Deep Abyss on its back. As you ride, it shares "
            "the history of the ocean through song - tales of the Guardian who protects the final gate."
        ),
        "choices": [
            "-> Ride the whale down to the Deep Abyss (go to Page 8)",
        ],
    },
]


pages += [
    {
        "title": "The Deep Abyss",
        "subtitle": "Page 8 - Ocean Merge Point",
        "script": (
            "Whether by ship's key or whale's song, you arrive at the Deep Abyss - a vast underwater cavern "
            "where the ocean floor drops away into infinite darkness. But it's not empty: thousands of "
            "bioluminescent creatures swirl in patterns, forming a living constellation.\n\n"
            "At the center, a massive archway glows with blue-green light. Ancient runes carved into its "
            "frame spell out: 'The Final Gate awaits those who have journeyed through the depths.'\n\n"
            "You feel the ocean's power flowing through you. You are ready."
        ),
        "choices": [
            "-> Step through the archway to the Final Gate (go to Page 20)",
        ],
    },
    {
        "title": "Ancient Forest",
        "subtitle": "Page 9 - Forest Path Begins",
        "script": (
            "You step beneath the canopy and the world transforms. Towering trees with silver bark stretch "
            "hundreds of feet overhead, their leaves filtering the sunlight into dancing green patterns. "
            "The air is thick with the scent of moss and wildflowers.\n\n"
            "Tiny sprites zip between the branches, leaving trails of golden dust. A fox with two tails "
            "watches you from a mossy log, then darts down a winding trail."
        ),
        "choices": [
            "-> Follow the fox deeper into the forest (go to Page 12)",
            "-> Climb the nearest great tree to get your bearings (go to Page 13)",
        ],
    },
    {
        "title": "Ancient Forest (continued)",
        "subtitle": "Page 10 - The Whispering Path",
        "script": (
            "The trees here whisper to each other in a language older than words. If you listen carefully, "
            "you can almost understand them. They speak of a village hidden in the mushroom groves and "
            "a dragon who sleeps in the tallest tree.\n\n"
            "A wooden signpost stands at a fork in the path. One arrow points to 'Mushroom Village' "
            "and the other to 'The Dragon's Tree'. Both are carved with intricate vine patterns."
        ),
        "choices": [
            "-> Head toward Mushroom Village (go to Page 12)",
            "-> Seek the Dragon's Tree (go to Page 13)",
        ],
    },
]


pages += [
    {
        "title": "Ancient Forest (continued)",
        "subtitle": "Page 11 - The Heartwood",
        "script": (
            "Deep in the forest's heart, you find a clearing where the oldest tree stands - its trunk "
            "wider than a castle tower. Its roots form natural archways and its bark is covered in "
            "glowing moss that writes messages in a script you can barely read.\n\n"
            "A forest sprite lands on your shoulder. 'The Crystal Clearing is where all forest paths lead,' "
            "she chimes. 'But you must earn your way. Visit the Mushroom Village for wisdom, "
            "or the Dragon's Tree for courage.'"
        ),
        "choices": [
            "-> Seek wisdom at Mushroom Village (go to Page 12)",
            "-> Seek courage at the Dragon's Tree (go to Page 13)",
        ],
    },
    {
        "title": "Mushroom Village",
        "subtitle": "Page 12 - Forest Sub-path A",
        "script": (
            "The Mushroom Village is extraordinary - dozens of enormous mushrooms have been hollowed out "
            "into cozy homes, connected by rope bridges and spiral staircases. Tiny forest folk bustle about, "
            "tending glowing gardens and brewing potions in acorn cups.\n\n"
            "The village elder, a wizened gnome with a beard of living moss, approaches you. "
            "'Ah, a seeker! You must drink from our Well of Visions to understand the forest's heart. "
            "Only then can you face the Crystal Clearing.'\n\n"
            "You drink. The liquid tastes like starlight, and suddenly you understand the language of trees."
        ),
        "choices": [
            "-> Journey to the Crystal Clearing with your new wisdom (go to Page 14)",
        ],
    },
    {
        "title": "Dragon's Tree",
        "subtitle": "Page 13 - Forest Sub-path B",
        "script": (
            "The Dragon's Tree is the tallest in the forest - a colossal oak whose upper branches disappear "
            "into the clouds. Coiled around its trunk is a dragon, but not the fearsome kind from legends. "
            "This dragon is covered in flower petals instead of scales, and breathes warm mist instead of fire.\n\n"
            "'You wish to reach the Crystal Clearing?' the dragon rumbles gently. 'Then you must answer "
            "my riddle: What grows stronger the more it is shared, yet cannot be held in your hands?'\n\n"
            "You answer: 'Courage.' The dragon smiles and lifts you on its back."
        ),
        "choices": [
            "-> Fly with the dragon to the Crystal Clearing (go to Page 14)",
        ],
    },
]


pages += [
    {
        "title": "The Crystal Clearing",
        "subtitle": "Page 14 - Forest Merge Point",
        "script": (
            "The Crystal Clearing is a perfect circle in the heart of the ancient forest. Enormous crystals "
            "grow from the earth like frozen trees, refracting sunlight into a thousand rainbows. "
            "At the center, a pool of liquid silver reflects not your face, but your truest self.\n\n"
            "The forest spirits gather around you - sprites, talking animals, the flower dragon overhead. "
            "They bow in unison. 'You have proven yourself worthy,' they chorus. 'The path to the "
            "Final Gate is open.'\n\n"
            "A crystal archway materializes, pulsing with emerald light."
        ),
        "choices": [
            "-> Step through the crystal archway to the Final Gate (go to Page 20)",
        ],
    },
    {
        "title": "Storm Peaks",
        "subtitle": "Page 15 - Mountain Path Begins",
        "script": (
            "The Mountain path is steep and treacherous from the start. Wind howls around jagged rocks "
            "as you climb higher, and lightning flashes illuminate a landscape of dramatic cliffs and "
            "bottomless chasms. The air grows thin but electric with energy.\n\n"
            "Above you, two distinct peaks pierce the storm clouds. The left peak holds what appears to be "
            "a temple with golden spires. The right peak is riddled with cave openings that glow "
            "with an eerie orange light."
        ),
        "choices": [
            "-> Climb toward the Sky Temple on the left peak (go to Page 17)",
            "-> Explore the Cave of Winds on the right peak (go to Page 18)",
        ],
    },
    {
        "title": "Storm Peaks (continued)",
        "subtitle": "Page 16 - The Narrow Ridge",
        "script": (
            "You traverse a narrow ridge between the two peaks. On one side, a sheer drop into clouds. "
            "On the other, a vertical cliff face with ancient handholds carved into the stone. "
            "Thunder booms around you and the rock trembles.\n\n"
            "A mountain eagle with a wingspan wider than you are tall lands on a nearby outcrop. "
            "It caws twice and spreads its wings toward the two peaks, as if offering to carry you "
            "to either destination."
        ),
        "choices": [
            "-> Ask the eagle to carry you to the Sky Temple (go to Page 17)",
            "-> Ask the eagle to carry you to the Cave of Winds (go to Page 18)",
        ],
    },
]


pages += [
    {
        "title": "Sky Temple",
        "subtitle": "Page 17 - Mountain Sub-path A",
        "script": (
            "The Sky Temple floats above the peak, connected to the mountain by a bridge of solidified "
            "lightning. Inside, the walls are made of compressed clouds and the floor is polished obsidian "
            "that reflects the stars despite it being daytime.\n\n"
            "Monks made of living wind meditate in perfect stillness. Their leader rises and speaks in a "
            "voice like a gentle breeze: 'You seek the Summit. To reach it, you must learn to walk on air. "
            "Close your eyes. Feel the wind beneath your feet. Trust.'\n\n"
            "You step forward into nothing - and the wind holds you."
        ),
        "choices": [
            "-> Walk on the wind to the Summit merge point (go to Page 19)",
        ],
    },
    {
        "title": "Cave of Winds",
        "subtitle": "Page 18 - Mountain Sub-path B",
        "script": (
            "The Cave of Winds is a labyrinth of tunnels carved by centuries of powerful gales. The walls "
            "are smooth as glass, and the wind creates haunting music as it passes through chambers of "
            "different sizes - a natural organ of stone and air.\n\n"
            "Deep inside, you find a chamber where the wind stops completely. In the silence, you hear "
            "a heartbeat - the mountain's heartbeat. A stone golem awakens from the wall. "
            "'Prove your strength against the storm,' it rumbles, 'and I will show you the Summit path.'\n\n"
            "You brace yourself against its wind blast and hold your ground. The golem nods approvingly."
        ),
        "choices": [
            "-> Follow the golem's path to the Summit (go to Page 19)",
        ],
    },
    {
        "title": "Summit Merge Point",
        "subtitle": "Page 19 - Mountain Merge",
        "script": (
            "You reach the Summit - the highest point in the world. Above the clouds, the sky is a deep "
            "purple studded with visible stars even in daylight. The air is perfectly still here, "
            "as if the storms below dare not reach this sacred place.\n\n"
            "A massive stone doorway stands at the peak, carved with lightning bolt patterns. "
            "The mountain eagle, the wind monks, and the stone golem all appear as silent witnesses. "
            "'You have conquered the heights,' the wind whispers. 'The Final Gate awaits.'"
        ),
        "choices": [
            "-> Pass through the stone doorway to the Final Gate (go to Page 20)",
        ],
    },
]


pages += [
    {
        "title": "The Final Gate",
        "subtitle": "Page 20 - Five Endings",
        "script": (
            "All paths converge here at the Final Gate - a towering archway that shimmers with every color "
            "imaginable. The gate recognizes your journey and the choices you've made. Five pedestals "
            "stand before it, each holding a glowing orb that represents a different destiny:\n\n"
            "1. OCEAN GUARDIAN - A blue orb pulses with tidal power. You become the eternal protector "
            "of the seas, commanding waves and befriending all ocean creatures.\n\n"
            "2. FOREST SPIRIT - A green orb hums with life force. You merge with the ancient forest, "
            "becoming a timeless spirit who nurtures all growing things.\n\n"
            "3. HYBRID TRAVELER - A swirling multi-colored orb. You gain the ability to walk between "
            "all three realms forever, belonging to none but welcome in all.\n\n"
            "4. SKY WANDERER - A silver orb crackles with lightning. You ascend beyond the peaks "
            "to explore the endless skies and the worlds beyond the clouds.\n\n"
            "5. CAVE KEEPER - A warm amber orb radiates ancient wisdom. You become the keeper of "
            "all underground secrets, guardian of the earth's deepest mysteries.\n\n"
            "Which destiny do you choose? The gate opens to your future..."
        ),
        "choices": [
            "-> Touch the blue orb: Become the Ocean Guardian",
            "-> Touch the green orb: Become the Forest Spirit",
            "-> Touch the multi-colored orb: Become the Hybrid Traveler",
            "-> Touch the silver orb: Become the Sky Wanderer",
            "-> Touch the amber orb: Become the Cave Keeper",
        ],
    },
]


# ─── GENERATE PDF ─────────────────────────────────────────────────────────────

def generate_pdf():
    pdf = AdventureBook(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    for i, page in enumerate(pages):
        pdf.add_page()
        pdf.add_title(page["title"], page["subtitle"])
        pdf.add_image_placeholder()
        pdf.add_script(page["script"])
        pdf.add_choices(page["choices"])

    output_path = "/projects/sandbox/new/adventure_book.pdf"
    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")
    print(f"Total pages: {len(pages)}")

if __name__ == "__main__":
    generate_pdf()
