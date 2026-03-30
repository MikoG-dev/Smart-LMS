from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Text, func
from database.session import Base
from sqlalchemy.orm import relationship


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("User", back_populates="practice_sessions")
    course = relationship("Course")