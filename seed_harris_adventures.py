#!/usr/bin/env python3
"""Seed Harris Adventures full show bible into show_bible.db"""
from show_bible import (set_meta, add_character, add_storyline,
                        add_theme, add_song, add_scene, init_db)

init_db()
print("Seeding Harris Adventures Show Bible...")

# ── SHOW META ────────────────────────────────────────────────────────────────
set_meta("show_name", "Harris Adventures")
set_meta("tagline", "Family legacy. Love surviving time. Adventure through imagination.")
set_meta("visual_style", "Studio Ghibli-inspired hand-painted aesthetic. Soft color palettes, atmospheric haze, cinematic warmth, magical realism, whimsical environments, expressive characters, subtle sci-fi elements. Atlanta city realism blended with dreamlike fantasy. Warm cinematic lighting with glowing practical light sources. Slight film grain. Dynamic camera movement. Large expressive eyes and emotional facial animation. Mix cozy interiors with enormous magical landscapes. Emotional moments held with quiet pauses.")
set_meta("music_style", "Deep lofi jazz, soulful textures, hip-hop rhythm, orchestral swells during major reveals, ominous distorted jazz motifs during parasite scenes.")
set_meta("magic_rules", "The Harris bloodline carries a recessive genetic ability. Travel activates only when Dada, Jude, and Zen sleep under the same roof during specific moon alignments. When activated: purple energy leaks from windows, a sonic boom erupts, gravity reverses, the Harris family floats upward from bed, a black hole forms overhead, bodies ascend into cosmic space.")
set_meta("main_threat", "THE PARASITE — Ancient corruption infecting Olympic World. Living black web structures, organic veins, flower roots infected by darkness. Corrupts memory, corrupts nature, turns color into grayness. Feeds on forgotten love and forgotten family bonds.")
set_meta("setting_earth", "Modern Atlanta loft. White ceramic floors, high ceilings, massive windows, Atlanta skyline visible, Mercedes-Benz Stadium visible. Cozy but modern. IKEA bunk bed, robot toys, matchbox cars, plush toys. Dada drives an older vintage white Jeep — rustic and slightly worn but loved.")
set_meta("setting_olympic_world", "Fantasy dream dimension accessed through black holes while sleeping. Floating rocks, giant glowing flowers, alien plants, massive orange planets overhead, soft blue forests, living landscapes, friendly creatures with large teeth, floating islands, cosmic campfires, ancient magical structures, dream physics.")
set_meta("weapon_arrow_of_legacy", "Grandpa's legendary arrow. Glows with family memories and golden energy. Can destroy parasite corruption. Requires remembering family history and love to activate.")
print("  ✓ Show meta set")

# ── CHARACTERS ───────────────────────────────────────────────────────────────
add_character(
    name="Dada",
    role="Main protagonist — father",
    description="Black father in early adulthood. Athletic build. Trim beard. Black shirt almost always worn with cargo pants and Rick Owens Converse-style sneakers.",
    personality="Emotional and playful. Loves his sons deeply. Acts cool but becomes childlike during adventures.",
    backstory="Father of Jude and Zen. Carries the Harris bloodline magic. Represents fatherly love and silliness. His love for his sons is the anchor of the entire story.",
    visual_prompt="Studio Ghibli style. Black father early adulthood, athletic build, trim beard, black shirt, cargo pants, Rick Owens Converse-style sneakers. Large expressive eyes. Warm cinematic lighting. Soft color palette. Hand-painted animation aesthetic."
)
print("  ✓ Character: Dada")

add_character(
    name="Jude",
    role="Main protagonist — younger son",
    description="Young boy with huge curly hair that expands wildly in all directions. Red shirt is signature look. Wide-leg jeans.",
    personality="Innocent but secretly mischievous. Wants to do the right thing but curiosity often gets him into trouble. Large expressive emotions.",
    backstory="Younger Harris son. Carries the bloodline magic. His curiosity and heart are his greatest strengths and greatest weaknesses.",
    visual_prompt="Studio Ghibli style. Young Black boy with huge curly hair exploding in all directions, red shirt, wide-leg jeans. Enormous expressive eyes, giant smile. Childhood wonder energy. Warm hand-painted animation aesthetic."
)
print("  ✓ Character: Jude")

add_character(
    name="Zen",
    role="Main protagonist — older son",
    description="Young boy with long braids. Blue shirt signature look.",
    personality="Tries hard to act cool and emotionally controlled but has an enormous loving heart underneath. Often suppresses smiles. Slightly skeptical expression.",
    backstory="Older Harris son. Carries the bloodline magic. His emotional control and loyalty make him the steady force of the brothers.",
    visual_prompt="Studio Ghibli style. Young Black boy with long braids, blue shirt. Tries to look cool and unimpressed but warm eyes betray his heart. Slightly skeptical expression with suppressed smile. Hand-painted animation aesthetic."
)
print("  ✓ Character: Zen")

add_character(
    name="Eastman",
    role="Guide / interdimensional ally",
    description="Large purple creature with glowing green eyes. Friendly monster appearance with Garfield-like black stripes. Massive smile with big teeth. Mischievous but protective. Speaks entirely in old-school lyrical rap style. Exists between dimensions and guides the Harris family into Olympic World. Strongest form: muscular cosmic body with stars visible beneath skin texture, purple rocket-like energy trails when flying.",
    personality="Mischievous but deeply protective of the Harris family. Communicates only in lyrical rap. Has waited 25 years for this activation.",
    backstory="Interdimensional guide assigned to the Harris bloodline. Serves under Pops. Has been monitoring for the activation conditions for 25 years. Launches like a purple rocket when the family activates.",
    visual_prompt="Studio Ghibli meets cosmic fantasy. Large purple creature, glowing green eyes, Garfield-like black stripes, massive smile with big teeth, friendly monster energy. When in strongest form: muscular cosmic body with stars visible beneath skin, purple rocket energy trails. Hand-painted animation aesthetic, warm cinematic lighting."
)
print("  ✓ Character: Eastman")

add_character(
    name="Grandpa",
    role="Family elder — greatest warrior",
    description="Expert adventurer and greatest warrior in the family lineage. Wears camo fisherman hat with drawstrings. Expert archer and magical practitioner. Carries bow and arrows. Expression rapidly changes from grumpy scowl to giant smile while eyes remain kind.",
    personality="Gruff exterior, enormous heart. Wise but impatient. Expressions shift dramatically — grumpy to overjoyed in an instant.",
    backstory="Greatest warrior in the Harris family lineage. Holds the Arrow of Legacy. His knowledge of Olympic World and the parasite threat is unmatched.",
    visual_prompt="Studio Ghibli style. Older Black man, camo fisherman hat with drawstrings, carries bow and arrows. Expression shifts rapidly between grumpy scowl and giant smile, eyes always kind. Expert warrior energy. Hand-painted animation aesthetic."
)
set_meta("grandpa_catchphrase", "I can bring you to the water but I can't make you drink it.")
print("  ✓ Character: Grandpa")

add_character(
    name="Pops",
    role="Patriarch — ruler of Olympic World",
    description="Grandpa's father. Looks similar to Grandpa but thinner. Resembles an African king with regal features inspired by Haile Selassie energy while remaining original. Silver-gray hair and silver beard. Gruff New York accent mixed with Southern Virginia twang. Military uniform with royal elements. Lives in Olympic World seated on a grand throne. Calm, wise, funny. Smokes cigars.",
    personality="Calm authority. Deeply wise. Has a dry humor that cuts through tension. The final word on everything in Olympic World.",
    backstory="Patriarch of the Harris bloodline. Rules Olympic World from his throne. Has watched the parasite threat grow. Knows the Harris family is the only hope.",
    visual_prompt="Studio Ghibli style. Older Black man, regal African king energy, inspired by Haile Selassie. Silver-gray hair and beard. Military uniform with royal elements. Seated on grand cosmic throne in Olympic World. Smokes cigar. Calm commanding presence. Hand-painted animation aesthetic."
)
print("  ✓ Character: Pops")

# ── THEMES ───────────────────────────────────────────────────────────────────
add_theme("Family Legacy",
    "The Harris bloodline carries magic, memory, and responsibility across generations. The strength of the family's love is literally a weapon against darkness.",
    "warm, weighty, epic")
add_theme("Fathers and Sons",
    "At its core: Dada and his boys. Every adventure is really about how deeply a father loves his children and how that love shapes who they become.",
    "tender, playful, emotional")
add_theme("Memory and Forgotten Love",
    "The parasite feeds on forgotten family bonds. Remembering — truly remembering — is an act of power and resistance.",
    "bittersweet, urgent, healing")
add_theme("Healing Generations",
    "Each generation of the Harris family carries wounds. The adventures are how those wounds get seen, named, and healed.",
    "hopeful, quiet, profound")
add_theme("Childhood Wonder",
    "The world through Jude and Zen's eyes is enormous, magical, and full of possibility. That wonder is not naive — it is a form of strength.",
    "joyful, expansive, curious")
add_theme("Humor During Hardship",
    "The Harris family laughs during the hardest moments. Comedy is how they survive, connect, and remind each other they are loved.",
    "light, warm, disarming")
add_theme("Family Unity Defeating Corruption",
    "The parasite cannot survive in the presence of real family love. Unity is the only weapon that truly works.",
    "triumphant, earned, powerful")
print("  ✓ Themes seeded")

# ── EPISODE 1 STORYLINES ─────────────────────────────────────────────────────
add_storyline(
    title="Airport Reunion",
    arc="Act 1 — Setup",
    synopsis="Dada waits at Atlanta International Airport. Jude sprints toward him with arms wide open. Zen walks behind trying to hide his excitement. Dada has tears in his eyes. Laughter, lemon pepper wings from Jr Crickets debated immediately. The boys are home.",
    episode=1
)
add_storyline(
    title="Drive Through Atlanta",
    arc="Act 1 — Setup",
    synopsis="The white Jeep rolls through Atlanta golden sunset. Bank of America building visible. Boys in booster seats laughing. Warm jazz plays. The city feels like home and magic at once.",
    episode=1
)
add_storyline(
    title="The Loft at Night — Activation",
    arc="Act 1 — Inciting Incident",
    synopsis="Night falls. Moon rises fast. Everyone asleep in pajamas. Purple energy begins leaking from windows. Sonic boom. Gravity reverses. Beds shake. Toys float. Blankets drift. Black hole forms overhead. The Harris family ascends into the cosmos.",
    episode=1
)
add_storyline(
    title="Pops and Eastman — Olympic World",
    arc="Act 2 — Rising Action",
    synopsis="Pops sits on his throne smoking a cigar. Eastman is late. Pops delivers his line: 'Eastman you've been waiting for this 25 years and you're still late to the party!' Eastman grabs space suits and launches — a purple rocket streaking across stars. Cut to: a giant flower in Olympic World slowly turning black. The parasite is spreading.",
    episode=1
)
add_storyline(
    title="First Arrival in Olympic World",
    arc="Act 2 — Rising Action",
    synopsis="The Harris family emerges from the black hole into Olympic World. Floating rocks. Glowing plants. Alien creatures watching. Jude is immediately excited and wide-eyed. Zen tries to stay cool — and fails. Dada is completely stunned. Eastman arrives dramatically, speaks in rhythmic rap. The adventure has officially begun.",
    episode=1
)
print("  ✓ Episode 1 storylines seeded")

# ── SCENES ───────────────────────────────────────────────────────────────────
add_scene(
    episode=1, sequence=1,
    title="Airport Arrival",
    description="Atlanta International Airport. Warm golden lighting. Jude runs toward Dada with giant smile and arms stretched open. Zen walks behind with roller bag trying to hide excitement. Dada has tears in his eyes. Dialogue playful and loving. Ends with lemon pepper wings from Jr Crickets debate.",
    characters=["Dada", "Jude", "Zen"],
    location="Atlanta International Airport",
    mood="warm, joyful, emotional",
    dialogue="Jude: DADAAAAAA! / Dada: (tears, arms open) There he is! There's my boy! / Zen: (cool walk, suppressed grin) Hey Dad. / Dada: ZEN! (grabs both boys) / Jude: WHERE ARE THE LEMON PEPPER WINGS FROM JR CRICKETS?!",
    visual_prompt="Studio Ghibli style. Atlanta International Airport interior. Warm golden lighting. Young Black boy with huge curly hair (red shirt) sprinting toward tall Black man (black shirt, cargo pants, Rick Owens sneakers) with tears streaming. Another boy with long braids (blue shirt) walking behind pulling roller bag with suppressed smile. Cinematic warmth, large expressive eyes, emotional animation. Hand-painted aesthetic."
)
add_scene(
    episode=1, sequence=2,
    title="Drive Through Atlanta",
    description="Exterior driving shot. Older rustic white Jeep driving through Atlanta at golden sunset. Bank of America building visible. Boys in booster seats laughing. Warm jazz music. The city glows.",
    characters=["Dada", "Jude", "Zen"],
    location="Atlanta streets",
    mood="warm, golden, cozy",
    dialogue="Laughter. Back and forth about the city, the trip, plans for the visit.",
    visual_prompt="Studio Ghibli style. Older rustic white Jeep driving through Atlanta, golden sunset light. Bank of America building visible in background. Through rear window: two young Black boys laughing in booster seats — curly hair boy in red shirt, braids boy in blue shirt. Warm jazz atmosphere. Cinematic golden hour. Atmospheric haze, hand-painted animation aesthetic."
)
add_scene(
    episode=1, sequence=3,
    title="The Loft — Activation",
    description="Night. Loft interior. White ceramic floors, high ceilings, massive windows with Atlanta skyline and Mercedes-Benz Stadium visible. Everyone asleep in pajamas. Purple energy begins leaking through windows. Sonic boom erupts outside. Gravity reverses. Beds shake. Toys float upward. Blankets drift. Black hole forms overhead. Bodies slowly rise.",
    characters=["Dada", "Jude", "Zen"],
    location="The Atlanta loft",
    mood="mysterious, magical, dreamlike",
    dialogue="None — silent except for the sonic boom and ambient magical sounds.",
    visual_prompt="Studio Ghibli style. Modern Atlanta loft interior night. White ceramic floors, high ceilings, massive windows showing Atlanta skyline and Mercedes-Benz Stadium. Three sleeping figures in pajamas beginning to float upward. Purple cosmic energy leaking through windows, toys and blankets drifting in zero gravity, massive black hole forming in ceiling. Dreamlike magical atmosphere, soft purple glow, cinematic wonder."
)
add_scene(
    episode=1, sequence=4,
    title="Olympic World — Pops and Eastman",
    description="Olympic World. Grand ancient throne room. Pops seated smoking a cigar with total calm. Eastman scrambling to get space suits. Pops delivers his line. Eastman launches from Olympic World like a purple rocket leaving a massive energy trail across stars. Cut to: a giant glowing flower beginning to turn black. Parasite corruption spreading.",
    characters=["Pops", "Eastman"],
    location="Olympic World — throne room",
    mood="regal, humorous, ominous",
    dialogue="Pops: 'Eastman you've been waiting for this for 25 years and you're still late to the party! Why I oughta... If this cigar wasn't so smooth, I might get off my throne.'",
    visual_prompt="Studio Ghibli meets cosmic fantasy. Ancient grand throne room in Olympic World. Older regal Black man (silver-gray hair and beard, military uniform with royal elements) seated on cosmic throne smoking cigar with total calm. Large purple creature with glowing green eyes and black stripes launching like a rocket leaving purple energy trails across star field. Separate shot: enormous glowing magical flower slowly turning black at edges — parasite corruption beginning. Orchestral ominous tone visually."
)
add_scene(
    episode=1, sequence=5,
    title="Arrival in Olympic World",
    description="Harris family emerges from black hole into Olympic World. Floating rocks. Giant glowing flowers. Alien plants. Massive orange planets overhead. Soft blue forests. Alien creatures with large teeth watching curiously. Jude immediately overwhelmed with excitement. Zen trying desperately to stay cool. Dada completely stunned. Eastman arrives dramatically speaking in rhythmic rap. The adventure begins.",
    characters=["Dada", "Jude", "Zen", "Eastman"],
    location="Olympic World — arrival zone",
    mood="wonder, excitement, epic",
    dialogue="Jude: OH MY— WHAT IS— DAD ARE YOU SEEING THIS?! / Zen: (internal screaming, external cool) ...it's fine. / Dada: What. Is. Happening. / Eastman: (rap) 'Harris family rise, the stars aligned tonight / twenty-five years I've been waiting on this flight!'",
    visual_prompt="Studio Ghibli meets cosmic fantasy. Family of three (tall Black man in black shirt, young boy with huge curly hair in red shirt, young boy with braids in blue shirt) emerging from swirling black hole into Olympic World. Floating rocks, massive glowing flowers in purples and golds, alien plants, enormous orange planets filling the sky, soft blue forest in distance. Friendly alien creatures with large teeth watching. Large purple creature with glowing green eyes arriving dramatically. Overwhelming magical scale, cinematic wonder, warm atmospheric lighting."
)
print("  ✓ Episode 1 scenes seeded")

print("\n" + "═"*56)
print("  HARRIS ADVENTURES — Show Bible Seeded")
print("═"*56)
print("  Run: python3 seed_show.py --status")
print("  to verify everything loaded correctly.\n")
