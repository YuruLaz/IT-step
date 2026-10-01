from fastapi import FastAPI

from app.database import init_db
from app.routers import bookings, hotels, rooms

app = FastAPI(title="Hotel Booking API")

init_db()

app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(bookings.router)


@app.get("/")
def root():
    return {"message": "Hotel Booking API is running. See /docs for the Swagger UI."}
