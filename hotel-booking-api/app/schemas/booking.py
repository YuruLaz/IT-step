from datetime import date

from pydantic import BaseModel, Field


class BookingIn(BaseModel):
    room_id: int
    check_in: date
    check_out: date
    customer_name: str = Field(..., min_length=2)
    customer_phone: str = Field(..., min_length=5)


class BookingOut(BaseModel):
    id: int
    room_id: int
    user_id: int
    check_in: date
    check_out: date
    total_price: int
    is_confirmed: bool
    customer_name: str
    customer_phone: str

    class Config:
        from_attributes = True
