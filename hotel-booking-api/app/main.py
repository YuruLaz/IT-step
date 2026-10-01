from fastapi import FastAPI

from app.database import init_db
from app.endpoints import booking_routes, hotel_routes, room_routes

app = FastAPI(title="Hotel Booking API")

init_db()

app.include_router(hotel_routes.router)
app.include_router(room_routes.router)
app.include_router(booking_routes.router)


@app.get("/")
def root():
    return {"message": "Hotel Booking API is running. See /docs for the Swagger UI."}
