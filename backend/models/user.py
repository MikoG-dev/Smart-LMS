from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func
from database.session import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student") 
    
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    year_level = Column(Integer, nullable=True) 

    points = Column(Integer, default=0) 
    
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    practice_sessions = relationship("PracticeSession", back_populates="student")
    contributions = relationship("Question", back_populates="contributor")
    department = relationship("Department", back_populates="users")