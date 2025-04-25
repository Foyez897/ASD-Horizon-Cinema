import sqlite3
import bcrypt
from database.database_setup import get_db_connection


# User Authentication & Authorization


def authenticate_user(username, password):
    """
    Authenticate a user by username and password.
    Returns a dictionary with user info if valid, else None.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, role FROM users WHERE LOWER(username) = LOWER(?)", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            return {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }
        return None


def get_user_role(user_id):
    """
    Fetch the role of a user by ID.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        return result["role"] if result else None


def is_authorized(user_id, allowed_roles):
    """
    Check if user_id has a role within allowed_roles (list).
    """
    role = get_user_role(user_id)
    return role in allowed_roles

# manager login ( manager credintial)

def login_manager(username, password):
    return authenticate_user(username, password)