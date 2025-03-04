import datetime
import random
import string
from utils.db_connection import execute_query

def generate_booking_reference():
    """Generate a truly unique booking reference by checking existing records before returning."""
    # Create a temporary table to store used references if it doesn't exist
    execute_query("CREATE TABLE IF NOT EXISTS temp_booking_references (reference TEXT UNIQUE NOT NULL);", commit=True)

    while True:
        # Generate a random 8-character reference
        reference = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        try:
            # Try inserting the reference into the temporary table
            execute_query("INSERT INTO temp_booking_references (reference) VALUES (?);", (reference,), commit=True)

            # If successful, return the unique reference
            return reference

        except Exception as e:
            if "UNIQUE constraint failed" in str(e):  # If the reference already exists, retry
                continue
            else:
                print(f"❌ Database Error: {e}")
                return None  # Return None if a database issue occurs
def check_seat_availability(showtime_id, num_tickets, seat_type):
    query = """
    SELECT COUNT(*) FROM seats 
    WHERE showtime_id = ? AND seat_type = ? AND is_booked = 0;
    """
    result = execute_query(query, (showtime_id, seat_type), fetch_one=True)
    
    seat_count = result[0] if isinstance(result, tuple) else result
    print(f"🔍 Checking seat availability: ShowTime {showtime_id}, Type {seat_type}, Found Seats: {seat_count}, Needed: {num_tickets}")

    return seat_count >= num_tickets


def book_tickets(booking_staff_id, customer_name, customer_phone, customer_email, showtime_id, num_tickets, seat_type):
    """Book a specified number of tickets if seats are available."""
    if not check_seat_availability(showtime_id, num_tickets, seat_type):
        return "❌ Not enough seats available!"

    try:
        query = """
        SELECT id, price FROM seats 
        WHERE showtime_id = ? AND seat_type = ? AND is_booked = 0 
        LIMIT ?;
        """
        available_seats = execute_query(query, (showtime_id, seat_type, num_tickets), fetch_all=True)

        if not available_seats:
            return "❌ Seats could not be allocated!"

        booking_reference = generate_booking_reference()
        if not booking_reference:
            return "❌ Failed to generate booking reference."

        total_price = sum(seat[1] for seat in available_seats)

        for seat in available_seats:
            seat_id = seat[0]
            query = """
            INSERT INTO bookings (booking_staff_id, customer_name, customer_phone, customer_email, 
                                  showtime_id, seat_id, booking_reference, total_price, booking_date) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            params = (
                booking_staff_id, customer_name, customer_phone, customer_email, showtime_id, seat_id,
                booking_reference, total_price, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            execute_query(query, params, commit=True)
            execute_query("UPDATE seats SET is_booked = 1 WHERE id = ?", (seat_id,), commit=True)

        return f"✅ Booking Successful! Reference: {booking_reference}, Total Price: £{total_price}"

    except Exception as e:
        print(f"❌ Database Error in booking tickets: {e}")
        return "❌ Booking failed due to an internal error."


def cancel_booking(booking_reference):
    """Cancel a booking and apply refund rules."""
    try:
        query = """
        SELECT bookings.id, showtimes.show_time, bookings.total_price, bookings.seat_id 
        FROM bookings 
        JOIN showtimes ON bookings.showtime_id = showtimes.id
        WHERE booking_reference = ?;
        """
        booking = execute_query(query, (booking_reference,), fetch_one=True)

        if not booking:
            return "❌ Booking reference not found!"

        booking_id, show_time, total_price, seat_id = booking

        show_date = datetime.datetime.strptime(show_time, "%Y-%m-%d %H:%M:%S").date()
        today = datetime.date.today()

        if today >= show_date:
            return "❌ Cannot cancel on the day of the show. No refund!"

        if (show_date - today).days < 1:
            return "❌ You can only cancel at least 1 day before the showtime!"

        refund_amount = total_price * 0.5

        query = """
        INSERT INTO cancellations (booking_id, cancellation_date, refund_amount) 
        VALUES (?, ?, ?);
        """
        execute_query(query, (booking_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), refund_amount), commit=True)
        execute_query("UPDATE seats SET is_booked = 0 WHERE id = ?", (seat_id,), commit=True)

        return f"✅ Booking Canceled! Refund Amount: £{refund_amount}"

    except Exception as e:
        print(f"❌ Database Error in cancelling booking: {e}")
        return "❌ Cancellation failed due to an internal error."