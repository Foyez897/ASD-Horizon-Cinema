from database.database_setup import get_db_connection
import bcrypt
from datetime import datetime

# Manager Login
def manager_login(username, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password, role FROM users WHERE LOWER(username) = LOWER(?)", (username,))
        user = cursor.fetchone()

    if not user:
        return {"success": False, "message": "User not found"}

    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return {"success": False, "message": "Invalid password"}

    if user["role"] != "manager":
        return {"success": False, "message": "Unauthorized: Not a manager account"}

    return {"success": True, "manager_id": user["id"]}


# Dashboard Data
def get_manager_dashboard(manager_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (manager_id,))
        user = cursor.fetchone()

        if not user or user["role"] not in ["manager", "admin"]:
            return {"success": False, "message": "Unauthorized access"}

        cursor.execute("""
            SELECT films.id, films.title, films.genre, films.age_rating,
                   GROUP_CONCAT(DISTINCT showtimes.show_time) AS showtimes
            FROM films
            LEFT JOIN showtimes ON films.id = showtimes.film_id AND showtimes.show_time > CURRENT_TIMESTAMP
            GROUP BY films.id
        """)
        booking_summary = cursor.fetchall()

    return {"success": True, "booking_summary": booking_summary}


# Add Cinema & Screens
def add_cinema(city, address, num_of_screens, seat_config, seat_data_per_screen):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cinemas (city, location, num_of_screens) VALUES (?, ?, ?)",
            (city, address, num_of_screens)
        )
        cinema_id = cursor.lastrowid

        for i in range(1, num_of_screens + 1):
            total_seats = seat_data_per_screen.get(f"total_seats_{i}", 50)
            vip_count = seat_data_per_screen.get(f"vip_count_{i}", 0)

            cursor.execute(
                "INSERT INTO screens (cinema_id, screen_number, total_seats) VALUES (?, ?, ?)",
                (cinema_id, i, total_seats)
            )
            screen_id = cursor.lastrowid

            generate_seats(cursor, screen_id, total_seats, vip_count)

        conn.commit()

    return {"success": True, "message": "Cinema and screens added successfully"}


# Seat Generator
def generate_seats(cursor, screen_id, total_seats, vip_count=10):
    lower = round(total_seats * 0.3)
    vip = min(vip_count, total_seats - lower)
    upper = total_seats - lower - vip
    seat_number = 1

    for _ in range(lower):
        cursor.execute(
            "INSERT INTO seats (screen_id, seat_number, seat_type, is_booked) VALUES (?, ?, ?, 0)",
            (screen_id, seat_number, "Lower Hall"))
        seat_number += 1

    for _ in range(upper):
        cursor.execute(
            "INSERT INTO seats (screen_id, seat_number, seat_type, is_booked) VALUES (?, ?, ?, 0)",
            (screen_id, seat_number, "Upper Gallery"))
        seat_number += 1

    for _ in range(vip):
        cursor.execute(
            "INSERT INTO seats (screen_id, seat_number, seat_type, is_booked) VALUES (?, ?, ?, 0)",
            (screen_id, seat_number, "VIP"))
        seat_number += 1


# ✅ Get all cinemas
def get_all_cinemas():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, city, location, num_of_screens FROM cinemas")
        cinemas = cursor.fetchall()
    return cinemas


# ✅ Delete cinema
def delete_cinema(cinema_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cinemas WHERE id = ?", (cinema_id,))
        conn.commit()
    return {"success": True, "message": "Cinema deleted successfully"}


# ✅ Update cinema screen count
def update_cinema_screens(cinema_id, new_screen_count):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE cinemas SET num_of_screens = ? WHERE id = ?", (new_screen_count, cinema_id))
        conn.commit()
    return {"success": True, "message": "Number of screens updated"}
