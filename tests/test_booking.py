import re
import sys
import os

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.booking_controller import book_tickets, cancel_booking

FUTURE_SHOWTIME_ID = 6  # Ensure this is a valid future showtime ID in your database
FUTURE_CINEMA_ID = 1  # Change this to a valid cinema ID
NUM_TICKETS = 1  # Specify the number of tickets you want to book

# 🔹 Test Booking (Booking Staff ID: 3, Customer: "John Doe", Showtime: FUTURE_SHOWTIME_ID, NUM_TICKETS Tickets, Lower Hall)
print("\n🔷 Attempting to book tickets...")
result = book_tickets(3, "John Doe", "07440316630", "johndoe@example.com", FUTURE_SHOWTIME_ID, NUM_TICKETS, "lower_hall")
print(result)

match = re.search(r"Reference: (\w+)", result)
if match:
    booking_reference = match.group(1)
    print(f"🔹 Use this reference for cancellation: {booking_reference}")

    print("\n🔷 Attempting to cancel booking...")
    cancel_result = cancel_booking(booking_reference)
    print(cancel_result)
else:
    print("❌ Booking failed, skipping cancellation test.")