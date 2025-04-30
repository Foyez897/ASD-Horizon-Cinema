import sqlite3

DB_PATH = "database/horizon_cinemas.db"  # ✅ Adjust this if needed

def get_db_connection():
    """
    Establish and return a connection to the SQLite database.
    Ensures rows can be accessed by column name.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Allows dict-like row access
        print("✅ get_db_connection() called")
        print(f"📍 USING DB: {DB_PATH}")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

def execute_query(query, params=(), fetch_one=False, fetch_all=False, commit=False):
    """
    Executes a query on the SQLite DB with flexible options.
    - fetch_one: returns one row
    - fetch_all: returns all rows
    - commit: commits changes for INSERT/UPDATE/DELETE
    """
    conn = get_db_connection()
    if not conn:
        return None

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