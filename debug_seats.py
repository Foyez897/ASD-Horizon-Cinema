import os
from utils.db_connection import execute_query

db_path = os.path.abspath("horizon_cinemas.db")
print(f"📂 Checking Database File: {db_path}")

def check_seat_availability(showtime_id, seat_type):
    query = """
    SELECT COUNT(*) FROM seats 
    WHERE showtime_id = ? AND seat_type = ? AND is_booked = 0;
    """
    result = execute_query(query, (showtime_id, seat_type), fetch_one=True)  

    # Ensure we correctly extract the integer value
    return result[0] if isinstance(result, tuple) else result

# Test for showtime_id = 1, seat_type = 'lower_hall'
available_seats = check_seat_availability(1, "lower_hall")
print(f"🔍 Available Seats: {available_seats}")