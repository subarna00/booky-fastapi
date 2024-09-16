from pydantic import BaseModel,Field
from datetime import datetime
import uuid
class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email:str
    first_name: str
    last_name: str
    is_verified: bool
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime