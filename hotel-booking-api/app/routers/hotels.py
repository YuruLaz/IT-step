from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.hotel import Hotel
from app.models.room import Room
from app.schemas.hotel import HotelDetail, HotelIn, HotelSummary

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("", response_model=list[HotelSummary])
def get_hotels(city: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Hotel)
    if city:
        query = query.filter(Hotel.city == city)
    return query.all()


@router.post("", response_model=HotelSummary, status_code=status.HTTP_201_CREATED)
def create_hotel(hotel: HotelIn, db: Session = Depends(get_db)):
    new_hotel = Hotel(
        name=hotel.name,
        address=hotel.address,
        city=hotel.city,
        featured_image=hotel.featured_image,
    )
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel


@router.get("/cities", response_model=list[str])
def get_cities(db: Session = Depends(get_db)):
    rows = db.query(Hotel.city).distinct().order_by(Hotel.city).all()
    return [row[0] for row in rows]


@router.get("/{hotel_id}", response_model=HotelDetail)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.get(Hotel, hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return hotel


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.get(Hotel, hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")

    has_rooms = db.query(Room).filter(Room.hotel_id == hotel_id).first() is not None
    if has_rooms:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Delete this hotel's rooms before deleting the hotel",
        )

    db.delete(hotel)
    db.commit()
    return {"message": "Hotel deleted"}
