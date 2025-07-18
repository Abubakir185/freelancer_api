from pydantic import BaseModel, validator
from typing import List, Optional

class FreelancerBase(BaseModel):
    full_name: str
    phone_number: str
    age: int
    skills: List[str]
    status: str

    @validator("phone_number")
    def check_phone_number(cls, value: str) -> str:
        if not value.startswith("+998"):
            raise ValueError("Telefon raqam +998 bilan boshlanishi kerak")
        if len(value) != 13:
            raise ValueError("Telefon raqam +998 bilan va jami 13 belgidan iborat bo‘lishi kerak")
        return value

    @validator("age")
    def age_must_be_positive(cls, v):
        if v <= 1:
            raise ValueError("yosh '0 yoki 0 dan kichik bolishi mumkin emas")
        return v
    
    @validator("full_name")
    def namecheck(cls, v):
        for i in v:
            if i.isdigit():
                raise ValueError("Ism familiyada raqam bo'lishi mumkinmas")
        return v
    
    @validator("status")
    def check_status(cls, v):
        if v not in ["on_leave", "available", "busy"]:
            raise ValueError("Status 'on_leave' yoki 'available' yoki 'busy' bo'lishi kerak")
        return v
        
    @validator("skills")
    def check_skills_not_empty(cls, v):
        if not v:
            raise ValueError("Kamida bitta skill bo'lishi kerak")
        return v


class FreelancerCreate(FreelancerBase):
    username: str
    password: str

class FreelancerUpdate(FreelancerBase):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    age: Optional[int] = None
    skills: Optional[List[str]] = None
    status: str

class Freelancer(FreelancerBase):
    id: int
    username: str

    class Config:
        orm_mode = True

class FreelancerLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None