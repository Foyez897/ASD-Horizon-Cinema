import sqlite3

DB_PATH = "database/horizon_cinemas.db"  # Path to the SQLite database

def get_connection():
    """Establish and return a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

def execute_query(query, params=(), fetch_one=False, fetch_all=False, commit=False):
    """Executes an SQLite query safely and ensures proper return types."""
    conn = sqlite3.connect(DB_PATH)  # Correct path to the database
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        if commit:
            conn.commit()
        if fetch_one:
            result = cursor.fetchone()
            return result if result else (0,)  # Ensure tuple return
        if fetch_all:
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ SQL Error: {e}")
        return None
    finally:
        conn.close()