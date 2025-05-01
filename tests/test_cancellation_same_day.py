import pytest
import sqlite3
from datetime import datetime
from database.database_setup import get_db_connection
from controllers.booking_controller import process_refund

def setup_test_db():
    with get_db_connection(testing=True) as conn:
        cursor = conn.cursor()
        cursor.executescript("""
            DROP TABLE IF EXISTS cancellations;
            DROP TABLE IF EXISTS bookings;
            DROP TABLE IF EXISTS seats;
            DROP TABLE IF EXISTS showtimes;
            DROP TABLE IF EXISTS screens;
            DROP TABLE IF EXISTS cinemas;
            DROP TABLE IF EXISTS films;

            CREATE TABLE films (
                id INTEGER PRIMARY KEY,
                title TEXT,
                genre TEXT,
                age_rating TEXT
            );

            CREATE TABLE cinemas (
                id INTEGER PRIMARY KEY,
                city TEXT,
                location TEXT
            );

            CREATE TABLE screens (
                id INTEGER PRIMARY KEY,
                screen_number INTEGER,
                cinema_id INTEGER
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
                id INTEGER PRIMARY KEY,
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

            CREATE TABLE cancellations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER,
                cancellation_date TEXT,
                refund_amount REAL
            );
        """)

        # Insert test data for same-day showtime
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO films VALUES (1, 'Test Film', 'Drama', 'PG')")
        cursor.execute("INSERT INTO cinemas VALUES (1, 'London', 'Central')")
        cursor.execute("INSERT INTO screens VALUES (1, 1, 1)")
        cursor.execute("INSERT INTO showtimes VALUES (1, ?, 1, 1, 1)", (now_str,))
        cursor.execute("INSERT INTO seats VALUES (1, 'A1', 'lower hall', 1)")

        cursor.execute("""
            INSERT INTO bookings (
                id, customer_name, customer_email, customer_phone,
                showtime_id, seat_id, booking_reference, total_price,
                booking_staff_id, booking_date
            ) VALUES (1, 'SameDay User', 'sameday@example.com', '0000000000',
                      1, 1, 'SAME1234', 10.0, 3, ?)
        """, (now_str,))

        conn.commit()

@pytest.fixture(autouse=True)
def run_setup():
    setup_test_db()

def test_refund_denied_same_day():
    result = process_refund(1, testing=True)  # ✅ Pass testing=True
    assert result["success"] is False
    assert "not allowed" in result["message"].lower()