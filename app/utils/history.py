import psycopg2
from database import DATABASE_URL

def fetch_user_history(user_id: str):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT history FROM users WHERE id = %s", (user_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        return result[0]  # Assuming `history` is a TEXT column
    return ""
