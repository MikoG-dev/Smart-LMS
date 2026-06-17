from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from ..database.database import init_db
from ..models.questions_m import QuestionDB
from ..models.users_m import UsersData
from ..security.user_auth2 import current_admin
from ..schemas.schemas import showUsers
from typing import List

router = APIRouter(
    prefix='/admin',
    tags=["Admin's"]
)

@router.get('/get-users', response_model=List[showUsers])
def get_users(verified:Optional[bool]=None, user=Depends(current_admin), db: Session = Depends(init_db)):
    
    users = db.query(UsersData).filter(UsersData.is_verified==verified if verified != None else True).all()
    
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No pending users!') 
    
    return users

@router.get("/pending-questions")
def pending_questions(user=Depends(current_admin), db: Session = Depends(init_db)):
    pend_quest = db.query(QuestionDB).filter(QuestionDB.status == "pending").all()
    
    if not pend_quest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No pending questions!')
    filtered = []

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

@router.put('/approve_user/{user_id}', status_code=status.HTTP_202_ACCEPTED)
def approve_user(user_id:int, user=Depends(current_admin), db: Session=Depends(init_db)):
    userr = db.query(UsersData).filter(UsersData.id == user_id).first()

    if not userr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found!')
    if userr.is_verified:
        return {'detail': 'User aleady verified!'}
    
    userr.is_verified = True
    db.commit()

    return {'msg': 'User verified successfully!'}, userr

# --- Path Parameter ------
@router.put("/approve-questions/{question_id}", status_code=status.HTTP_202_ACCEPTED)
def approve(question_id: int, user=Depends(current_admin), db: Session=Depends(init_db)):
    
    question = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Question not found!')
    
    question.status = "approved"

    db.commit()

    return {"message": "Question approved successfully!"}, question

@router.put("/reject-questions/{question_id}", status_code=status.HTTP_202_ACCEPTED)
def reject(question_id: int, user=Depends(current_admin), db: Session=Depends(init_db)):
    
    question = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Question not found!')
    
    question.status = "rejected"

    db.commit()

    return {"message":"Question rejected successfully!"}, question
    
@router.delete("/delete-questions/{question_id}")
def delete(question_id: int, user=Depends(current_admin), db: Session=Depends(init_db)):
    
    q = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()

    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Question not found!')
    
    db.delete(q)
    db.commit()

    return {"message":"question deleted successfully!"}, q

@router.delete('/remove-user/{user_id}')
def remove_user(user_id:int, user=Depends(current_admin), db: Session=Depends(init_db)):
    user = db.query(UsersData).filter(UsersData.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404,
                            detail='User not found!')
    
    if user.role == 'user':
        db.delete(user)
        db.commit()

        return {'detail':'User removed successfully!'}
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User can't be removed!")