from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

from sqlalchemy import DateTime
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    member = "member"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(Enum(UserRole))
    api_key = Column(String, unique=True)
    credits = Column(Integer, default=100)

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    pattern = Column(String)
    action = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))

class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    command_text = Column(String)
    matched_rule_id = Column(Integer)
    status = Column(String)
    output = Column(Text)
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String)        # e.g. "RULE_CREATED"
    description = Column(String)   # any detail: "Pattern: ^ls"
    timestamp = Column(DateTime, default=datetime.utcnow)
