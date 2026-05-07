from pydantic import BaseModel
from typing import List


# ---- input models -----
class Choice(BaseModel):
    text: str
    is_correct: bool = False

class QuestionCreate(BaseModel):
    course_title: str
    year_level: int
    question: str
    choices: List[Choice]

class User(BaseModel):
    fullname: str
    username: str
    password: str

class Course(BaseModel):
    tit: str
    year_l: int
