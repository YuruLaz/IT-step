from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas import BookingIn, BookingOut

router = APIRouter(prefix="/api/Booking", tags=["Booking"])


def _row_to_booking(row) -> BookingOut:
    return BookingOut(
        id=row["id"],
        room_id=row["room_id"],
        check_in=row["check_in"],
        check_out=row["check_out"],
        total_price=row["total_price"],
        is_confirmed=row["is_confirmed"],
        customer_name=row["customer_name"],
        customer_phone=row["customer_phone"],
    )


@router.get("", response_model=list[BookingOut])
def get_bookings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = [_row_to_booking(row) for row in cursor.fetchall()]
    conn.close()
    return bookings


@router.post("", response_model=BookingOut)
def create_booking(booking: BookingIn):
    if booking.check_out <= booking.check_in:
        raise HTTPException(status_code=400, detail="check_out must be after check_in")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rooms WHERE id = %s", (booking.room_id,))
    room = cursor.fetchone()
    if room is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Room not found")

    cursor.execute("SELECT check_in, check_out FROM bookings WHERE room_id = %s", (booking.room_id,))
    for existing in cursor.fetchall():
        overlaps = existing["check_in"] < booking.check_out and existing["check_out"] > booking.check_in
        if overlaps:
            conn.close()
            raise HTTPException(status_code=409, detail="Room is already booked for these dates")

    nights = (booking.check_out - booking.check_in).days
    total_price = nights * room["price_per_night"]

    cursor.execute(
        """
        INSERT INTO bookings (room_id, check_in, check_out, total_price, is_confirmed, customer_name, customer_phone)
        VALUES (%s, %s, %s, %s, TRUE, %s, %s)
        RETURNING *
        """,
        (
            booking.room_id,
            booking.check_in,
            booking.check_out,
            total_price,
            booking.customer_name,
            booking.customer_phone,
        ),
    )
    new_row = cursor.fetchone()
    conn.commit()
    conn.close()
    return _row_to_booking(new_row)


@router.delete("/{booking_id}")
def cancel_booking(booking_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM bookings WHERE id = %s", (booking_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Booking not found")

    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    conn.commit()
    conn.close()
    return {"message": "Booking cancelled"}
