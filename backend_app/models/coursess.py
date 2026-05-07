from sqlalchemy import Column, Integer, String
from backend_app.database.database import Base
from sqlalchemy.orm import relationship


class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    year_level = Column(Integer)

    questions = relationship("QuestionDB", back_populates=("courses"))

