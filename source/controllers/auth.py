from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from source.databases.db import get_db
from source.schemas.auth import LoginRequest, RegisterRequest, AuthResponse, UserInfo
from source.services import auth
from source.models.models import Admin

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(Admin).filter(Admin.username == req.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user = auth.register_user(db, req.username, req.role, req.password)
    return {"message": "User registered successfully", "user_id": user.id, "username": user.username}

@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": user.username})
    return AuthResponse(
        user = UserInfo.model_validate(user),
        token=access_token)