import crud
import schema
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from utils import hash_password, verify_password
from auth import create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/register/", response_model=schema.Freelancer)
def register(data: schema.FreelancerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Freelancer).filter(models.Freelancer.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = models.Freelancer(
        username=data.username,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        phone_number=data.phone_number,
        age=data.age,
        skills=data.skills
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Freelancer).filter(models.Freelancer.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invlalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/", response_model=list[schema.Freelancer])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.get("/users/{user_id}", response_model=schema.Freelancer)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")
    return user

@router.put("/users/{user_id}", response_model=schema.Freelancer)
def update_user(user_id: int, user: schema.FreelancerUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="Yangilash uchun user topilmadi")
    return db_user

@router.patch("/users/{user_id}/status", response_model=schema.FreelancerUpdate)
def change_user_status(user_id: int, status_data: schema.FreelancerUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_status(db, user_id, status_data.status)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", response_model=schema.Freelancer)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="O'chirish uchun user topilmadi")
    return user


@router.get("/users/by-skill/", response_model=list[schema.Freelancer])
def users_by_skill(skill: str, db: Session = Depends(get_db)):
    return crud.get_users_by_skill(db, skill)
