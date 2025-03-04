import sqlite3

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect("horizon_cinemas.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
    conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign keys
    return conn

def initialize_database():
    """Creates required tables for the Horizon Cinemas Booking System."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table (Admins, Managers, Booking Staff)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin', 'manager', 'booking_staff')) NOT NULL
        )
    ''')

    # Cinemas Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cinemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            location TEXT NOT NULL,
            num_of_screens INTEGER NOT NULL
        )
    ''')

    # Films Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            age_rating TEXT NOT NULL,
            description TEXT,
            actors TEXT
        )
    ''')

    # Pricing Table (Missing in Your Code)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pricing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            lower_hall_price REAL NOT NULL
        )
    ''')

    # Screens Table (Missing in Your Code)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS screens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cinema_id INTEGER NOT NULL,
            screen_number INTEGER NOT NULL,
            total_seats INTEGER NOT NULL,
            FOREIGN KEY (cinema_id) REFERENCES cinemas(id) ON DELETE CASCADE
        )
    ''')

    # Showtimes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS showtimes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            film_id INTEGER NOT NULL,
            cinema_id INTEGER NOT NULL,
            screen_number INTEGER NOT NULL,
            show_time TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (film_id) REFERENCES films(id) ON DELETE CASCADE,
            FOREIGN KEY (cinema_id) REFERENCES cinemas(id) ON DELETE CASCADE
        )
    ''')

    # Seats Table (Fixed seat_number & added price)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            showtime_id INTEGER NOT NULL,
            seat_number TEXT NOT NULL,  -- Changed from INTEGER to TEXT
            seat_type TEXT NOT NULL CHECK(seat_type IN ('lower_hall', 'upper_gallery', 'vip')),
            is_booked INTEGER DEFAULT 0,
            price REAL NOT NULL,  -- Added this column
            FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE CASCADE
        )
    ''')

    # Bookings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_staff_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            showtime_id INTEGER NOT NULL,
            seat_id INTEGER NOT NULL,
            booking_reference TEXT UNIQUE NOT NULL,
            total_price REAL NOT NULL,
            booking_date TEXT NOT NULL,
            FOREIGN KEY (booking_staff_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE
        )
    ''')

    # Cancellations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cancellations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            cancellation_date TEXT NOT NULL,
            refund_amount REAL NOT NULL,
            FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database Initialized Successfully!")

if __name__ == "__main__":
    initialize_database()