from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    room_type_id: Mapped[int] = mapped_column(ForeignKey("room_types.id"), nullable=False)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price_per_night: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_guests: Mapped[int] = mapped_column(Integer, nullable=False)
    available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    hotel = relationship("Hotel", back_populates="rooms")
    room_type = relationship("RoomType")
    images = relationship("RoomImage", back_populates="room", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="room")
