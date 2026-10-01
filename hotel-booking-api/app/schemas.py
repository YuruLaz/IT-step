from datetime import date

from pydantic import BaseModel, Field


class RoomType(BaseModel):
    id: int
    name: str


class HotelSummary(BaseModel):
    id: int
    name: str
    address: str
    city: str
    featured_image: str


class RoomOut(BaseModel):
    id: int
    hotel_id: int
    room_type_id: int
    name: str
    price_per_night: int
    maximum_guests: int
    available: bool
    images: list[str]


class HotelDetail(HotelSummary):
    rooms: list[RoomOut]


class HotelIn(BaseModel):
    name: str = Field(..., min_length=2)
    address: str = Field(..., min_length=2)
    city: str = Field(..., min_length=2)
    featured_image: str = Field(..., min_length=2)


class RoomIn(BaseModel):
    hotel_id: int
    room_type_id: int
    name: str = Field(..., min_length=2)
    price_per_night: int = Field(..., gt=0)
    maximum_guests: int = Field(..., gt=0)
    images: list[str] = []


class RoomFilter(BaseModel):
    room_type_id: int | None = None
    price_from: int | None = None
    price_to: int | None = None
    maximum_guests: int | None = None
    check_in: date | None = None
    check_out: date | None = None


class BookingIn(BaseModel):
    room_id: int
    check_in: date
    check_out: date
    customer_name: str = Field(..., min_length=2)
    customer_phone: str = Field(..., min_length=5)


class BookingOut(BaseModel):
    id: int
    room_id: int
    check_in: date
    check_out: date
    total_price: int
    is_confirmed: bool
    customer_name: str
    customer_phone: str
