from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.booking import Booking
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.room_image import RoomImage
from app.models.room_type import RoomType
from app.models.user import User
from app.schemas.room import RoomFilter, RoomIn, RoomOut, RoomTypeOut
from app.security import require_admin

router = APIRouter(prefix="/rooms", tags=["rooms"])


def _is_available_for_dates(db: Session, room_id: int, check_in: date, check_out: date) -> bool:
    bookings = db.query(Booking).filter(Booking.room_id == room_id).all()
    for booking in bookings:
        overlaps = booking.check_in < check_out and booking.check_out > check_in
        if overlaps:
            return False
    return True


@router.get("", response_model=list[RoomOut])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


@router.post("", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomIn, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if not db.get(Hotel, room.hotel_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")

    if not db.get(RoomType, room.room_type_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room type not found")

    new_room = Room(
        hotel_id=room.hotel_id,
        room_type_id=room.room_type_id,
        name=room.name,
        price_per_night=room.price_per_night,
        maximum_guests=room.maximum_guests,
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    for url in room.images:
        db.add(RoomImage(room_id=new_room.id, url=url))
    db.commit()
    db.refresh(new_room)

    return new_room


@router.get("/types", response_model=list[RoomTypeOut])
def get_room_types(db: Session = Depends(get_db)):
    return db.query(RoomType).all()


@router.get("/available", response_model=list[RoomOut])
def get_available_rooms(check_in: date, check_out: date, db: Session = Depends(get_db)):
    if check_out <= check_in:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="check_out must be after check_in")

    rooms = db.query(Room).filter(Room.available.is_(True)).all()
    return [room for room in rooms if _is_available_for_dates(db, room.id, check_in, check_out)]


@router.post("/filter", response_model=list[RoomOut])
def get_filtered_rooms(filters: RoomFilter, db: Session = Depends(get_db)):
    if (filters.check_in is None) != (filters.check_out is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="check_in and check_out must be provided together",
        )

    if filters.check_in and filters.check_out and filters.check_out <= filters.check_in:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="check_out must be after check_in")

    query = db.query(Room).filter(Room.available.is_(True))

    if filters.room_type_id is not None:
        query = query.filter(Room.room_type_id == filters.room_type_id)
    if filters.price_from is not None:
        query = query.filter(Room.price_per_night >= filters.price_from)
    if filters.price_to is not None:
        query = query.filter(Room.price_per_night <= filters.price_to)
    if filters.maximum_guests is not None:
        query = query.filter(Room.maximum_guests >= filters.maximum_guests)

    rooms = query.all()

    if filters.check_in and filters.check_out:
        rooms = [room for room in rooms if _is_available_for_dates(db, room.id, filters.check_in, filters.check_out)]

    return rooms


@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room


@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    has_bookings = db.query(Booking).filter(Booking.room_id == room_id).first() is not None
    if has_bookings:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cancel this room's bookings before deleting it",
        )

    db.delete(room)
    db.commit()
    return {"message": "Room deleted"}
