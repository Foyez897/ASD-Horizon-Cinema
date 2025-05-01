import pytest
import os
import sqlite3
from datetime import datetime, timedelta
from controllers.booking_controller import process_refund
from database.database_setup import get_db_connection


TEST_DB_PATH = "database/horizon_cinemas_test.db"


def setup_test_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    with get_db_connection(testing=True) as conn:
        cursor = conn.cursor()

        # Create necessary tables
        cursor.executescript("""
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

            CREATE TABLE showtimes (
                id INTEGER PRIMARY KEY,
                show_time TEXT,
                cinema_id INTEGER,
                screen_number INTEGER,
                film_id INTEGER
            );

            CREATE TABLE cancellations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER,
                cancellation_date TEXT,
                refund_amount REAL
            );

            CREATE TABLE cinemas (
                id INTEGER PRIMARY KEY,
                city TEXT,
                location TEXT
            );

            CREATE TABLE screens (
                id INTEGER PRIMARY KEY,
                cinema_id INTEGER,
                screen_number INTEGER
            );

            CREATE TABLE seats (
                id INTEGER PRIMARY KEY,
                screen_id INTEGER,
                seat_number TEXT,
                seat_type TEXT
            );
        """)

        # Insert test cinema, screen, showtime, seat, booking
        now = datetime.now()
        future_showtime = (now + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO cinemas (id, city, location) VALUES (1, 'London', 'Central')")
        cursor.execute("INSERT INTO screens (id, cinema_id, screen_number) VALUES (1, 1, 1)")
        cursor.execute("INSERT INTO seats (id, screen_id, seat_number, seat_type) VALUES (1, 1, 'A1', 'Lower Hall')")
        cursor.execute("INSERT INTO showtimes (id, show_time, cinema_id, screen_number, film_id) VALUES (1, ?, 1, 1, 1)", (future_showtime,))
        cursor.execute("""
            INSERT INTO bookings (
                id, customer_name, customer_email, customer_phone,
                showtime_id, seat_id, booking_reference,
                total_price, booking_staff_id, booking_date
            ) VALUES (
                1, 'Test User', 'test@example.com', '1234567890',
                1, 1, 'TESTREF',
                10.00, 1, ?
            )
        """, (future_showtime,))

        conn.commit()


@pytest.fixture(autouse=True)
def run_setup():
    setup_test_db()


def test_successful_refund():
    result = process_refund(1, testing=True)  # ✅ now uses test DB
    assert result["success"] is True
    assert result["refund"] == 5.00  # 50% of £10