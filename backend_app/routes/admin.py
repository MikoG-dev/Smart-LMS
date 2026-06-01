from fastapi import APIRouter
from backend_app.security.admin_auth import create_token
router = APIRouter()

@router.post("/admin/login")
def admin_login(username: str, password: str):

    if username=="maadmin" and password=="quiz1admin":

        token = create_token({"user": username})
        return {"access token": token}
    
    return {"error": "invaid credentials!"}
    
