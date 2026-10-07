from datetime import date

from pydantic import BaseModel, Field, field_validator


class RoomTypeOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RoomOut(BaseModel):
    id: int
    hotel_id: int
    room_type_id: int
    name: str
    price_per_night: int
    maximum_guests: int
    available: bool
    images: list[str] = []

    @field_validator("images", mode="before")
    @classmethod
    def extract_image_urls(cls, value):
        return [item.url if hasattr(item, "url") else item for item in value]

    class Config:
        from_attributes = True


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
