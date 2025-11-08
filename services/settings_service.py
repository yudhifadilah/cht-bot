from services.database import get_conn
import json

def set_setting(key, value):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO settings(key, value) VALUES(?, ?)", (key, str(value)))
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row["value"]
    return default
