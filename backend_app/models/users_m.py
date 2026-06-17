from ..database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum 
import enum

class RoleEnum(str, enum.Enum):
    user = 'user'
    admin = 'admin'
    manager = 'manager'

class UsersData(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    is_verified = Column(Boolean, default = False)

    role = Column(Enum(RoleEnum), default=RoleEnum.user)




    

