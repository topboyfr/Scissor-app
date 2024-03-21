from pydantic import BaseModel, EmailStr
from fastapi import Request
from typing import Optional

class UserBase(BaseModel):
    first_name: str
    last_name: str

class UserLogin(UserBase):
    username : str
    
class UserCreate(UserBase):
    email: EmailStr
    password: str

class loginForm:
    def __init__(self, request:Request):
        self.request:Request = request
        self.username:Optional[str]=None
        self.password:Optional[str]=None

    async def create_auth_form(self):
        form = await self.request.form()
        self.username= form.get("email")
        self.password= form.get("password")

class ShowUser(UserLogin):
    id : int
    
