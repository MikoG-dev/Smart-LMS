from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models.users_m import UsersData
from ..database.database import init_db
from sqlalchemy.orm import Session

SECRET_KEY = "myuserskey"
ALGORITHM = "HS256"
# ----- create token -----
def create_token(data: dict):
    tobe_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=10)
    tobe_encode.update({"exp":expire})

    token = jwt.encode(tobe_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

# ------- verify token --------
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
  
# --- security ----
security = HTTPBearer()

def current_user(db:Session=Depends(init_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get('user')
    user = db.query(UsersData).filter(UsersData.username == username).first()
    
    return user

def current_admin(db:Session=Depends(init_db), credentials: HTTPAuthorizationCredentials = Depends(security)):

    user = current_user(db, credentials)
    
    if user.role == 'user':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Not Authorized')
    
    return user

def current_manager(db:Session=Depends(init_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    user = current_user(db, credentials)
    
    if user.role != 'manager':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Not Authorized')
    
    return user