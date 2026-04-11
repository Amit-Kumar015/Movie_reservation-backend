from fastapi import FastAPI
from app.db.database import engine, Base
import app.db.base
from app.api.routes import auth, movie, reservation, seats, showtime
from app.api.routes.admin import genre_admin, movie_admin, screen_admin, seat_admin, showtime_admin, venue_admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/hello")
def root():
    return {"message": "Welcome to the Movie Ticket Booking System"}
  
app.include_router(auth.router)
app.include_router(movie.router)
app.include_router(reservation.router)
app.include_router(seats.router)
app.include_router(showtime.router)
app.include_router(genre_admin.router)
app.include_router(movie_admin.router)
app.include_router(screen_admin.router)
app.include_router(seat_admin.router)
app.include_router(showtime_admin.router)
app.include_router(venue_admin.router)