from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm as opr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..security.user_auth1 import create_token, current_user
from ..database.database import init_db
from ..schemas.schemas import User, changePd
from ..models.users_m import UsersData
from ..hashing.pwdHash import hashed, pwdVerify

router = APIRouter(
    prefix='/user',
    tags=["User"]
)

@router.post("/register")
def user_register(info: User, db: Session=Depends(init_db)):
    
    user = db.query(UsersData).filter(UsersData.username == info.username.lower()).first()
    if user:
        return {"error": "username is taken!"}
    
    hashed_pwd = hashed(info.password)
    
    db_user = UsersData(fullname=info.fullname,
                        username=info.username.lower(), 
                        password=hashed_pwd)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Username is taken!')

    return {"message": "Registered Successsfully"}

@router.post("/login")
def user_login(info: opr=Depends(), db: Session=Depends(init_db)):

    db_user = db.query(UsersData).filter( UsersData.username == info.username.lower()).first()
    
    if db_user:
        if pwdVerify(info.password, db_user.password):
            if not db_user.is_verified:
                return {'detail': 'User not verified!'}
        
            token = create_token({"user":info.username})
            return {"access_token":token}
    
    raise HTTPException(status_code=401,
                        detail='Invalid username or password!')

@router.post('/change-pwd')
def change_pd(req:changePd, user=Depends(current_user), db: Session=Depends(init_db)):
    
    if pwdVerify(req.current_pd, user.password):
        user.password = hashed(req.new_pd)
        db.commit()

        return {"detail": 'Password changed successfully!'}
    
    raise HTTPException(status_code=401,
                        detail='Invalid password!')
    
