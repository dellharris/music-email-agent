#!/usr/bin/env python3
"""
Show Bible — SQLite knowledge base for the animated show.
Stores characters, storylines, themes, songs, scenes, and visual references.
All agents read from and write to this shared database.
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "show_bible.db")

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS show_meta (
            key   TEXT PRIMARY KEY,
            value TEXT
        );

        CREATE TABLE IF NOT EXISTS characters (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            role          TEXT,
            description   TEXT,
            personality   TEXT,
            backstory     TEXT,
            visual_prompt TEXT,
            image_path    TEXT,
            image_b64     TEXT,
            magica_model  TEXT,
            created_at    TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS storylines (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            arc         TEXT,
            synopsis    TEXT,
            episode     INTEGER,
            status      TEXT DEFAULT 'draft',
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS themes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT,
            mood        TEXT,
            examples    TEXT
        );

        CREATE TABLE IF NOT EXISTS songs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            artist      TEXT,
            mood        TEXT,
            lyrics      TEXT,
            usage       TEXT,
            file_path   TEXT,
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS scenes (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            episode        INTEGER DEFAULT 1,
            sequence       INTEGER,
            title          TEXT,
            description    TEXT,
            characters     TEXT,
            location       TEXT,
            mood           TEXT,
            dialogue       TEXT,
            visual_prompt  TEXT,
            image_path     TEXT,
            status         TEXT DEFAULT 'pending',
            created_at     TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS agent_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            agent      TEXT,
            action     TEXT,
            result     TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    db.commit()
    db.close()

# ── Show meta ────────────────────────────────────────────────────────────────

def set_meta(key, value):
    db = get_db()
    db.execute("INSERT OR REPLACE INTO show_meta (key, value) VALUES (?,?)", (key, str(value)))
    db.commit(); db.close()

def get_meta(key, default=None):
    db = get_db()
    row = db.execute("SELECT value FROM show_meta WHERE key=?", (key,)).fetchone()
    db.close()
    return row["value"] if row else default

# ── Characters ───────────────────────────────────────────────────────────────

def add_character(name, role=None, description=None, personality=None,
                  backstory=None, visual_prompt=None, image_path=None):
    db = get_db()
    db.execute("""INSERT INTO characters
        (name,role,description,personality,backstory,visual_prompt,image_path)
        VALUES (?,?,?,?,?,?,?)""",
        (name, role, description, personality, backstory, visual_prompt, image_path))
    db.commit(); db.close()

def get_characters():
    db = get_db()
    rows = db.execute("SELECT * FROM characters ORDER BY id").fetchall()
    db.close()
    return [dict(r) for r in rows]

def update_character(char_id, **kwargs):
    db = get_db()
    sets = ", ".join(f"{k}=?" for k in kwargs)
    db.execute(f"UPDATE characters SET {sets} WHERE id=?", (*kwargs.values(), char_id))
    db.commit(); db.close()

# ── Storylines ───────────────────────────────────────────────────────────────

def add_storyline(title, arc=None, synopsis=None, episode=1):
    db = get_db()
    db.execute("INSERT INTO storylines (title,arc,synopsis,episode) VALUES (?,?,?,?)",
               (title, arc, synopsis, episode))
    db.commit(); db.close()

def get_storylines(episode=None):
    db = get_db()
    if episode:
        rows = db.execute("SELECT * FROM storylines WHERE episode=? ORDER BY id", (episode,)).fetchall()
    else:
        rows = db.execute("SELECT * FROM storylines ORDER BY episode, id").fetchall()
    db.close()
    return [dict(r) for r in rows]

# ── Themes ───────────────────────────────────────────────────────────────────

def add_theme(name, description=None, mood=None, examples=None):
    db = get_db()
    db.execute("INSERT INTO themes (name,description,mood,examples) VALUES (?,?,?,?)",
               (name, description, mood, json.dumps(examples or [])))
    db.commit(); db.close()

def get_themes():
    db = get_db()
    rows = db.execute("SELECT * FROM themes ORDER BY id").fetchall()
    db.close()
    return [dict(r) for r in rows]

# ── Songs ────────────────────────────────────────────────────────────────────

def add_song(title, artist=None, mood=None, lyrics=None, usage=None, file_path=None):
    db = get_db()
    db.execute("INSERT INTO songs (title,artist,mood,lyrics,usage,file_path) VALUES (?,?,?,?,?,?)",
               (title, artist, mood, lyrics, usage, file_path))
    db.commit(); db.close()

def get_songs():
    db = get_db()
    rows = db.execute("SELECT * FROM songs ORDER BY id").fetchall()
    db.close()
    return [dict(r) for r in rows]

# ── Scenes ───────────────────────────────────────────────────────────────────

def add_scene(episode=1, sequence=None, title=None, description=None,
              characters=None, location=None, mood=None, dialogue=None, visual_prompt=None):
    db = get_db()
    db.execute("""INSERT INTO scenes
        (episode,sequence,title,description,characters,location,mood,dialogue,visual_prompt)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (episode, sequence, title, description,
         json.dumps(characters or []), location, mood, dialogue, visual_prompt))
    db.commit(); db.close()

def get_scenes(episode=1):
    db = get_db()
    rows = db.execute("SELECT * FROM scenes WHERE episode=? ORDER BY sequence", (episode,)).fetchall()
    db.close()
    return [dict(r) for r in rows]

def update_scene(scene_id, **kwargs):
    db = get_db()
    sets = ", ".join(f"{k}=?" for k in kwargs)
    db.execute(f"UPDATE scenes SET {sets} WHERE id=?", (*kwargs.values(), scene_id))
    db.commit(); db.close()

# ── Agent log ────────────────────────────────────────────────────────────────

def log_agent(agent, action, result=None):
    db = get_db()
    db.execute("INSERT INTO agent_log (agent,action,result) VALUES (?,?,?)",
               (agent, action, result))
    db.commit(); db.close()

def get_agent_log(limit=50):
    db = get_db()
    rows = db.execute("SELECT * FROM agent_log ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    db.close()
    return [dict(r) for r in rows]

init_db()
