import sqlite3
import bcrypt
from database.database_setup import get_db_connection

def authenticate_user(username, password):
    """
    Authenticate a user by username and password.
    Returns a dictionary with user info if valid, else None.
    """
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # Ensures dictionary-style row access
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, role FROM users WHERE LOWER(username) = LOWER(?)", (username,))
        user = cursor.fetchone()
        conn.close()

        # Debug: show what type we received
        print("🔍 Raw DB result type:", type(user))

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            user_dict = {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }
            print("✅ Authenticated user:", user_dict)
            return user_dict

    except Exception as e:
        print("❌ Error in authenticate_user():", e)

    return None