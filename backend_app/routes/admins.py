from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend_app.database.database import init_db
from backend_app.models.questions_m import QuestionDB
from backend_app.models.users_m import UsersData
from backend_app.security.admin_auth import current_admin
router = APIRouter()


@router.get('/admin/pending-users')
def pending_users(db: Session = Depends(init_db)):
    users = db.query(UsersData).filter(UsersData.is_verified == False)
    
    filt = []

    if filt == []:
        return {'msg': 'No users!'} 
    
    for user in users:
        filt.append({
            'id': user.id,
            'Full Name': user.fullname,
            'Username': user.username
        })
    
    return filt

@router.put('/admin/approve_user/{user_id}')
def approve_user(user_id:int, db: Session=Depends(init_db)):
    user = db.query(UsersData).filter(UsersData.id == user_id).first()

    if not user:
        return {'error': 'User not found!'}
    
    user.is_verified = True
    db.commit()

    return {'msg': 'User verified successfully!'}


@router.get("/admin/pending-questions")
def pending_questions(user=Depends(current_admin), db: Session = Depends(init_db)):
    pend_quest = db.query(QuestionDB).filter(QuestionDB.status == "pending").all()
    
    filtered = []
    if filtered == []:
        return {'msg': 'No pending questions!'} 

    for pend in pend_quest:
        filtered.append({
            "Id": pend.id,
            "Question": pend.question,
            "Status":pend.status,
            "Choices": [
                {
        #           "id": c.id,
                    "Choice": c.choice_text,
                    "Is_Answer": c.is_answer
                }
                for c in pend.choices
            ]
        })

    return filtered


# --- Path Parameter ------
@router.put("/admin/approve-questions/{question_id}")
def approve(question_id: int, user=Depends(current_admin), db: Session=Depends(init_db)):
    
    question = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()

    if not question:
        return {"Error": "Question not found"}
    
    question.status = "approved"

    db.commit()

    return {"message": "Question approved successfully!"}


@router.put("/admin/reject-questions/{question_id}")
def reject(question_id: int, user=Depends(current_admin), db: Session=Depends(init_db)):
    
    question = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()

    if not question:
        return {"error": "Question not found!"}
    
    question.status = "rejected"

    db.commit()

    return {"message":"Question rejected successfully!"}
    

@router.delete("/admin/delete-questions/{question_id}")
def delete(question_id: int, user=Depends(current_admin), db: Session=Depends(init_db)):
    
    q = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()

    if not q:
        return {"error":"Question not found!"}
    
    db.delete(q)
    db.commit()

    return {"message":"question deleted successfully!"}

