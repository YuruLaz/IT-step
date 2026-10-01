from datetime import date

from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas import RoomFilter, RoomIn, RoomOut, RoomType

router = APIRouter(prefix="/api/Rooms", tags=["Rooms"])


def _room_images(cursor, room_id: int) -> list[str]:
    cursor.execute("SELECT url FROM room_images WHERE room_id = %s", (room_id,))
    return [row["url"] for row in cursor.fetchall()]


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


def _is_available_for_dates(cursor, room_id: int, check_in: date, check_out: date) -> bool:
    cursor.execute("SELECT check_in, check_out FROM bookings WHERE room_id = %s", (room_id,))

    for booking in cursor.fetchall():
        overlaps = booking["check_in"] < check_out and booking["check_out"] > check_in
        if overlaps:
            return False

    return True


@router.post("", response_model=RoomOut)
def create_room(room: RoomIn):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM hotels WHERE id = %s", (room.hotel_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Hotel not found")

    cursor.execute("SELECT id FROM room_types WHERE id = %s", (room.room_type_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Room type not found")

    cursor.execute(
        """
        INSERT INTO rooms (hotel_id, room_type_id, name, price_per_night, maximum_guests, available)
        VALUES (%s, %s, %s, %s, %s, TRUE)
        RETURNING *
        """,
        (room.hotel_id, room.room_type_id, room.name, room.price_per_night, room.maximum_guests),
    )
    new_row = cursor.fetchone()

    for url in room.images:
        cursor.execute("INSERT INTO room_images (room_id, url) VALUES (%s, %s)", (new_row["id"], url))

    conn.commit()
    created_room = _row_to_room(cursor, new_row)
    conn.close()
    return created_room


@router.delete("/{room_id}")
def delete_room(room_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM rooms WHERE id = %s", (room_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Room not found")

    cursor.execute("SELECT COUNT(*) AS count FROM bookings WHERE room_id = %s", (room_id,))
    if cursor.fetchone()["count"] > 0:
        conn.close()
        raise HTTPException(status_code=409, detail="Cancel this room's bookings before deleting it")

    cursor.execute("DELETE FROM room_images WHERE room_id = %s", (room_id,))
    cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
    conn.commit()
    conn.close()
    return {"message": "Room deleted"}


@router.get("/GetAll", response_model=list[RoomOut])
def get_all_rooms():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rooms = [_row_to_room(cursor, row) for row in cursor.fetchall()]
    conn.close()
    return rooms


@router.get("/GetRoom/{room_id}", response_model=RoomOut)
def get_room(room_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Room not found")

    room = _row_to_room(cursor, row)
    conn.close()
    return room


@router.get("/GetRoomTypes", response_model=list[RoomType])
def get_room_types():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM room_types")
    room_types = [RoomType(id=row["id"], name=row["name"]) for row in cursor.fetchall()]
    conn.close()
    return room_types


@router.get("/GetAvailableRooms", response_model=list[RoomOut])
def get_available_rooms(check_in: date, check_out: date):
    if check_out <= check_in:
        raise HTTPException(status_code=400, detail="check_out must be after check_in")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms WHERE available = TRUE")
    rows = cursor.fetchall()

    available_rooms = [
        _row_to_room(cursor, row)
        for row in rows
        if _is_available_for_dates(cursor, row["id"], check_in, check_out)
    ]
    conn.close()
    return available_rooms


@router.post("/GetFiltered", response_model=list[RoomOut])
def get_filtered_rooms(filters: RoomFilter):
    if (filters.check_in is None) != (filters.check_out is None):
        raise HTTPException(status_code=400, detail="check_in and check_out must be provided together")

    if filters.check_in and filters.check_out and filters.check_out <= filters.check_in:
        raise HTTPException(status_code=400, detail="check_out must be after check_in")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms WHERE available = TRUE")
    filtered = cursor.fetchall()

    if filters.room_type_id is not None:
        filtered = [row for row in filtered if row["room_type_id"] == filters.room_type_id]

    if filters.price_from is not None:
        filtered = [row for row in filtered if row["price_per_night"] >= filters.price_from]

    if filters.price_to is not None:
        filtered = [row for row in filtered if row["price_per_night"] <= filters.price_to]

    if filters.maximum_guests is not None:
        filtered = [row for row in filtered if row["maximum_guests"] >= filters.maximum_guests]

    if filters.check_in and filters.check_out:
        filtered = [
            row
            for row in filtered
            if _is_available_for_dates(cursor, row["id"], filters.check_in, filters.check_out)
        ]

    rooms = [_row_to_room(cursor, row) for row in filtered]
    conn.close()
    return rooms
