from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas import HotelDetail, HotelIn, HotelSummary, RoomOut

router = APIRouter(prefix="/api/Hotels", tags=["Hotels"])


def _room_images(cursor, room_id: int) -> list[str]:
    cursor.execute("SELECT url FROM room_images WHERE room_id = %s", (room_id,))
    return [row["url"] for row in cursor.fetchall()]


def _row_to_hotel_summary(row) -> HotelSummary:
    return HotelSummary(
        id=row["id"],
        name=row["name"],
        address=row["address"],
        city=row["city"],
        featured_image=row["featured_image"],
    )


def _row_to_room(cursor, row) -> RoomOut:
    return RoomOut(
        id=row["id"],
        hotel_id=row["hotel_id"],
        room_type_id=row["room_type_id"],
        name=row["name"],
        price_per_night=row["price_per_night"],
        maximum_guests=row["maximum_guests"],
        available=row["available"],
        images=_room_images(cursor, row["id"]),
    )


@router.post("", response_model=HotelSummary)
def create_hotel(hotel: HotelIn):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO hotels (name, address, city, featured_image) VALUES (%s, %s, %s, %s) RETURNING *",
        (hotel.name, hotel.address, hotel.city, hotel.featured_image),
    )
    new_row = cursor.fetchone()
    conn.commit()
    conn.close()
    return _row_to_hotel_summary(new_row)


@router.get("/GetAll", response_model=list[HotelSummary])
def get_all_hotels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hotels")
    hotels = [_row_to_hotel_summary(row) for row in cursor.fetchall()]
    conn.close()
    return hotels


@router.get("/GetHotels", response_model=list[HotelSummary])
def get_hotels(city: str | None = None):
    conn = get_connection()
    cursor = conn.cursor()
    if city:
        cursor.execute("SELECT * FROM hotels WHERE city = %s", (city,))
    else:
        cursor.execute("SELECT * FROM hotels")
    hotels = [_row_to_hotel_summary(row) for row in cursor.fetchall()]
    conn.close()
    return hotels


@router.get("/GetCities", response_model=list[str])
def get_cities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT city FROM hotels ORDER BY city")
    cities = [row["city"] for row in cursor.fetchall()]
    conn.close()
    return cities


@router.get("/GetHotel/{hotel_id}", response_model=HotelDetail)
def get_hotel(hotel_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hotels WHERE id = %s", (hotel_id,))
    hotel_row = cursor.fetchone()
    if hotel_row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Hotel not found")

    cursor.execute("SELECT * FROM rooms WHERE hotel_id = %s", (hotel_id,))
    rooms = [_row_to_room(cursor, row) for row in cursor.fetchall()]
    conn.close()

    return HotelDetail(**_row_to_hotel_summary(hotel_row).model_dump(), rooms=rooms)


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM hotels WHERE id = %s", (hotel_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Hotel not found")

    cursor.execute("SELECT COUNT(*) AS count FROM rooms WHERE hotel_id = %s", (hotel_id,))
    if cursor.fetchone()["count"] > 0:
        conn.close()
        raise HTTPException(status_code=409, detail="Delete this hotel's rooms before deleting the hotel")

    cursor.execute("DELETE FROM hotels WHERE id = %s", (hotel_id,))
    conn.commit()
    conn.close()
    return {"message": "Hotel deleted"}
