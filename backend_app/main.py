from fastapi import FastAPI
from backend_app.database.database import Base, engine
from backend_app.routes import questions, admin, admins, users
from backend_app.models.coursess import Courses
from backend_app.database.database import SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(questions.router)
app.include_router(admins.router)
app.include_router(admin.router)
app.include_router(users.router)

db = SessionLocal()
courses = [
    Courses(title="Mathematics", year_level=9),
    Courses(title="Physics", year_level=9),
    Courses(title="Chemistry", year_level=9),
    Courses(title="Biology", year_level=9),
    Courses(title="Mathematics", year_level=10),
    Courses(title="Physics", year_level=10),
    Courses(title="Chemistry", year_level=10),
    Courses(title="Biology", year_level=10),
    Courses(title="Mathematics", year_level=11),
    Courses(title="Physics", year_level=11),
    Courses(title="Chemistry", year_level=11),
    Courses(title="Biology", year_level=11),
    Courses(title="Chemistry", year_level=11),
    Courses(title="Mathematics", year_level=12),
    Courses(title="Physics", year_level=12),
    Courses(title="Chemistry", year_level=12),
    Courses(title="Biology", year_level=12),
]

db.add_all(courses)
db.commit()