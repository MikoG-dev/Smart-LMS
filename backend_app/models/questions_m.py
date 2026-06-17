from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database.database import Base


# ----- database tables -------

class QuestionDB (Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    course_title = Column(String)
    year_level = Column(Integer)
    question = Column(String)
    status = Column(String, default="pending")

    contributor_id = Column(Integer, ForeignKey("users.id"))
    course_code = Column(Integer, ForeignKey("courses.id"))

    choices = relationship("ChoiceDB", back_populates="question")
    courses = relationship("Courses", back_populates="questions")

class ChoiceDB(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String)
    is_answer = Column(Boolean, default=False)

    question_id = Column(Integer, ForeignKey("questions.id"))

    question = relationship("QuestionDB", back_populates="choices")

