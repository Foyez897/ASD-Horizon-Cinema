from database.database_setup import get_db_connection

def get_bookings_per_film():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.title AS film_title, COUNT(b.id) AS total_bookings
            FROM bookings b
            JOIN showtimes s ON b.showtime_id = s.id
            JOIN films f ON s.film_id = f.id
            GROUP BY f.title
            ORDER BY total_bookings DESC
        """)
        return cursor.fetchall()

def get_monthly_revenue():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y-%m', s.show_time) AS month, SUM(s.price) AS revenue
            FROM bookings b
            JOIN showtimes s ON b.showtime_id = s.id
            GROUP BY month
            ORDER BY month ASC
        """)
        return cursor.fetchall()

def get_top_film():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.title AS film_title, COUNT(b.id) AS total_bookings
            FROM bookings b
            JOIN showtimes s ON b.showtime_id = s.id
            JOIN films f ON s.film_id = f.id
            GROUP BY f.title
            ORDER BY total_bookings DESC
            LIMIT 1
        """)
        return cursor.fetchone()

def get_staff_bookings():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.username AS staff_name,
                   strftime('%Y-%m', b.booking_date) AS month,
                   COUNT(b.id) AS total_bookings
            FROM bookings b
            JOIN users u ON b.booking_staff_id = u.id
            GROUP BY u.username, month
            ORDER BY month DESC, total_bookings DESC
        """)
        return cursor.fetchall()
