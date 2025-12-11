from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from fastapi.security import APIKeyHeader
from database import get_db
from models import Command, Rule, User
from logger import add_log

from schemas import CommandCreate, CommandResponse
import re

router = APIRouter(prefix="/commands", tags=["Commands"])

api_key_header = APIKeyHeader(name="x-api-key")

def get_current_user(db: Session = Depends(get_db), x_api_key = Security(api_key_header)):
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user:
        raise HTTPException(401, "Invalid API key")
    return user


@router.post("/", response_model=CommandResponse)
def submit(data: CommandCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):

    if user.credits <= 0:
        add_log(db, user.id, "COMMAND_REJECTED", f"No credits: {data.command_text}")
        raise HTTPException(400, "No credits")

    rules = db.query(Rule).all()

    matched = None
    for r in rules:
        if re.search(r.pattern, data.command_text):
            matched = r
            break

    if matched is None:
        add_log(db, user.id, "COMMAND_REJECTED", f"No rule match: {data.command_text}")
        raise HTTPException(400, "Rejected (no rule matches)")

    if matched.action == "AUTO_REJECT":
        add_log(db, user.id, "COMMAND_REJECTED", f"Rule rejected ({matched.pattern}) : {data.command_text}")
        raise HTTPException(400, "Rejected by rule")

    output = f"[MOCK] Executed: {data.command_text}"
    user.credits -= 1

    cmd = Command(
        user_id=user.id,
        command_text=data.command_text,
        matched_rule_id=matched.id,
        status="executed",
        output=output
    )

    db.add(cmd)
    db.commit()
    db.refresh(cmd)

    return cmd


@router.get("/", response_model=list[CommandResponse])
def history(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(Command).filter(Command.user_id == user.id).all()
