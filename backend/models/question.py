from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Text, func
from database.session import Base
from sqlalchemy.orm import relationship

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False) 
    difficulty = Column(String, default="medium") 
    status = Column(String, default="pending") 
    
    # Foreign Keys
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    contributor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    course = relationship("Course", back_populates="questions")
    contributor = relationship("User", back_populates="contributions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False) 
    is_correct = Column(Boolean, default=False)
    explanation = Column(Text, nullable=True) 
    
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    # Relationships
    question = relationship("Question", back_populates="options")