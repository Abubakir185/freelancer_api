from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schema.Freelancer)
def create_user(user: schema.FreelancerCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

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

@router.delete("/users/{user_id}", response_model=schema.Freelancer)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="O'chirish uchun user topilmadi")
    return user


@router.get("/users/by-skill/", response_model=list[schema.Freelancer])
def users_by_skill(skill: str, db: Session = Depends(get_db)):
    return crud.get_users_by_skill(db, skill)
