from pydantic import BaseModel
from typing import List
from sqlalchemy import Enum

# ---- input models -----
class Choice(BaseModel):
    text: str
    is_correct: bool = False

class QuestionCreate(BaseModel):
    course_title: str = 'Physics'
    year_level: int = 9
    question: str
    choices: List[Choice]

class User(BaseModel):
    fullname: str
    username: str
    password: str

class UserL(BaseModel):
    username: str='user1'
    password: str='user'

class showUsers(BaseModel):
    id: int
    fullname: str
    username: str
    role: str
    class config:
        orm_mode=True

class changePd(BaseModel):
    current_pd: str
    new_pd: str

class Course(BaseModel):
    tit: str
    year_l: int

class Role(BaseModel):
    role:str='user'