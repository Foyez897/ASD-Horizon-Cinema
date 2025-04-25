from database.database_setup import get_db_connection

def get_showtime_map_for_cinema(cinema_id, date):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.screen_number, s.show_time, f.title
            FROM showtimes s
            JOIN films f ON s.film_id = f.id
            WHERE s.cinema_id = ? AND DATE(s.show_time) = ?
        """, (cinema_id, date))
        showtimes = cursor.fetchall()

    showtime_map = {}
    for s in showtimes:
        key = (s["screen_number"], s["show_time"][11:16])
        showtime_map[key] = s["title"]
    return showtime_map