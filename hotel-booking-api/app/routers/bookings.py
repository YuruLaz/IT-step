from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.booking import Booking
from app.models.room import Room
from app.models.user import User
from app.schemas.booking import BookingIn, BookingOut
from app.security import get_current_user

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", response_model=list[BookingOut])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: BookingIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if booking.check_out <= booking.check_in:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="check_out must be after check_in")

    room = db.get(Room, booking.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    existing_bookings = db.query(Booking).filter(Booking.room_id == booking.room_id).all()
    for existing in existing_bookings:
        overlaps = existing.check_in < booking.check_out and existing.check_out > booking.check_in
        if overlaps:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Room is already booked for these dates")

    nights = (booking.check_out - booking.check_in).days
    total_price = nights * room.price_per_night

    new_booking = Booking(
        room_id=booking.room_id,
        user_id=current_user.id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        total_price=total_price,
        customer_name=booking.customer_name,
        customer_phone=booking.customer_phone,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only cancel your own bookings")

    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled"}
