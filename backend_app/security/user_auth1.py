from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..models.users_m import UsersData
from ..database.database import init_db
from sqlalchemy.orm import Session

SECRET_KEY = "myuserskey"
ALGORITHM = "HS256"

oauth_scheme = OAuth2PasswordBearer(tokenUrl='user/login')

# ----- create token -----
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now().utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode,  SECRET_KEY, algorithm=ALGORITHM)

    return encoded

# ------- verify token --------
def verify_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get("user")

        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="invalid credentials!")
        return payload
    except JWTError:
        return None
     
def current_user(db:Session=Depends(init_db), token:str=Depends(oauth_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401,
                            detail="Invalid Credentials")
    username = payload.get('user')
    user = db.query(UsersData).filter(UsersData.username == username).first()
    
    return user
    
def current_admin(db:Session=Depends(init_db), token:str = Depends(oauth_scheme)):

    user = current_user(db, token)
    
    if user.role == 'user':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Not Authorized')
    
    return user

def current_manager(db:Session=Depends(init_db), token:str = Depends(oauth_scheme)):
    
    user = current_user(db, token)
    
    if user.role != 'manager':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Not Authorized')
    
    return user