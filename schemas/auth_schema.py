from pydantic import BaseConfig, BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password_hash: str
    auth_provider: str
    age: int

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    user: str
    password: str

    class Config:
        orm_mode = True
