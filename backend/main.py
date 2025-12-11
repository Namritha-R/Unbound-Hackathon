from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware

from routers import users, rules, commands, logs

app = FastAPI(title="Command Gateway")   # MUST COME FIRST

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(name="x-api-key")

# Routers
app.include_router(users.router)
app.include_router(rules.router)
app.include_router(commands.router)
app.include_router(logs.router)  # ← THIS FIXES YOUR ERROR

@app.get("/")
def root():
    return {"message": "Running"}
