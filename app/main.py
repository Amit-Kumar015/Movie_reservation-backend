from fastapi import FastAPI
from app.db.database import engine, Base
from app.api.routes import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/hello")
def root():
    return {"message": "Welcome to the Movie Ticket Booking System"}
  
app.include_router(auth.router)