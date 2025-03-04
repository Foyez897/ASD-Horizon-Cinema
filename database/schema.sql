CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin', 'manager', 'booking_staff')) NOT NULL
        );
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE cinemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            location TEXT NOT NULL,
            num_of_screens INTEGER NOT NULL
        );
CREATE TABLE films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            age_rating TEXT NOT NULL,
            description TEXT,
            actors TEXT
        );
CREATE TABLE pricing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            lower_hall_price REAL NOT NULL
        );
CREATE TABLE screens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cinema_id INTEGER NOT NULL,
            screen_number INTEGER NOT NULL,
            total_seats INTEGER NOT NULL,
            FOREIGN KEY (cinema_id) REFERENCES cinemas(id) ON DELETE CASCADE
        );
CREATE TABLE showtimes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            film_id INTEGER NOT NULL,
            cinema_id INTEGER NOT NULL,
            screen_number INTEGER NOT NULL,
            show_time TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (film_id) REFERENCES films(id) ON DELETE CASCADE,
            FOREIGN KEY (cinema_id) REFERENCES cinemas(id) ON DELETE CASCADE
        );
CREATE TABLE seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            showtime_id INTEGER NOT NULL,
            seat_number TEXT NOT NULL,  -- Changed from INTEGER to TEXT
            seat_type TEXT NOT NULL CHECK(seat_type IN ('lower_hall', 'upper_gallery', 'vip')),
            is_booked INTEGER DEFAULT 0,
            price REAL NOT NULL,  -- Added this column
            FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE CASCADE
        );
CREATE TABLE bookings (
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
        );
CREATE TABLE cancellations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            cancellation_date TEXT NOT NULL,
            refund_amount REAL NOT NULL,
            FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
        );
