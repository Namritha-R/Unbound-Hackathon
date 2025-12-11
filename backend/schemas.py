from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    role: str
    credits: int
    api_key: str

    class Config:
        from_attributes = True

class RuleCreate(BaseModel):
    pattern: str
    action: str

class RuleResponse(BaseModel):
    id: int
    pattern: str
    action: str

    class Config:
        from_attributes = True

class CommandCreate(BaseModel):
    command_text: str

class CommandResponse(BaseModel):
    id: int
    command_text: str
    status: str
    output: str

    class Config:
        from_attributes = True
