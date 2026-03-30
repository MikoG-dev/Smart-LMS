from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.session import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) # e.g., "Computer Science"
    type = Column(String, default="university") 

    # Relationships
    users = relationship("User", back_populates="department")
    courses = relationship("Course", back_populates="department")
