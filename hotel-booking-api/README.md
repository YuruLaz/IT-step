# Hotel Booking API

A backend for the "Hotel Booking" final project — built from scratch with FastAPI, not just
a frontend talking to IT-Step's existing API. It covers the same hotels / rooms / bookings
domain as `https://hotelbooking.stepprojects.ge/swagger/index.html`, with equivalent endpoints,
and Swagger docs generated automatically by FastAPI at `/docs` — no separate documentation work
needed.

## Folder structure

```
hotel-booking-api/
  app/
    main.py            # creates the FastAPI app, wires up the three routers
    database.py         # PostgreSQL connection, table schema, seed data
    schemas.py           # Pydantic models — the shape of every request/response
    routers/
      hotels.py           # /api/Hotels/...
      rooms.py              # /api/Rooms/...
      bookings.py            # /api/Booking/...
  requirements.txt
  .gitignore
```

Each router file only talks to the database directly with plain SQL (via `psycopg2`) — no ORM,
no sessions to manage, so every query is visible exactly where it's used.

## Database

Uses a real PostgreSQL database named `hotel_booking`, connected to via peer authentication as
your local Linux user (`lazosh`) — the same way `psql -U lazosh -l` already works on this
machine, so no password or connection string to configure.

You can browse it with pgAdmin (already installed) or `psql`:

```bash
psql -U "$USER" -d hotel_booking -c "\dt"              # list tables
psql -U "$USER" -d hotel_booking -c "SELECT * FROM bookings;"
```

## Running it

The repo's existing `venv` (at `../venv`) already has `fastapi`, `uvicorn`, and `psycopg2-binary`
installed, so no install step is needed — just make sure the PostgreSQL service is running
(`systemctl status postgresql`, it starts automatically on boot on this machine):

```bash
cd hotel-booking-api
source ../venv/bin/activate
uvicorn app.main:app --reload
```

`requirements.txt` is only needed if you set up a fresh environment that doesn't have these
packages yet (e.g. a grader cloning just this folder):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

First run creates the `hotel_booking` database (if it doesn't already exist), creates the 5
tables, and seeds them with 3 hotels (Tbilisi, Batumi, Kutaisi), 10 rooms across the 3 room
types, and 2 sample bookings. Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI,
or `http://127.0.0.1:8000/` for a health-check message.

To start over with a clean database:
```bash
psql -U "$USER" -d postgres -c "DROP DATABASE hotel_booking;"
```
It gets recreated and reseeded automatically the next time the server starts.

## Endpoints

| Method | Path | What it does |
|---|---|---|
| POST | `/api/Hotels` | Create a hotel |
| GET | `/api/Hotels/GetAll` | All hotels (no nested rooms) |
| GET | `/api/Hotels/GetHotels?city=` | Hotels, optionally filtered by city |
| GET | `/api/Hotels/GetCities` | Distinct list of cities that have hotels |
| GET | `/api/Hotels/GetHotel/{id}` | One hotel with its rooms (and each room's images) nested in |
| DELETE | `/api/Hotels/{id}` | Delete a hotel — `409` if it still has rooms |
| POST | `/api/Rooms` | Create a room under a hotel — `404` if the hotel or room type doesn't exist |
| GET | `/api/Rooms/GetAll` | Every room, across every hotel |
| GET | `/api/Rooms/GetRoom/{id}` | One room |
| GET | `/api/Rooms/GetRoomTypes` | The 3 fixed room types (Single/Double/Deluxe) |
| GET | `/api/Rooms/GetAvailableRooms?check_in=&check_out=` | Rooms with no booking overlapping that date range |
| POST | `/api/Rooms/GetFiltered` | Rooms matching any combination of type, price range, guest count, and dates |
| DELETE | `/api/Rooms/{id}` | Delete a room — `409` if it still has bookings |
| GET | `/api/Booking` | Every booking in the system |
| POST | `/api/Booking` | Create a booking — server computes `total_price` and rejects overlapping dates |
| DELETE | `/api/Booking/{id}` | Cancel (delete) a booking |

Deleting is deliberately **restrictive, not cascading**: a hotel with rooms can't be deleted until
those rooms are gone, and a room with bookings can't be deleted until those bookings are
cancelled. The alternative — silently deleting a hotel's rooms and their bookings along with it —
is the kind of thing that looks convenient until it accidentally wipes data you didn't mean to
touch. Work bottom-up: cancel bookings → delete rooms → delete the hotel.

## How availability is checked

Two dates overlap if `existing.check_in < requested.check_out AND existing.check_out >
requested.check_in`. That one comparison (in `_is_available_for_dates` in both `rooms.py` and
`bookings.py`) is reused everywhere a date range matters — browsing available rooms, filtering,
and double-booking prevention when a booking is created.

## Where this deliberately differs from the real stepprojects.ge API

Built to be easy to read first, byte-for-byte compatible second:

- **Field names are `snake_case`** (`price_per_night`, `check_in`, ...) instead of the real
  API's C#-style `camelCase`/`PascalCase` — standard Python/FastAPI convention, and one less
  thing (field aliases) to explain if asked about the code.
- **`GetAll`/`GetHotels` never include rooms.** The real API returns `"rooms": []` on those —
  empty, always — which is really just "we didn't load that," not useful data. Here, only
  `GetHotel/{id}` returns nested rooms, which is the only place the brief actually needs them.
- **Room images are a plain list of URL strings**, not `{id, source, roomId}` objects — the id
  and roomId on each image were never used for anything once you already have the room.
- **`total_price` is computed server-side** (`nights × price_per_night`) instead of trusted from
  the client. The real API accepts whatever number the client sends, which is how its public
  test data ended up with negative and zero totals.
- **Booking creation rejects overlapping dates with `409 Conflict`.** The real API doesn't
  enforce this at all (same room can be double-booked). This one check is the main "backend
  logic" piece of the whole project, so it's worth having it actually work.
- **No `customerId` field on bookings** — in the real API it's an unused string every test
  request just filled with `"string"`. Dropped as dead weight; only `customer_name` and
  `customer_phone` remain, matching what the brief actually asks for.

## What I verified before handing this off

Ran the server against a real PostgreSQL database and hit every endpoint for real (not just read
the code): confirmed the `hotel_booking` database and all 5 tables actually exist via `psql`;
hotel list/detail/city filter/404 on a missing id; all 10 seeded rooms returned; `GetAvailableRooms`
correctly excludes a room with an overlapping existing booking and rejects a reversed date range
with 400; `GetFiltered` combining room type + max price; creating a booking computes the right
total, a second overlapping booking on the same room gets rejected with 409, a reversed date
range gets 400, booking a nonexistent room gets 404; cancelling a real booking succeeds and
cancelling a nonexistent one 404s — then re-queried the `bookings` table directly with `psql` to
confirm the cancelled row was actually gone and the new one actually there. Also confirmed the
Swagger UI at `/docs` renders with all three resource groups.
