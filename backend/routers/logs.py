from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import APIKeyHeader
from database import get_db
from models import AuditLog, User

router = APIRouter(prefix="/logs", tags=["Logs"])

api_key_header = APIKeyHeader(name="x-api-key")

def get_current_user(db: Session = Depends(get_db), x_api_key = Security(api_key_header)):
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user:
        raise HTTPException(401, "Invalid API key")
    return user

@router.get("/me")
def my_logs(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(AuditLog).filter(AuditLog.user_id == user.id).all()

@router.get("/system")
def system_logs(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admins only")
    return db.query(AuditLog).all()

@router.get("/user/{uid}")
def logs_by_user(uid: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admins only")
    return db.query(AuditLog).filter(AuditLog.user_id == uid).all()
