from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database.database import init_db
from ..models.users_m import UsersData
from ..schemas.schemas import Role
from ..security.user_auth1 import current_manager

router = APIRouter(
    prefix='/manager',
    tags=["Manager's"]
)

@router.post('/promote-user/{user_id}')
def promote(user_id:int, request:Role, u=Depends(current_manager), db:Session=Depends(init_db)):
    user = db.query(UsersData).filter(UsersData.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found!')
    
    if user.role == request.role:
        raise HTTPException(status_code=208,
                            detail='User already promoted!')
    
    user.role = request.role
    db.commit()

    return {'detail': 'User promoted successfully!'}, user

