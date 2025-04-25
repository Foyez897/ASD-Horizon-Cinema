from database.database_setup import get_db_connection
from datetime import datetime

def get_films_showing_today():
    """
    Fetch films with showtimes scheduled for today.
    Returns a list of dictionaries containing film and showtime info.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    result = []

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.id, f.title, f.genre, f.age_rating, f.description,
                   s.show_time, c.city
            FROM films f
            JOIN showtimes s ON f.id = s.film_id
            JOIN cinemas c ON s.cinema_id = c.id
            WHERE DATE(s.show_time) = ?
            ORDER BY s.show_time
        """, (today,))
        rows = cursor.fetchall()

    film_map = {}

    for row in rows:
        fid = row["id"]
        if fid not in film_map:
            film_map[fid] = {
                "title": row["title"],
                "genre": row["genre"],
                "age_rating": row["age_rating"],
                "description": row["description"],
                "showtimes": []
            }
        film_map[fid]["showtimes"].append({
            "time": row["show_time"][11:16],
            "cinema": row["city"]
        })

    return list(film_map.values())