from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend_app.security.user_auth import create_token
from backend_app.database.database import init_db
from backend_app.schemas.schemas import User
from backend_app.models.users_m import UsersData

router = APIRouter()

@router.post("/user/register")
def user_register(info: User, db: Session=Depends(init_db)):
    
    user = db.query(UsersData).filter(UsersData.username == info.username).first()
    if user:
        return {"error": "username is taken!"}
    
    db_user = UsersData(fullname=info.fullname,
                        username=info.username, 
                        password=info.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "Registered Successsfully"}

@router.post("/user/login")
def user_login(info: User, db: Session=Depends(init_db)):
    
    db_user = db.query(UsersData).filter(
        UsersData.username == info.username,
        UsersData.password == info.password).first()
    
    if db_user:
        token = create_token({"user":info.username})

        return {"acces token":token}
    
    return {"error":"Invalid username or password!"}


