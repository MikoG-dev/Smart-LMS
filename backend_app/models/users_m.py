from backend_app.database.database import Base
from sqlalchemy import Column, Integer, String, Boolean

class UsersData(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    is_verified = Column(Boolean, default = False)
    

