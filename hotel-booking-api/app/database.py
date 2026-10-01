import psycopg2
import psycopg2.extras

DB_NAME = "hotel_booking"

SCHEMA = """
CREATE TABLE IF NOT EXISTS hotels (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    featured_image TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS room_types (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    room_type_id INTEGER NOT NULL REFERENCES room_types(id),
    name TEXT NOT NULL,
    price_per_night INTEGER NOT NULL,
    maximum_guests INTEGER NOT NULL,
    available BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS room_images (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES rooms(id),
    url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES rooms(id),
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    total_price INTEGER NOT NULL,
    is_confirmed BOOLEAN NOT NULL DEFAULT TRUE,
    customer_name TEXT NOT NULL,
    customer_phone TEXT NOT NULL
);
"""

ROOM_TYPES = ["Single Room", "Double Room", "Deluxe Room"]

HOTELS = [
    ("Tbilisi Grand Hotel", "12 Rustaveli Ave", "Tbilisi", "https://picsum.photos/seed/tbilisi-grand/800/600"),
    ("Batumi Sea View", "5 Sherif Khimshiashvili St", "Batumi", "https://picsum.photos/seed/batumi-sea/800/600"),
    ("Kutaisi Plaza", "20 Tsereteli St", "Kutaisi", "https://picsum.photos/seed/kutaisi-plaza/800/600"),
]

# (hotel index, room_type_id, name, price_per_night, maximum_guests)
ROOMS = [
    (0, 1, "Standard Single", 80, 1),
    (0, 2, "Standard Double", 120, 2),
    (0, 3, "Executive Deluxe", 220, 3),
    (0, 2, "City View Double", 150, 2),
    (1, 1, "Sea View Single", 95, 1),
    (1, 2, "Sea View Double", 160, 2),
    (1, 3, "Penthouse Deluxe", 320, 4),
    (2, 1, "Economy Single", 60, 1),
    (2, 2, "Family Double", 110, 3),
    (2, 3, "Royal Deluxe", 200, 4),
]


def get_connection():
    conn = psycopg2.connect(dbname=DB_NAME)
    conn.cursor_factory = psycopg2.extras.RealDictCursor
    return conn


def _create_database_if_missing() -> None:
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    if cursor.fetchone() is None:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
    conn.close()


def init_db() -> None:
    _create_database_if_missing()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SCHEMA)
    conn.commit()
    _seed_if_empty(conn)
    conn.close()


def _seed_if_empty(conn) -> None:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM hotels")
    if cursor.fetchone()["count"] > 0:
        return

    for name in ROOM_TYPES:
        cursor.execute("INSERT INTO room_types (name) VALUES (%s)", (name,))

    hotel_ids = []
    for name, address, city, image in HOTELS:
        cursor.execute(
            "INSERT INTO hotels (name, address, city, featured_image) VALUES (%s, %s, %s, %s) RETURNING id",
            (name, address, city, image),
        )
        hotel_ids.append(cursor.fetchone()["id"])

    for hotel_index, room_type_id, name, price, max_guests in ROOMS:
        cursor.execute(
            """
            INSERT INTO rooms (hotel_id, room_type_id, name, price_per_night, maximum_guests, available)
            VALUES (%s, %s, %s, %s, %s, TRUE)
            RETURNING id
            """,
            (hotel_ids[hotel_index], room_type_id, name, price, max_guests),
        )
        room_id = cursor.fetchone()["id"]
        for photo_number in (1, 2):
            cursor.execute(
                "INSERT INTO room_images (room_id, url) VALUES (%s, %s)",
                (room_id, f"https://picsum.photos/seed/room{room_id}-{photo_number}/800/600"),
            )

    cursor.execute(
        """
        INSERT INTO bookings (room_id, check_in, check_out, total_price, is_confirmed, customer_name, customer_phone)
        VALUES (2, '2026-10-10', '2026-10-14', 480, TRUE, 'Nina Beridze', '+995555112233')
        """
    )
    cursor.execute(
        """
        INSERT INTO bookings (room_id, check_in, check_out, total_price, is_confirmed, customer_name, customer_phone)
        VALUES (6, '2026-11-01', '2026-11-03', 320, TRUE, 'Giorgi Kapanadze', '+995555998877')
        """
    )

    conn.commit()
