from fastapi import FastAPI

from app.database import SessionLocal
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.room_image import RoomImage
from app.models.room_type import RoomType
from app.routers import bookings, hotels, rooms, users

app = FastAPI(title="Hotel Booking API")

# Table creation and schema changes are handled by Alembic migrations now
# (see migrations/), not by the app itself. Run `alembic upgrade head` before
# starting the server.

ROOM_TYPE_NAMES = ["Single Room", "Double Room", "Deluxe Room"]

HOTELS = [
    ("Tbilisi Grand Hotel", "12 Rustaveli Ave", "Tbilisi", "https://picsum.photos/seed/tbilisi-grand/800/600"),
    ("Batumi Sea View", "5 Sherif Khimshiashvili St", "Batumi", "https://picsum.photos/seed/batumi-sea/800/600"),
    ("Kutaisi Plaza", "20 Tsereteli St", "Kutaisi", "https://picsum.photos/seed/kutaisi-plaza/800/600"),
]

# (hotel index, room_type index, name, price_per_night, maximum_guests)
ROOMS = [
    (0, 0, "Standard Single", 80, 1),
    (0, 1, "Standard Double", 120, 2),
    (0, 2, "Executive Deluxe", 220, 3),
    (0, 1, "City View Double", 150, 2),
    (1, 0, "Sea View Single", 95, 1),
    (1, 1, "Sea View Double", 160, 2),
    (1, 2, "Penthouse Deluxe", 320, 4),
    (2, 0, "Economy Single", 60, 1),
    (2, 1, "Family Double", 110, 3),
    (2, 2, "Royal Deluxe", 200, 4),
]


def seed_if_empty() -> None:
    db = SessionLocal()
    try:
        if db.query(Hotel).first() is not None:
            return

        room_types = [RoomType(name=name) for name in ROOM_TYPE_NAMES]
        db.add_all(room_types)
        db.flush()

        hotels = [
            Hotel(name=name, address=address, city=city, featured_image=image)
            for name, address, city, image in HOTELS
        ]
        db.add_all(hotels)
        db.flush()

        for hotel_index, room_type_index, name, price, max_guests in ROOMS:
            room = Room(
                hotel_id=hotels[hotel_index].id,
                room_type_id=room_types[room_type_index].id,
                name=name,
                price_per_night=price,
                maximum_guests=max_guests,
            )
            db.add(room)
            db.flush()

            for photo_number in (1, 2):
                db.add(RoomImage(room_id=room.id, url=f"https://picsum.photos/seed/room{room.id}-{photo_number}/800/600"))

        db.commit()
    finally:
        db.close()


seed_if_empty()

app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hotel Booking API is running. See /docs for the Swagger UI."}
