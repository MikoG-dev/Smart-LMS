from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "myadminskey"
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

def current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return payload