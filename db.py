import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "newsletter.db")

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id TEXT,
            subject     TEXT,
            preview_text TEXT,
            sent_at     TEXT DEFAULT (datetime('now')),
            html_file   TEXT
        );
        CREATE TABLE IF NOT EXISTS seeds (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            content    TEXT NOT NULL,
            source_url TEXT,
            added_at   TEXT DEFAULT (datetime('now')),
            used_at    TEXT,
            campaign_id TEXT
        );
    """)
    db.commit()
    db.close()

def log_campaign(campaign_id, subject, preview_text, html_file):
    db = get_db()
    db.execute(
        "INSERT INTO campaigns (campaign_id, subject, preview_text, html_file) VALUES (?,?,?,?)",
        (campaign_id, subject, preview_text, html_file)
    )
    db.commit()
    db.close()

def get_campaigns():
    db = get_db()
    rows = db.execute("SELECT * FROM campaigns ORDER BY sent_at DESC").fetchall()
    db.close()
    return rows

def get_seeds(used=False):
    db = get_db()
    if used:
        rows = db.execute("SELECT * FROM seeds WHERE used_at IS NOT NULL ORDER BY used_at DESC").fetchall()
    else:
        rows = db.execute("SELECT * FROM seeds WHERE used_at IS NULL ORDER BY added_at ASC").fetchall()
    db.close()
    return rows

def add_seed(content, source_url=None):
    db = get_db()
    db.execute("INSERT INTO seeds (content, source_url) VALUES (?,?)", (content, source_url))
    db.commit()
    db.close()

def pop_next_seed():
    db = get_db()
    row = db.execute("SELECT * FROM seeds WHERE used_at IS NULL ORDER BY added_at ASC LIMIT 1").fetchone()
    if row:
        db.execute("UPDATE seeds SET used_at = datetime('now') WHERE id = ?", (row["id"],))
        db.commit()
    db.close()
    return dict(row) if row else None

def delete_seed(seed_id):
    db = get_db()
    db.execute("DELETE FROM seeds WHERE id = ?", (seed_id,))
    db.commit()
    db.close()

init_db()
