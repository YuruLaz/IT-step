from pydantic import BaseModel, Field

from app.schemas.room import RoomOut


class HotelSummary(BaseModel):
    id: int
    name: str
    address: str
    city: str
    featured_image: str

    class Config:
        from_attributes = True


class HotelDetail(HotelSummary):
    rooms: list[RoomOut]


class HotelIn(BaseModel):
    name: str = Field(..., min_length=2)
    address: str = Field(..., min_length=2)
    city: str = Field(..., min_length=2)
    featured_image: str = Field(..., min_length=2)
