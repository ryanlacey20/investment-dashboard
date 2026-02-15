import sqlite3

DB_PATH = "tokens.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY,
            refresh_token TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_refresh_token():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT refresh_token FROM tokens WHERE id = 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def save_refresh_token(token):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO tokens (id, refresh_token) VALUES (1, ?)", (token,))
    conn.commit()
    conn.close()
