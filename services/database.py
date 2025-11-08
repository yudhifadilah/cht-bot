import sqlite3
from contextlib import closing
from config import DATABASE

def get_conn():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# initialize tables
_conn = get_conn()
with closing(_conn.cursor()) as cur:
    # users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        username TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)
    # settings table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    # products: links stored as JSON string (comma separated)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        links TEXT,
        description TEXT
    )
    """)
    # orders
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        price INTEGER,
        status TEXT,
        resi TEXT,
        proof_file_id TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    _conn.commit()
_conn.close()
