from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

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
    return {"message": "Hotel Booking API is running. See /docs for Swagger, /scalar for the Scalar UI."}


@app.get("/scalar", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
