from database import SessionLocal
from models import User, UserRole
import secrets

db = SessionLocal()
api_key = secrets.token_hex(16)

admin = User(
    name="admin",
    role=UserRole.admin,
    api_key=api_key,
    credits=100
)

db.add(admin)
db.commit()

print("Admin created!")
print("API KEY:", api_key)
