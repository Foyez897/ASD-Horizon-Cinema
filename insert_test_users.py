import sqlite3
import bcrypt
from database.database_setup import get_db_connection

def insert_test_users():
    users = [
        ("admin1", "adminpass", "admin"),
        ("manager1", "managerpass", "manager"),
        ("staff1", "staffpass", "staff")
    ]

    conn = get_db_connection()
    cursor = conn.cursor()

    for username, plain_password, role in users:
        # Hash password
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed, role)
            )
        except sqlite3.IntegrityError:
            print(f"User '{username}' already exists. Skipping.")
    
    conn.commit()
    conn.close()
    print("✅ Test users inserted successfully.")

if __name__ == "__main__":
    insert_test_users()