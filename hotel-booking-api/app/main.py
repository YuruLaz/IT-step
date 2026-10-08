from fastapi import FastAPI

from app.routers import bookings, hotels, rooms, users

app = FastAPI(title="Hotel Booking API")

# Table creation and schema changes are handled by Alembic migrations now
# (see migrations/), not by the app itself. Run `alembic upgrade head` before
# starting the server.

app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hotel Booking API is running. See /docs for the Swagger UI."}
