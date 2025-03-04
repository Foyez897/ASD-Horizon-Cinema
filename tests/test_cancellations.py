import re
import sys
import os
from datetime import datetime, timedelta

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.booking_controller import cancel_booking
from utils.db_connection import execute_query

# 🔹 Helper function to check if booking reference exists
def booking_exists(booking_reference):
    query = "SELECT COUNT(*) FROM bookings WHERE booking_reference = ?"
    result = execute_query(query, (booking_reference,), fetch_one=True)
    return result[0] > 0

# 🔹 Test Cancellation Logic
def test_cancellation():
    print("\n🔷 Testing Booking Cancellation...")

    # 🔹 Manually enter the booking reference
    booking_reference = input("Enter the booking reference number to cancel: ").strip()

    # 🔹 Ensure the booking reference exists in the database
    if not booking_exists(booking_reference):
        print("❌ Booking reference not found in the database.")
        return

    print(f"🔹 Using Booking Reference: {booking_reference}")

    # 🔹 Check the booking date
    query = """
    SELECT showtimes.show_time 
    FROM bookings
    JOIN showtimes ON bookings.showtime_id = showtimes.id
    WHERE booking_reference = ?;
    """
    booking_time = execute_query(query, (booking_reference,), fetch_one=True)[0]

    # Convert the showtime string to a datetime object
    show_time = datetime.strptime(booking_time, "%Y-%m-%d %H:%M:%S")

    # If the showtime is less than a day away, cancellation shouldn't be allowed
    if (show_time - datetime.now()).days < 1:
        print("❌ Cannot cancel on the day of the show. No refund!")
        return

    # 🔹 Attempt to cancel booking
    cancel_result = cancel_booking(booking_reference)
    print(cancel_result)

# Run the cancellation test
if __name__ == "__main__":
    test_cancellation()