from utils.db_connection import get_db_connection

def get_showtime_map_for_cinema(cinema_id, date):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Fetch all showtimes for the selected cinema and date
        cursor.execute("""
            SELECT s.screen_number, s.show_time, f.title
            FROM showtimes s
            JOIN films f ON s.film_id = f.id
            WHERE s.cinema_id = ? AND DATE(s.show_time) = ?
        """, (cinema_id, date))
        showtimes = cursor.fetchall()

        # Fetch all unique screen numbers for the cinema
        cursor.execute("""
            SELECT DISTINCT screen_number
            FROM showtimes
            WHERE cinema_id = ?
        """, (cinema_id,))
        screens = [row["screen_number"] for row in cursor.fetchall()]

        # Define standard time slots (you can make this dynamic if needed)
        time_slots = ["12:00", "15:00", "18:00", "21:00"]

    # Build mapping: (screen_number, time_slot) -> dict with full info
    showtime_map = {}
    for s in showtimes:
        time_str = s["show_time"][11:16]  # Extract HH:MM from show_time
        key = (s["screen_number"], time_str)
        showtime_map[key] = {
            "title": s["title"],
            "show_time": s["show_time"]
        }

    return showtime_map, screens, time_slots