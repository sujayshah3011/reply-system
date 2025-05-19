import sqlite3

def init_db():
    conn = sqlite3.connect("replies.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            post_text TEXT,
            generated_reply TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_reply(platform: str, post_text: str, generated_reply: str, timestamp: str):
    conn = sqlite3.connect("replies.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO replies (platform, post_text, generated_reply, timestamp) VALUES (?, ?, ?, ?)",
        (platform, post_text, generated_reply, timestamp)
    )
    conn.commit()
    conn.close()