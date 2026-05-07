from fastapi import APIRouter, Depends
from backend_app.schemas.schemas import QuestionCreate
from backend_app.database.database import SessionLocal
from backend_app.models.questions_m import QuestionDB, ChoiceDB
from backend_app.models.users_m import UsersData
from backend_app.security.user_auth import current_user
from backend_app.models.coursess import Courses


router = APIRouter()

@router.post("/questions/add-question")
def add_question(q: QuestionCreate, user=Depends(current_user)):
    db = SessionLocal()

    course = db.query(Courses).filter(Courses.title == q.course_title, Courses.year_level== q.year_level).first()
    if not course:
        return {"error":"Course not found!"}
    user_name = user["user"];
    cur_user= db.query(UsersData.id).filter(UsersData.username == user_name).first()
    # creating question
    db_question = QuestionDB(course_title=q.course_title, 
                             year_level = q.year_level,
                             question=q.question,
                             course_code = course.id,
                             contributor_id=cur_user.id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # add choices
    for c in q.choices:
        db_choice = ChoiceDB(
            choice_text = c.text,
            is_answer = c.is_correct,
            question_id = db_question.id
        )
        db.add(db_choice)

    db.commit()
    db.close()

    return {"message":"Question added successfully!"}

@router.get("/questions/get-questions")
def get_questions(user=Depends(current_user)):
    db = SessionLocal()

    questions = db.query(QuestionDB).all()

    result = []

    for question in questions:
        result.append({
        #   "Id": question.id,
            "c_title":question.course_title,
            "year":question.year_level,
            "Question": question.question,
            "c_code":question.courses.id,
            "contri":question.contributor_id,
            "Status":question.status,
            "Choices": [
                {
        #           "id": c.id,
                    "Choice": c.choice_text,
        #           "Is_Answer": c.is_answer
                }
                for c in question.choices
            ]
        })
    
    db.close()
    return result