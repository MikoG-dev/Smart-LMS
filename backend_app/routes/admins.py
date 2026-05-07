from fastapi import APIRouter, Depends
from backend_app.database.database import SessionLocal
from backend_app.models.questions_m import QuestionDB
from backend_app.security.admin_auth import current_admin
router = APIRouter()




@router.get("/admin/pending-questions")
def pending_questions(user=Depends(current_admin)):
    db = SessionLocal()

    pend_quest = db.query(QuestionDB).filter(QuestionDB.status == "pending").all()
    
    
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

    db.close()
    return filtered

@router.put("/admin/approve-questions/{question_id}")
def approve(question_id: int, user=Depends(current_admin)):
    db = SessionLocal()

    question = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()

    if not question:
        db.close()
        return {"Error": "Question not found"}
    
    question.status = "approved"

    db.commit()
    db.close()

    return {"message": "Question approved successfully!"}


@router.put("/admin/reject-questions/{question_id}")
def reject(question_id: int, user=Depends(current_admin)):
    db = SessionLocal()

    question = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()

    if not question:
        db.close()
        return {"error": "Question not found!"}
    
    question.status = "rejected"

    db.commit()
    db.close()

    return {"message":"Question rejected successfully!"}
    

@router.delete("/admin/delete-questions/{question_id}")
def delete(question_id: int, user=Depends(current_admin)):
    db = SessionLocal()
    
    q = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()

    if not q:
        db.close()
        return {"error":"Question not found!"}
    
    db.delete(q)
    db.commit()
    db.close()

    return {"message":"question deleted successfully!"}

