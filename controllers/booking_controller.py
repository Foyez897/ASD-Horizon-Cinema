import os
import sqlite3
import uuid
from datetime import datetime, timedelta
from database.database_setup import get_db_connection


#  Booking Staff Login


def login_staff(username, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE LOWER(username) = LOWER(?)", (username,))
        user = cursor.fetchone()

    if user and password == user["password"]:  # Replace this with secure hash check if needed
        return {"success": True, "user_id": user["id"]}
    else:
        return {"success": False, "message": "Invalid username or password"}



#  Cinema & Film Data


def fetch_cinemas():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, city, location FROM cinemas")
        return cursor.fetchall()


def fetch_films_by_cinema(cinema_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT films.id, films.title, films.genre, films.age_rating, films.description,
                   GROUP_CONCAT(showtimes.show_time) AS showtimes
            FROM films
            JOIN showtimes ON films.id = showtimes.film_id
            WHERE showtimes.cinema_id = ?
            GROUP BY films.id
        """, (cinema_id,))
        return cursor.fetchall()


def get_showtime_seats(showtime_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id AS showtime_id, s.show_time, s.screen_number, s.cinema_id, f.title
            FROM showtimes s
            JOIN films f ON s.film_id = f.id
            WHERE s.id = ?
        """, (showtime_id,))
        showtime = cursor.fetchone()

        if not showtime:
            return {"error": "Showtime not found"}

        cursor.execute("SELECT city FROM cinemas WHERE id = ?", (showtime["cinema_id"],))
        city = cursor.fetchone()["city"]

        cursor.execute("""
            SELECT id FROM screens
            WHERE screen_number = ? AND cinema_id = ?
        """, (showtime["screen_number"], showtime["cinema_id"]))
        screen_id = cursor.fetchone()["id"]

        cursor.execute("""
            SELECT s.id, s.seat_number, s.seat_type,
                   CASE WHEN b.id IS NOT NULL THEN 1 ELSE 0 END AS is_booked
            FROM seats s
            LEFT JOIN bookings b ON s.id = b.seat_id AND b.showtime_id = ?
            WHERE s.screen_id = ?
            ORDER BY s.seat_number
        """, (showtime_id, screen_id))
        seats = cursor.fetchall()

        seat_list = []
        for seat in seats:
            seat_dict = dict(seat)
            seat_dict["price"] = get_dynamic_price(city, showtime["show_time"], seat_dict["seat_type"])
            seat_list.append(seat_dict)

        return {
            "showtime": dict(showtime),
            "seats": seat_list
        }



#  Price Calculation


def get_dynamic_price(city, show_time, seat_type):
    show_time_obj = datetime.strptime(show_time, "%Y-%m-%d %H:%M:%S")
    hour = show_time_obj.hour
    base_prices = {
        "Birmingham": [5, 6, 7],
        "Bristol": [6, 7, 8],
        "Cardiff": [5, 6, 7],
        "London": [10, 11, 12]
    }
    if 8 <= hour < 12:
        slot = 0
    elif 12 <= hour < 17:
        slot = 1
    else:
        slot = 2
    base = base_prices.get(city, [6, 7, 8])[slot]
    if seat_type.lower() == "upper gallery":
        return round(base * 1.2, 2)
    elif seat_type.lower() == "vip":
        return round(base * 1.2 * 1.2, 2)
    return round(base, 2)



#  Booking Tickets


def book_tickets(user_id, showtime_id, name, email, phone, seat_ids):
    if isinstance(seat_ids, str):
        seat_ids = seat_ids.split(",")

    booking_reference = str(uuid.uuid4())[:8]
    now = datetime.now()
    total_price = 0
    discounts = []

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT show_time, cinema_id FROM showtimes WHERE id = ?", (showtime_id,))
        data = cursor.fetchone()
        if not data:
            return {"error": "Invalid showtime"}

        show_time, cinema_id = data
        dt = datetime.strptime(show_time, "%Y-%m-%d %H:%M:%S")

        if dt > now + timedelta(days=7):
            return {"error": "Booking allowed up to 7 days only"}

        within_30 = 0 <= (dt - now).total_seconds() <= 1800

        cursor.execute("SELECT city FROM cinemas WHERE id = ?", (cinema_id,))
        city = cursor.fetchone()["city"]

        cursor.execute("SELECT COUNT(*) FROM seats WHERE screen_id IN (SELECT id FROM screens WHERE cinema_id = ?)", (cinema_id,))
        total_seats = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM bookings WHERE showtime_id = ?", (showtime_id,))
        booked_seats = cursor.fetchone()[0]
        occupancy = booked_seats / total_seats if total_seats else 1

        last_minute = within_30 and occupancy < 0.7
        family_discount = len(seat_ids) >= 4

        for sid in seat_ids:
            cursor.execute("SELECT seat_type FROM seats WHERE id = ?", (sid,))
            row = cursor.fetchone()
            seat_type = row["seat_type"] if row else "Lower Hall"
            price = get_dynamic_price(city, show_time, seat_type)

            if last_minute:
                price *= 0.75
                if "last_minute" not in discounts:
                    discounts.append("last_minute")
            if family_discount:
                price *= 0.80
                if "family" not in discounts:
                    discounts.append("family")

            total_price += price

            cursor.execute("""
                INSERT INTO bookings (
                    customer_name, customer_email, customer_phone,
                    showtime_id, seat_id, booking_reference, total_price,
                    booking_staff_id, booking_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone, showtime_id, sid, booking_reference,
                  price, user_id, now.strftime("%Y-%m-%d %H:%M:%S")))
            cursor.execute("UPDATE seats SET is_booked = 1 WHERE id = ?", (sid,))

        conn.commit()

    return {
        "booking_reference": booking_reference,
        "total_price": round(total_price, 2),
        "discounts": discounts
    }

# get all cinemas


def get_all_cinemas():
    return fetch_cinemas()


# REFUND

def get_booking_by_ref_or_email(ref_or_email):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.*, s.show_time
            FROM bookings b
            JOIN showtimes s ON b.showtime_id = s.id
            WHERE b.booking_reference = ? OR b.customer_email = ?
        """, (ref_or_email, ref_or_email))
        return cursor.fetchall()

def process_refund(booking_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT showtime_id, total_price, booking_date FROM bookings WHERE id = ?", (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            return {"success": False, "message": "Booking not found"}

        showtime_id = booking["showtime_id"]
        total_price = booking["total_price"]
        booking_date = booking["booking_date"]

        from datetime import datetime, timedelta
        showtime_date = datetime.strptime(booking_date, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()

        if showtime_date.date() <= now.date():
            return {"success": False, "message": "Cancellation not allowed on the day of show"}

        refund = round(total_price * 0.5, 2)
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        cursor.execute("""
            INSERT INTO cancellations (booking_id, cancellation_date, refund_amount)
            VALUES (?, ?, ?)
        """, (booking_id, now.strftime("%Y-%m-%d %H:%M:%S"), refund))
        conn.commit()

        return {"success": True, "refund": refund}