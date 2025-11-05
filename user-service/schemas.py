from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name : str
    surname : str
    age : int
    email : EmailStr


class CreateUser(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
