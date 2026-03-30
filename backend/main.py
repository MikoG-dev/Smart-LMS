from fastapi import FastAPI
from database.session import engine, Base
from models import *
from routers import auth


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quiz Bank API")

app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Database connected and all tables created!"}