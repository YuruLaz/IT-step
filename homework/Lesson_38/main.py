from fastapi import FastAPI, HTTPException

app = FastAPI()


movies = [
    {
        "id": 1,
        "title": "The Matrix",
        "genre": "sci-fi",
        "year": 1999,
        "rating": 8.7
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "genre": "action",
        "year": 2008,
        "rating": 9.0
    },
    {
        "id": 3,
        "title": "The Hangover",
        "genre": "comedy",
        "year": 2009,
        "rating": 7.7
    },
    {
        "id": 4,
        "title": "Joker",
        "genre": "drama",
        "year": 2019,
        "rating": 8.4
    },
    {
        "id": 5,
        "title": "The Matrix Reloaded",
        "genre": "sci-fi",
        "year": 2003,
        "rating": 7.2
    },
    {
        "id": 6,
        "title": "Inception",
        "genre": "sci-fi",
        "year": 2010,
        "rating": 8.8
    },
    {
        "id": 7,
        "title": "Superbad",
        "genre": "comedy",
        "year": 2007,
        "rating": 7.6
    },
    {
        "id": 8,
        "title": "Interstellar",
        "genre": "sci-fi",
        "year": 2014,
        "rating": 8.7
    }
]


@app.get("/movies")
def get_movies(
    genre: str | None = None,
    year: int | None = None,
    min_rating: float | None = None,
    search: str | None = None
):
    filtered_movies = movies

    if genre is not None:
        filtered_movies = [
            movie
            for movie in filtered_movies
            if movie["genre"].lower() == genre.lower()
        ]

    if year is not None:
        filtered_movies = [
            movie
            for movie in filtered_movies
            if movie["year"] == year
        ]

    if min_rating is not None:
        filtered_movies = [
            movie
            for movie in filtered_movies
            if movie["rating"] >= min_rating
        ]

    if search is not None:
        filtered_movies = [
            movie
            for movie in filtered_movies
            if search.lower() in movie["title"].lower()
        ]

    return filtered_movies


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie

    raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )