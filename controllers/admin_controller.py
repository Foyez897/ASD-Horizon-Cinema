from database.database_setup import get_db_connection
from datetime import datetime
import bcrypt


# Authentication

def authenticate_user(username, password, allowed_roles=("admin", "manager")):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        if user["role"] in allowed_roles:
            return user["id"], user["role"]
    return None, None


# Admin Dashboard Data

def get_admin_dashboard_data():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT films.id AS film_id, films.title, films.genre, films.age_rating,
                   showtimes.cinema_id, GROUP_CONCAT(DISTINCT showtimes.show_time) AS showtimes
            FROM films
            LEFT JOIN showtimes ON films.id = showtimes.film_id
            GROUP BY films.id, showtimes.cinema_id
        """)
        film_rows = cursor.fetchall()

        films = []
        film_cinemas = {}

        for row in film_rows:
            fid = row["film_id"]
            if not any(f["id"] == fid for f in films):
                films.append({
                    "id": fid,
                    "title": row["title"],
                    "genre": row["genre"],
                    "age_rating": row["age_rating"],
                    "showtimes": row["showtimes"] or "None"
                })
            if row["cinema_id"]:
                cursor.execute("SELECT id, city, location FROM cinemas WHERE id = ?", (row["cinema_id"],))
                cinema = cursor.fetchone()
                if cinema:
                    film_cinemas.setdefault(fid, []).append(cinema)

        seen_ids = set()
        cinema_dropdown = []
        for clist in film_cinemas.values():
            for cinema in clist:
                if cinema["id"] not in seen_ids:
                    seen_ids.add(cinema["id"])
                    cinema_dropdown.append(cinema)

        if not cinema_dropdown:
            cursor.execute("SELECT id, city, location FROM cinemas")
            cinema_dropdown = cursor.fetchall()

    return films, film_cinemas, cinema_dropdown


# Utility Fetchers

def get_cinemas():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, city, location FROM cinemas")
        return cursor.fetchall()

def get_film_info():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM films")
        return cursor.fetchall()

def get_screens_by_cinema(cinema_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT screen_number FROM screens WHERE cinema_id = ?", (cinema_id,))
        return [row["screen_number"] for row in cursor.fetchall()]


def get_all_cinemas():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, city, location FROM cinemas")
        return cursor.fetchall()


# Film Management

def add_new_film(title, genre, age_rating, description, cinema_id, showtimes, screens, price):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO films (title, genre, age_rating, description)
            VALUES (?, ?, ?, ?)
        """, (title, genre, age_rating, description))
        film_id = cursor.lastrowid

        for show_time, screen_number in zip(showtimes, screens):
            cursor.execute("""
                INSERT INTO showtimes (film_id, cinema_id, screen_number, show_time, price)
                VALUES (?, ?, ?, ?, ?)
            """, (film_id, cinema_id, int(screen_number), show_time, price))

        conn.commit()
        return True

def delete_film(film_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM films WHERE id = ?", (film_id,))
        cursor.execute("DELETE FROM showtimes WHERE film_id = ?", (film_id,))
        conn.commit()
    return True

def update_film(film_id, title, genre, age_rating):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE films
            SET title = ?, genre = ?, age_rating = ?
            WHERE id = ?
        """, (title, genre, age_rating, film_id))
        conn.commit()
    return True


# Showtime Grid View Logic

def get_manage_film_data(cinema_id, selected_date=None):
    selected_date = selected_date or datetime.now().strftime('%Y-%m-%d')

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM films")
        films = cursor.fetchall()

        cursor.execute("SELECT id, city, location FROM cinemas WHERE id = ?", (cinema_id,))
        cinema = cursor.fetchone()

        screens = get_screens_by_cinema(cinema_id)

        cursor.execute("""
            SELECT s.id AS showtime_id, s.screen_number, s.show_time, s.price,
                   f.title, f.id AS film_id
            FROM showtimes s
            JOIN films f ON f.id = s.film_id
            WHERE s.cinema_id = ? AND DATE(s.show_time) = ?
        """, (cinema_id, selected_date))

        showtime_map = {}
        for row in cursor.fetchall():
            key = (row["screen_number"], row["show_time"][11:16])
            showtime_map[key] = {
                "title": row["title"],
                "showtime_id": row["showtime_id"],
                "price": row["price"],
                "film_id": row["film_id"]
            }

    return films, cinema, screens, showtime_map


# Ajax Showtime Addition

def add_showtime_ajax(film_id, cinema_id, screen_number, date, time_slot, price=10.0):
    show_time = f"{date} {time_slot}:00"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM films WHERE id = ?", (film_id,))
        film = cursor.fetchone()

        if not film:
            return False, "Film not found"

        cursor.execute("""
            INSERT INTO showtimes (film_id, cinema_id, screen_number, show_time, price)
            VALUES (?, ?, ?, ?, ?)
        """, (film_id, cinema_id, screen_number, show_time, price))
        conn.commit()

    return True, film["title"]


def get_films_showing_today():
    today = datetime.now().strftime('%Y-%m-%d')
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
        fid = row['id']
        if fid not in film_map:
            film_map[fid] = {
                "id": fid,
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


def validate_admin_credentials(username, password):
    return authenticate_user(username, password, allowed_roles=("admin",))


def get_film_listings(cinema_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, genre, age_rating, description FROM films")
        rows = cursor.fetchall()

    films = []
    for row in rows:
        films.append({
            "id": row["id"],
            "title": row["title"],
            "genre": row["genre"],
            "age_rating": row["age_rating"],
            "description": row["description"]
        })

    return films


def delete_showtime(showtime_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM showtimes WHERE id = ?", (showtime_id,))
        conn.commit()
    return True


def get_showtime_id_by_screen_time(cinema_id, screen_number, time_slot, date):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
    SELECT s.id AS showtime_id, f.title AS film_title
    FROM showtimes s
    JOIN films f ON s.film_id = f.id
    WHERE s.cinema_id = ? AND s.screen_number = ? AND time(s.show_time) = time(?) AND date(s.show_time) = date(?)
""", (cinema_id, screen_number, time_slot, date))
        return cursor.fetchone()