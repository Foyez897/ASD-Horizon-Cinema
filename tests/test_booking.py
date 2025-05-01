import pytest
from controllers.booking_controller import book_tickets, get_dynamic_price
from database.database_setup import get_db_connection

def setup_test_db():
    with get_db_connection(testing=True) as conn:
        cursor = conn.cursor()
        cursor.executescript("""
            DROP TABLE IF EXISTS bookings;
            DROP TABLE IF EXISTS seats;
            DROP TABLE IF EXISTS showtimes;
            DROP TABLE IF EXISTS screens;
            DROP TABLE IF EXISTS cinemas;
            DROP TABLE IF EXISTS films;

            CREATE TABLE cinemas (
                id INTEGER PRIMARY KEY,
                city TEXT,
                location TEXT
            );

            CREATE TABLE films (
                id INTEGER PRIMARY KEY,
                title TEXT,
                genre TEXT,
                age_rating TEXT,
                description TEXT
            );

            CREATE TABLE screens (
                id INTEGER PRIMARY KEY,
                cinema_id INTEGER,
                screen_number INTEGER
            );

            CREATE TABLE showtimes (
                id INTEGER PRIMARY KEY,
                show_time TEXT,
                cinema_id INTEGER,
                screen_number INTEGER,
                film_id INTEGER
            );

            CREATE TABLE seats (
                id INTEGER PRIMARY KEY,
                seat_number TEXT,
                seat_type TEXT,
                screen_id INTEGER
            );

            CREATE TABLE bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                customer_email TEXT,
                customer_phone TEXT,
                showtime_id INTEGER,
                seat_id INTEGER,
                booking_reference TEXT,
                total_price REAL,
                booking_staff_id INTEGER,
                booking_date TEXT
            );
        """)

        # ✅ Insert dummy cinema, film, screen, showtime, seat
        cursor.execute("INSERT INTO cinemas VALUES (1, 'London', 'Main St')")
        cursor.execute("INSERT INTO films VALUES (1, 'Test Movie', 'Drama', 'PG', 'Test Desc')")
        cursor.execute("INSERT INTO screens VALUES (1, 1, 1)")
        cursor.execute("INSERT INTO showtimes VALUES (1, '2025-05-05 14:00:00', 1, 1, 1)")
        cursor.execute("INSERT INTO seats VALUES (1, 'A1', 'Lower Hall', 1)")

        conn.commit()

@pytest.fixture(autouse=True)
def run_setup():
    setup_test_db()

def test_successful_booking():
    response = book_tickets(
        user_id=1,
        showtime_id=1,
        name="Test User",
        email="test@example.com",
        phone="1234567890",
        seat_ids=["1"]
    )
    assert response["booking_reference"]
    assert response["total_price"] > 0
    assert isinstance(response["discounts"], list)