from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from fastapi.security import APIKeyHeader
from database import get_db
from models import UserRole, Rule, User
from schemas import RuleCreate, RuleResponse
from logger import add_log     # <-- IMPORTANT
import re

router = APIRouter(prefix="/rules", tags=["Rules"])

api_key_header = APIKeyHeader(name="x-api-key")

def get_current_user(db: Session = Depends(get_db), x_api_key = Security(api_key_header)):
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user:
        raise HTTPException(401, "Invalid or missing API key")
    return user

@router.post("/", response_model=RuleResponse)
def create_rule(
    data: RuleCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    if user.role != UserRole.admin:
        raise HTTPException(403, "Admin only")

    # Validate regex
    try:
        re.compile(data.pattern)
    except:
        raise HTTPException(400, "Invalid regex")

    rule = Rule(pattern=data.pattern, action=data.action, created_by=user.id)
    db.add(rule)
    db.commit()
    db.refresh(rule)

    # ✅ ADD LOG HERE
    add_log(
        db=db,
        user_id=user.id,
        action="RULE_CREATED",
        description=f"Pattern={data.pattern}, Action={data.action}"
    )

    return rule


@router.get("/", response_model=list[RuleResponse])
def list_rules(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user.role != UserRole.admin:
        raise HTTPException(403, "Admin only")

    rules = db.query(Rule).all()

    # ✅ OPTIONAL: LOG RULE VIEW
    add_log(
        db=db,
        user_id=user.id,
        action="RULE_LIST_VIEWED",
        description="Admin viewed rule list"
    )

    return rules
