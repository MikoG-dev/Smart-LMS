from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.schemas import QuestionCreate
from ..database.database import init_db
from ..models.questions_m import QuestionDB, ChoiceDB
from ..models.users_m import UsersData
from ..security.user_auth1 import current_user
from ..models.coursess import Courses


router = APIRouter(
    prefix='/questions',
    tags=["Question"]
)

@router.post("/add-question")
def add_question(q: QuestionCreate, user=Depends(current_user), db: Session=Depends(init_db)):
 
    course = db.query(Courses).filter(Courses.title == q.course_title, Courses.year_level== q.year_level).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Course not found!')
    
    #cur_user= db.query(UsersData.id).filter(UsersData.username == user.user_name).first()
    
    # creating question
    db_question = QuestionDB(course_title=q.course_title, 
                             year_level = q.year_level,
                             question=q.question,
                             course_code = course.id,
                             contributor_id=user.id)
    db.add(db_question)
    

    # add choices
    for c in q.choices:
        db_choice = ChoiceDB(
            choice_text = c.text,
            is_answer = c.is_correct,
            question_id = db_question.id
        )
        db.add(db_choice)

    db.commit()
    db.refresh(db_question)

    return {"message":"Question added successfully!"}, {'id':db.question.id}

@router.get("/get-questions")
def get_questions(year_level = 9, course = '', user=Depends(current_user), db: Session=Depends(init_db)):

    questions = db.query(QuestionDB).filter( QuestionDB.status == 'approved', 
                                            QuestionDB.year_level == year_level ,
                                            QuestionDB.course_title == course.capitalize() if course != '' else True
                                            ).all()

    result = []

    for question in questions:
        result.append({
            "Question": question.question,
            "Choices": [{"Choice": c.choice_text} for c in question.choices]
        })
    
    if result == []:
        return {'msg': 'No questions'}
    return result