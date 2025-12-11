from sqlalchemy.orm import Session
from models import AuditLog

def add_log(db: Session, user_id: int, action: str, description: str):
    log = AuditLog(
        user_id=user_id,
        action=action,
        description=description,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
