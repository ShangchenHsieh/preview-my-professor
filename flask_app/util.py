import db_config

def test_db_connection() -> dict:
    cur, conn = db_config.get_cursor_and_connection()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res


# test_db_connection()
