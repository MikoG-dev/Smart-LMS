from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.session import get_db
from models.user import User
from schemas.user_schema import UserCreate, UserOut, Token
from core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.phone_number == user_data.phone_number).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # 2. Hash password
    hashed_pwd = get_password_hash(user_data.password)

    # 3. Role verification logic
    is_verified = True if user_data.role == "student" else False

    # 4. Create user
    new_user = User(
        full_name=user_data.full_name,
        phone_number=user_data.phone_number,
        hashed_password=hashed_pwd,
        role=user_data.role,
        department_id=user_data.department_id,
        year_level=user_data.year_level,
        is_verified=is_verified
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = db.query(User).filter(User.phone_number == form_data.username).first()
    
    # 2. Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Account pending admin approval."
        )

    # 4. Generate the JWT Token
    access_token = create_access_token(
        data={"sub": user.phone_number, "role": user.role, "id": user.id}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}