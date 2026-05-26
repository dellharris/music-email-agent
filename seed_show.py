#!/usr/bin/env python3
"""
Seed the Show Bible — add characters, storylines, themes, and songs
from the command line or interactively.

Usage:
  python3 seed_show.py --show-name "My Show" --tagline "Where music meets magic"
  python3 seed_show.py --character
  python3 seed_show.py --storyline
  python3 seed_show.py --theme
  python3 seed_show.py --song
  python3 seed_show.py --status
"""
import argparse, json
from show_bible import (set_meta, get_meta, add_character, get_characters,
                        add_storyline, get_storylines, add_theme, get_themes,
                        add_song, get_songs)

def prompt(label, required=False, multiline=False):
    print(f"\n  {label}{'*' if required else ''}: ", end="")
    if multiline:
        print("(press Enter twice to finish)")
        lines = []
        while True:
            line = input("  ")
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        return "\n".join(lines[:-1]).strip()
    val = input().strip()
    if required and not val:
        print("  Required — please enter a value.")
        return prompt(label, required, multiline)
    return val or None

def add_character_interactive():
    print("\n── Add Character ──────────────────────────────")
    name        = prompt("Name", required=True)
    role        = prompt("Role (e.g. protagonist, antagonist, sidekick)")
    description = prompt("Physical description")
    personality = prompt("Personality traits")
    backstory   = prompt("Backstory", multiline=True)
    visual      = prompt("Visual generation prompt (for Magica/image AI)")
    image       = prompt("Local image path (optional)")
    add_character(name, role, description, personality, backstory, visual, image)
    print(f"\n  ✓ Character '{name}' added.")

def add_storyline_interactive():
    print("\n── Add Storyline ──────────────────────────────")
    title    = prompt("Title", required=True)
    episode  = prompt("Episode number") or "1"
    arc      = prompt("Story arc (e.g. Act 1 setup, climax, resolution)")
    synopsis = prompt("Synopsis", multiline=True)
    add_storyline(title, arc, synopsis, int(episode))
    print(f"\n  ✓ Storyline '{title}' added.")

def add_theme_interactive():
    print("\n── Add Theme ──────────────────────────────────")
    name        = prompt("Theme name", required=True)
    description = prompt("What this theme means to the show")
    mood        = prompt("Mood/tone (e.g. nostalgic, urgent, playful)")
    add_theme(name, description, mood)
    print(f"\n  ✓ Theme '{name}' added.")

def add_song_interactive():
    print("\n── Add Song ───────────────────────────────────")
    title     = prompt("Song title", required=True)
    artist    = prompt("Artist")
    mood      = prompt("Mood/vibe")
    usage     = prompt("How it's used (e.g. opening theme, scene 3 montage)")
    lyrics    = prompt("Key lyrics or full lyrics", multiline=True)
    file_path = prompt("Local file path (optional)")
    add_song(title, artist, mood, lyrics, usage, file_path)
    print(f"\n  ✓ Song '{title}' added.")

def print_status():
    show_name = get_meta("show_name", "Untitled Show")
    tagline   = get_meta("tagline", "")
    print(f"\n{'═'*56}")
    print(f"  {show_name}")
    if tagline: print(f"  {tagline}")
    print(f"{'═'*56}")

    chars = get_characters()
    print(f"\n  CHARACTERS ({len(chars)})")
    for c in chars:
        print(f"    • {c['name']} — {c['role'] or 'no role set'}")

    stories = get_storylines()
    print(f"\n  STORYLINES ({len(stories)})")
    for s in stories:
        print(f"    • Ep{s['episode']} — {s['title']}")

    themes = get_themes()
    print(f"\n  THEMES ({len(themes)})")
    for t in themes:
        print(f"    • {t['name']} — {t['mood'] or ''}")

    songs = get_songs()
    print(f"\n  SONGS ({len(songs)})")
    for s in songs:
        print(f"    • {s['title']} by {s['artist'] or 'unknown'} — {s['usage'] or ''}")
    print()

def main():
    parser = argparse.ArgumentParser(description="Seed the Show Bible")
    parser.add_argument("--show-name",  help="Set the show name")
    parser.add_argument("--tagline",    help="Set the show tagline")
    parser.add_argument("--character",  action="store_true")
    parser.add_argument("--storyline",  action="store_true")
    parser.add_argument("--theme",      action="store_true")
    parser.add_argument("--song",       action="store_true")
    parser.add_argument("--status",     action="store_true")
    args = parser.parse_args()

    if args.show_name: set_meta("show_name", args.show_name)
    if args.tagline:   set_meta("tagline",   args.tagline)
    if args.character: add_character_interactive()
    if args.storyline: add_storyline_interactive()
    if args.theme:     add_theme_interactive()
    if args.song:      add_song_interactive()
    if args.status or not any(vars(args).values()):
        print_status()

if __name__ == "__main__":
    main()
