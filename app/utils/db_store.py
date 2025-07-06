import psycopg2
import os
from database import DATABASE_URL


def update_user_history(user_id: str, new_entry: str):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Fetch current history
        cur.execute("SELECT history FROM users WHERE id = %s", (user_id,))
        current = cur.fetchone()
        current_history = current[0] if current else ""

        # Append new entry
        updated_history = (current_history + "\n" + new_entry).strip()
        cur.execute("UPDATE users SET history = %s WHERE id = %s", (updated_history, user_id))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB update error:", e)
