from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserRole
from schemas import UserCreate, UserResponse
from logger import add_log   # ← ADD THIS
import secrets

router = APIRouter(prefix="/users", tags=["Users"])

api_key_header = APIKeyHeader(name="x-api-key")

# -------------------------------
# GET CURRENT USER
# -------------------------------
def get_current_user(db: Session = Depends(get_db), x_api_key = Security(api_key_header)):
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user:
        raise HTTPException(401, "Invalid API key")
    return user


# -------------------------------
# CREATE USER (ADMIN ONLY)
# -------------------------------
@router.post("/", response_model=UserResponse)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != UserRole.admin:
        raise HTTPException(403, "Admin only")

    # Generate API key
    api_key = secrets.token_hex(16)

    new_user = User(
        name=data.name,
        role=data.role,
        api_key=api_key,
        credits=100
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # ------------------------------
    # LOG ENTRY HERE
    # ------------------------------
    add_log(
        db=db,
        user_id=current_user.id,
        action="USER_CREATED",
        description=f"Created user '{new_user.name}' with role {new_user.role}"
    )

    return new_user


# -------------------------------
# GET CURRENT USER INFO
# -------------------------------
@router.get("/me", response_model=UserResponse)
def get_me(user = Depends(get_current_user)):
    return user


# -------------------------------
# LIST ALL USERS (ADMIN ONLY)
# -------------------------------
@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(403, "Admin only")

    users = db.query(User).all()

    # LOG VIEWING USERS (optional)
    add_log(
        db=db,
        user_id=current_user.id,
        action="VIEW_USERS",
        description="Admin viewed all users"
    )

    return users
